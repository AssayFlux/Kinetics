"""Target-specific model fitting workflow; definitions only, not executed during build."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold, KFold, cross_val_score

from .experiments import build_experiment_manifest, save_experiment_manifest
from .metrics import regression_report
from .uncertainty import conformal_quantile
from .applicability import ApplicabilityDomain
from .model_card import write_model_card
from .provenance import file_record, write_json_atomic

LOG = logging.getLogger("kinetics_core.modeling")


def _load_feature_file(path: str | Path) -> dict[str, np.ndarray]:
    with np.load(path, allow_pickle=False) as data:
        required = {"X", "y_log10"}
        missing = required - set(data.files)
        if missing:
            raise ValueError(f"Feature archive is missing arrays: {sorted(missing)}")
        payload = {name: data[name] for name in data.files}
    X = np.asarray(payload["X"], dtype=np.float32)
    y = np.asarray(payload["y_log10"], dtype=np.float32).reshape(-1)
    if X.ndim != 2 or len(X) != len(y) or len(y) < 2:
        raise ValueError(f"Invalid feature/target dimensions: X={X.shape}, y={y.shape}")
    if not np.isfinite(X).all() or not np.isfinite(y).all():
        raise ValueError("Feature archive contains NaN or infinite values")
    payload["X"], payload["y_log10"] = X, y
    return payload


def fit_target_model(
    train_archive: str | Path,
    test_archive: str | Path,
    *,
    target: str,
    output_dir: str | Path,
    group_array: str | None = None,
    holdout_group_arrays: tuple[str, ...] = (),
    random_state: int = 42,
    n_estimators: int = 500,
    max_depth: int = 6,
    n_splits: int = 5,
    calibration_archive: str | Path | None = None,
    conformal_alpha: float = 0.1,
    context_encoder_path: str | Path | None = None,
    applicability_quantile: float = 0.95,
) -> dict[str, Any]:
    """Fit one target model, evaluate a held-out archive, and save full metadata.

    This function is part of the future execution pipeline. It is not invoked
    during repository construction. For publication work, supply precomputed
    protein/scaffold groups to use GroupKFold rather than row-random CV.
    """
    if target not in ("km", "kcat"):
        raise ValueError("target must be 'km' or 'kcat'")
    try:
        from xgboost import XGBRegressor
        import joblib
    except ImportError as exc:
        raise RuntimeError("Model fitting requires xgboost and joblib; install the baseline extra") from exc

    train = _load_feature_file(train_archive)
    test = _load_feature_file(test_archive)
    X_train, y_train = train["X"], train["y_log10"]
    X_test, y_test = test["X"], test["y_log10"]
    if X_test.shape[1] != X_train.shape[1] or len(y_test) == 0:
        raise ValueError("Held-out archive dimensions do not match training features")
    for metadata_key in ("feature_model", "fingerprint_radius", "fingerprint_bits"):
        if metadata_key in train and metadata_key in test:
            if not np.array_equal(train[metadata_key], test[metadata_key]):
                raise ValueError(f"Training and held-out feature metadata differ: {metadata_key}")
    for group_name in holdout_group_arrays:
        if group_name not in train or group_name not in test:
            raise ValueError(f"Holdout grouping array is missing from train/test: {group_name}")
        train_groups = np.asarray(train[group_name]).reshape(-1)
        test_groups = np.asarray(test[group_name]).reshape(-1)
        if len(train_groups) != len(y_train) or len(test_groups) != len(y_test):
            raise ValueError(f"Holdout grouping array does not align with rows: {group_name}")
        if set(train_groups.astype(str)).intersection(set(test_groups.astype(str))):
            raise ValueError(f"Group leakage detected for held-out axis: {group_name}")

    if "target" in train and str(train["target"].reshape(-1)[0]) != target:
        raise ValueError("Training archive target does not match requested target")
    if "target" in test and str(test["target"].reshape(-1)[0]) != target:
        raise ValueError("Held-out archive target does not match requested target")

    if group_array:
        if group_array not in train:
            raise ValueError(f"Requested group array {group_array!r} is absent")
        if group_array not in test:
            raise ValueError(f"Held-out archive is missing grouping array {group_array!r}")
        groups = np.asarray(train[group_array]).reshape(-1)
        held_out_groups = np.asarray(test[group_array]).reshape(-1)
        if len(groups) != len(y_train) or len(np.unique(groups)) < 2:
            raise ValueError("Group array must align with training rows and contain >=2 groups")
        if len(held_out_groups) != len(y_test):
            raise ValueError("Held-out group array does not align with held-out rows")
        if set(groups.astype(str)).intersection(set(held_out_groups.astype(str))):
            raise ValueError("Group leakage detected between training and held-out archives")
        folds = min(n_splits, len(np.unique(groups)))
        if folds < 2:
            raise ValueError("At least two unique groups are required for grouped CV")
        cv = GroupKFold(n_splits=folds)
        cv_scores = -cross_val_score(
            XGBRegressor(
                n_estimators=n_estimators, max_depth=max_depth, learning_rate=0.05,
                subsample=0.85, colsample_bytree=0.85, objective="reg:squarederror",
                n_jobs=-1, random_state=random_state, tree_method="hist",
            ),
            X_train, y_train, cv=cv, groups=groups,
            scoring="neg_root_mean_squared_error", n_jobs=1,
        )
        split_strategy = f"group_k_fold:{group_array}"
    else:
        folds = min(n_splits, len(y_train))
        if folds < 2:
            raise ValueError("At least two training rows are required")
        cv = KFold(n_splits=folds, shuffle=True, random_state=random_state)
        cv_scores = -cross_val_score(
            XGBRegressor(
                n_estimators=n_estimators, max_depth=max_depth, learning_rate=0.05,
                subsample=0.85, colsample_bytree=0.85, objective="reg:squarederror",
                n_jobs=-1, random_state=random_state, tree_method="hist",
            ),
            X_train, y_train, cv=cv,
            scoring="neg_root_mean_squared_error", n_jobs=1,
        )
        split_strategy = "row_random_k_fold_diagnostic_only"

    estimator = XGBRegressor(
        n_estimators=n_estimators, max_depth=max_depth, learning_rate=0.05,
        subsample=0.85, colsample_bytree=0.85, objective="reg:squarederror",
        n_jobs=-1, random_state=random_state, tree_method="hist",
    )
    estimator.fit(X_train, y_train)
    predictions = estimator.predict(X_test)
    calibration = _load_feature_file(calibration_archive) if calibration_archive else None
    conformal_q = None
    if calibration is not None:
        X_cal, y_cal = calibration["X"], calibration["y_log10"]
        if X_cal.shape[1] != X_train.shape[1]:
            raise ValueError("Calibration feature dimension does not match training features")
        if "target" in calibration and str(calibration["target"].reshape(-1)[0]) != target:
            raise ValueError("Calibration archive target does not match requested target")
        for metadata_key in ("feature_model", "fingerprint_radius", "fingerprint_bits"):
            if metadata_key in train and metadata_key in calibration:
                if not np.array_equal(train[metadata_key], calibration[metadata_key]):
                    raise ValueError(f"Calibration feature metadata differ: {metadata_key}")
        for group_name in holdout_group_arrays:
            if group_name not in calibration:
                raise ValueError(f"Calibration archive missing leakage-check array: {group_name}")
            train_groups = set(np.asarray(train[group_name]).astype(str).reshape(-1))
            calibration_groups = set(np.asarray(calibration[group_name]).astype(str).reshape(-1))
            test_groups = set(np.asarray(test[group_name]).astype(str).reshape(-1))
            if train_groups.intersection(calibration_groups):
                raise ValueError(f"Group leakage between training and calibration: {group_name}")
            if train_groups.intersection(test_groups) or calibration_groups.intersection(test_groups):
                raise ValueError(f"Group leakage across train/calibration/test: {group_name}")
        calibration_predictions = estimator.predict(X_cal)
        conformal_q = conformal_quantile(
            y_cal, calibration_predictions, alpha=conformal_alpha
        )

    domain = ApplicabilityDomain(quantile=applicability_quantile).fit(X_train)
    domain_test = domain.score(X_test)
    applicability_summary = {
        "method": domain_test["method"],
        "threshold": float(domain_test["threshold"]),
        "quantile": float(domain_test["quantile"]),
        "reference_size": int(domain_test["reference_size"]),
        "within_domain_fraction": float(np.mean(domain_test["within_domain"])),
        "n_flagged": int(np.sum(~domain_test["within_domain"])),
        "interpretation": domain_test["interpretation"],
    }
    if "source_record_ids" in test:
        record_ids = np.asarray(test["source_record_ids"]).astype(str)
    else:
        record_ids = np.arange(len(y_test)).astype(str)
    prediction_table = pd.DataFrame({
        "source_record_id": record_ids,
        "y_true_log10": y_test.astype(float),
        "y_pred_log10": predictions.astype(float),
        "y_true_canonical": np.power(10.0, y_test.astype(float)),
        "y_pred_canonical": np.power(10.0, predictions.astype(float)),
    })
    report = {
        "target": target,
        "cross_validation": {
            "strategy": split_strategy,
            "folds": int(folds),
            "rmse_mean_log10": float(np.mean(cv_scores)),
            "rmse_std_log10": float(np.std(cv_scores)),
            "fold_rmse_log10": cv_scores.tolist(),
        },
        "held_out": regression_report(y_test, predictions, target=target),
        "n_train": int(len(y_train)),
        "n_held_out": int(len(y_test)),
        "feature_dimension": int(X_train.shape[1]),
        "random_state": random_state,
        "model_parameters": {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": 0.05,
            "subsample": 0.85,
            "colsample_bytree": 0.85,
        },
        "applicability_domain": applicability_summary,
        "calibration": ({
            "method": "split_conformal_absolute_residual",
            "alpha": float(conformal_alpha),
            "quantile_log10": float(conformal_q),
            "n_calibration": int(len(calibration["y_log10"])),
            "test_empirical_coverage": float(np.mean(
                np.abs(y_test - predictions) <= conformal_q
            )),
            "test_mean_interval_width_log10": float(2.0 * conformal_q),
            "coverage_note": (
                "Empirical coverage on the held-out test set is descriptive; "
                "formal split-conformal guarantees require exchangeability and "
                "a calibration set untouched by model selection."
            ),
        } if calibration is not None else {
            "method": None,
            "status": "not_calibrated",
            "reason": "No independent calibration archive was supplied."
        }),
        "warning": (
            "Row-random CV is diagnostic only; it does not establish protein or "
            "chemical cold-start generalization."
            if not group_array else None
        ),
    }
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    bundle = {
        "estimator": estimator,
        "target": target,
        "feature_dimension": int(X_train.shape[1]),
        "feature_model": str(train.get("feature_model", np.asarray(["unknown"])).reshape(-1)[0]),
        "fingerprint_radius": int(train.get("fingerprint_radius", np.asarray([-1])).reshape(-1)[0]),
        "fingerprint_bits": int(train.get("fingerprint_bits", np.asarray([-1])).reshape(-1)[0]),
        "canonical_unit": "M" if target == "km" else "s^-1",
        "conformal_quantile_log10": conformal_q,
        "conformal_alpha": float(conformal_alpha) if conformal_q is not None else None,
        "applicability_domain": domain,
        "context_encoder": None,
    }
    if context_encoder_path is not None:
        bundle["context_encoder"] = joblib.load(context_encoder_path)

    joblib.dump(bundle, output / f"{target}_model.joblib", compress=3)
    estimator.save_model(output / f"{target}_model.json")
    metrics_path = output / f"{target}_metrics.json"
    write_json_atomic(report, metrics_path)
    predictions_path = output / f"{target}_predictions.csv"
    prediction_table.to_csv(predictions_path, index=False)

    model_path = output / f"{target}_model.joblib"
    model_card_path = output / f"{target}_MODEL_CARD.md"
    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    write_model_card({
        "model_name": f"Kinetics {target} predictor",
        "model_version": "0.1.0",
        "software_version": "0.2.0",
        "created_at": run_stamp,
        "intended_use": [
            "Research analysis and hypothesis generation under documented applicability limits.",
            "Prioritization of candidates for subsequent experimental measurement."
        ],
        "out_of_scope_use": [
            "Treating predictions as experimental measurements.",
            "Clinical, regulatory, or safety-critical decisions without independent validation."
        ],
        "dataset": {
            "name": "Training feature archive",
            "version": "see experiment manifest",
            "source_url": "see source dataset provenance",
            "license": "see source dataset provenance",
            "n_observations": int(len(y_train)),
            "manifest": f"{target}_experiment_manifest.json"
        },
        "evaluation": {
            "split_strategy": split_strategy,
            "n_test": int(len(y_test)),
            "metrics": report["held_out"],
            "uncertainty_method": "not calibrated by this fitting function"
        },
        "limitations": [
            "Performance depends on dataset coverage, assay context, and distribution shift.",
            "A held-out score does not establish external validity unless the split is genuinely independent.",
            "No uncertainty interval is produced by this fitting function."
        ],
        "experiment_manifest": f"{target}_experiment_manifest.json",
        "feature_encoder": bundle["feature_model"],
        "model_sha256": file_record(model_path)["sha256"],
        "random_seed": random_state
    }, model_card_path)

    manifest = build_experiment_manifest(
        experiment_id=f"{target}-{run_stamp}",
        research_question=f"Estimate enzyme {target} from protein sequence and substrate representation",
        inputs=[train_archive, test_archive],
        outputs=[model_path, output / f"{target}_model.json", metrics_path,
                 predictions_path, model_card_path],
        configuration={
            "target": target,
            "cross_validation_strategy": split_strategy,
            "group_array": group_array,
            "holdout_group_arrays": list(holdout_group_arrays),
            "folds": int(folds),
            "random_state": random_state,
            "model_parameters": report["model_parameters"]
        },
        notes=[
            "This manifest is generated when the fitting function is run.",
            "Predictions are computational estimates, not experimental measurements."
        ]
    )
    save_experiment_manifest(manifest, output / f"{target}_experiment_manifest.json")
    LOG.info("Saved %s model, model card, metrics, and experiment manifest under %s", target, output)
    return report
