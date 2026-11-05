"""ESM-2 mean embeddings and RDKit Morgan fingerprints with per-record disk cache."""
from __future__ import annotations

import argparse
import hashlib
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator

LOG = logging.getLogger("kinetics.features")
DEFAULT_ESM = "facebook/esm2_t6_8M_UR50D"
TARGETS = ["log10_km", "log10_kcat"]


def smiles_fingerprint(smiles: str, n_bits: int = 2048, radius: int = 2) -> np.ndarray:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles!r}")
    generator = rdFingerprintGenerator.GetMorganGenerator(radius=radius, fpSize=n_bits)
    fp = generator.GetFingerprint(mol)
    arr = np.zeros((n_bits,), dtype=np.float32)
    DataStructs.ConvertToNumpyArray(fp, arr)
    return arr


class ESMEmbedder:
    """Lazy-loaded, mean-pooled ESM-2 encoder; uses CPU by default for portability."""

    def __init__(self, model_name: str = DEFAULT_ESM, device: str | None = None, max_length: int = 1022):
        self.model_name, self.device, self.max_length = model_name, device, max_length
        self._tokenizer = self._model = None

    def _load(self) -> None:
        if self._model is not None:
            return
        try:
            import torch
            from transformers import AutoModel, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("ESM embeddings require torch and transformers. Install requirements.txt.") from exc
        self.device = self.device or ("cuda" if torch.cuda.is_available() else "cpu")
        LOG.info("Loading %s on %s", self.model_name, self.device)
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModel.from_pretrained(self.model_name)
        self._model.to(self.device)
        self._model.eval()

    def encode(self, sequence: str) -> np.ndarray:
        self._load()
        import torch
        seq = sequence.strip().upper()
        if not seq or len(seq) > self.max_length:
            raise ValueError(f"Sequence length must be 1..{self.max_length}; got {len(seq)}")
        tokens = self._tokenizer(seq, return_tensors="pt", truncation=False)
        tokens = {key: value.to(self.device) for key, value in tokens.items()}
        with torch.inference_mode():
            hidden = self._model(**tokens).last_hidden_state
            mask = tokens["attention_mask"].bool()
            # Exclude special tokens (BOS/EOS); tokenizers mark both as attended.
            if mask.shape[1] > 2:
                mask[:, 0] = False
                mask[:, -1] = False
            pooled = (hidden * mask.unsqueeze(-1)).sum(dim=1) / mask.sum(dim=1, keepdim=True).clamp(min=1)
        return pooled[0].detach().float().cpu().numpy()


class FeatureExtractor:
    def __init__(
        self, model_name: str = DEFAULT_ESM, cache_dir: str | Path | None = "data/cache",
        n_bits: int = 2048, radius: int = 2, device: str | None = None,
    ):
        self.embedder = ESMEmbedder(model_name, device)
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.n_bits, self.radius = n_bits, radius
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_path(self, sequence: str, smiles: str) -> Path | None:
        if self.cache_dir is None:
            return None
        key = hashlib.sha256(
            f"{self.embedder.model_name}|{self.n_bits}|{self.radius}|{sequence}|{smiles}".encode()
        ).hexdigest()
        return self.cache_dir / f"{key}.npz"

    def transform_one(self, sequence: str, smiles: str) -> np.ndarray:
        path = self._cache_path(sequence, smiles)
        if path and path.exists():
            with np.load(path, allow_pickle=False) as cached:
                return cached["features"].astype(np.float32, copy=False)
        protein = self.embedder.encode(sequence)
        chemical = smiles_fingerprint(smiles, self.n_bits, self.radius)
        combined = np.concatenate((protein, chemical)).astype(np.float32, copy=False)
        if path:
            tmp = path.with_suffix(".tmp.npz")
            np.savez_compressed(tmp, features=combined)
            tmp.replace(path)
        return combined

    def transform_frame(self, frame: pd.DataFrame) -> np.ndarray:
        required = {"sequence", "smiles"}
        if not required.issubset(frame.columns):
            raise ValueError(f"Feature input must contain {sorted(required)}")
        rows = []
        for idx, row in enumerate(frame.itertuples(index=False)):
            try:
                rows.append(self.transform_one(row.sequence, row.smiles))
            except Exception as exc:
                raise RuntimeError(f"Feature extraction failed at row {idx}: {exc}") from exc
            if (idx + 1) % 25 == 0:
                LOG.info("Extracted %d/%d records", idx + 1, len(frame))
        if not rows:
            raise ValueError("No records supplied for feature extraction.")
        return np.stack(rows)

    def transform_csv(self, input_csv: str | Path, output_npz: str | Path) -> Path:
        frame = pd.read_csv(input_csv)
        features = self.transform_frame(frame)
        missing = set(TARGETS) - set(frame.columns)
        if missing:
            raise ValueError(f"Feature CSV is missing target columns: {sorted(missing)}")
        out = Path(output_npz)
        out.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            out, X=features, y=frame[TARGETS].to_numpy(dtype=np.float32),
            sequences=frame["sequence"].astype(str).to_numpy(),
            smiles=frame["smiles"].astype(str).to_numpy(),
        )
        LOG.info("Saved features %s with shape %s", out, features.shape)
        return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Cleaned train.csv or test.csv")
    parser.add_argument("--output", required=True, help="Output .npz path")
    parser.add_argument("--model", default=DEFAULT_ESM)
    parser.add_argument("--cache-dir", default="data/cache")
    parser.add_argument("--device", default=None, help="cpu, cuda, or mps (auto if omitted)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    FeatureExtractor(args.model, args.cache_dir, device=args.device).transform_csv(args.input, args.output)


if __name__ == "__main__":
    main()
