"""Leakage-aware comparison of classical regression baselines.

Candidate selection uses training-only cross-validation. The held-out archive is
scored after selection and must never be used to choose a model or tune settings.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    ExtraTreesRegressor,
    HistGradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold, KFold, cross_val_score

from .context import context_design_matrix, make_context_pipeline
from .experiments import build_experiment_manifest, save_experiment_manifest
from .metrics import regression_report, subgroup_regression_report
from .modeling import _load_feature_file, _validate_feature_metadata
from .validation import (
    bootstrap_cluster_regression_intervals,
    bootstrap_regression_intervals,
)
from .model_card import write_model_card
from .provenance import file_record, write_json_atomic


def _candidates(random_state: int) -> dict[str, Any]:
    return {
        "ridge": Ridge(alpha=10.0),
        "random_forest": RandomForestRegressor(
            n_estimators=500, min_samples_leaf=2, max_features=0.8,
            n_jobs=-1, random_state=random_state,
        ),
        "extra_trees": ExtraTreesRegressor(
            n_estimators=500, min_samples_leaf=2, max_features=0.8,
            n_jobs=-1, random_state=random_state,
        ),
        "hist_gradient_boosting": HistGradientBoostingRegressor(
            max_iter=300, learning_rate=0.05, l2_regularization=1.0,
            random_state=random_state,
        ),
    }


def compare_regressors(
    train_archive: str | Path,
    test_archive: str | Path,
    *,
    target: str,
    output_dir: str | Path,
    group_array: str | None = None,
    holdout_group_arrays: tuple[str, ...] = (),
    random_state: int = 42,
    n_splits: int = 5,
) -> dict[str, Any]:
    """Compare fixed baselines with CV selection and one untouched test score."""
    if target not in ("km", "kcat"):
        raise ValueError("target must be 'km' or 'kcat'")
    train, test = _load_feature_file(train_archive), _load_feature_file(test_archive)
    context_enabled = "X_base" in train
    if context_enabled != ("X_base" in test):
        raise ValueError("Training and held-out archives differ in assay-context availability")
    if context_enabled:
        X_train, X_test = context_design_matrix(train), context_design_matrix(test)
        numeric_columns = tuple(train["context_numeric_columns"].astype(str))
        categorical_columns = tuple(train["context_categorical_columns"].astype(str))
        if tuple(test["context_numeric_columns"].astype(str)) != numeric_columns:
            raise ValueError("Training and held-out numeric context columns differ")
        if tuple(test["context_categorical_columns"].astype(str)) != categorical_columns:
            raise ValueError("Training and held-out categorical context columns differ")
        base_dimension = int(train["X_base"].shape[1])
    else:
        X_train, X_test = train["X"], test["X"]
        numeric_columns, categorical_columns = (), ()
        base_dimension = int(X_train.shape[1])
    y_train, y_test = train["y_log10"], test["y_log10"]
    if X_train.shape[1] != X_test.shape[1]:
        raise ValueError("train/test feature dimensions differ")
    _validate_feature_metadata(train, test, label="training/held-out")
    for name in holdout_group_arrays:
        if name not in train or name not in test:
            raise ValueError(f"Missing required holdout grouping array: {name}")
        left_values = np.asarray(train[name]).astype(str).reshape(-1)
        right_values = np.asarray(test[name]).astype(str).reshape(-1)
        if len(left_values) != len(y_train) or len(right_values) != len(y_test):
            raise ValueError(f"Holdout grouping array does not align with rows: {name}")
        left = set(left_values)
        right = set(right_values)
        if left.intersection(right):
            raise ValueError(f"Group leakage detected on holdout axis {name}")
    if "target" in train and str(train["target"].reshape(-1)[0]) != target:
        raise ValueError("training archive target mismatch")
    if "target" in test and str(test["target"].reshape(-1)[0]) != target:
        raise ValueError("test archive target mismatch")

    if group_array:
        if group_array not in train or group_array not in test:
            raise ValueError(f"Missing grouped CV array: {group_array}")
        groups = np.asarray(train[group_array]).astype(str).reshape(-1)
        test_groups = np.asarray(test[group_array]).astype(str).reshape(-1)
        if (
            len(groups) != len(y_train)
            or len(test_groups) != len(y_test)
            or len(np.unique(groups)) < 2
        ):
            raise ValueError("group arrays must align with train/test rows and train contain >=2 groups")
        if set(groups).intersection(set(test_groups)):
            raise ValueError("Group leakage between training and held-out archive")
        folds = min(n_splits, len(np.unique(groups)))
        splitter = GroupKFold(n_splits=folds)
        cv_groups = groups
        split_label = f"group_k_fold:{group_array}"
    else:
        folds = min(n_splits, len(y_train))
        splitter = KFold(n_splits=folds, shuffle=True, random_state=random_state)
        cv_groups = None
        split_label = "row_random_k_fold_diagnostic_only"
    if folds < 2:
        raise ValueError("At least two CV folds are required")

    results = []
    fitted = {}
    for name, estimator in _candidates(random_state).items():
        candidate = (
            make_context_pipeline(
                estimator,
                numeric_columns=numeric_columns,
                categorical_columns=categorical_columns,
                base_dimension=base_dimension,
            )
            if context_enabled else estimator
        )
        scores = -cross_val_score(
            candidate, X_train, y_train, cv=splitter, groups=cv_groups,
            scoring="neg_root_mean_squared_error", n_jobs=1,
        )
        fitted[name] = candidate
        results.append({
            "model": name,
            "cv_rmse_mean_log10": float(np.mean(scores)),
            "cv_rmse_std_log10": float(np.std(scores)),
            "fold_rmse_log10": scores.tolist(),
        })
    results.sort(key=lambda row: row["cv_rmse_mean_log10"])
    selected_name = results[0]["model"]
    selected = fitted[selected_name]
    selected.fit(X_train, y_train)
    test_prediction = selected.predict(X_test)
    report = {
        "target": target,
        "selection_rule": "minimum mean training-only CV RMSE; held-out test excluded from selection",
        "cv_strategy": split_label,
        "folds": int(folds),
        "selected_model": selected_name,
        "context_features_enabled": context_enabled,
        "feature_dimension": base_dimension,
        "candidates": results,
        "held_out": regression_report(y_test, test_prediction, target=target),
        "held_out_confidence_intervals": bootstrap_regression_intervals(
            y_test, test_prediction, target=target, random_state=random_state,
        ),
        "held_out_cluster_confidence_intervals": {
            name: bootstrap_cluster_regression_intervals(
                y_test, test_prediction, np.asarray(test[name]).reshape(-1),
                target=target, random_state=random_state,
            )
            for name in holdout_group_arrays
        },
        "n_train": int(len(y_train)),
        "n_held_out": int(len(y_test)),
        "subgroup_diagnostics": {
            name: subgroup_regression_report(
                y_test, test_prediction, np.asarray(test[name]).reshape(-1),
                target=target, min_group_size=5,
            )
            for name in holdout_group_arrays
        },
        "warning": (
            "Random row CV is diagnostic only and does not establish cold-start "
            "generalization."
            if group_array is None else None
        ),
    }
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    import joblib
    model_path = output / f"{target}_baseline_comparison_model.joblib"
    report_path = output / f"{target}_baseline_comparison.json"
    predictions_path = output / f"{target}_baseline_predictions.csv"
    model_card_path = output / f"{target}_BASELINE_MODEL_CARD.md"
    joblib.dump({
        "estimator": selected,
        "target": target,
        "feature_dimension": base_dimension,
        "selected_model": selected_name,
        "context_enabled": context_enabled,
        "context_numeric_columns": list(numeric_columns),
        "context_categorical_columns": list(categorical_columns),
        "selection_rule": report["selection_rule"],
    }, model_path, compress=3)
    prediction_table = pd.DataFrame({
        "source_record_id": (
            np.asarray(test["source_record_ids"]).astype(str)
            if "source_record_ids" in test else np.arange(len(y_test)).astype(str)
        ),
        "y_true_log10": y_test.astype(float),
        "y_pred_log10": test_prediction.astype(float),
        "residual_log10": (test_prediction - y_test).astype(float),
    })
    prediction_table.to_csv(predictions_path, index=False)
    write_json_atomic(report, report_path)
    write_model_card({
        "target": target,
        "model_name": f"Kinetics {target} baseline comparison",
        "model_version": "0.1.0",
        "software_version": "0.2.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "intended_use": ["Research baseline comparison and hypothesis generation."],
        "out_of_scope_use": ["Treating predictions as experimental measurements."],
        "dataset": {
            "name": "Training feature archive",
            "version": "see experiment manifest",
            "source_url": "see source provenance",
            "license": "see source provenance",
            "n_observations": int(len(y_train)),
        },
        "evaluation": {
            "split_strategy": split_label,
            "n_test": int(len(y_test)),
            "metrics": report["held_out"],
            "model_selection": report["selection_rule"],
            "uncertainty_method": "not calibrated",
        },
        "limitations": [
            "Model selection uses fixed candidates and training-only cross-validation.",
            "Held-out results are not used for candidate selection.",
            "No uncertainty calibration is performed by this comparison workflow.",
        ],
        "experiment_manifest": f"{target}_baseline_experiment_manifest.json",
        "feature_encoder": str(train.get("feature_model", np.asarray(["unknown"])).reshape(-1)[0]),
        "model_sha256": file_record(model_path)["sha256"],
        "random_seed": random_state,
    }, model_card_path)
    manifest = build_experiment_manifest(
        experiment_id=f"{target}-baseline-comparison",
        research_question=f"Compare classical baselines for enzyme {target} prediction",
        inputs=[train_archive, test_archive],
        outputs=[model_path, report_path, predictions_path, model_card_path],
        configuration={
            "target": target,
            "cv_strategy": split_label,
            "folds": int(folds),
            "selected_model": selected_name,
            "candidate_results": results,
            "random_state": random_state,
        },
        notes=[
            "Candidate selection uses training-only CV; the held-out archive is scored once.",
            "Predictions are computational estimates, not experimental measurements.",
        ],
    )
    save_experiment_manifest(manifest, output / f"{target}_baseline_experiment_manifest.json")
    return report
