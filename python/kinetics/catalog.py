"""Versioned, source-attributed gene catalogue; presence never implies tool validation."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class GeneEntry:
    symbol:str
    organism:str
    domains:tuple[str,...]
    source:str
    source_release:str
    evidence_status:str="catalogued"
    notes:str=""

def validate_gene_catalog(entries:list[GeneEntry]) -> None:
    seen=set()
    for entry in entries:
        key=(entry.organism.casefold(),entry.symbol.upper())
        if not entry.symbol or not entry.organism or not entry.source or not entry.source_release:
            raise ValueError("Gene entries require symbol, organism, source and source release")
        if key in seen: raise ValueError(f"Duplicate gene entry: {entry.organism}:{entry.symbol}")
        seen.add(key)
        if entry.evidence_status not in {"catalogued","prioritised","implemented","validated"}:
            raise ValueError(f"Unknown evidence status: {entry.evidence_status}")
        if entry.evidence_status=="validated":
            raise ValueError("Validation status requires a linked validation record; use registry evidence workflow")
