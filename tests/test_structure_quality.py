from __future__ import annotations

import pytest

from kinetics.structure import Atom
from kinetics.structure_quality import structure_geometry_metrics


def atom(serial: int, chain: str, residue_number: int, x: float, element: str = "C") -> Atom:
    return Atom(serial, "CA", "ALA", chain, residue_number, x, 0.0, 0.0, element)


def test_geometry_metrics_report_clashes_without_assigning_quality_grade() -> None:
    result = structure_geometry_metrics([
        atom(1, "A", 1, 0.0),
        atom(2, "B", 2, 1.0),
        atom(3, "A", 1, 20.0),
    ])
    assert result["atom_count"] == 3
    assert result["residue_count"] == 2
    assert result["clash_count"] == 1
    assert result["severe_clash_count"] == 1
    assert result["quality_badge"] == "not_assessed"
    assert result["assessment_status"] == "geometry_screen_only"


def test_geometry_metrics_exclude_unknown_elements_and_bound_candidate_work() -> None:
    result = structure_geometry_metrics([
        atom(1, "A", 1, 0.0, "XX"),
        atom(2, "B", 2, 1.0, "C"),
    ])
    assert result["assessed_atom_count"] == 1
    assert result["unassessed_element_counts"] == {"XX": 1}
    with pytest.raises(ValueError, match="max_candidate_pairs"):
        structure_geometry_metrics(
            [atom(1, "A", 1, 0.0), atom(2, "B", 2, 1.0), atom(3, "C", 3, 2.0)],
            max_candidate_pairs=1,
        )


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"max_atoms": True}, "max_atoms"),
        ({"max_reported_clashes": 1.5}, "max_reported_clashes"),
        ({"clash_overlap_angstrom": float("nan")}, "clash_overlap_angstrom"),
        ({"severe_overlap_angstrom": 0.2}, "severe overlap"),
    ],
)
def test_geometry_metrics_reject_invalid_limits(kwargs, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        structure_geometry_metrics([atom(1, "A", 1, 0.0)], **kwargs)


def test_geometry_metrics_keep_only_configured_top_clash_records() -> None:
    result = structure_geometry_metrics(
        [atom(1, "A", 1, 0.0), atom(2, "B", 2, 1.0), atom(3, "C", 3, 2.0)],
        max_reported_clashes=1,
    )
    assert result["clash_count"] == 3
    assert len(result["top_clashes"]) == 1
