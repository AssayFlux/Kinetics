#!/usr/bin/env python3
"""Compare exploratory NB2 IRLS with an independent SciPy likelihood optimizer."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

try:
    import numpy as np
    import scipy
    from scipy.optimize import minimize
    from scipy.special import gammaln
    from scipy.stats import norm
except ImportError as error:
    raise SystemExit(
        "Install the pinned validation dependencies from validation/requirements-scipy.txt"
    ) from error

from kinetics.omics import negative_binomial_differential_expression


def median(values: list[float]) -> float:
    ordered = sorted(values)
    middle = len(ordered) // 2
    return ordered[middle] if len(ordered) % 2 else (
        ordered[middle - 1] + ordered[middle]
    ) / 2.0


def size_factors(counts: np.ndarray) -> np.ndarray:
    sample_count = counts.shape[1]
    ratios: list[list[float]] = [[] for _ in range(sample_count)]
    for row in counts:
        if np.all(row > 0):
            geometric_mean = float(np.exp(np.log(row).mean()))
            for sample in range(sample_count):
                ratios[sample].append(float(row[sample] / geometric_mean))
    if not all(ratios):
        raise ValueError("Reference fixture requires positive ratios for every sample")
    factors = np.asarray([median(values) for values in ratios], dtype=float)
    return factors / float(np.exp(np.log(factors).mean()))


def scipy_nb2_fit(
    counts: np.ndarray,
    condition: np.ndarray,
    offsets: np.ndarray,
    alpha: float,
) -> dict[str, float | bool]:
    design = np.column_stack((np.ones(condition.size), condition))
    size = 1.0 / alpha

    def objective(beta: np.ndarray) -> float:
        mean = np.exp(design @ beta + offsets)
        log_likelihood = (
            gammaln(counts + size) - gammaln(size) - gammaln(counts + 1.0)
            + size * np.log(size / (size + mean))
            + counts * np.log(mean / (size + mean))
        )
        return -float(np.sum(log_likelihood))

    def gradient(beta: np.ndarray) -> np.ndarray:
        mean = np.exp(design @ beta + offsets)
        return design.T @ ((mean - counts) / (1.0 + alpha * mean))

    initial = np.asarray([
        math.log((float(counts.sum()) + 0.5) / condition.size) - float(offsets.mean()),
        0.0,
    ])
    fitted = minimize(
        objective,
        initial,
        jac=gradient,
        method="L-BFGS-B",
        options={"gtol": 1e-10, "ftol": 1e-15, "maxiter": 10_000, "maxls": 50},
    )
    mean = np.exp(design @ fitted.x + offsets)
    weights = mean / (1.0 + alpha * mean)
    information = design.T @ (weights[:, None] * design)
    covariance = np.linalg.inv(information)
    standard_error = float(np.sqrt(covariance[1, 1]))
    z_value = float(fitted.x[1] / standard_error)
    p_value = float(2.0 * norm.sf(abs(z_value)))
    return {
        "converged": bool(fitted.success),
        "condition_coefficient": float(fitted.x[1]),
        "standard_error": standard_error,
        "wald_z": z_value,
        "p_value": p_value,
        "gradient_max_abs": float(np.max(np.abs(fitted.jac))),
    }


def run() -> dict[str, object]:
    raw_counts = np.asarray([
        [90, 110, 95, 105, 100, 98, 102, 101],
        [15, 18, 16, 17, 70, 75, 72, 78],
    ], dtype=float)
    condition = np.asarray([0, 0, 0, 0, 1, 1, 1, 1], dtype=float)
    factors = size_factors(raw_counts)
    offsets = np.log(factors)
    local = negative_binomial_differential_expression(
        raw_counts.astype(int).tolist(), condition.astype(int).tolist(),
        feature_ids=["stable", "induced"],
    )
    comparisons = []
    for index, feature_id in enumerate(("stable", "induced")):
        normalized = raw_counts[index] / factors
        mean = float(normalized.mean())
        variance = float(normalized.var(ddof=1))
        alpha = min(10.0, max(1e-8, (variance - mean) / max(mean * mean, 1e-12)))
        reference = scipy_nb2_fit(raw_counts[index], condition, offsets, alpha)
        observed = local[index]
        checks = {
            "condition_coefficient": abs(
                float(observed["condition_coefficient"]) - reference["condition_coefficient"]
            ) <= 1e-6,
            "standard_error": abs(
                float(observed["standard_error"]) - reference["standard_error"]
            ) <= 1e-6,
            "wald_p_value": abs(
                float(observed["p_value"]) - reference["p_value"]
            ) <= 1e-6,
            "local_converged": bool(observed["converged"]),
            "reference_converged": bool(reference["converged"]),
            "reference_gradient": float(reference["gradient_max_abs"]) <= 1e-6,
        }
        comparisons.append({
            "feature_id": feature_id,
            "dispersion": alpha,
            "checks": checks,
            "pass": all(checks.values()),
            "kinetics": {
                "condition_coefficient": observed["condition_coefficient"],
                "standard_error": observed["standard_error"],
                "wald_z": observed["wald_z"],
                "p_value": observed["p_value"],
            },
            "scipy_reference": reference,
        })
    return {
        "validation_id": "kinetics-nb2-scipy-reference-2026-11-09",
        "reference": "scipy.optimize.minimize (L-BFGS-B), NB2 log likelihood",
        "scipy_version": scipy.__version__,
        "numpy_version": np.__version__,
        "method": "fixed shared median-of-ratios offsets and per-feature moment dispersion; independent likelihood optimization",
        "tolerances": {
            "condition_coefficient": 1e-6,
            "standard_error": 1e-6,
            "wald_p_value": 1e-6,
            "reference_gradient_max_abs": 1e-6,
        },
        "comparisons": comparisons,
        "overall_pass": all(item["pass"] for item in comparisons),
        "limitations": [
            "Deterministic synthetic counts only; no external omics dataset is included.",
            "Dispersion is fixed to the local moment estimate to isolate the GLM optimizer comparison.",
            "Does not validate dispersion moderation, repeated measures, outlier robustness, null calibration, power or FDR control.",
            "This host-only reference does not establish Android runtime or biological validity.",
        ],
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["overall_pass"]:
        raise SystemExit(1)
