#!/usr/bin/env python3
"""Compare Kinetics neighbour joining with Biopython on an additive fixture.

This is a synthetic algorithm-concordance check, not a published phylogeny.
"""
from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

try:
    import Bio
    from Bio.Phylo.TreeConstruction import DistanceMatrix, DistanceTreeConstructor
except ImportError as error:
    raise SystemExit(
        "Install the pinned validation dependency from validation/requirements-biopython.txt"
    ) from error

from kinetics.phylo import leaf_names, neighbor_joining, patristic_distance


def run() -> dict[str, object]:
    labels = ["A", "B", "C", "D"]
    matrix = [
        [0.0, 3.0, 4.0, 6.0],
        [3.0, 0.0, 5.0, 7.0],
        [4.0, 5.0, 0.0, 4.0],
        [6.0, 7.0, 4.0, 0.0],
    ]
    lower_triangle = [
        [0.0],
        [3.0, 0.0],
        [4.0, 5.0, 0.0],
        [6.0, 7.0, 4.0, 0.0],
    ]
    local_tree = neighbor_joining(matrix, labels)
    reference_tree = DistanceTreeConstructor().nj(DistanceMatrix(labels, lower_triangle))
    local_leaves = sorted(leaf_names(local_tree))
    reference_leaves = sorted(
        terminal.name for terminal in reference_tree.get_terminals()
    )
    comparisons = []
    for first, second in combinations(labels, 2):
        observed = patristic_distance(local_tree, first, second)
        expected = float(reference_tree.distance(first, second))
        comparisons.append({
            "pair": [first, second],
            "kinetics_distance": observed,
            "biopython_distance": expected,
            "absolute_error": abs(observed - expected),
            "pass": abs(observed - expected) <= 1e-8,
        })
    return {
        "validation_id": "kinetics-neighbor-joining-biopython-2026-11-09",
        "reference": "Bio.Phylo.TreeConstruction.DistanceTreeConstructor.nj",
        "biopython_version": Bio.__version__,
        "method": "additive four-taxon matrix; all six patristic distances",
        "tolerance": 1e-8,
        "local_leaves": local_leaves,
        "reference_leaves": reference_leaves,
        "comparisons": comparisons,
        "overall_pass": (
            local_leaves == sorted(labels)
            and reference_leaves == sorted(labels)
            and all(item["pass"] for item in comparisons)
        ),
        "limitations": [
            "Synthetic additive distances only; no published or experimental alignment/tree is included.",
            "Checks neighbour-joining patristic distances, not evolutionary model adequacy or topology uncertainty.",
            "Does not validate ML/Bayesian inference, rate heterogeneity, search, viewers or Android performance.",
        ],
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["overall_pass"]:
        raise SystemExit(1)
