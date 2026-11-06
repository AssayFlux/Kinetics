import hashlib

import pytest

from kinetics_core.proteomics import (
    ProteinSequenceRecord,
    ResidueMapping,
    StructureFeature,
    StructureRecord,
    sequence_sha256,
)


def records():
    sequence = ProteinSequenceRecord(
        source="UniProt", source_record_id="entry:Q9TEST", accession="Q9TEST",
        sequence=" acd ef ", source_version="2026_01", license_id="CC-BY-4.0",
    )
    structure = StructureRecord(
        source="PDB", source_record_id="pdb:1ABC", structure_id="1ABC",
        coordinate_sha256="a" * 64, coordinate_format="pdb", model_kind="experimental",
        chain_ids=("A",), source_version="2026-01", license_id="PDB-terms",
    )
    return sequence, structure


def test_sequence_normalization_and_digest_are_deterministic():
    sequence, _ = records()
    assert sequence.sequence == "ACDEF"
    assert sequence.as_dict()["sequence_length"] == 5
    assert sequence_sha256("ACDEF") == hashlib.sha256(b"ACDEF").hexdigest()


def test_sequence_rejects_non_amino_acid_symbols():
    with pytest.raises(ValueError, match="unsupported"):
        ProteinSequenceRecord("db", "r1", "P1", "ACD*", "v1", "license")


def test_structure_keeps_predicted_and_experimental_distinct():
    _, structure = records()
    assert structure.as_dict()["model_kind"] == "experimental"
    with pytest.raises(ValueError, match="model_kind"):
        StructureRecord("db", "r", "s", "a" * 64, "pdb", "unknown", ("A",), "v1", "L")


def test_residue_mapping_is_explicit_and_checked_against_chain_and_sequence():
    sequence, structure = records()
    mapping = ResidueMapping("Q9TEST", 2, "1ABC", "A", 17, "CYS", "SIFTS",
                             "sifts:1ABC:A:17")
    mapping.validate_against(sequence, structure)
    with pytest.raises(ValueError, match="chain"):
        ResidueMapping("Q9TEST", 2, "1ABC", "B", 17, "CYS", "manual",
                       "evidence").validate_against(sequence, structure)
    with pytest.raises(ValueError, match="exceeds"):
        ResidueMapping("Q9TEST", 6, "1ABC", "A", 17, "CYS", "manual",
                       "evidence").validate_against(sequence, structure)


def test_derived_feature_requires_tool_parameters_frame_and_mapping_evidence():
    feature = StructureFeature("f1", "1ABC", "ca_distance", 3.2, "angstrom",
                               "kinetics-geometry", "0.1", "b" * 64, "model-1",
                               ("sifts:1ABC:A:17",))
    assert feature.as_dict()["schema_version"] == "kinetics.structure-feature/1.0"
    with pytest.raises(ValueError, match="mapping evidence"):
        StructureFeature("f1", "1ABC", "x", 1.0, "A", "tool", "1", "b" * 64,
                         "model-1", ())
