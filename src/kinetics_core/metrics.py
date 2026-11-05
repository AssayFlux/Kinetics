"""Target-specific regression metrics in log and original measurement scales."""
from __future__ import annotations

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def regression_report(y_true_log10, y_pred_log10, *, target: str) -> dict:
    """Summarize log-scale and original-unit error for Km or kcat.

    Inputs are log10(M) for Km or log10(s^-1) for kcat. Metrics are computed
    separately per target; this function deliberately does not combine targets.
    """
    if target not in ("km", "kcat"):
        raise ValueError("target must be 'km' or 'kcat'")
    truth = np.asarray(y_true_log10, dtype=float).reshape(-1)
    prediction = np.asarray(y_pred_log10, dtype=float).reshape(-1)
    if truth.shape != prediction.shape or truth.size == 0:
        raise ValueError("truth and prediction must be non-empty arrays with equal shape")
    if not np.isfinite(truth).all() or not np.isfinite(prediction).all():
        raise ValueError("truth and prediction must contain only finite values")

    true_value = np.power(10.0, truth)
    predicted_value = np.power(10.0, prediction)
    absolute_error = np.abs(predicted_value - true_value)
    relative_error = absolute_error / true_value
    fold_error = np.maximum(predicted_value / true_value, true_value / predicted_value)
    unit = "M" if target == "km" else "s^-1"
    return {
        "target": target,
        "n": int(truth.size),
        "canonical_unit": unit,
        "log10": {
            "mae": float(mean_absolute_error(truth, prediction)),
            "rmse": float(np.sqrt(mean_squared_error(truth, prediction))),
            "r2": float(r2_score(truth, prediction)) if truth.size > 1 else None,
        },
        "original_scale": {
            "mae": float(np.mean(absolute_error)),
            "rmse": float(np.sqrt(np.mean(np.square(predicted_value - true_value)))),
            "median_absolute_relative_error": float(np.median(relative_error)),
            "median_fold_error": float(np.median(fold_error)),
        },
    }



def subgroup_regression_report(
    y_true_log10,
    y_pred_log10,
    groups,
    *,
    target: str,
    min_group_size: int = 5,
    conformal_quantile_log10: float | None = None,
) -> dict:
    """Report per-group errors and optional empirical interval coverage.

    Small groups remain visible but are marked insufficient for stable metric
    interpretation. Coverage is descriptive, not a subgroup guarantee.
    """
    if target not in ("km", "kcat"):
        raise ValueError("target must be 'km' or 'kcat'")
    truth = np.asarray(y_true_log10, dtype=float).reshape(-1)
    prediction = np.asarray(y_pred_log10, dtype=float).reshape(-1)
    labels = np.asarray(groups).astype(str).reshape(-1)
    if truth.shape != prediction.shape or truth.shape != labels.shape:
        raise ValueError("truth, prediction, and groups must have equal lengths")
    if truth.size == 0 or not np.isfinite(truth).all() or not np.isfinite(prediction).all():
        raise ValueError("truth and prediction must be non-empty and finite")
    if min_group_size < 1:
        raise ValueError("min_group_size must be positive")
    if conformal_quantile_log10 is not None and (
        not np.isfinite(conformal_quantile_log10) or conformal_quantile_log10 < 0
    ):
        raise ValueError("conformal quantile must be finite and non-negative")
    results = []
    for label in sorted(np.unique(labels)):
        mask = labels == label
        n = int(mask.sum())
        item = {"group": label, "n": n}
        if n < min_group_size:
            item["status"] = "insufficient_group_size"
        else:
            item["status"] = "reported"
            item["metrics"] = regression_report(
                truth[mask], prediction[mask], target=target
            )
        if conformal_quantile_log10 is not None:
            item["empirical_interval_coverage"] = float(np.mean(
                np.abs(truth[mask] - prediction[mask]) <= conformal_quantile_log10
            ))
            item["interval_width_log10"] = float(2.0 * conformal_quantile_log10)
        results.append(item)
    return {
        "target": target,
        "min_group_size": int(min_group_size),
        "n_groups": int(len(results)),
        "groups": results,
        "coverage_interpretation": (
            "Subgroup coverage is descriptive and does not establish a formal "
            "conditional coverage guarantee."
            if conformal_quantile_log10 is not None else None
        ),
    }
