"""Conservative coordinate-geometry metrics for S2 structure review.

Metrics are descriptive screening signals only. They do not produce a calibrated
structure-quality grade, validation badge, or experimental/prediction confidence.
"""
from __future__ import annotations

import heapq
from collections import defaultdict
from math import floor, isfinite, sqrt
from typing import Iterable

from .structure import Atom

_VDW_RADII = {
    "H": 1.20, "C": 1.70, "N": 1.55, "O": 1.52, "F": 1.47,
    "P": 1.80, "S": 1.80, "CL": 1.75, "BR": 1.85, "I": 1.98,
}


def structure_geometry_metrics(
    atoms: Iterable[Atom],
    *,
    clash_overlap_angstrom: float = 0.4,
    severe_overlap_angstrom: float = 0.8,
    max_atoms: int = 200_000,
    max_candidate_pairs: int = 2_000_000,
    max_reported_clashes: int = 20,
) -> dict[str, object]:
    """Summarize atom/residue counts and bounded nonbonded steric-overlap candidates.

    Pairs in the same residue are excluded because this Atom model has no bond
    topology. Only elements with an explicit radius are assessed. Unknown elements
    are counted and excluded, never assigned an invented radius.
    """
    for name, value in (
        ("max_atoms", max_atoms),
        ("max_candidate_pairs", max_candidate_pairs),
        ("max_reported_clashes", max_reported_clashes),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    for name, threshold in (
        ("clash_overlap_angstrom", clash_overlap_angstrom),
        ("severe_overlap_angstrom", severe_overlap_angstrom),
    ):
        if (
            isinstance(threshold, bool)
            or not isinstance(threshold, (int, float))
            or not isfinite(threshold)
            or threshold <= 0
        ):
            raise ValueError(f"{name} must be finite and positive")
    if severe_overlap_angstrom < clash_overlap_angstrom:
        raise ValueError("severe overlap threshold must be >= clash threshold")

    points: list[Atom] = []
    for atom in atoms:
        if len(points) >= max_atoms:
            raise ValueError("Structure exceeds max_atoms")
        if not all(isfinite(value) for value in (atom.x, atom.y, atom.z)):
            raise ValueError("Structure contains non-finite coordinates")
        points.append(atom)
    if not points:
        raise ValueError("Structure must contain at least one atom")

    residues = {(atom.chain, atom.residue_number, atom.residue) for atom in points}
    supported: list[tuple[int, Atom, float]] = []
    unknown_elements: dict[str, int] = defaultdict(int)
    for index, atom in enumerate(points):
        element = atom.element.strip().upper()
        radius = _VDW_RADII.get(element)
        if radius is None:
            unknown_elements[element or "<blank>"] += 1
        else:
            supported.append((index, atom, radius))

    cell_size = 4.0
    cells: dict[tuple[int, int, int], list[tuple[int, Atom, float]]] = defaultdict(list)
    for supported_atom in supported:
        atom = supported_atom[1]
        key = (floor(atom.x / cell_size), floor(atom.y / cell_size), floor(atom.z / cell_size))
        cells[key].append(supported_atom)

    top_clashes: list[tuple[float, int, dict[str, object]]] = []
    candidate_pairs = 0
    severe_count = 0
    clash_count = 0
    for index, atom, radius in supported:
        key = (floor(atom.x / cell_size), floor(atom.y / cell_size), floor(atom.z / cell_size))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for other_index, other, other_radius in cells.get(
                        (key[0] + dx, key[1] + dy, key[2] + dz), (),
                    ):
                        if other_index <= index:
                            continue
                        if atom.chain == other.chain and atom.residue_number == other.residue_number:
                            continue
                        candidate_pairs += 1
                        if candidate_pairs > max_candidate_pairs:
                            raise ValueError("Structure exceeds max_candidate_pairs")
                        distance = sqrt(
                            (atom.x - other.x) ** 2
                            + (atom.y - other.y) ** 2
                            + (atom.z - other.z) ** 2
                        )
                        overlap = radius + other_radius - distance
                        if overlap <= clash_overlap_angstrom:
                            continue
                        clash_count += 1
                        severe = overlap > severe_overlap_angstrom
                        severe_count += int(severe)
                        record = {
                            "atom_index_1": index,
                            "atom_index_2": other_index,
                            "chain_1": atom.chain,
                            "residue_1": atom.residue_number,
                            "atom_1": atom.name,
                            "chain_2": other.chain,
                            "residue_2": other.residue_number,
                            "atom_2": other.name,
                            "distance_angstrom": round(distance, 4),
                            "overlap_angstrom": round(overlap, 4),
                            "severity": "severe" if severe else "candidate",
                        }
                        heap_entry: tuple[float, int, dict[str, object]] = (overlap, candidate_pairs, record)
                        if len(top_clashes) < max_reported_clashes:
                            heapq.heappush(top_clashes, heap_entry)
                        else:
                            heapq.heappushpop(top_clashes, heap_entry)

    clashes = [
        item[2] for item in sorted(top_clashes, key=lambda entry: entry[0], reverse=True)
    ]
    return {
        "schema": "kinetics.structure-geometry-metrics.v1",
        "atom_count": len(points),
        "residue_count": len(residues),
        "assessed_atom_count": len(supported),
        "unassessed_element_counts": dict(sorted(unknown_elements.items())),
        "candidate_pair_count": candidate_pairs,
        "clash_count": clash_count,
        "severe_clash_count": severe_count,
        "clash_threshold_angstrom": clash_overlap_angstrom,
        "severe_threshold_angstrom": severe_overlap_angstrom,
        "top_clashes": clashes,
        "quality_badge": "not_assessed",
        "assessment_status": "geometry_screen_only",
        "limitations": [
            "Same-residue pairs are excluded because covalent bond topology is unavailable.",
            "Only listed element van der Waals radii are assessed; unknown elements are excluded.",
            "No hydrogens, alternate conformations, occupancies, bond geometry or protonation are inferred.",
            "This is not a MolProbity clashscore, Ramachandran analysis or calibrated quality grade.",
            "Experimental resolution/R-free and predicted pLDDT/PAE are not available in the Atom model.",
        ],
    }
