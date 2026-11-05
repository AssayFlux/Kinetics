"""Split-conformal intervals for regression predictions on the log10 target scale."""
from __future__ import annotations

import math

import numpy as np


def conformal_quantile(calibration_truth, calibration_prediction, *, alpha: float = 0.1) -> float:
    """Return the finite-sample absolute-residual conformal quantile."""
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be strictly between 0 and 1")
    truth = np.asarray(calibration_truth, dtype=float).reshape(-1)
    prediction = np.asarray(calibration_prediction, dtype=float).reshape(-1)
    if truth.shape != prediction.shape or truth.size == 0:
        raise ValueError("Calibration arrays must be non-empty and have equal shape")
    if not np.isfinite(truth).all() or not np.isfinite(prediction).all():
        raise ValueError("Calibration arrays must be finite")
    residuals = np.abs(truth - prediction)
    n = residuals.size
    rank = min(n, math.ceil((n + 1) * (1.0 - alpha)))
    return float(np.partition(residuals, rank - 1)[rank - 1])


def conformal_interval(prediction_log10, quantile: float, *, target: str) -> dict:
    """Convert a log10 conformal interval to canonical original units."""
    if target not in ("km", "kcat"):
        raise ValueError("target must be 'km' or 'kcat'")
    if not math.isfinite(float(quantile)) or quantile < 0:
        raise ValueError("quantile must be finite and non-negative")
    prediction = np.asarray(prediction_log10, dtype=float)
    if not np.isfinite(prediction).all():
        raise ValueError("predictions must be finite")
    lower_log = prediction - quantile
    upper_log = prediction + quantile
    unit = "M" if target == "km" else "s^-1"
    return {
        "target": target,
        "canonical_unit": unit,
        "prediction_log10": prediction,
        "lower_log10": lower_log,
        "upper_log10": upper_log,
        "prediction": np.power(10.0, prediction),
        "lower": np.power(10.0, lower_log),
        "upper": np.power(10.0, upper_log),
        "method": "split_conformal_absolute_residual",
        "quantile": float(quantile),
    }
