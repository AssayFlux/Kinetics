"""CLI and lightweight inference for Kinetics."""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import numpy as np

from .feature_extraction import DEFAULT_ESM, FeatureExtractor

LOG = logging.getLogger("kinetics.predict")


def _onnx_session(path: Path):
    import onnxruntime as ort
    options = ort.SessionOptions()
    options.intra_op_num_threads = 1
    options.inter_op_num_threads = 1
    options.enable_mem_pattern = False
    return ort.InferenceSession(str(path), sess_options=options, providers=["CPUExecutionProvider"])


def predict(sequence: str, smiles: str, model_dir: str | Path = "models",
            cache_dir: str | Path = "data/cache", prefer_onnx: bool = True) -> dict:
    import joblib
    model_dir = Path(model_dir)
    bundle_path = model_dir / "kinetics_model.joblib"
    if not bundle_path.is_file():
        raise FileNotFoundError(f"Model bundle not found: {bundle_path}. Train the model first.")
    bundle = joblib.load(bundle_path)
    if not sequence or not smiles:
        raise ValueError("Both sequence and SMILES must be non-empty.")
    extractor = FeatureExtractor(
        model_name=bundle.get("esm_model", DEFAULT_ESM), cache_dir=cache_dir,
        n_bits=int(bundle.get("fingerprint_bits", 2048)),
        radius=int(bundle.get("radius", 2)),
    )
    features = extractor.transform_one(sequence, smiles).reshape(1, -1)
    if features.shape[1] != int(bundle["feature_dim"]):
        raise ValueError(f"Feature dimension mismatch: {features.shape[1]} != {bundle['feature_dim']}")

    logs = {}
    for target in ("log10_km", "log10_kcat"):
        candidates = ([model_dir / "onnx" / f"{target}.int8.onnx",
                       model_dir / "onnx" / f"{target}.fp16.onnx",
                       model_dir / "onnx" / f"{target}.onnx"] if prefer_onnx else [])
        model_path = next((p for p in candidates if p.is_file()), None)
        if model_path is not None:
            try:
                session = _onnx_session(model_path)
                input_name = session.get_inputs()[0].name
                output = session.run(None, {input_name: features.astype(np.float32)})[0]
                logs[target] = float(np.asarray(output).reshape(-1)[0])
                LOG.info("Used ONNX runtime: %s", model_path.name)
                continue
            except Exception as exc:
                LOG.warning("ONNX inference failed (%s); falling back to joblib.", exc)
        logs[target] = float(bundle["models"][target].predict(features)[0])

    # Targets are defined in mM and s^-1 at preprocessing time.
    km_log, kcat_log = logs["log10_km"], logs["log10_kcat"]
    return {
        "log10_km": km_log, "km_mM": float(10.0 ** km_log),
        "log10_kcat": kcat_log, "kcat_s-1": float(10.0 ** kcat_log),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sequence", required=True, help="Standard 20-amino-acid protein sequence")
    parser.add_argument("--smiles", required=True, help="Substrate SMILES")
    parser.add_argument("--model-dir", default="models")
    parser.add_argument("--cache-dir", default="data/cache")
    parser.add_argument("--no-onnx", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        result = predict(args.sequence, args.smiles, args.model_dir, args.cache_dir, not args.no_onnx)
        print(json.dumps(result, indent=2))
    except Exception as exc:
        LOG.error("%s", exc)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
