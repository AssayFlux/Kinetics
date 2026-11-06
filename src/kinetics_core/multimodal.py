"""Multimodal protein/chemical/assay-context training and inference.

This first Kinetics-Multi implementation is a feature-fusion MLP baseline. It
uses ESM-2 vectors, Morgan fingerprints, pooled molecular graph descriptors and
optional raw assay context. It is not a message-passing GNN or a validated
scientific predictor.
"""
from __future__ import annotations

import json
import logging
import warnings
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import GroupKFold, KFold, cross_val_score
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .context import context_design_matrix, make_context_pipeline
from .experiments import build_experiment_manifest, save_experiment_manifest
from .metrics import regression_report, subgroup_regression_report
from .model_card import write_model_card
from .modeling import _load_feature_file, _validate_feature_metadata
from .provenance import file_record, write_json_atomic
from .uncertainty import conformal_quantile

LOG = logging.getLogger("kinetics_core.multimodal")
GRAPH_SUMMARY_SCHEMA = "1.0"


def _graph_summary(payload: dict[str, np.ndarray]) -> np.ndarray:
    """Create fixed-width per-molecule summaries from packed graph arrays."""
    required = {
        "graph_atom_features", "graph_bond_features",
        "graph_atom_offsets", "graph_edge_offsets",
    }
    missing = required - set(payload)
    if missing:
        raise ValueError(f"Feature archive lacks molecular graph arrays: {sorted(missing)}")
    atoms = np.asarray(payload["graph_atom_features"], dtype=np.float32)
    bonds = np.asarray(payload["graph_bond_features"], dtype=np.float32)
    atom_offsets = np.asarray(payload["graph_atom_offsets"], dtype=np.int64).reshape(-1)
    edge_offsets = np.asarray(payload["graph_edge_offsets"], dtype=np.int64).reshape(-1)
    n_rows = len(payload["X"])
    if (
        atoms.ndim != 2 or atoms.shape[1] != 9
        or bonds.ndim != 2 or bonds.shape[1] != 4
        or len(atom_offsets) != n_rows + 1
        or len(edge_offsets) != n_rows + 1
        or atom_offsets[0] != 0 or edge_offsets[0] != 0
        or atom_offsets[-1] != len(atoms) or edge_offsets[-1] != len(bonds)
        or np.any(np.diff(atom_offsets) <= 0) or np.any(np.diff(edge_offsets) < 0)
        or np.any(np.diff(edge_offsets) % 2 != 0)
    ):
        raise ValueError("Molecular graph arrays have invalid dimensions or offsets")
    if not np.isfinite(atoms).all() or not np.isfinite(bonds).all():
        raise ValueError("Molecular graph arrays contain non-finite values")
    rows: list[np.ndarray] = []
    for index in range(n_rows):
        atom_part = atoms[atom_offsets[index]:atom_offsets[index + 1]]
        bond_part = bonds[edge_offsets[index]:edge_offsets[index + 1]]
        atom_stats = np.concatenate((atom_part.mean(axis=0), atom_part.max(axis=0)))
        bond_stats = (
            bond_part.mean(axis=0) if len(bond_part)
            else np.zeros((4,), dtype=np.float32)
        )
        rows.append(np.concatenate((
            atom_stats,
            bond_stats,
            np.asarray([len(atom_part), len(bond_part) / 2.0], dtype=np.float32),
        )))
    result = np.asarray(rows, dtype=np.float32)
    if result.shape != (n_rows, 24):
        raise RuntimeError(f"Unexpected graph summary shape: {result.shape}")
    return result


def _multimodal_design(payload: dict[str, np.ndarray]) -> tuple[np.ndarray | pd.DataFrame, bool]:
    """Join base ESM/Morgan features, graph summaries and optional raw context."""
    X = np.asarray(payload["X"], dtype=np.float32)
    if X.ndim != 2 or not np.isfinite(X).all():
        raise ValueError("Base protein/chemical feature matrix must be finite and two-dimensional")
    graph = _graph_summary(payload)
    base = np.concatenate((X, graph), axis=1).astype(np.float32, copy=False)
    numeric = tuple(
        np.asarray(payload.get("context_numeric_columns", np.asarray([], dtype=str))).astype(str)
    )
    categorical = tuple(
        np.asarray(payload.get("context_categorical_columns", np.asarray([], dtype=str))).astype(str)
    )
    context_enabled = bool(numeric or categorical)
    if context_enabled:
        enriched = dict(payload)
        enriched["X_base"] = base
        frame = context_design_matrix(enriched)
        return frame, True
    return base, False


def _validate_archives(
    train: dict[str, np.ndarray],
    other: dict[str, np.ndarray],
    *,
    label: str,
    target: str,
    holdout_group_arrays: tuple[str, ...],
) -> None:
    _validate_feature_metadata(train, other, label=label)
    for key in ("feature_schema_version", "feature_metadata_json"):
        if (key in train) != (key in other):
            raise ValueError(f"{label} feature metadata presence differs: {key}")
        if key in train and not np.array_equal(train[key], other[key]):
            raise ValueError(f"{label} feature metadata differ: {key}")
    if "target" in other and str(other["target"].reshape(-1)[0]) != target:
        raise ValueError(f"{label} archive target does not match requested target")
    if other["X"].shape[1] != train["X"].shape[1]:
        raise ValueError(f"{label} base feature dimension differs")
    for name in holdout_group_arrays:
        if name not in train or name not in other:
            raise ValueError(f"{label} archive missing leakage group array: {name}")
        left = np.asarray(train[name]).astype(str).reshape(-1)
        right = np.asarray(other[name]).astype(str).reshape(-1)
        if len(left) != len(train["y_log10"]) or len(right) != len(other["y_log10"]):
            raise ValueError(f"{label} group array does not align: {name}")
        if set(left).intersection(right):
            raise ValueError(f"Group leakage between training and {label.lower()}: {name}")


def _make_estimator(
    *,
    random_state: int,
    hidden_layer_sizes: tuple[int, ...],
    alpha: float,
    max_iter: int,
    context_enabled: bool,
    numeric_columns: tuple[str, ...],
    categorical_columns: tuple[str, ...],
    base_dimension: int,
) -> Pipeline:
    estimator = MLPRegressor(
        hidden_layer_sizes=hidden_layer_sizes,
        activation="relu",
        solver="adam",
        alpha=alpha,
        batch_size="auto",
        learning_rate_init=1e-3,
        max_iter=max_iter,
        early_stopping=False,
        random_state=random_state,
    )
    if context_enabled:
        fold_local = make_context_pipeline(
            "passthrough",
            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
            base_dimension=base_dimension,
        )
        return Pipeline([
            ("context", fold_local),
            ("scaler", StandardScaler()),
            ("estimator", estimator),
        ])
    return Pipeline([("scaler", StandardScaler()), ("estimator", estimator)])


def fit_multimodal_model(
    train_archive: str | Path,
    test_archive: str | Path,
    *,
    target: str,
    output_dir: str | Path,
    calibration_archive: str | Path | None = None,
    group_array: str | None = None,
    holdout_group_arrays: tuple[str, ...] = (),
    random_state: int = 42,
    n_splits: int = 5,
    hidden_layer_sizes: tuple[int, ...] = (256, 128),
    alpha: float = 1e-4,
    max_iter: int = 500,
    conformal_alpha: float = 0.1,
) -> dict[str, Any]:
    """Train one independent Km or kcat feature-fusion model and retain artifacts."""
    if target not in ("km", "kcat"):
        raise ValueError("target must be 'km' or 'kcat'")
    if not hidden_layer_sizes or any(width < 1 for width in hidden_layer_sizes):
        raise ValueError("hidden_layer_sizes must contain positive widths")
    if alpha < 0 or max_iter < 1 or n_splits < 2:
        raise ValueError("alpha must be >= 0, max_iter >= 1 and n_splits >= 2")
    train = _load_feature_file(train_archive)
    test = _load_feature_file(test_archive)
    if len(train["y_log10"]) < 4:
        raise ValueError("At least four training rows are required for grouped model selection")
    if "target" in train and str(train["target"].reshape(-1)[0]) != target:
        raise ValueError("Training archive target does not match requested target")
    leakage_axes = tuple(dict.fromkeys(
        (*holdout_group_arrays, *((group_array,) if group_array else ()))
    ))
    _validate_archives(
        train, test, label="held-out", target=target,
        holdout_group_arrays=leakage_axes,
    )
    X_train, context_enabled = _multimodal_design(train)
    X_test, test_context = _multimodal_design(test)
    if context_enabled != test_context:
        raise ValueError("Training and held-out assay-context availability differs")
    if context_enabled:
        numeric_columns = tuple(train.get(
            "context_numeric_columns", np.asarray([], dtype=str)
        ).astype(str))
        categorical_columns = tuple(train.get(
            "context_categorical_columns", np.asarray([], dtype=str)
        ).astype(str))
        if tuple(test.get("context_numeric_columns", np.asarray([], dtype=str)).astype(str)) != numeric_columns:
            raise ValueError("Training and held-out numeric context columns differ")
        if tuple(test.get("context_categorical_columns", np.asarray([], dtype=str)).astype(str)) != categorical_columns:
            raise ValueError("Training and held-out categorical context columns differ")
    else:
        numeric_columns, categorical_columns = (), ()
    y_train, y_test = train["y_log10"], test["y_log10"]
    if len(y_test) == 0:
        raise ValueError("Held-out archive must contain at least one observation")
    base_dimension = train["X"].shape[1] + 24

    if group_array:
        if group_array not in train or group_array not in test:
            raise ValueError(f"Requested CV group array is missing: {group_array}")
        groups = np.asarray(train[group_array]).astype(str).reshape(-1)
        if len(groups) != len(y_train) or len(np.unique(groups)) < 2:
            raise ValueError("CV group array must align and contain at least two groups")
        if set(groups).intersection(np.asarray(test[group_array]).astype(str)):
            raise ValueError("CV group leakage between training and held-out archives")
        folds = min(n_splits, len(np.unique(groups)))
        cv = GroupKFold(n_splits=folds)
        split_strategy = f"group_k_fold:{group_array}"
        score_kwargs = {"groups": groups}
    else:
        folds = min(n_splits, len(y_train))
        cv = KFold(n_splits=folds, shuffle=True, random_state=random_state)
        split_strategy = "row_random_k_fold_diagnostic_only"
        score_kwargs = {}
    if folds < 2:
        raise ValueError("At least two CV folds are required")
    estimator_factory = lambda: _make_estimator(
        random_state=random_state,
        hidden_layer_sizes=hidden_layer_sizes,
        alpha=alpha,
        max_iter=max_iter,
        context_enabled=context_enabled,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        base_dimension=base_dimension,
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        scores = -cross_val_score(
            estimator_factory(), X_train, y_train, cv=cv,
            scoring="neg_root_mean_squared_error", n_jobs=1, **score_kwargs,
        )
        estimator = estimator_factory()
        estimator.fit(X_train, y_train)
    convergence_warnings = [
        str(item.message) for item in caught if issubclass(item.category, ConvergenceWarning)
    ]
    if not np.isfinite(scores).all():
        raise RuntimeError("Cross-validation produced non-finite RMSE values")
    predictions = estimator.predict(X_test)
    calibration = _load_feature_file(calibration_archive) if calibration_archive else None
    conformal_q = None
    if calibration is not None:
        _validate_archives(
            train, calibration, label="calibration", target=target,
            holdout_group_arrays=leakage_axes,
        )
        X_cal, calibration_context = _multimodal_design(calibration)
        if calibration_context != context_enabled:
            raise ValueError("Calibration archive assay-context availability differs")
        if context_enabled:
            if tuple(calibration["context_numeric_columns"].astype(str)) != numeric_columns:
                raise ValueError("Calibration numeric context columns differ")
            if tuple(calibration["context_categorical_columns"].astype(str)) != categorical_columns:
                raise ValueError("Calibration categorical context columns differ")
        conformal_q = conformal_quantile(
            calibration["y_log10"], estimator.predict(X_cal), alpha=conformal_alpha
        )

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    run_id = f"{target}_kinetics_multi"
    model_path = output / f"{run_id}.joblib"
    predictions_path = output / f"{run_id}_predictions.csv"
    metrics_path = output / f"{run_id}_metrics.json"
    card_path = output / f"{run_id}_MODEL_CARD.md"
    prediction_frame = pd.DataFrame({
        "source_record_id": np.asarray(
            test.get("source_record_ids", np.arange(len(y_test))).astype(str)
        ),
        "target": target,
        "y_true_log10": y_test.astype(float),
        "y_pred_log10": predictions.astype(float),
        "y_true_canonical": np.power(10.0, y_test.astype(float)),
        "y_pred_canonical": np.power(10.0, predictions.astype(float)),
        "canonical_unit": "M" if target == "km" else "s^-1",
        "residual_log10": (predictions - y_test).astype(float),
    })
    if conformal_q is not None:
        prediction_frame["lower_log10"] = predictions - conformal_q
        prediction_frame["upper_log10"] = predictions + conformal_q
        prediction_frame["lower_canonical"] = np.power(10.0, predictions - conformal_q)
        prediction_frame["upper_canonical"] = np.power(10.0, predictions + conformal_q)
    report = {
        "model_family": "Kinetics-Multi feature-fusion MLP",
        "target": target,
        "canonical_unit": "M" if target == "km" else "s^-1",
        "input_modalities": [
            "ESM-2 protein sequence embedding",
            "Morgan chemical fingerprint",
            "pooled molecular graph descriptors",
            *(["raw assay context with fold-local preprocessing"] if context_enabled else []),
        ],
        "graph_summary_schema": GRAPH_SUMMARY_SCHEMA,
        "graph_summary_dimension": 24,
        "cross_validation": {
            "strategy": split_strategy,
            "folds": int(folds),
            "rmse_mean_log10": float(np.mean(scores)),
            "rmse_std_log10": float(np.std(scores)),
            "fold_rmse_log10": scores.tolist(),
        },
        "held_out": regression_report(y_test, predictions, target=target),
        "n_train": int(len(y_train)),
        "n_held_out": int(len(y_test)),
        "base_feature_dimension": int(train["X"].shape[1]),
        "fused_feature_dimension": int(base_dimension),
        "model_parameters": {
            "hidden_layer_sizes": list(hidden_layer_sizes),
            "alpha": float(alpha),
            "max_iter": int(max_iter),
            "random_state": int(random_state),
        },
        "calibration": ({
            "method": "split_conformal_absolute_residual",
            "alpha": float(conformal_alpha),
            "quantile_log10": float(conformal_q),
            "n_calibration": int(len(calibration["y_log10"])),
            "test_empirical_coverage": float(np.mean(
                np.abs(y_test - predictions) <= conformal_q
            )),
            "mean_interval_width_log10": float(2.0 * conformal_q),
            "coverage_note": (
                "Empirical held-out coverage is descriptive. Formal guarantees require "
                "exchangeability and calibration data untouched by model selection."
            ),
        } if calibration is not None else {
            "status": "not_calibrated",
            "reason": "No independent calibration archive was supplied.",
        }),
        "convergence_warnings": convergence_warnings,
        "warning": (
            "Row-random CV is diagnostic only; it does not establish cold-start generalization."
            if not group_array else None
        ),
        "limitations": [
            "This is a feature-fusion MLP, not a message-passing graph neural network.",
            "It is not scientifically validated until trained and evaluated on reviewed real data.",
            "Predictions are estimates, not experimental measurements or clinical advice.",
        ],
    }
    report["subgroup_diagnostics"] = {
        name: subgroup_regression_report(
            y_test, predictions, np.asarray(test[name]).reshape(-1),
            target=target, min_group_size=5,
            conformal_quantile_log10=conformal_q,
        )
        for name in leakage_axes if name in test
    }
    bundle = {
        "model_family": "Kinetics-Multi feature-fusion MLP",
        "estimator": estimator,
        "target": target,
        "canonical_unit": "M" if target == "km" else "s^-1",
        "base_feature_dimension": int(train["X"].shape[1]),
        "graph_summary_schema": GRAPH_SUMMARY_SCHEMA,
        "feature_schema_version": str(
            train.get("feature_schema_version", np.asarray(["unknown"])).reshape(-1)[0]
        ),
        "feature_metadata_json": str(
            train.get("feature_metadata_json", np.asarray(["{}"])).reshape(-1)[0]
        ),
        "context_enabled": context_enabled,
        "context_numeric_columns": list(numeric_columns),
        "context_categorical_columns": list(categorical_columns),
        "conformal_quantile_log10": conformal_q,
        "conformal_alpha": float(conformal_alpha) if conformal_q is not None else None,
    }
    joblib.dump(bundle, model_path, compress=3)
    write_json_atomic(report, metrics_path)
    prediction_frame.to_csv(predictions_path, index=False)
    write_model_card({
        "model_name": f"Kinetics-Multi {target} feature-fusion MLP",
        "model_version": "0.1.0",
        "software_version": "0.2.0",
        "intended_use": [
            "Exploratory enzyme-kinetics research and hypothesis generation.",
            "Prioritizing candidates for subsequent experimental measurement.",
        ],
        "out_of_scope_use": [
            "Clinical, regulatory or safety-critical decisions.",
            "Replacing experimental Km or kcat measurements.",
        ],
        "dataset": {
            "name": "Training feature archive",
            "version": "See experiment manifest and feature manifest.",
            "n_observations": int(len(y_train)),
        },
        "evaluation": {
            "split_strategy": split_strategy,
            "n_test": int(len(y_test)),
            "metrics": report["held_out"],
            "uncertainty_method": (
                f"Split conformal alpha={conformal_alpha}" if conformal_q is not None
                else "Not calibrated"
            ),
        },
        "limitations": report["limitations"] + [
            "No real-data validation is implied by software tests.",
            "Assay context is optional; omitted context can confound kinetic values.",
        ],
        "feature_encoder": "ESM-2 + Morgan + pooled RDKit molecular graph features",
        "random_seed": random_state,
        "model_sha256": file_record(model_path)["sha256"],
    }, card_path)
    manifest = build_experiment_manifest(
        experiment_id=run_id,
        research_question=f"Estimate enzyme {target} with multimodal feature fusion",
        inputs=[train_archive, test_archive] + ([calibration_archive] if calibration_archive else []),
        outputs=[model_path, metrics_path, predictions_path, card_path],
        configuration={
            "model_family": report["model_family"],
            "target": target,
            "group_array": group_array,
            "holdout_group_arrays": list(holdout_group_arrays),
            "random_state": random_state,
            "n_splits": n_splits,
            "hidden_layer_sizes": list(hidden_layer_sizes),
            "alpha": alpha,
            "max_iter": max_iter,
            "graph_summary_schema": GRAPH_SUMMARY_SCHEMA,
            "calibration_alpha": conformal_alpha if conformal_q is not None else None,
        },
        notes=report["limitations"],
    )
    save_experiment_manifest(manifest, output / f"{run_id}_experiment_manifest.json")
    report["artifacts"] = {
        "model": str(model_path),
        "metrics": str(metrics_path),
        "predictions": str(predictions_path),
        "model_card": str(card_path),
        "experiment_manifest": str(output / f"{run_id}_experiment_manifest.json"),
    }
    return report


def predict_multimodal_model(
    model_path: str | Path,
    feature_archive: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    """Run inference from a trusted locally generated joblib model bundle."""
    bundle = joblib.load(model_path)  # joblib is pickle-based; never load untrusted files.
    with np.load(feature_archive, allow_pickle=False) as archive:
        payload = {name: archive[name] for name in archive.files}
    required = {"X", "target"}
    missing = required - set(payload)
    if missing:
        raise ValueError(f"Inference archive is missing arrays: {sorted(missing)}")
    X = np.asarray(payload["X"], dtype=np.float32)
    if X.ndim != 2 or not np.isfinite(X).all():
        raise ValueError("Inference base feature matrix must be finite and two-dimensional")
    if X.shape[1] != bundle["base_feature_dimension"]:
        raise ValueError("Inference feature dimension differs from the trained model")
    target = str(payload["target"].reshape(-1)[0])
    if target != bundle["target"]:
        raise ValueError("Inference target does not match the trained model target")
    schema = str(payload.get("feature_schema_version", np.asarray(["unknown"])).reshape(-1)[0])
    if schema != bundle["feature_schema_version"]:
        raise ValueError("Inference feature schema differs from the trained model")
    metadata_json = str(payload.get("feature_metadata_json", np.asarray(["{}"])).reshape(-1)[0])
    if metadata_json != bundle["feature_metadata_json"]:
        raise ValueError("Inference representation metadata differs from the trained model")
    design, context_enabled = _multimodal_design(payload)
    if context_enabled != bundle["context_enabled"]:
        raise ValueError("Inference assay-context availability differs from training")
    if context_enabled:
        numeric = tuple(payload.get("context_numeric_columns", np.asarray([], dtype=str)).astype(str))
        categorical = tuple(payload.get("context_categorical_columns", np.asarray([], dtype=str)).astype(str))
        if list(numeric) != bundle["context_numeric_columns"]:
            raise ValueError("Inference numeric context schema differs from training")
        if list(categorical) != bundle["context_categorical_columns"]:
            raise ValueError("Inference categorical context schema differs from training")
    predictions = np.asarray(bundle["estimator"].predict(design), dtype=np.float64).reshape(-1)
    if len(predictions) != len(X) or not np.isfinite(predictions).all():
        raise RuntimeError("Model returned invalid inference predictions")
    ids = np.asarray(payload.get("source_record_ids", np.arange(len(X)))).astype(str)
    if len(ids) != len(predictions):
        raise ValueError("Inference source_record_ids do not align with feature rows")
    table = pd.DataFrame({
        "source_record_id": ids,
        "target": target,
        "y_pred_log10": predictions,
        "y_pred_canonical": np.power(10.0, predictions),
        "canonical_unit": bundle["canonical_unit"],
    })
    q = bundle.get("conformal_quantile_log10")
    if q is not None:
        table["lower_log10"] = predictions - float(q)
        table["upper_log10"] = predictions + float(q)
        table["lower_canonical"] = np.power(10.0, predictions - float(q))
        table["upper_canonical"] = np.power(10.0, predictions + float(q))
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(output, index=False)
    return {
        "target": target,
        "n_predictions": int(len(table)),
        "canonical_unit": bundle["canonical_unit"],
        "output": file_record(output),
        "model": file_record(model_path),
        "warning": "Predictions are estimates, not experimental measurements.",
    }
