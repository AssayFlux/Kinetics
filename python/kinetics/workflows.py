"""Bounded, local FASTA quality-control workflow.

This is basic sequence parsing/statistics, not sequence identification or
biological/clinical interpretation.
"""
from __future__ import annotations

from typing import Any

from .sequence import parse_fasta, sequence_statistics

MAX_FASTA_CHARS = 1_000_000
MAX_FASTA_RECORDS = 1_000
MAX_FASTA_BASES = 500_000


def _positive_limit(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def analyze_fasta_text(
    text: str,
    *,
    max_chars: int = MAX_FASTA_CHARS,
    max_records: int = MAX_FASTA_RECORDS,
    max_bases: int = MAX_FASTA_BASES,
) -> dict[str, Any]:
    """Parse bounded FASTA text and report per-record lengths/GC/ambiguous counts.

    GC percentage uses all sequence symbols as its denominator; non-ACGT
    symbols are reported separately and are not silently discarded.
    """
    max_chars = _positive_limit("max_chars", max_chars)
    max_records = _positive_limit("max_records", max_records)
    max_bases = _positive_limit("max_bases", max_bases)
    if not isinstance(text, str):
        raise TypeError("FASTA input must be text")
    if len(text) > max_chars:
        raise ValueError("FASTA input exceeds the configured character limit")
    records = parse_fasta(text)
    if len(records) > max_records:
        raise ValueError("FASTA input exceeds the configured record limit")
    total_bases = sum(len(record.sequence) for record in records)
    if total_bases > max_bases:
        raise ValueError("FASTA input exceeds the configured total-base limit")

    summaries = []
    for record in records:
        stats = sequence_statistics(record.sequence)
        summaries.append(
            {
                "identifier": record.identifier,
                "description": record.description,
                "length": int(stats["length"]),
                "gc_percent": round(float(stats["gc_fraction"]) * 100.0, 3),
                "ambiguous_count": int(stats["ambiguous_count"]),
            }
        )
    return {
        "record_count": len(summaries),
        "total_bases": total_bases,
        "gc_denominator": "all sequence symbols",
        "records": summaries,
        "limitations": [
            "Basic parsing and composition statistics only",
            "No identity, homology, gene function or protein function inference",
            "No pathogenicity or clinical interpretation",
            "Independent biological validation is not claimed",
        ],
    }
