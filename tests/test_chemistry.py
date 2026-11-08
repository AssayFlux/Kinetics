from __future__ import annotations

import pytest

from kinetics.chemistry import (
    graph_descriptors, parse_sdf_record, path_fingerprint, substructure_match, tanimoto,
)


def molecule(elements: list[str], bonds: list[tuple[int, int, int]]) -> dict[str, object]:
    atoms = [{"element": element, "x": 0.0, "y": 0.0, "z": 0.0} for element in elements]
    return {"atoms": atoms, "bonds": bonds}


def test_sdf_v2000_parses_formula_and_rejects_non_finite_coordinates() -> None:
    counts = f"{2:3d}{1:3d}  0  0  0  0            999 V2000"
    atom_a = f"{0.0:10.4f}{0.0:10.4f}{0.0:10.4f} {'C':>3s}"
    atom_b = f"{1.0:10.4f}{0.0:10.4f}{0.0:10.4f} {'C':>3s}"
    bond = f"{1:3d}{2:3d}{1:3d}"
    parsed = parse_sdf_record("\n".join(["ethane", "Kinetics", "", counts, atom_a, atom_b, bond, "M  END", "$$$$"]))
    assert parsed["formula"] == "C2"
    assert parsed["atom_count"] == 2
    assert graph_descriptors(parsed)["cycle_rank"] == 0


def test_graph_descriptors_and_path_fingerprint_are_deterministic() -> None:
    ring = molecule(["C", "C", "C"], [(0, 1, 1), (1, 2, 1), (2, 0, 1)])
    result = graph_descriptors(ring)
    assert result["cycle_rank"] == 1
    assert result["connected_components"] == 1
    assert path_fingerprint(ring) == path_fingerprint(ring)


def test_exact_substructure_match_respects_elements_and_bond_order() -> None:
    target = molecule(["C", "C", "O"], [(0, 1, 1), (1, 2, 1)])
    carbon_pair = molecule(["C", "C"], [(0, 1, 1)])
    double_bond = molecule(["C", "C"], [(0, 1, 2)])
    oxygen_pair = molecule(["O", "O"], [(0, 1, 1)])
    assert substructure_match(target, carbon_pair)
    assert not substructure_match(target, double_bond)
    assert not substructure_match(target, oxygen_pair)


def test_substructure_search_has_a_hard_state_limit() -> None:
    target = molecule(["C"] * 8, [(index, index + 1, 1) for index in range(7)])
    query = molecule(["C"] * 4, [(index, index + 1, 1) for index in range(3)])
    with pytest.raises(ValueError, match="max_search_states"):
        substructure_match(target, query, max_search_states=1)


def test_tanimoto_handles_empty_and_disjoint_fingerprints() -> None:
    assert tanimoto(frozenset(), frozenset()) == 1
    assert tanimoto(frozenset({"a"}), frozenset({"b"})) == 0


def test_sdf_iterator_reads_multiple_records_and_skips_empty_blocks() -> None:
    from kinetics.chemistry import iter_sdf_records

    counts = f"{1:3d}{0:3d}  0  0  0  0            999 V2000"
    atom = f"{0.0:10.4f}{0.0:10.4f}{0.0:10.4f} {'C':>3s}"
    record = "\n".join(["methane", "Kinetics", "", counts, atom, "M  END"])
    parsed = list(iter_sdf_records(record + "\n$$$$\n\n" + record + "\n$$$$\n"))
    assert len(parsed) == 2
    assert parsed[0]["formula"] == "C"
    assert parsed[1]["atom_count"] == 1
