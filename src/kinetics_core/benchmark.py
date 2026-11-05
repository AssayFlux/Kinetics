"""Leakage-aware comparison of classical regression baselines.

Candidate selection uses training-only cross-validation. The held-out archive is
scored after selection and must never be used to choose a model or tune settings.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold, KFold, cross_val_score

from .metrics import regression_report
from .modeling import _load_feature_file, _validate_feature_metadata
from .provenance import write_json_atomic


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
    X_train, y_train = train["X"], train["y_log10"]
    X_test, y_test = test["X"], test["y_log10"]
    if X_train.shape[1] != X_test.shape[1]:
        raise ValueError("train/test feature dimensions differ")
    _validate_feature_metadata(train, test, label="training/held-out")
    for name in holdout_group_arrays:
        if name not in train or name not in test:
            raise ValueError(f"Missing required holdout grouping array: {name}")
        left = set(np.asarray(train[name]).astype(str).reshape(-1))
        right = set(np.asarray(test[name]).astype(str).reshape(-1))
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
        if len(groups) != len(y_train) or len(np.unique(groups)) < 2:
            raise ValueError("group array must align with training rows and contain >=2 groups")
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
        scores = -cross_val_score(
            estimator, X_train, y_train, cv=splitter, groups=cv_groups,
            scoring="neg_root_mean_squared_error", n_jobs=1,
        )
        fitted[name] = estimator
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
        "candidates": results,
        "held_out": regression_report(y_test, test_prediction, target=target),
        "n_train": int(len(y_train)),
        "n_held_out": int(len(y_test)),
        "warning": (
            "Random row CV is diagnostic only and does not establish cold-start "
            "generalization."
            if group_array is None else None
        ),
    }
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    import joblib
    joblib.dump({
        "estimator": selected,
        "target": target,
        "feature_dimension": int(X_train.shape[1]),
        "selected_model": selected_name,
        "selection_rule": report["selection_rule"],
    }, output / f"{target}_baseline_comparison_model.joblib", compress=3)
    write_json_atomic(report, output / f"{target}_baseline_comparison.json")
    return report
