import hashlib

import pytest

from kinetics_core.pdb_adapter import calculate_ca_distance, parse_pdb_coordinates
from kinetics_core.proteomics import ProteinSequenceRecord, ResidueMapping, StructureRecord


def atom_line(serial, residue, chain, number, x, y, z, insertion=""):
    return (
        f"ATOM  {serial:5d} {'CA':>4s} {residue:>3s} {chain}{number:4d}"
        f"{(insertion or ' ')}   {x:8.3f}{y:8.3f}{z:8.3f}{1.0:6.2f}{20.0:6.2f}"
        f"          {'C':>2s}"
    )


def setup_records(content):
    sequence = ProteinSequenceRecord(
        source="fixture", source_record_id="fixture:AC", accession="P-AC",
        sequence="AC", source_version="1", license_id="CC0-1.0",
    )
    structure = StructureRecord(
        source="fixture", source_record_id="fixture:1ABC", structure_id="1ABC",
        coordinate_sha256=hashlib.sha256(content).hexdigest(), coordinate_format="pdb",
        model_kind="experimental", chain_ids=("A",), source_version="1",
        license_id="CC0-1.0",
    )
    return sequence, structure


def mappings(second_number=2, second_insertion=None):
    first = ResidueMapping(
        "P-AC", 1, "1ABC", "A", 1, "ALA", "fixture-map", "map:first"
    )
    second = ResidueMapping(
        "P-AC", 2, "1ABC", "A", second_number, "CYS", "fixture-map",
        "map:second", insertion_code=second_insertion,
    )
    return first, second


def test_parse_pdb_and_calculate_evidence_linked_ca_distance():
    content = (
        atom_line(1, "ALA", "A", 1, 0, 0, 0) + "\n"
        + atom_line(2, "CYS", "A", 2, 3, 4, 0) + "\nEND\n"
    ).encode("ascii")
    sequence, record = setup_records(content)
    parsed = parse_pdb_coordinates(content, record)
    feature = calculate_ca_distance(parsed, sequence, *mappings())
    assert feature.value == pytest.approx(5.0)
    assert feature.unit == "angstrom"
    assert feature.mapping_evidence_ids == ("map:first", "map:second")
    assert feature.as_dict()["coordinate_frame"] == "pdb-model:1"


def test_pdb_parser_rejects_coordinate_digest_mismatch():
    content = (atom_line(1, "ALA", "A", 1, 0, 0, 0) + "\n").encode("ascii")
    _, record = setup_records(content)
    with pytest.raises(ValueError, match="digest"):
        parse_pdb_coordinates(content + b"REMARK tamper\n", record)


def test_pdb_parser_rejects_unregistered_chain_and_non_finite_coordinates():
    content = (atom_line(1, "ALA", "B", 1, 0, 0, 0) + "\n").encode("ascii")
    _, record = setup_records(content)
    with pytest.raises(ValueError, match="chain"):
        parse_pdb_coordinates(content, record)
    bad = atom_line(1, "ALA", "A", 1, float("nan"), 0, 0) + "\n"
    _, bad_record = setup_records(bad.encode("ascii"))
    with pytest.raises(ValueError, match="non-finite"):
        parse_pdb_coordinates(bad.encode("ascii"), bad_record)


def test_mapping_requires_sequence_identity_and_explicit_insertion_code():
    content = (
        atom_line(1, "ALA", "A", 1, 0, 0, 0) + "\n"
        + atom_line(2, "CYS", "A", 2, 3, 4, 0, insertion="A") + "\n"
    ).encode("ascii")
    sequence, record = setup_records(content)
    parsed = parse_pdb_coordinates(content, record)
    first, second = mappings(second_insertion="A")
    assert calculate_ca_distance(parsed, sequence, first, second).value == pytest.approx(5.0)
    wrong = ResidueMapping(
        "P-AC", 2, "1ABC", "A", 2, "ALA", "fixture-map", "wrong-residue",
        insertion_code="A",
    )
    with pytest.raises(ValueError, match="identity"):
        calculate_ca_distance(parsed, sequence, first, wrong)
