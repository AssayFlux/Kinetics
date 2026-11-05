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
