"""Inference interface for target-specific Kinetics model artifacts."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from .features import ObservationFeatureBuilder
from .uncertainty import conformal_interval


def predict_one(
    sequence: str,
    smiles: str,
    *,
    model_path: str | Path,
    target: str,
    cache_dir: str | Path = "data/cache",
    device: str | None = None,
    conformal_q: float | None = None,
) -> dict[str, Any]:
    """Predict one target and optionally attach a pre-calibrated conformal interval."""
    if target not in ("km", "kcat"):
        raise ValueError("target must be 'km' or 'kcat'")
    try:
        import joblib
    except ImportError as exc:
        raise RuntimeError("Model loading requires joblib; install the baseline extra") from exc
    path = Path(model_path)
    if not path.is_file():
        raise FileNotFoundError(path)
    bundle = joblib.load(path)
    if bundle.get("target") != target:
        raise ValueError("Requested target does not match the saved model artifact")
    builder = ObservationFeatureBuilder(
        model_name=bundle.get("feature_model", "facebook/esm2_t6_8M_UR50D"),
        cache_dir=cache_dir,
        radius=int(bundle.get("fingerprint_radius", 2)),
        n_bits=int(bundle.get("fingerprint_bits", 2048)),
        device=device,
    )
    features = builder.transform_one(sequence, smiles).reshape(1, -1)
    if features.shape[1] != int(bundle["feature_dimension"]):
        raise ValueError("Generated feature dimension does not match the model artifact")
    prediction_log10 = float(bundle["estimator"].predict(features)[0])
    unit = "M" if target == "km" else "s^-1"
    result: dict[str, Any] = {
        "target": target,
        "prediction_log10": prediction_log10,
        "prediction": float(10.0 ** prediction_log10),
        "canonical_unit": unit,
        "interpretation": "computational estimate; not an experimental measurement",
    }
    if conformal_q is not None:
        interval = conformal_interval(np.asarray([prediction_log10]), conformal_q, target=target)
        result["interval"] = {
            "method": interval["method"],
            "quantile_log10": interval["quantile"],
            "lower": float(interval["lower"][0]),
            "upper": float(interval["upper"][0]),
            "canonical_unit": unit,
        }
    return result
