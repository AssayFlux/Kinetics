"""Enzyme kinetics models and transparent, dependency-free parameter estimation."""
from __future__ import annotations

from math import isfinite, log, sqrt


def michaelis_menten(substrate: float, vmax: float, km: float) -> float:
    if not all(isfinite(x) for x in (substrate, vmax, km)):
        raise ValueError("Inputs must be finite")
    if substrate < 0 or vmax < 0 or km <= 0:
        raise ValueError("Require S>=0, Vmax>=0 and Km>0")
    return vmax * substrate / (km + substrate)


def inhibition_rate(
    substrate: float, inhibitor: float, vmax: float, km: float,
    ki: float, mode: str, ki_uncompetitive: float | None = None,
) -> float:
    if not all(isfinite(x) for x in (substrate, inhibitor, vmax, km, ki)):
        raise ValueError("Inputs must be finite")
    if substrate < 0 or inhibitor < 0 or vmax < 0 or km <= 0 or ki <= 0:
        raise ValueError("Require S,I,Vmax>=0 and Km,Ki>0")
    alpha = 1 + inhibitor / ki
    if mode == "competitive":
        return vmax * substrate / (alpha * km + substrate)
    if mode == "uncompetitive":
        return vmax * substrate / (km + alpha * substrate)
    if mode == "noncompetitive":
        return (vmax / alpha) * substrate / (km + substrate)
    if mode == "mixed":
        if ki_uncompetitive is None or not isfinite(ki_uncompetitive) or ki_uncompetitive <= 0:
            raise ValueError("mixed inhibition requires finite ki_uncompetitive>0")
        alpha_prime = 1 + inhibitor / ki_uncompetitive
        return vmax * substrate / (alpha * km + alpha_prime * substrate)
    raise ValueError("mode must be competitive, uncompetitive, noncompetitive or mixed")


def fit_michaelis_menten(
    substrates: list[float], rates: list[float], *,
    vmax_bounds: tuple[float, float] | None = None,
    km_bounds: tuple[float, float] | None = None, grid_size: int = 100,
) -> dict[str, object]:
    """Exploratory log-grid fit; diagnostics are descriptive, not validation."""
    if len(substrates) != len(rates) or len(rates) < 3:
        raise ValueError("Need >=3 paired observations")
    if grid_size < 10:
        raise ValueError("grid_size must be >=10")
    if not all(isfinite(x) for x in [*substrates, *rates]):
        raise ValueError("Inputs must be finite")
    if any(x < 0 for x in [*substrates, *rates]):
        raise ValueError("Inputs must be non-negative")
    if max(substrates) == 0 or max(rates) == 0:
        raise ValueError("Non-informative data")

    smax, rmax = max(substrates), max(rates)
    vlo, vhi = vmax_bounds or (rmax * 0.5, rmax * 5)
    klo, khi = km_bounds or (max(smax / 1000, 1e-12), smax * 100)
    if not all(isfinite(x) for x in (vlo, vhi, klo, khi)):
        raise ValueError("Bounds must be finite")
    if not (0 < vlo < vhi and 0 < klo < khi):
        raise ValueError("Bounds must be positive and increasing")

    best: tuple[float, float, float, list[float]] | None = None
    for i in range(grid_size):
        vmax = vlo * (vhi / vlo) ** (i / (grid_size - 1))
        for j in range(grid_size):
            km = klo * (khi / klo) ** (j / (grid_size - 1))
            residuals = [
                observed - michaelis_menten(substrate, vmax, km)
                for substrate, observed in zip(substrates, rates)
            ]
            sse = sum(x * x for x in residuals)
            if best is None or sse < best[0]:
                best = (sse, vmax, km, residuals)

    assert best is not None
    sse, vmax, km, residuals = best
    n = len(rates)
    mean_rate = sum(rates) / n
    total_ss = sum((x - mean_rate) ** 2 for x in rates)
    residual_mean = sum(residuals) / n
    residual_sd = sqrt(sum((x - residual_mean) ** 2 for x in residuals) / (n - 1))
    r_squared = None if total_ss == 0 else 1 - sse / total_ss

    # Gaussian least-squares AIC/BIC, assuming independent homoscedastic errors.
    # A perfect fit has degenerate plug-in likelihood; report undefined values.
    if sse == 0:
        aic = bic = None
    else:
        likelihood_term = n * log(sse / n)
        aic = likelihood_term + 2 * 3  # Vmax, Km and residual variance
        bic = likelihood_term + 3 * log(n)

    warnings = [
        "No confidence intervals calculated",
        "Grid search is approximate; the optimum may lie between grid points",
        "Inspect residual structure and parameter identifiability",
        "AIC/BIC assume independent observations and constant Gaussian variance",
        "Concentration and rate units must be consistent; units are not inferred",
    ]
    if r_squared is None:
        warnings.append("R-squared is undefined because observed rates have zero variance")
    if aic is None:
        warnings.append("AIC/BIC are undefined for a perfect zero-residual fit")

    return {
        "vmax": vmax, "km": km, "sse": sse, "rmse": sqrt(sse / n), "n": n,
        "estimator": "log-grid least squares", "confidence_intervals": None,
        "residuals": residuals, "residual_mean": residual_mean,
        "residual_sample_sd": residual_sd, "r_squared": r_squared,
        "aic": aic, "bic": bic,
        "information_criteria_assumptions": [
            "independent observations", "constant Gaussian residual variance",
            "two fitted kinetic parameters plus residual variance",
        ],
        "warnings": warnings,
    }


def _validate_transform_data(
    substrates: list[float], rates: list[float],
) -> None:
    if len(substrates) != len(rates) or len(rates) < 2:
        raise ValueError("Need >=2 paired observations")
    if not all(isfinite(value) for value in [*substrates, *rates]):
        raise ValueError("Transform inputs must be finite")
    if any(value <= 0 for value in [*substrates, *rates]):
        raise ValueError("Linearized transforms require strictly positive S and v")


def lineweaver_burk(substrates: list[float], rates: list[float]) -> dict[str, object]:
    """Return reciprocal coordinates; error weighting is distorted by reciprocals."""
    _validate_transform_data(substrates, rates)
    return {
        "x": [1.0 / value for value in substrates],
        "y": [1.0 / value for value in rates],
        "axes": ["1/[S]", "1/v"],
        "warning": "Exploratory reciprocal transform; low-substrate errors are strongly amplified",
    }


def eadie_hofstee(substrates: list[float], rates: list[float]) -> dict[str, object]:
    """Return Eadie-Hofstee coordinates; both axes contain the measured rate."""
    _validate_transform_data(substrates, rates)
    return {
        "x": [rate / substrate for substrate, rate in zip(substrates, rates)],
        "y": list(rates),
        "axes": ["v/[S]", "v"],
        "warning": "Exploratory transform; x and y share measured v and therefore correlated errors",
    }


def hanes_woolf(substrates: list[float], rates: list[float]) -> dict[str, object]:
    """Return Hanes-Woolf coordinates; transformed errors remain heteroscedastic."""
    _validate_transform_data(substrates, rates)
    return {
        "x": list(substrates),
        "y": [substrate / rate for substrate, rate in zip(substrates, rates)],
        "axes": ["[S]", "[S]/v"],
        "warning": "Exploratory transform; transformed errors are not generally constant variance",
    }
