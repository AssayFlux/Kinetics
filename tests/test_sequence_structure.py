from __future__ import annotations

import pytest

from kinetics.sequence_structure import map_exact_chain_sequence
from kinetics.structure import Atom


def atom(serial: int, residue: str, number: int, chain: str = "A") -> Atom:
    return Atom(serial, "CA", residue, chain, number, float(serial), 0.0, 0.0, "C")


def test_unique_exact_chain_mapping_preserves_structure_numbering() -> None:
    atoms = [
        atom(1, "ALA", 10), atom(2, "GLY", 11), atom(3, "SER", 12),
        atom(4, "VAL", 13), atom(5, "LEU", 14, "B"),
    ]
    result = map_exact_chain_sequence("MAGS VLK".replace(" ", ""), atoms, chain_id="A")
    assert result["status"] == "exact_unique_match"
    assert result["query_start_1based"] == 2
    mapped = result["mapped_residues"]
    assert [item["query_position_1based"] for item in mapped] == [2, 3, 4, 5]
    assert [item["structure_residue_number"] for item in mapped] == [10, 11, 12, 13]


def test_repeated_exact_match_abstains_instead_of_choosing() -> None:
    result = map_exact_chain_sequence(
        "AGSVAGSV", [atom(1, "ALA", 1), atom(2, "GLY", 2), atom(3, "SER", 3), atom(4, "VAL", 4)],
        chain_id="A",
    )
    assert result["status"] == "ambiguous_exact_match"
    assert result["candidate_query_starts_1based"] == [1, 5]
    assert result["mapped_residues"] == []


def test_no_match_and_nonstandard_residue_are_explicit() -> None:
    result = map_exact_chain_sequence("AAAA", [atom(1, "GLY", 1)], chain_id="A")
    assert result["status"] == "no_exact_match"
    with pytest.raises(ValueError, match="Unsupported/non-standard"):
        map_exact_chain_sequence("AAAA", [atom(1, "MSE", 1)], chain_id="A")


def test_mapping_validates_sequence_and_chain() -> None:
    with pytest.raises(ValueError, match="canonical"):
        map_exact_chain_sequence("ABZ", [atom(1, "ALA", 1)], chain_id="A")
    with pytest.raises(ValueError, match="chain_id"):
        map_exact_chain_sequence("A", [atom(1, "ALA", 1)], chain_id="")


def test_numbering_gaps_and_conflicting_residue_identity_abstain() -> None:
    gap = map_exact_chain_sequence(
        "AGSV", [atom(1, "ALA", 10), atom(2, "GLY", 12)], chain_id="A",
    )
    assert gap["status"] == "noncontiguous_structure_numbering"
    assert gap["mapped_residues"] == []

    with pytest.raises(ValueError, match="Conflicting residue identity"):
        map_exact_chain_sequence(
            "A", [atom(1, "ALA", 10), atom(2, "GLY", 10)], chain_id="A",
        )
