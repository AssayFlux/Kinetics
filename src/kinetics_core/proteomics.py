"""Provenance-preserving protein and structure contracts.

This module validates identifiers and mappings; it does not infer residue mappings,
interpret structure quality, or claim biological validity.
"""
from __future__ import annotations

import hashlib
import math
import re
from dataclasses import asdict, dataclass
from typing import Literal

PROTEIN_SCHEMA = "kinetics.protein-sequence/1.0"
STRUCTURE_SCHEMA = "kinetics.protein-structure/1.0"
MAPPING_SCHEMA = "kinetics.residue-mapping/1.0"
FEATURE_SCHEMA = "kinetics.structure-feature/1.0"
_AMINO_ACIDS = frozenset("ACDEFGHIKLMNPQRSTVWYBXZJUO")
_RESIDUE_CODES = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
    "MSE": "U", "SEC": "U", "PYL": "O", "ASX": "B", "GLX": "Z",
}


def sequence_sha256(sequence: str) -> str:
    """Hash a normalized amino-acid sequence using UTF-8 bytes."""
    normalized = normalize_sequence(sequence)
    return hashlib.sha256(normalized.encode("ascii")).hexdigest()


def normalize_sequence(sequence: str) -> str:
    if not isinstance(sequence, str):
        raise TypeError("protein sequence must be text")
    normalized = "".join(sequence.split()).upper()
    if not normalized:
        raise ValueError("protein sequence cannot be empty")
    invalid = sorted(set(normalized) - _AMINO_ACIDS)
    if invalid:
        raise ValueError(f"unsupported amino-acid symbols: {invalid}")
    return normalized


def _required(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} is required")
    return value.strip()


def _sha256(value: str, name: str) -> str:
    value = _required(value, name).lower()
    if not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError(f"{name} must be a lowercase SHA-256 digest")
    return value


@dataclass(frozen=True, slots=True)
class ProteinSequenceRecord:
    source: str
    source_record_id: str
    accession: str
    sequence: str
    source_version: str
    license_id: str
    organism: str | None = None

    def __post_init__(self) -> None:
        for name in ("source", "source_record_id", "accession", "source_version", "license_id"):
            _required(getattr(self, name), name)
        object.__setattr__(self, "sequence", normalize_sequence(self.sequence))
        if self.organism is not None:
            _required(self.organism, "organism")

    def as_dict(self) -> dict:
        return {
            "schema_version": PROTEIN_SCHEMA,
            **asdict(self),
            "sequence_length": len(self.sequence),
            "sequence_sha256": sequence_sha256(self.sequence),
        }


@dataclass(frozen=True, slots=True)
class StructureRecord:
    source: str
    source_record_id: str
    structure_id: str
    coordinate_sha256: str
    coordinate_format: Literal["pdb", "mmcif"]
    model_kind: Literal["experimental", "predicted"]
    chain_ids: tuple[str, ...]
    source_version: str
    license_id: str
    sequence_accession: str | None = None

    def __post_init__(self) -> None:
        for name in ("source", "source_record_id", "structure_id", "source_version", "license_id"):
            _required(getattr(self, name), name)
        _sha256(self.coordinate_sha256, "coordinate_sha256")
        if self.coordinate_format not in ("pdb", "mmcif"):
            raise ValueError("coordinate_format must be pdb or mmcif")
        if self.model_kind not in ("experimental", "predicted"):
            raise ValueError("model_kind must be experimental or predicted")
        chains = tuple(_required(chain, "chain_id") for chain in self.chain_ids)
        if not chains or len(set(chains)) != len(chains):
            raise ValueError("chain_ids must be non-empty and unique")
        object.__setattr__(self, "chain_ids", chains)
        if self.sequence_accession is not None:
            _required(self.sequence_accession, "sequence_accession")

    def as_dict(self) -> dict:
        return {"schema_version": STRUCTURE_SCHEMA, **asdict(self)}


@dataclass(frozen=True, slots=True)
class ResidueMapping:
    sequence_accession: str
    sequence_position: int
    structure_id: str
    chain_id: str
    residue_number: int
    residue_name: str
    mapping_method: str
    evidence_id: str
    insertion_code: str | None = None
    numbering_scheme: Literal["author", "label"] = "author"

    def __post_init__(self) -> None:
        for name in ("sequence_accession", "structure_id", "chain_id", "residue_name",
                     "mapping_method", "evidence_id"):
            _required(getattr(self, name), name)
        if isinstance(self.sequence_position, bool) or self.sequence_position < 1:
            raise ValueError("sequence_position must be a positive 1-based position")
        if isinstance(self.residue_number, bool):
            raise ValueError("residue_number must be an integer")
        if self.numbering_scheme not in ("author", "label"):
            raise ValueError("numbering_scheme must be author or label")
        if self.insertion_code is not None and len(self.insertion_code) > 1:
            raise ValueError("insertion_code must be empty, absent, or one character")

    def validate_against(
        self, sequence: ProteinSequenceRecord, structure: StructureRecord
    ) -> None:
        if self.sequence_accession != sequence.accession:
            raise ValueError("mapping sequence accession does not match sequence record")
        if self.sequence_position > len(sequence.sequence):
            raise ValueError("mapping sequence position exceeds sequence length")
        if self.structure_id != structure.structure_id:
            raise ValueError("mapping structure ID does not match structure record")
        if self.chain_id not in structure.chain_ids:
            raise ValueError("mapping chain is absent from structure record")
        residue_code = _RESIDUE_CODES.get(self.residue_name.upper())
        if residue_code and sequence.sequence[self.sequence_position - 1] not in {
            residue_code, "X"
        }:
            raise ValueError("mapped residue identity does not match the protein sequence")

    def as_dict(self) -> dict:
        return {"schema_version": MAPPING_SCHEMA, **asdict(self)}


@dataclass(frozen=True, slots=True)
class StructureFeature:
    feature_id: str
    structure_id: str
    feature_name: str
    value: float
    unit: str
    tool_name: str
    tool_version: str
    parameter_sha256: str
    coordinate_frame: str
    mapping_evidence_ids: tuple[str, ...]
    uncertainty_method: str | None = None

    def __post_init__(self) -> None:
        for name in ("feature_id", "structure_id", "feature_name", "unit", "tool_name",
                     "tool_version", "coordinate_frame"):
            _required(getattr(self, name), name)
        if (
            isinstance(self.value, bool)
            or not isinstance(self.value, (int, float))
            or not math.isfinite(self.value)
        ):
            raise ValueError("feature value must be finite")
        _sha256(self.parameter_sha256, "parameter_sha256")
        evidence = tuple(
            _required(item, "mapping_evidence_id") for item in self.mapping_evidence_ids
        )
        if not evidence:
            raise ValueError("derived structure features require mapping evidence IDs")
        object.__setattr__(self, "mapping_evidence_ids", evidence)

    def as_dict(self) -> dict:
        return {"schema_version": FEATURE_SCHEMA, **asdict(self)}
