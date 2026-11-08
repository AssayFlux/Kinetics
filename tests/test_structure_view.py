from __future__ import annotations

import json

import pytest

from kinetics.structure import Atom
from kinetics.structure_view import (
    PAYLOAD_SCHEMA,
    prepare_viewer_payload,
    serialize_viewer_payload,
)


def atom(serial: int = 1, x: float = 1.0) -> Atom:
    return Atom(serial, "CA", "ALA", "A", 1, x, 2.0, 3.0, "C")


def test_viewer_payload_is_deterministic_and_explicit_about_limits() -> None:
    payload = prepare_viewer_payload([atom()], source_format="PDB")
    assert payload["schema"] == PAYLOAD_SCHEMA
    assert payload["coordinate_unit"] == "angstrom"
    assert payload["atom_count"] == 1
    assert payload["atoms"][0]["xyz"] == [1.0, 2.0, 3.0]
    assert "No inferred bonds" in payload["limitations"][0]
    encoded = serialize_viewer_payload(payload)
    assert encoded == serialize_viewer_payload(payload)
    assert json.loads(encoded) == payload


def test_viewer_payload_rejects_empty_or_unsupported_inputs() -> None:
    with pytest.raises(ValueError, match="empty"):
        prepare_viewer_payload([], source_format="pdb")
    with pytest.raises(ValueError, match="source_format"):
        prepare_viewer_payload([atom()], source_format="xyz")


def test_viewer_payload_enforces_atom_limit_and_unique_serials() -> None:
    with pytest.raises(ValueError, match="atom limit"):
        prepare_viewer_payload([atom(1), atom(2)], source_format="pdb", max_atoms=1)
    with pytest.raises(ValueError, match="Duplicate atom serial"):
        prepare_viewer_payload([atom(1), atom(1, 2.0)], source_format="pdb")


def test_viewer_payload_rejects_nonfinite_coordinates_and_bad_annotations() -> None:
    with pytest.raises(ValueError, match="non-finite"):
        prepare_viewer_payload([atom(x=float("nan"))], source_format="pdb")
    invalid = Atom(1, "C" * 9, "ALA", "A", 1, 0.0, 0.0, 0.0, "C")
    with pytest.raises(ValueError, match="oversized"):
        prepare_viewer_payload([invalid], source_format="pdb")


def test_viewer_payload_serializer_rejects_unknown_schema() -> None:
    with pytest.raises(ValueError, match="schema"):
        serialize_viewer_payload({"schema": "future"})
