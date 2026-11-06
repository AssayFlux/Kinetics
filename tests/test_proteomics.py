import hashlib

import pytest

from kinetics_core.proteomics import (
    ProteinSequenceRecord,
    ResidueMapping,
    StructureFeature,
    StructureRecord,
    normalize_sequence,
)


def sequence():
    return ProteinSequenceRecord(
        source="fixture", source_record_id="seq:1", accession="P12345",
        sequence=" ac d ", source_version="v1", license_id="CC0-1.0",
    )


def structure():
    return StructureRecord(
        source="fixture", source_record_id="pdb:1ABC", structure_id="1ABC",
        coordinate_sha256=hashlib.sha256(b"coordinates").hexdigest(),
        coordinate_format="pdb", model_kind="experimental",
        chain_ids=("A",), source_version="1", license_id="CC0-1.0",
    )


def test_sequence_normalization_and_hash_are_stable():
    record = sequence()
    assert record.sequence == "ACD"
    assert record.as_dict()["sequence_length"] == 3
    assert len(record.as_dict()["sequence_sha256"]) == 64
    assert normalize_sequence(" a\nc d ") == "ACD"


@pytest.mark.parametrize("value", ["", "AC*D", "123", None])
def test_invalid_sequences_are_rejected(value):
    with pytest.raises((TypeError, ValueError)):
        normalize_sequence(value)


def test_structure_metadata_and_explicit_mapping_validate():
    protein, model = sequence(), structure()
    mapping = ResidueMapping(
        "P12345", 2, "1ABC", "A", 12, "CYS", "alignment-v1", "evidence:12",
    )
    mapping.validate_against(protein, model)
    assert mapping.as_dict()["schema_version"] == "kinetics.residue-mapping/1.0"


@pytest.mark.parametrize("position", [0, -1, 1.5, True])
def test_mapping_rejects_non_integer_or_non_positive_sequence_positions(position):
    with pytest.raises(ValueError, match="sequence_position"):
        ResidueMapping("P12345", position, "1ABC", "A", 12, "CYS", "map", "e1")


@pytest.mark.parametrize("number", [1.5, True])
def test_mapping_rejects_non_integer_author_residue_numbers(number):
    with pytest.raises(ValueError, match="residue_number"):
        ResidueMapping("P12345", 2, "1ABC", "A", number, "CYS", "map", "e1")


def test_mapping_rejects_accession_chain_structure_and_residue_mismatches():
    protein, model = sequence(), structure()
    wrong_accession = ResidueMapping("P99999", 2, "1ABC", "A", 12, "CYS", "map", "e1")
    with pytest.raises(ValueError, match="accession"):
        wrong_accession.validate_against(protein, model)
    wrong_chain = ResidueMapping("P12345", 2, "1ABC", "B", 12, "CYS", "map", "e1")
    with pytest.raises(ValueError, match="chain"):
        wrong_chain.validate_against(protein, model)
    wrong_residue = ResidueMapping("P12345", 2, "1ABC", "A", 12, "ALA", "map", "e1")
    with pytest.raises(ValueError, match="identity"):
        wrong_residue.validate_against(protein, model)


def test_feature_requires_finite_value_and_parameter_digest():
    feature = StructureFeature(
        feature_id="f1", structure_id="1ABC", feature_name="distance",
        value=1.25, unit="angstrom", tool_name="fixture", tool_version="1",
        parameter_sha256=hashlib.sha256(b"params").hexdigest(),
        coordinate_frame="pdb-model:1", mapping_evidence_ids=("e1", "e2"),
    )
    assert feature.as_dict()["schema_version"] == "kinetics.structure-feature/1.0"
    with pytest.raises(ValueError, match="finite"):
        StructureFeature(
            feature_id="f2", structure_id="1ABC", feature_name="distance",
            value=float("nan"), unit="angstrom", tool_name="fixture", tool_version="1",
            parameter_sha256=hashlib.sha256(b"params").hexdigest(),
            coordinate_frame="pdb-model:1", mapping_evidence_ids=("e1",),
        )
