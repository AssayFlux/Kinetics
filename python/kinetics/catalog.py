"""Source-attributed, expandable ingestion of the full NCBI Gene gene_info schema."""
from __future__ import annotations

import gzip
from dataclasses import dataclass
from pathlib import Path
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
    locus_tag: str = ""
    dbxrefs: tuple[str, ...] = ()
    chromosome: str = ""
    map_location: str = ""
    gene_type: str = ""
    nomenclature_symbol: str = ""
    nomenclature_full_name: str = ""
    nomenclature_status: str = ""
    other_designations: tuple[str, ...] = ()
    modification_date: str = ""
    feature_type: str = ""


def _split_pipe(value: str) -> tuple[str, ...]:
    return tuple(sorted({item for item in value.split("|") if item not in {"", "-"}}))


def iter_ncbi_gene_info(lines: Iterable[str], *, source_release: str) -> Iterator[GeneEntry]:
    """Stream all 16 NCBI gene_info columns; data remains source/release attributed."""
    if not source_release.strip():
        raise ValueError("Pin the NCBI gene_info release/date before import")
    for line_number, raw in enumerate(lines, 1):
        line = raw.rstrip("\r\n")
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) < 16:
            raise ValueError(f"gene_info line {line_number}: expected all 16 NCBI columns")
        (
            tax_id, gene_id, symbol, locus_tag, synonyms, dbxrefs, chromosome,
            map_location, description, gene_type, nomenclature_symbol,
            nomenclature_full_name, nomenclature_status, other_designations,
            modification_date, feature_type,
        ) = fields[:16]
        if not tax_id.isdigit() or not gene_id.isdigit() or not symbol or symbol == "-":
            raise ValueError(f"gene_info line {line_number}: invalid tax_id, GeneID or symbol")
        if modification_date and (len(modification_date) != 8 or not modification_date.isdigit()):
            raise ValueError(f"gene_info line {line_number}: invalid modification date")
        yield GeneEntry(
            tax_id=tax_id,
            gene_id=gene_id,
            symbol=symbol,
            description="" if description == "-" else description,
            synonyms=_split_pipe(synonyms),
            source="NCBI Gene gene_info",
            source_release=source_release,
            locus_tag="" if locus_tag == "-" else locus_tag,
            dbxrefs=_split_pipe(dbxrefs),
            chromosome="" if chromosome == "-" else chromosome,
            map_location="" if map_location == "-" else map_location,
            gene_type="" if gene_type == "-" else gene_type,
            nomenclature_symbol="" if nomenclature_symbol == "-" else nomenclature_symbol,
            nomenclature_full_name="" if nomenclature_full_name == "-" else nomenclature_full_name,
            nomenclature_status="" if nomenclature_status == "-" else nomenclature_status,
            other_designations=_split_pipe(other_designations),
            modification_date=modification_date,
            feature_type="" if feature_type == "-" else feature_type,
        )


def validate_gene_catalog(entries: Iterable[GeneEntry]) -> None:
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        if not all((
            entry.tax_id.isdigit(), entry.gene_id.isdigit(), entry.symbol,
            entry.source, entry.source_release,
        )):
            raise ValueError("Gene entries require valid tax_id, GeneID, symbol, source and release")
        key = (entry.tax_id, entry.gene_id)
        if key in seen:
            raise ValueError(f"Duplicate NCBI gene entry: {entry.tax_id}:{entry.gene_id}")
        seen.add(key)
        if entry.evidence_status not in {"catalogued", "prioritised", "implemented", "validated"}:
            raise ValueError(f"Unknown evidence status: {entry.evidence_status}")
        if entry.evidence_status == "validated":
            raise ValueError("A catalogue import cannot confer validated status")


def iter_ncbi_gene_info_file(
    path: str | Path, *, source_release: str,
) -> Iterator[GeneEntry]:
    """Stream plain or gzip-compressed NCBI gene_info without loading it into memory."""
    source = Path(path)
    if source.suffix.lower() == ".gz":
        with gzip.open(source, "rt", encoding="utf-8", newline="") as handle:
            yield from iter_ncbi_gene_info(handle, source_release=source_release)
    else:
        with source.open("rt", encoding="utf-8", newline="") as handle:
            yield from iter_ncbi_gene_info(handle, source_release=source_release)
