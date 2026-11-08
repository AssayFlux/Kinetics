from __future__ import annotations

import json

import pytest

from kinetics.structure import Atom
from kinetics.structure_view import (
    PAYLOAD_SCHEMA,
    build_preparation_record,
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
    assert "no inferred bonds" in payload["limitations"][0]
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


def test_preparation_record_is_reproducible_and_content_addressed() -> None:
    source = b"PDB fixture bytes"
    payload = prepare_viewer_payload([atom()], source_format="pdb")
    record = build_preparation_record(source, payload, parser_version="kinetics-pdb-1")
    assert record["record_schema"] == "kinetics.structure-preparation.v1"
    assert record["source_bytes"] == len(source)
    assert len(record["source_sha256"]) == 64
    assert len(record["payload_sha256"]) == 64
    assert record["atom_count"] == 1
    assert record == build_preparation_record(source, payload, parser_version="kinetics-pdb-1")


def test_preparation_record_rejects_invalid_metadata() -> None:
    payload = prepare_viewer_payload([atom()], source_format="pdb")
    with pytest.raises(ValueError, match="source_bytes"):
        build_preparation_record(b"", payload, parser_version="1")
    with pytest.raises(ValueError, match="parser_version"):
        build_preparation_record(b"x", payload, parser_version=" ")
    with pytest.raises(ValueError, match="dropped_record_count"):
        build_preparation_record(b"x", payload, parser_version="1", dropped_record_count=-1)


def test_viewer_payload_rejects_non_integer_or_boolean_atom_limits() -> None:
    for invalid_limit in (True, 1.5, "10"):
        with pytest.raises(ValueError, match="max_atoms"):
            prepare_viewer_payload([atom()], source_format="pdb", max_atoms=invalid_limit)  # type: ignore[arg-type]
