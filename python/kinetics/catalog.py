"""Source-attributed, expandable gene catalogue ingestion for NCBI gene_info."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator


@dataclass(frozen=True)
class GeneEntry:
    tax_id: str
    gene_id: str
    symbol: str
    description: str
    synonyms: tuple[str, ...]
    source: str
    source_release: str
    evidence_status: str = "catalogued"


def iter_ncbi_gene_info(lines: Iterable[str], *, source_release: str) -> Iterator[GeneEntry]:
    """Stream NCBI gene_info TSV rows; data is user-supplied and source-attributed."""
    if not source_release.strip():
        raise ValueError("Pin the NCBI gene_info release/date before import")
    for line_number, raw in enumerate(lines, 1):
        line = raw.rstrip("\\r\\n")
        if not line or line.startswith("#"):
            continue
        fields = line.split("\\t")
        if len(fields) < 9:
            raise ValueError(f"gene_info line {line_number}: expected at least 9 columns")
        tax_id, gene_id, symbol, _, synonyms, _, _, _, description = fields[:9]
        if not tax_id.isdigit() or not gene_id.isdigit() or not symbol:
            raise ValueError(f"gene_info line {line_number}: invalid tax_id, GeneID or symbol")
        aliases = tuple(sorted({value for value in synonyms.split("|") if value not in {"", "-"}}))
        yield GeneEntry(tax_id, gene_id, symbol, description, aliases,
                        "NCBI Gene gene_info", source_release)


def validate_gene_catalog(entries: Iterable[GeneEntry]) -> None:
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        if not all((entry.tax_id, entry.gene_id, entry.symbol, entry.source, entry.source_release)):
            raise ValueError("Gene entries require tax_id, GeneID, symbol, source and release")
        key = (entry.tax_id, entry.gene_id)
        if key in seen:
            raise ValueError(f"Duplicate NCBI gene entry: {entry.tax_id}:{entry.gene_id}")
        seen.add(key)
        if entry.evidence_status not in {"catalogued", "prioritised", "implemented", "validated"}:
            raise ValueError(f"Unknown evidence status: {entry.evidence_status}")
        if entry.evidence_status == "validated":
            raise ValueError("A catalogue import cannot confer validated status")
