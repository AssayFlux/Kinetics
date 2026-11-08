"""Deterministic, bounded structure payload preparation for offline viewers.

This module is a data boundary only. It does not render structures, infer chemistry,
or assign quality/confidence labels.
"""
from __future__ import annotations

import json
from math import isfinite
from typing import Any, Iterable

from .structure import Atom

PAYLOAD_SCHEMA = "kinetics.structure-view.v1"
SUPPORTED_SOURCE_FORMATS = frozenset({"pdb", "mmcif"})


def prepare_viewer_payload(
    atoms: Iterable[Atom],
    *,
    source_format: str,
    max_atoms: int = 200_000,
) -> dict[str, Any]:
    """Build a deterministic, size-bounded atom payload in Angstrom coordinates."""
    normalized_format = source_format.lower().strip()
    if normalized_format not in SUPPORTED_SOURCE_FORMATS:
        raise ValueError("source_format must be 'pdb' or 'mmcif'")
    if isinstance(max_atoms, bool) or max_atoms < 1:
        raise ValueError("max_atoms must be a positive integer")

    records: list[dict[str, Any]] = []
    seen_serials: set[int] = set()
    for atom in atoms:
        if len(records) >= max_atoms:
            raise ValueError(f"Structure exceeds configured atom limit ({max_atoms})")
        if atom.serial in seen_serials:
            raise ValueError(f"Duplicate atom serial: {atom.serial}")
        seen_serials.add(atom.serial)
        if not all(isfinite(value) for value in (atom.x, atom.y, atom.z)):
            raise ValueError(f"Atom {atom.serial} has non-finite coordinates")
        if atom.serial < 0 or atom.residue_number < 0:
            raise ValueError(f"Atom {atom.serial} has a negative identifier")
        fields = (atom.name, atom.residue, atom.chain, atom.element)
        if any(not isinstance(value, str) for value in fields):
            raise ValueError(f"Atom {atom.serial} contains a non-text annotation")
        if len(atom.name) > 8 or len(atom.residue) > 8 or len(atom.chain) > 8:
            raise ValueError(f"Atom {atom.serial} contains an oversized annotation")
        element = atom.element.strip().upper()
        if len(element) > 3:
            raise ValueError(f"Atom {atom.serial} has an invalid element label")
        records.append({
            "serial": atom.serial,
            "name": atom.name.strip(),
            "residue": atom.residue.strip(),
            "chain": atom.chain.strip(),
            "residue_number": atom.residue_number,
            "element": element,
            "xyz": [atom.x, atom.y, atom.z],
        })

    if not records:
        raise ValueError("Cannot prepare an empty structure")
    return {
        "schema": PAYLOAD_SCHEMA,
        "source_format": normalized_format,
        "coordinate_unit": "angstrom",
        "atom_count": len(records),
        "atoms": records,
        "limitations": [
            "Coordinates and annotations only; no inferred bonds or protonation.",
            "No secondary-structure, quality, confidence, or biological interpretation.",
            "Viewer rendering and WebView security are separate validated components.",
        ],
    }


def serialize_viewer_payload(payload: dict[str, Any]) -> str:
    """Serialize a prepared payload deterministically without NaN/Infinity extensions."""
    if payload.get("schema") != PAYLOAD_SCHEMA:
        raise ValueError("Unsupported structure viewer payload schema")
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
