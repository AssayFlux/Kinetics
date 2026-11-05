"""Target-specific model fitting workflow; definitions only, not executed during build."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.model_selection import GroupKFold, KFold, cross_val_score

from .metrics import regression_report
from .provenance import write_json_atomic

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
    random_state: int = 42,
    n_estimators: int = 500,
    max_depth: int = 6,
    n_splits: int = 5,
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
    except ImportError as exc:
        raise RuntimeError("Model fitting requires xgboost; install the baseline extra") from exc

    train = _load_feature_file(train_archive)
    test = _load_feature_file(test_archive)
    X_train, y_train = train["X"], train["y_log10"]
    X_test, y_test = test["X"], test["y_log10"]
    if X_test.shape[1] != X_train.shape[1] or len(y_test) == 0:
        raise ValueError("Held-out archive dimensions do not match training features")
    if "target" in train and str(train["target"].reshape(-1)[0]) != target:
        raise ValueError("Training archive target does not match requested target")
    if "target" in test and str(test["target"].reshape(-1)[0]) != target:
        raise ValueError("Held-out archive target does not match requested target")

    if group_array:
        if group_array not in train:
            raise ValueError(f"Requested group array {group_array!r} is absent")
        groups = np.asarray(train[group_array]).reshape(-1)
        if len(groups) != len(y_train) or len(np.unique(groups)) < 2:
            raise ValueError("Group array must align with training rows and contain >=2 groups")
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
    }
    joblib.dump(bundle, output / f"{target}_model.joblib", compress=3)
    estimator.save_model(output / f"{target}_model.json")
    write_json_atomic(report, output / f"{target}_metrics.json")
    LOG.info("Saved %s model and report under %s", target, output)
    return report
