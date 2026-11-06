import hashlib

import pytest

from kinetics_core.mmcif_adapter import parse_mmcif_coordinates
from kinetics_core.pdb_adapter import calculate_ca_distance
from kinetics_core.proteomics import ProteinSequenceRecord, ResidueMapping, StructureRecord


def cif_text(second_chain="A", second_x="3.0"):
    return f"""data_demo
#
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_alt_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_entity_id
_atom_site.label_seq_id
_atom_site.pdbx_PDB_ins_code
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.occupancy
_atom_site.B_iso_or_equiv
_atom_site.auth_seq_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_atom_id
_atom_site.pdbx_PDB_model_num
ATOM 1 C CA . ALA A 1 1 ? 0.0 0.0 0.0 1.0 20.0 1 ALA A CA 1
ATOM 2 C CA . CYS A 1 2 ? {second_x} 4.0 0.0 1.0 20.0 2 CYS {second_chain} CA 1
#
""".encode()


def fixture(content):
    sequence = ProteinSequenceRecord(
        source="fixture", source_record_id="fixture:AC", accession="P-AC",
        sequence="AC", source_version="1", license_id="CC0-1.0",
    )
    structure = StructureRecord(
        source="fixture", source_record_id="fixture:1ABC", structure_id="1ABC",
        coordinate_sha256=hashlib.sha256(content).hexdigest(), coordinate_format="mmcif",
        model_kind="experimental", chain_ids=("A",), source_version="1",
        license_id="CC0-1.0",
    )
    mappings = (
        ResidueMapping("P-AC", 1, "1ABC", "A", 1, "ALA", "fixture-map", "map:first"),
        ResidueMapping("P-AC", 2, "1ABC", "A", 2, "CYS", "fixture-map", "map:second"),
    )
    return sequence, structure, mappings


def test_mmcif_parse_and_evidence_linked_distance():
    content = cif_text()
    sequence, structure, mappings = fixture(content)
    parsed = parse_mmcif_coordinates(content, structure)
    feature = calculate_ca_distance(parsed, sequence, *mappings)
    assert feature.value == pytest.approx(5.0)
    assert feature.coordinate_frame == "mmcif-model:1"
    assert feature.mapping_evidence_ids == ("map:first", "map:second")


def test_mmcif_rejects_digest_mismatch_and_unregistered_chain():
    content = cif_text()
    _, structure, _ = fixture(content)
    with pytest.raises(ValueError, match="digest"):
        parse_mmcif_coordinates(content + b"# tampered\\n", structure)

    bad = cif_text(second_chain="B")
    _, bad_structure, _ = fixture(bad)
    with pytest.raises(ValueError, match="chain"):
        parse_mmcif_coordinates(bad, bad_structure)


def test_mmcif_rejects_non_finite_coordinates():
    content = cif_text(second_x="nan")
    _, structure, _ = fixture(content)
    with pytest.raises(ValueError, match="non-finite"):
        parse_mmcif_coordinates(content, structure)
