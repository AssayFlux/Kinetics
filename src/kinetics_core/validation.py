"""Deterministic paired-bootstrap uncertainty summaries for held-out benchmarks."""
from __future__ import annotations

import numpy as np

from .metrics import regression_report


def bootstrap_regression_intervals(
    y_true_log10,
    y_pred_log10,
    *,
    target: str,
    n_resamples: int = 2000,
    confidence_level: float = 0.95,
    random_state: int = 42,
) -> dict:
    """Percentile CIs from paired row bootstrap; descriptive, not a new test set.

    Resampling preserves truth/prediction pairing. These intervals quantify
    held-out sample uncertainty only; they do not correct dataset shift,
    dependence within protein/scaffold clusters, or model-selection bias.
    """
    truth = np.asarray(y_true_log10, dtype=float).reshape(-1)
    prediction = np.asarray(y_pred_log10, dtype=float).reshape(-1)
    if truth.shape != prediction.shape or truth.size < 2:
        raise ValueError("truth and prediction must have equal length >= 2")
    if not np.isfinite(truth).all() or not np.isfinite(prediction).all():
        raise ValueError("truth and prediction must be finite")
    if n_resamples < 100:
        raise ValueError("n_resamples must be at least 100")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1")

    rng = np.random.default_rng(random_state)
    n = truth.size
    metrics = ("mae", "rmse")
    samples = {name: [] for name in metrics}
    for _ in range(n_resamples):
        indices = rng.integers(0, n, size=n)
        report = regression_report(truth[indices], prediction[indices], target=target)
        for name in metrics:
            samples[name].append(report["log10"][name])
    alpha = (1.0 - confidence_level) / 2.0
    intervals = {
        name: {
            "lower": float(np.quantile(values, alpha)),
            "upper": float(np.quantile(values, 1.0 - alpha)),
        }
        for name, values in samples.items()
    }
    return {
        "method": "paired_row_percentile_bootstrap",
        "n_resamples": int(n_resamples),
        "confidence_level": float(confidence_level),
        "random_state": int(random_state),
        "sample_size": int(n),
        "log10_metric_intervals": intervals,
        "limitations": [
            "Intervals are descriptive for this held-out sample.",
            "Row bootstrap does not account for dependence within protein or scaffold clusters.",
            "Intervals do not establish external validity or calibrated predictive uncertainty.",
        ],
    }


def bootstrap_cluster_regression_intervals(
    y_true_log10,
    y_pred_log10,
    cluster_ids,
    *,
    target: str,
    n_resamples: int = 2000,
    confidence_level: float = 0.95,
    random_state: int = 42,
) -> dict:
    """Percentile intervals from a paired cluster bootstrap.

    Unique clusters are sampled with replacement; all observations belonging
    to each sampled cluster are retained. This preserves within-cluster
    dependence. It does not address dataset shift or model-selection bias.
    """
    truth = np.asarray(y_true_log10, dtype=float).reshape(-1)
    prediction = np.asarray(y_pred_log10, dtype=float).reshape(-1)
    groups = np.asarray(cluster_ids).astype(str).reshape(-1)
    if truth.shape != prediction.shape or truth.size < 2:
        raise ValueError("truth and prediction must have equal length >= 2")
    if groups.size != truth.size:
        raise ValueError("cluster_ids must align with truth and prediction")
    if not np.isfinite(truth).all() or not np.isfinite(prediction).all():
        raise ValueError("truth and prediction must be finite")
    if n_resamples < 100:
        raise ValueError("n_resamples must be at least 100")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1")
    unique_groups = np.unique(groups)
    if len(unique_groups) < 2:
        raise ValueError("cluster bootstrap requires at least two clusters")

    members = {group: np.flatnonzero(groups == group) for group in unique_groups}
    rng = np.random.default_rng(random_state)
    samples = {"mae": [], "rmse": []}
    for _ in range(n_resamples):
        selected = rng.choice(unique_groups, size=len(unique_groups), replace=True)
        indices = np.concatenate([members[group] for group in selected])
        report = regression_report(truth[indices], prediction[indices], target=target)
        for metric in samples:
            samples[metric].append(report["log10"][metric])
    alpha = (1.0 - confidence_level) / 2.0
    return {
        "method": "paired_cluster_percentile_bootstrap",
        "n_resamples": int(n_resamples),
        "confidence_level": float(confidence_level),
        "random_state": int(random_state),
        "sample_size": int(truth.size),
        "cluster_count": int(len(unique_groups)),
        "log10_metric_intervals": {
            metric: {
                "lower": float(np.quantile(values, alpha)),
                "upper": float(np.quantile(values, 1.0 - alpha)),
            }
            for metric, values in samples.items()
        },
        "limitations": [
            "Intervals describe the supplied held-out clusters only.",
            "Few independent clusters can make percentile intervals unstable.",
            "Intervals do not establish external validity or calibrated predictive uncertainty.",
        ],
    }
