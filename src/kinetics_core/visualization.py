"""Publication-oriented diagnostic figures for target-specific model evaluation."""
from __future__ import annotations

from pathlib import Path

import numpy as np


def _pyplot():
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Scientific plotting requires matplotlib; install the plots extra") from exc
    return plt


def parity_plot(y_true_log10, y_pred_log10, *, target: str, output_path: str | Path,
                title: str | None = None) -> Path:
    """Create a parity plot with identity reference and equal axis limits."""
    if target not in ("km", "kcat"):
        raise ValueError("target must be 'km' or 'kcat'")
    truth = np.asarray(y_true_log10, dtype=float).reshape(-1)
    prediction = np.asarray(y_pred_log10, dtype=float).reshape(-1)
    if truth.shape != prediction.shape or truth.size == 0:
        raise ValueError("truth and prediction must be non-empty arrays with equal shape")
    if not np.isfinite(truth).all() or not np.isfinite(prediction).all():
        raise ValueError("truth and prediction must be finite")
    plt = _pyplot()
    low = float(min(truth.min(), prediction.min()))
    high = float(max(truth.max(), prediction.max()))
    padding = max((high - low) * 0.05, 0.05)
    low, high = low - padding, high + padding
    figure, axis = plt.subplots(figsize=(6.2, 6.0), constrained_layout=True)
    axis.scatter(truth, prediction, alpha=0.65, s=22, edgecolors="none")
    axis.plot([low, high], [low, high], linestyle="--", linewidth=1.2)
    axis.set_xlim(low, high)
    axis.set_ylim(low, high)
    axis.set_xlabel(f"Observed log10({target})")
    axis.set_ylabel(f"Predicted log10({target})")
    axis.set_title(title or f"Kinetics {target} parity")
    axis.grid(True, alpha=0.2)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(figure)
    return output


def residual_plot(y_true_log10, y_pred_log10, *, target: str,
                  output_path: str | Path) -> Path:
    """Plot log-scale residuals against fitted values."""
    if target not in ("km", "kcat"):
        raise ValueError("target must be 'km' or 'kcat'")
    truth = np.asarray(y_true_log10, dtype=float).reshape(-1)
    prediction = np.asarray(y_pred_log10, dtype=float).reshape(-1)
    if truth.shape != prediction.shape or truth.size == 0:
        raise ValueError("truth and prediction must be non-empty arrays with equal shape")
    if not np.isfinite(truth).all() or not np.isfinite(prediction).all():
        raise ValueError("truth and prediction must be finite")
    residuals = truth - prediction
    plt = _pyplot()
    figure, axis = plt.subplots(figsize=(7.0, 4.8), constrained_layout=True)
    axis.scatter(prediction, residuals, alpha=0.65, s=22, edgecolors="none")
    axis.axhline(0.0, linestyle="--", linewidth=1.2)
    axis.set_xlabel(f"Predicted log10({target})")
    axis.set_ylabel("Residual (observed - predicted)")
    axis.set_title(f"Kinetics {target} residual diagnostics")
    axis.grid(True, alpha=0.2)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(figure)
    return output
