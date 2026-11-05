"""Target-independent protein/substrate feature generation for normalized observations."""
from __future__ import annotations

import hashlib
import logging
from pathlib import Path

import numpy as np
import pandas as pd

LOG = logging.getLogger("kinetics_core.features")
DEFAULT_ESM_MODEL = "facebook/esm2_t6_8M_UR50D"


class ESM2Encoder:
    """Lazy ESM-2 mean-pooling encoder with explicit sequence-length checks."""

    def __init__(self, model_name: str = DEFAULT_ESM_MODEL, device: str | None = None,
                 max_residues: int = 1022):
        self.model_name = model_name
        self.device = device
        self.max_residues = max_residues
        self._tokenizer = None
        self._model = None

    def _load(self) -> None:
        if self._model is not None:
            return
        try:
            import torch
            from transformers import AutoModel, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("Protein embeddings require the baseline extra: torch and transformers") from exc
        self.device = self.device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModel.from_pretrained(self.model_name)
        self._model.to(self.device)
        self._model.eval()

    def encode(self, sequence: str) -> np.ndarray:
        self._load()
        import torch
        sequence = sequence.strip().upper()
        standard_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")
        if not sequence or len(sequence) > self.max_residues:
            raise ValueError(f"Sequence must contain 1..{self.max_residues} residues")
        if not set(sequence) <= standard_amino_acids:
            raise ValueError("Sequence contains non-standard amino-acid symbols")
        tokens = self._tokenizer(sequence, return_tensors="pt", truncation=False)
        tokens = {name: value.to(self.device) for name, value in tokens.items()}
        with torch.inference_mode():
            hidden = self._model(**tokens).last_hidden_state
            mask = tokens["attention_mask"].bool().clone()
            # ESM-2 tokenization adds BOS and EOS; exclude both from mean pooling.
            if mask.shape[1] >= 2:
                mask[:, 0] = False
                mask[:, -1] = False
            denominator = mask.sum(dim=1, keepdim=True).clamp(min=1)
            pooled = (hidden * mask.unsqueeze(-1)).sum(dim=1) / denominator
        return pooled[0].detach().float().cpu().numpy()


def morgan_fingerprint(smiles: str, *, radius: int = 2, n_bits: int = 2048) -> np.ndarray:
    """Return a fixed-length Morgan bit vector as float32."""
    try:
        from rdkit import Chem, DataStructs
        from rdkit.Chem import rdFingerprintGenerator
    except ImportError as exc:
        raise RuntimeError("Chemical fingerprints require RDKit; install the baseline extra") from exc
    molecule = Chem.MolFromSmiles(str(smiles))
    if molecule is None:
        raise ValueError(f"Invalid or empty SMILES: {smiles!r}")
    generator = rdFingerprintGenerator.GetMorganGenerator(radius=radius, fpSize=n_bits)
    fingerprint = generator.GetFingerprint(molecule)
    result = np.zeros((n_bits,), dtype=np.float32)
    DataStructs.ConvertToNumpyArray(fingerprint, result)
    return result


class ObservationFeatureBuilder:
    """Build reusable features for one-target-per-row canonical observation tables."""

    def __init__(self, model_name: str = DEFAULT_ESM_MODEL, cache_dir: str | Path = "data/cache",
                 radius: int = 2, n_bits: int = 2048, device: str | None = None):
        self.encoder = ESM2Encoder(model_name=model_name, device=device)
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.radius, self.n_bits = radius, n_bits
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_path(self, sequence: str, smiles: str) -> Path | None:
        if self.cache_dir is None:
            return None
        key_payload = "|".join([
            self.encoder.model_name, str(self.encoder.max_residues),
            str(self.radius), str(self.n_bits), sequence, smiles,
        ])
        key = hashlib.sha256(key_payload.encode("utf-8")).hexdigest()
        return self.cache_dir / f"{key}.npz"

    def transform_one(self, sequence: str, smiles: str) -> np.ndarray:
        path = self._cache_path(sequence, smiles)
        if path and path.is_file():
            with np.load(path, allow_pickle=False) as cached:
                return cached["features"].astype(np.float32, copy=False)
        protein = self.encoder.encode(sequence)
        chemical = morgan_fingerprint(smiles, radius=self.radius, n_bits=self.n_bits)
        features = np.concatenate([protein, chemical]).astype(np.float32, copy=False)
        if path:
            temporary = path.with_suffix(".partial.npz")
            np.savez_compressed(temporary, features=features)
            temporary.replace(path)
        return features

    def transform_frame(self, frame: pd.DataFrame, *, target: str,
                        output_path: str | Path,
                        group_columns: tuple[str, ...] = ()) -> Path:
        """Write an NPZ with X, log10 y, raw y, record IDs, and feature metadata."""
        required = {"sequence", "smiles", "canonical_value", "target", "source_record_id"}
        missing = required - set(frame.columns)
        if missing:
            raise ValueError(f"Canonical observation table is missing columns: {sorted(missing)}")
        if target not in ("km", "kcat"):
            raise ValueError("target must be 'km' or 'kcat'")
        selected = frame.loc[frame["target"] == target].copy()
        if selected.empty:
            raise ValueError(f"No observations found for target {target}")
        values = pd.to_numeric(selected["canonical_value"], errors="coerce").to_numpy(dtype=float)
        if not np.isfinite(values).all() or np.any(values <= 0):
            raise ValueError("canonical_value must contain finite positive values")
        if selected["sequence"].isna().any() or selected["smiles"].isna().any():
            raise ValueError("Feature generation requires sequence and SMILES for every selected row")
        rows = [
            self.transform_one(str(row.sequence), str(row.smiles))
            for row in selected.itertuples(index=False)
        ]
        X = np.stack(rows).astype(np.float32, copy=False)
        y = np.log10(values).astype(np.float32)
        reserved_names = {"X", "y_log10", "y_raw", "source_record_ids", "sequences",
                          "smiles", "target", "feature_model", "fingerprint_radius",
                          "fingerprint_bits"}
        collisions = reserved_names.intersection(group_columns)
        if collisions:
            raise ValueError(f"Grouping column names collide with reserved archive keys: {sorted(collisions)}")
        group_arrays = {}
        for column in group_columns:
            if column not in selected.columns:
                raise ValueError(f"Requested grouping column is missing: {column}")
            if selected[column].isna().any():
                raise ValueError(f"Grouping column {column} contains missing values")
            group_arrays[column] = selected[column].astype(str).to_numpy()

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            output, X=X, y_log10=y, y_raw=values.astype(np.float64),
            source_record_ids=selected["source_record_id"].astype(str).to_numpy(),
            sequences=selected["sequence"].astype(str).to_numpy(),
            smiles=selected["smiles"].astype(str).to_numpy(),
            target=np.asarray([target]),
            feature_model=np.asarray([self.encoder.model_name]),
            fingerprint_radius=np.asarray([self.radius]),
            fingerprint_bits=np.asarray([self.n_bits]),
            **group_arrays,
        )
        LOG.info("Saved %d %s feature rows to %s", len(selected), target, output)
        return output
