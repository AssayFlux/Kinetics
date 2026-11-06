"""Conservative sequence and chemical identity normalization."""
from __future__ import annotations

import hashlib
import re
from typing import Any

import pandas as pd

_VALID_AA = set("ACDEFGHIKLMNPQRSTVWYBXZJUO")


def normalize_biomolecular_identities(
    frame: pd.DataFrame,
    *,
    sequence_column: str = "sequence",
    smiles_column: str = "smiles",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Normalize sequence/SMILES and create deterministic content IDs.

    Missing identities remain missing. Invalid supplied identities are rejected with
    row-level reasons. IDs are hashes of normalized content, not external accessions.
    RDKit is required only when a non-empty SMILES value is present.
    """
    missing = [c for c in (sequence_column, smiles_column) if c not in frame.columns]
    if missing:
        raise ValueError(f"Missing configured identity columns: {missing}")
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for index, row in frame.iterrows():
        item = row.to_dict()
        try:
            sequence = _optional_text(row[sequence_column])
            smiles = _optional_text(row[smiles_column])
            if sequence is not None:
                normalized = re.sub(r"\s+", "", sequence).upper()
                invalid = sorted(set(normalized) - _VALID_AA)
                if not normalized or invalid:
                    raise ValueError(f"invalid amino-acid sequence symbols: {''.join(invalid)}")
                item["sequence_normalized"] = normalized
                item["protein_content_id"] = hashlib.sha256(normalized.encode()).hexdigest()
            else:
                item["sequence_normalized"] = None
                item["protein_content_id"] = None
            if smiles is not None:
                try:
                    from rdkit import Chem
                except ImportError as exc:
                    raise RuntimeError("RDKit is required to normalize a supplied SMILES") from exc
                molecule = Chem.MolFromSmiles(smiles)
                if molecule is None:
                    raise ValueError("invalid substrate SMILES")
                canonical = Chem.MolToSmiles(molecule, canonical=True, isomericSmiles=True)
                item["smiles_canonical"] = canonical
                item["compound_content_id"] = hashlib.sha256(canonical.encode()).hexdigest()
            else:
                item["smiles_canonical"] = None
                item["compound_content_id"] = None
            accepted.append(item)
        except (TypeError, ValueError, RuntimeError) as exc:
            rejected.append({
                "source_row_number": int(index) if isinstance(index, int) else str(index),
                "source_record_id": str(row.get("source_record_id", "")),
                "reason": str(exc),
            })
    accepted_columns = list(frame.columns) + [
        "sequence_normalized", "protein_content_id", "smiles_canonical", "compound_content_id"
    ]
    rejected_columns = ["source_row_number", "source_record_id", "reason"]
    return (
        pd.DataFrame(accepted, columns=accepted_columns),
        pd.DataFrame(rejected, columns=rejected_columns),
    )


def _optional_text(value: Any) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    return text or None
