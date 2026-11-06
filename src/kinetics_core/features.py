"""Reproducible protein and chemical representations for canonical observations."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import logging
import os
from pathlib import Path
import platform
import tempfile
from typing import Any

import numpy as np
import pandas as pd

from .chemistry import canonicalize_smiles
from .provenance import file_record, write_json_atomic

LOG = logging.getLogger("kinetics_core.features")
DEFAULT_ESM_MODEL = "facebook/esm2_t6_8M_UR50D"
DEFAULT_ESM_REVISION = "8c576d2aba1b27317e9321c8491d72f00d1b110a"
FEATURE_SCHEMA_VERSION = "2.0"
CACHE_SCHEMA_VERSION = "2"
_VALID_AA = set("ACDEFGHIKLMNPQRSTVWYXBZUO")


def _version(distribution: str) -> str | None:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return None


def _normalize_sequence(sequence: str, max_residues: int) -> str:
    normalized = "".join(str(sequence).split()).upper()
    if not normalized or len(normalized) > max_residues:
        raise ValueError(f"Sequence must contain 1..{max_residues} residues")
    invalid = sorted(set(normalized) - _VALID_AA)
    if invalid:
        raise ValueError(f"Sequence contains unsupported amino-acid symbols: {''.join(invalid)}")
    return normalized


class ESM2Encoder:
    """Lazy ESM-2 mean-pooling encoder with immutable model/tokenizer revisions."""

    def __init__(
        self,
        model_name: str = DEFAULT_ESM_MODEL,
        device: str | None = None,
        max_residues: int = 1022,
        model_revision: str = DEFAULT_ESM_REVISION,
        tokenizer_revision: str | None = None,
    ):
        if not model_revision or model_revision in {"main", "master"}:
            raise ValueError("model_revision must be an immutable model commit")
        self.model_name = model_name
        self.model_revision = model_revision
        self.tokenizer_revision = tokenizer_revision or model_revision
        if self.tokenizer_revision in {"main", "master"}:
            raise ValueError("tokenizer_revision must be an immutable tokenizer commit")
        if not 1 <= max_residues <= 1022:
            raise ValueError("max_residues must be between 1 and 1022 for this ESM-2 model")
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
            raise RuntimeError(
                "Protein embeddings require the baseline extra: torch and transformers"
            ) from exc
        self.device = self.device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            revision=self.tokenizer_revision,
            trust_remote_code=False,
        )
        self._model = AutoModel.from_pretrained(
            self.model_name,
            revision=self.model_revision,
            trust_remote_code=False,
        )
        self._model.to(self.device)
        self._model.eval()

    def encode_many(self, sequences: list[str] | tuple[str, ...]) -> list[np.ndarray]:
        """Encode a bounded batch; padding and BOS/EOS tokens are excluded from pooling."""
        if not sequences:
            return []
        normalized = [_normalize_sequence(value, self.max_residues) for value in sequences]
        self._load()
        import torch

        tokens = self._tokenizer(
            normalized, return_tensors="pt", padding=True, truncation=False
        )
        if int(tokens["input_ids"].shape[1]) > int(
            getattr(self._model.config, "max_position_embeddings", 1026)
        ):
            raise ValueError("Tokenized sequence exceeds the model positional embedding limit")
        tokens = {name: value.to(self.device) for name, value in tokens.items()}
        with torch.inference_mode():
            hidden = self._model(**tokens).last_hidden_state
            attention = tokens["attention_mask"].bool()
            positions = torch.arange(
                attention.shape[1], device=attention.device
            ).unsqueeze(0)
            # Keep residues only: position zero is BOS and the last attended token is EOS.
            residue_mask = attention & (positions > 0) & (
                positions < (attention.sum(dim=1, keepdim=True) - 1)
            )
            denominator = residue_mask.sum(dim=1, keepdim=True).clamp(min=1)
            pooled = (hidden * residue_mask.unsqueeze(-1)).sum(dim=1) / denominator
        return [
            vector.detach().float().cpu().numpy().astype(np.float32, copy=False)
            for vector in pooled
        ]

    def encode(self, sequence: str) -> np.ndarray:
        return self.encode_many([sequence])[0]

    def metadata(self) -> dict[str, Any]:
        return {
            "encoder": "ESM-2",
            "model_name": self.model_name,
            "model_revision": self.model_revision,
            "tokenizer_revision": self.tokenizer_revision,
            "pooling": "mean over residue tokens; BOS/EOS/padding excluded",
            "max_residues": self.max_residues,
            "accepted_amino_acids": "".join(sorted(_VALID_AA)),
            "device_policy": self.device or "auto",
            "resolved_device": self.device,
            "output_dtype": "float32",
        }


def morgan_fingerprint(
    smiles: str,
    *,
    radius: int = 2,
    n_bits: int = 2048,
    include_chirality: bool = True,
) -> np.ndarray:
    """Return a Morgan bit vector; chirality is retained by default."""
    if radius < 0 or n_bits < 1:
        raise ValueError("Morgan radius must be >= 0 and n_bits must be >= 1")
    try:
        from rdkit import Chem, DataStructs
        from rdkit.Chem import rdFingerprintGenerator
    except ImportError as exc:
        raise RuntimeError("Chemical fingerprints require RDKit; install the baseline extra") from exc
    molecule = Chem.MolFromSmiles(str(smiles))
    if molecule is None:
        raise ValueError(f"Invalid or empty SMILES: {smiles!r}")
    generator = rdFingerprintGenerator.GetMorganGenerator(
        radius=radius, fpSize=n_bits, includeChirality=include_chirality
    )
    fingerprint = generator.GetFingerprint(molecule)
    result = np.zeros((n_bits,), dtype=np.float32)
    DataStructs.ConvertToNumpyArray(fingerprint, result)
    return result


class ObservationFeatureBuilder:
    """Build versioned, provenance-carrying ESM-2 + Morgan feature archives."""

    def __init__(
        self,
        model_name: str = DEFAULT_ESM_MODEL,
        cache_dir: str | Path | None = "data/cache",
        radius: int = 2,
        n_bits: int = 2048,
        device: str | None = None,
        model_revision: str = DEFAULT_ESM_REVISION,
        tokenizer_revision: str | None = None,
        include_chirality: bool = True,
        encoder: ESM2Encoder | None = None,
    ):
        if radius < 0 or n_bits < 1:
            raise ValueError("Morgan radius must be >= 0 and n_bits must be >= 1")
        self.encoder = encoder or ESM2Encoder(
            model_name=model_name,
            device=device,
            model_revision=model_revision,
            tokenizer_revision=tokenizer_revision,
        )
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.radius, self.n_bits = radius, n_bits
        self.include_chirality = include_chirality
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _representation_metadata(self) -> dict[str, Any]:
        try:
            from rdkit import rdBase
            rdkit_version = rdBase.rdkitVersion
        except ImportError:
            rdkit_version = None
        encoder_metadata = (
            self.encoder.metadata()
            if hasattr(self.encoder, "metadata")
            else {"encoder": type(self.encoder).__name__}
        )
        return {
            "feature_schema_version": FEATURE_SCHEMA_VERSION,
            "protein": encoder_metadata,
            "chemical": {
                "fingerprint": "Morgan",
                "radius": self.radius,
                "bits": self.n_bits,
                "include_chirality": self.include_chirality,
                "smiles_policy": "RDKit canonical isomeric SMILES; no salt/tautomer stripping",
            },
            "software": {
                "python": platform.python_version(),
                "numpy": np.__version__,
                "pandas": pd.__version__,
                "rdkit": rdkit_version,
                "torch": _version("torch"),
                "transformers": _version("transformers"),
            },
        }

    def _cache_path(self, sequence: str, smiles: str) -> tuple[Path | None, str]:
        metadata = self._representation_metadata()
        payload = {
            "cache_schema_version": CACHE_SCHEMA_VERSION,
            "representation": metadata,
            "sequence": sequence,
            "canonical_smiles": smiles,
        }
        key = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return (
            self.cache_dir / f"{key}.npz" if self.cache_dir else None,
            key,
        )

    def _read_cache(self, path: Path, key: str) -> np.ndarray | None:
        try:
            with np.load(path, allow_pickle=False) as cached:
                if str(cached["cache_key"][0]) != key:
                    return None
                features = cached["features"].astype(np.float32, copy=False)
            if features.ndim != 1 or not np.isfinite(features).all():
                return None
            return features
        except (OSError, KeyError, ValueError, IndexError):
            return None

    @staticmethod
    def _write_cache(path: Path, key: str, features: np.ndarray) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.stem}.", suffix=".npz", dir=path.parent
        )
        try:
            with os.fdopen(descriptor, "wb") as handle:
                np.savez_compressed(
                    handle,
                    cache_key=np.asarray([key]),
                    features=np.asarray(features, dtype=np.float32),
                )
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, path)
        except Exception:
            Path(temporary_name).unlink(missing_ok=True)
            raise

    def transform_many(
        self,
        sequences: list[str] | tuple[str, ...],
        smiles_values: list[str] | tuple[str, ...],
        *,
        batch_size: int = 16,
    ) -> np.ndarray:
        """Transform a bounded batch of protein/compound pairs with deterministic cache keys."""
        if len(sequences) != len(smiles_values):
            raise ValueError("sequences and smiles_values must have the same length")
        if batch_size < 1:
            raise ValueError("batch_size must be >= 1")
        if not sequences:
            return np.empty((0, 0), dtype=np.float32)

        normalized_sequences = [
            _normalize_sequence(value, self.encoder.max_residues)
            for value in sequences
        ]
        canonical_smiles = [canonicalize_smiles(value) for value in smiles_values]
        rows: list[np.ndarray | None] = [None] * len(sequences)
        pending: list[tuple[int, str, str, Path | None, str]] = []
        sequence_embeddings: dict[str, np.ndarray] = {}

        for index, (sequence, smiles) in enumerate(
            zip(normalized_sequences, canonical_smiles)
        ):
            cache_path, key = self._cache_path(sequence, smiles)
            cached = self._read_cache(cache_path, key) if cache_path and cache_path.is_file() else None
            if cached is not None:
                rows[index] = cached
            else:
                pending.append((index, sequence, smiles, cache_path, key))

        if pending:
            unique_sequences = list(dict.fromkeys(item[1] for item in pending))
            for start in range(0, len(unique_sequences), batch_size):
                chunk = unique_sequences[start : start + batch_size]
                if hasattr(self.encoder, "encode_many"):
                    embeddings = self.encoder.encode_many(chunk)
                else:
                    embeddings = [self.encoder.encode(value) for value in chunk]
                if len(embeddings) != len(chunk):
                    raise RuntimeError("Protein encoder returned an unexpected batch size")
                for sequence, embedding in zip(chunk, embeddings):
                    vector = np.asarray(embedding, dtype=np.float32)
                    if vector.ndim != 1 or not np.isfinite(vector).all():
                        raise ValueError("Protein encoder returned a non-finite or non-vector embedding")
                    sequence_embeddings[sequence] = vector

            for index, sequence, smiles, cache_path, key in pending:
                chemical = morgan_fingerprint(
                    smiles,
                    radius=self.radius,
                    n_bits=self.n_bits,
                    include_chirality=self.include_chirality,
                )
                combined = np.concatenate(
                    [sequence_embeddings[sequence], chemical]
                ).astype(np.float32, copy=False)
                rows[index] = combined
                if cache_path:
                    self._write_cache(cache_path, key, combined)

        result = np.stack([row for row in rows if row is not None]).astype(
            np.float32, copy=False
        )
        if result.shape[0] != len(sequences):
            raise RuntimeError("Feature generation lost row alignment")
        return result

    def transform_one(self, sequence: str, smiles: str) -> np.ndarray:
        return self.transform_many([sequence], [smiles])[0]

    def transform_frame(
        self,
        frame: pd.DataFrame,
        *,
        target: str,
        output_path: str | Path,
        group_columns: tuple[str, ...] = (),
        batch_size: int = 16,
    ) -> Path:
        """Write an NPZ archive and adjacent JSON manifest with source and feature provenance."""
        required = {
            "sequence", "smiles", "canonical_value", "target", "source_record_id"
        }
        missing = required - set(frame.columns)
        if missing:
            raise ValueError(
                f"Canonical observation table is missing columns: {sorted(missing)}"
            )
        if target not in ("km", "kcat"):
            raise ValueError("target must be 'km' or 'kcat'")
        if batch_size < 1:
            raise ValueError("batch_size must be >= 1")
        selected = frame.loc[frame["target"] == target].copy().reset_index(drop=True)
        if selected.empty:
            raise ValueError(f"No observations found for target {target}")
        values = pd.to_numeric(
            selected["canonical_value"], errors="coerce"
        ).to_numpy(dtype=float)
        if not np.isfinite(values).all() or np.any(values <= 0):
            raise ValueError("canonical_value must contain finite positive values")
        if selected["sequence"].isna().any() or selected["smiles"].isna().any():
            raise ValueError("Feature generation requires sequence and SMILES for every selected row")
        if selected["source_record_id"].astype(str).str.strip().eq("").any():
            raise ValueError("source_record_id must be non-empty for every feature row")

        reserved_names = {
            "X", "y_log10", "y_raw", "source_record_ids", "sequences",
            "smiles", "target", "feature_metadata_json", "feature_schema_version",
            "fingerprint_radius", "fingerprint_bits", "fingerprint_include_chirality",
        }
        collisions = reserved_names.intersection(group_columns)
        if collisions:
            raise ValueError(
                f"Grouping column names collide with reserved archive keys: {sorted(collisions)}"
            )
        group_arrays = {}
        for column in group_columns:
            if column not in selected.columns:
                raise ValueError(f"Requested grouping column is missing: {column}")
            if selected[column].isna().any():
                raise ValueError(f"Grouping column {column} contains missing values")
            group_arrays[column] = selected[column].astype(str).to_numpy()

        feature_batches = []
        for start in range(0, len(selected), batch_size):
            batch = selected.iloc[start : start + batch_size]
            feature_batches.append(
                self.transform_many(
                    batch["sequence"].astype(str).tolist(),
                    batch["smiles"].astype(str).tolist(),
                    batch_size=batch_size,
                )
            )
        X = np.concatenate(feature_batches, axis=0).astype(np.float32, copy=False)
        metadata = self._representation_metadata()
        metadata["batch_size"] = batch_size
        metadata["row_alignment"] = "source_record_ids, sequences, smiles, y_raw, y_log10 align by row"
        metadata["determinism"] = (
            "Inference mode and explicit model/tokenizer revisions are used. "
            "Bitwise equality across different hardware or library builds is not guaranteed."
        )

        output = Path(output_path)
        manifest_path = output.with_suffix(output.suffix + ".manifest.json")
        if output.resolve() == manifest_path.resolve():
            raise ValueError("Feature archive and manifest paths must differ")
        output.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{output.name}.", suffix=".npz", dir=output.parent
        )
        try:
            with os.fdopen(descriptor, "wb") as handle:
                np.savez_compressed(
                    handle,
                    X=X,
                    y_log10=np.log10(values).astype(np.float32),
                    y_raw=values.astype(np.float64),
                    source_record_ids=selected["source_record_id"].astype(str).to_numpy(),
                    sequences=selected["sequence"].astype(str).to_numpy(),
                    smiles=selected["smiles"].astype(str).to_numpy(),
                    target=np.asarray([target]),
                    feature_schema_version=np.asarray([FEATURE_SCHEMA_VERSION]),
                    feature_metadata_json=np.asarray([
                        json.dumps(metadata, sort_keys=True)
                    ]),
                    fingerprint_radius=np.asarray([self.radius]),
                    fingerprint_bits=np.asarray([self.n_bits]),
                    fingerprint_include_chirality=np.asarray([self.include_chirality]),
                    **group_arrays,
                )
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, output)
        except Exception:
            Path(temporary_name).unlink(missing_ok=True)
            raise

        row_identity = [
            {
                "source": str(row.get("source", "")),
                "source_record_id": str(row["source_record_id"]),
                "sequence": _normalize_sequence(row["sequence"], self.encoder.max_residues),
                "smiles": canonicalize_smiles(row["smiles"]),
                "canonical_value": float(value),
            }
            for (_, row), value in zip(selected.iterrows(), values)
        ]
        row_identity_sha256 = hashlib.sha256(
            json.dumps(row_identity, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        manifest = {
            "schema_version": "1.0",
            "target": target,
            "rows": len(selected),
            "feature_shape": list(X.shape),
            "feature_dtype": str(X.dtype),
            "row_identity_sha256": row_identity_sha256,
            "source_record_ids_sha256": hashlib.sha256(
                "\n".join(selected["source_record_id"].astype(str)).encode()
            ).hexdigest(),
            "feature_metadata": metadata,
            "archive": file_record(output),
        }
        write_json_atomic(manifest, manifest_path)
        LOG.info("Saved %d %s feature rows to %s", len(selected), target, output)
        return output
