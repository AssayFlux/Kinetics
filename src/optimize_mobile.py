"""Export trained XGBoost estimators to ONNX and optionally quantize/convert to FP16.

XGBoost-to-ONNX requires onnxmltools and skl2onnx. ONNX Runtime's dynamic
quantizer only quantizes supported operators; tree ensembles may remain unchanged.
Always retain the original model as the compatibility fallback.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import joblib

LOG = logging.getLogger("kinetics.mobile")


def export_models(model_path: str | Path = "models/kinetics_model.joblib",
                  output_dir: str | Path = "models/onnx", quantize: bool = True,
                  fp16: bool = False) -> list[Path]:
    try:
        import onnxmltools
        from onnxmltools.convert.common.data_types import FloatTensorType
    except ImportError as exc:
        raise RuntimeError("ONNX export requires onnxmltools and skl2onnx.") from exc
    bundle = joblib.load(model_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    exported = []
    feature_dim = int(bundle["feature_dim"])
    for target, estimator in bundle["models"].items():
        onx = onnxmltools.convert_xgboost(
            estimator, initial_types=[("features", FloatTensorType([None, feature_dim]))],
            target_opset=15,
        )
        raw_path = out / f"{target}.onnx"
        raw_path.write_bytes(onx.SerializeToString())
        final_path = raw_path
        if quantize:
            try:
                from onnxruntime.quantization import QuantType, quantize_dynamic
                quant_path = out / f"{target}.int8.onnx"
                quantize_dynamic(str(raw_path), str(quant_path), weight_type=QuantType.QInt8)
                if quant_path.exists() and quant_path.stat().st_size < raw_path.stat().st_size:
                    final_path = quant_path
                else:
                    quant_path.unlink(missing_ok=True)
                    LOG.info("Quantization did not reduce %s; retaining FP32 graph", target)
            except Exception as exc:
                LOG.warning("INT8 quantization unavailable for %s: %s", target, exc)
        if fp16:
            try:
                import onnx
                from onnxconverter_common import float16
                graph = onnx.load(str(final_path))
                converted = float16.convert_float_to_float16(graph, keep_io_types=True)
                fp16_path = out / f"{target}.fp16.onnx"
                onnx.save(converted, str(fp16_path))
                final_path = fp16_path
            except Exception as exc:
                LOG.warning("FP16 conversion unavailable for %s: %s", target, exc)
        exported.append(final_path)
        LOG.info("Exported %s (%d bytes)", final_path, final_path.stat().st_size)
    return exported


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="models/kinetics_model.joblib")
    parser.add_argument("--output-dir", default="models/onnx")
    parser.add_argument("--no-quantize", action="store_true")
    parser.add_argument("--fp16", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    export_models(args.model, args.output_dir, not args.no_quantize, args.fp16)


if __name__ == "__main__":
    main()
