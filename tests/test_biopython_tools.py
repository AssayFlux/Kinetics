import pytest

from kinetics_core.biopython_tools import (
    align_protein_sequences,
    align_sequence_to_structure_chain,
    calculate_hydrogen_bonds,
    calculate_ligand_contacts,
    calculate_residue_contacts,
    calculate_residue_sasa,
    structure_summary,
    superimpose_ca_atoms,
)


def atom(serial, name, residue, chain, number, x, y, z, element="C"):
    return (
        f"ATOM  {serial:5d} {name:>4s} {residue:>3s} {chain}{number:4d}    "
        f"{x:8.3f}{y:8.3f}{z:8.3f}{1.0:6.2f}{20.0:6.2f}"
        f"          {element:>2s}\n"
    )


@pytest.fixture
def pdb_file(tmp_path):
    lines = []
    serial = 1
    # Three non-collinear CA positions; include N/C atoms for meaningful surface.
    for number, residue, x, y, z in [
        (1, "ALA", 0.0, 0.0, 0.0),
        (2, "CYS", 4.0, 0.0, 0.0),
        (3, "ASP", 0.0, 4.0, 0.0),
    ]:
        lines.append(atom(serial, "N", residue, "A", number, x - 0.8, y, z, "N"))
        serial += 1
        lines.append(atom(serial, "CA", residue, "A", number, x, y, z))
        serial += 1
        lines.append(atom(serial, "C", residue, "A", number, x + 0.8, y, z))
        serial += 1
    lines.append("TER\nEND\n")
    path = tmp_path / "tiny.pdb"
    path.write_text("".join(lines), encoding="ascii")
    return path


def test_structure_summary_tracks_digest_models_chains_and_residues(pdb_file):
    result = structure_summary(pdb_file, file_format="pdb")
    assert result["file_format"] == "pdb"
    assert len(result["source_sha256"]) == 64
    assert result["model_count"] == 1
    assert result["models"][0]["chains"][0]["chain_id"] == "A"
    assert result["models"][0]["chains"][0]["polymer_residue_count"] == 3


def test_sasa_and_contact_features_are_finite_and_provenance_linked(pdb_file):
    sasa = calculate_residue_sasa(pdb_file, file_format="pdb")
    assert sasa["feature"] == "residue_sasa"
    assert len(sasa["source_sha256"]) == 64
    assert len(sasa["residues"]) == 3
    assert all(item["sasa_angstrom2"] >= 0 for item in sasa["residues"])

    contacts = calculate_residue_contacts(
        pdb_file, file_format="pdb", cutoff_angstrom=4.5
    )
    assert contacts["feature"] == "residue_contacts"
    assert contacts["cutoff_angstrom"] == 4.5
    assert contacts["contacts"]
    assert all(
        item["minimum_heavy_atom_distance_angstrom"] <= 4.5
        for item in contacts["contacts"]
    )


def test_explicit_ca_superposition_reports_rmsd_and_transform(pdb_file):
    result = superimpose_ca_atoms(
        pdb_file,
        pdb_file,
        reference_format="pdb",
        mobile_format="pdb",
        chain_id="A",
        residue_pairs=[(1, 1), (2, 2), (3, 3)],
    )
    assert result["atom_count"] == 3
    assert result["rmsd_angstrom"] == pytest.approx(0.0, abs=1e-6)
    assert result["coordinate_transform"] == "mobile_to_reference"
    assert len(result["rotation"]) == 3


def test_pairwise_sequence_alignment_uses_biopython():
    result = align_protein_sequences("MKTAYIAKQRQISFVKSHFS", "MKTAYIAKQRQISFVKSHFS")
    assert result["method"] == "Biopython PairwiseAligner"
    assert result["score"] > 0
    assert "MKTAYIAK" in result["alignment"]


def test_invalid_contact_cutoff_is_rejected(pdb_file):
    with pytest.raises(ValueError, match="cutoff"):
        calculate_residue_contacts(pdb_file, file_format="pdb", cutoff_angstrom=0)



def test_sequence_to_structure_alignment_preserves_author_residue_ids(pdb_file):
    result = align_sequence_to_structure_chain(
        "ACD", pdb_file, file_format="pdb", chain_id="A"
    )
    assert result["mapped_residue_count"] == 3
    assert result["mismatch_count"] == 0
    assert result["alignment_is_unique"]
    assert [item["sequence_position"] for item in result["mapping"]] == [1, 2, 3]
    assert [item["structure_residue_number"] for item in result["mapping"]] == [1, 2, 3]


def test_hydrogen_bond_detector_does_not_infer_missing_hydrogens(pdb_file):
    result = calculate_hydrogen_bonds(pdb_file, file_format="pdb")
    assert result["status"] == "not_computed_no_explicit_hydrogens"
    assert result["hydrogen_bonds"] == []


def test_ligand_contact_detector_reports_absence_without_inference(pdb_file):
    result = calculate_ligand_contacts(pdb_file, file_format="pdb")
    assert result["status"] == "no_ligand_contacts_within_cutoff"
    assert result["contacts"] == []
