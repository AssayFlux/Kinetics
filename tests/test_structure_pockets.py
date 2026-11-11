from __future__ import annotations

import pytest

from kinetics.structure import Atom
from kinetics import ligand_site_candidates


def test_ligand_site_candidates_report_nearby_protein_residues_deterministically() -> None:
    atoms = [
        Atom(1, "C1", "LIG", "X", 900, 0.0, 0.0, 0.0, "C"),
        Atom(2, "O1", "LIG", "X", 900, 1.0, 0.0, 0.0, "O"),
        Atom(3, "CA", "ALA", "A", 10, 3.0, 0.0, 0.0, "C"),
        Atom(4, "CB", "ALA", "A", 10, 3.5, 0.0, 0.0, "C"),
        Atom(5, "CA", "GLY", "A", 11, 20.0, 0.0, 0.0, "C"),
        Atom(6, "O", "HOH", "W", 1, 0.5, 0.0, 0.0, "O"),
        Atom(7, "H", "ALA", "A", 10, 2.0, 0.0, 0.0, "H"),
    ]
    result = ligand_site_candidates(
        atoms, ligand_chain="X", ligand_residue_number=900,
        ligand_residue_name="LIG", cutoff_angstrom=4.0,
    )
    assert result["status"] == "candidates_found"
    assert result["candidate_residue_count"] == 1
    candidate = result["residue_candidates"][0]
    assert candidate["residue_number"] == 10
    assert candidate["atom_contact_count"] == 4
    assert result["interpretation"] == "ligand_proximal_geometric_site_candidates_only"


def test_ligand_site_candidates_require_explicit_existing_ligand() -> None:
    atoms = [Atom(1, "CA", "ALA", "A", 1, 0.0, 0.0, 0.0, "C")]
    with pytest.raises(ValueError, match="not found"):
        ligand_site_candidates(
            atoms, ligand_chain="X", ligand_residue_number=9, ligand_residue_name="LIG",
        )


def test_ligand_site_candidates_enforce_bounds_and_finite_coordinates() -> None:
    ligand = Atom(1, "C1", "LIG", "X", 9, 0.0, 0.0, 0.0, "C")
    protein = Atom(2, "CA", "ALA", "A", 1, 1.0, 0.0, 0.0, "C")
    with pytest.raises(ValueError, match="max_atoms"):
        ligand_site_candidates([ligand, protein], ligand_chain="X", ligand_residue_number=9,
                               ligand_residue_name="LIG", max_atoms=1)
    invalid = Atom(3, "CA", "ALA", "A", 1, float("nan"), 0.0, 0.0, "C")
    with pytest.raises(ValueError, match="non-finite"):
        ligand_site_candidates([ligand, invalid], ligand_chain="X", ligand_residue_number=9,
                               ligand_residue_name="LIG")
    with pytest.raises(ValueError, match="max_candidate_pairs"):
        ligand_site_candidates([ligand, protein], ligand_chain="X", ligand_residue_number=9,
                               ligand_residue_name="LIG", max_candidate_pairs=0)


def test_ligand_site_candidates_reject_canonical_protein_residue_as_ligand() -> None:
    atoms = [Atom(1, "CA", "ALA", "A", 1, 0.0, 0.0, 0.0, "C")]
    with pytest.raises(ValueError, match="canonical amino acid"):
        ligand_site_candidates(
            atoms, ligand_chain="A", ligand_residue_number=1, ligand_residue_name="ALA",
        )
