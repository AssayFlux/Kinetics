#!/usr/bin/env python3
"""Compare selected Kinetics translation tables with Biopython's NCBI tables."""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

try:
    import Bio
    from Bio.Data import CodonTable
except ImportError as error:
    raise SystemExit(
        "Install the pinned validation dependency from validation/requirements-biopython.txt"
    ) from error

from kinetics.genetic_code import GENETIC_CODES, translate_coding_sequence


def run() -> dict[str, object]:
    codons = [
        "".join(parts)
        for parts in itertools.product("ACGT", repeat=3)
    ]
    comparisons: list[dict[str, object]] = []
    for table_id in sorted(GENETIC_CODES):
        reference = CodonTable.unambiguous_dna_by_id[table_id]
        mismatches = []
        for codon in codons:
            expected = reference.forward_table.get(codon, "*")
            observed = translate_coding_sequence(codon, table_id=table_id)["protein"]
            if observed != expected:
                mismatches.append({
                    "codon": codon,
                    "expected": expected,
                    "observed": observed,
                })
        local = GENETIC_CODES[table_id]
        comparisons.append({
            "table_id": table_id,
            "table_name": local.name,
            "codons_checked": len(codons),
            "start_codons_match": local.starts == frozenset(reference.start_codons),
            "stop_codons_match": local.stops == frozenset(reference.stop_codons),
            "mismatches": mismatches,
            "pass": not mismatches
            and local.starts == frozenset(reference.start_codons)
            and local.stops == frozenset(reference.stop_codons),
        })
    return {
        "validation_id": "kinetics-genetic-code-biopython-2026-11-08",
        "reference": "Bio.Data.CodonTable.unambiguous_dna_by_id",
        "biopython_version": Bio.__version__,
        "method": "exhaustive 64-codon and start/stop set comparison",
        "tables_checked": sorted(GENETIC_CODES),
        "comparisons": comparisons,
        "overall_pass": all(item["pass"] for item in comparisons),
        "limitations": [
            "Checks table transcription against Biopython, not biological correctness of an organism assignment",
            "Only NCBI tables 1, 2, 4, 5 and 11 are implemented",
            "Does not infer genetic codes, find genes, identify organisms or predict function",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
