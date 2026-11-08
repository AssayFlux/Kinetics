"""Deterministic, exact-only local reference search for S6 triage.

This is a bounded evidence-producing primitive, not BLAST/HMMER, a gene caller,
or a calibrated homology/family classifier. A no-hit is never novelty evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO, TextIOWrapper
from hashlib import sha256
from typing import Iterable, Literal
from urllib.parse import urlparse

from kinetics.sequence import DNA, PROTEIN, RNA, SequenceRecord, iter_fasta_records, validate_sequence

SequenceType = Literal["DNA", "RNA", "protein"]


@dataclass(frozen=True)
class ReferencePack:
    name: str
    version: str
    license: str
    source: str
    content_sha256: str

    def validate(self) -> None:
        if not all(isinstance(value, str) and value.strip() for value in (
            self.name, self.version, self.license, self.source, self.content_sha256
        )):
            raise ValueError("Reference pack metadata fields must be non-empty strings")
        parsed = urlparse(self.source)
        if parsed.scheme not in {"https", "http", "doi"}:
            raise ValueError("Reference pack source must be an http(s) or doi URI")
        if len(self.content_sha256) != 64 or any(
            char not in "0123456789abcdef" for char in self.content_sha256
        ):
            raise ValueError("Reference pack content_sha256 must be lowercase SHA-256 hex")


def _alphabet(sequence_type: SequenceType) -> frozenset[str]:
    return {"DNA": DNA, "RNA": RNA, "protein": PROTEIN}[sequence_type]


def _normalise(sequence: str) -> str:
    return "".join(sequence.split()).upper()


def exact_reference_search(
    query: str,
    references: Iterable[SequenceRecord],
    *,
    sequence_type: SequenceType,
    reference_pack: ReferencePack,
    max_records: int = 100_000,
    max_total_residues: int = 50_000_000,
    max_query_residues: int = 5_000_000,
) -> dict[str, object]:
    """Return exact full-length matches and a provenance-complete abstaining result."""
    reference_pack.validate()
    if sequence_type not in ("DNA", "RNA", "protein"):
        raise ValueError("sequence_type must be DNA, RNA, or protein")
    normalized_query = _normalise(query)
    if not normalized_query:
        raise ValueError("Query sequence must not be empty")
    validate_sequence(normalized_query, _alphabet(sequence_type))
    limits = {
        "max_records": max_records,
        "max_total_residues": max_total_residues,
        "max_query_residues": max_query_residues,
    }
    for name, value in limits.items():
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if len(normalized_query) > max_query_residues:
        raise ValueError("Query sequence exceeds max_query_residues limit")

    query_hash = sha256(normalized_query.encode("ascii")).hexdigest()
    hits: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    record_count = 0
    total_residues = 0
    for record in references:
        record_count += 1
        if record_count > max_records:
            raise ValueError("Reference pack exceeds max_records limit")
        if not record.identifier or record.identifier in seen_ids:
            raise ValueError("Reference identifiers must be non-empty and unique")
        seen_ids.add(record.identifier)
        target = _normalise(record.sequence)
        if not target:
            raise ValueError(f"Reference {record.identifier!r} has an empty sequence")
        validate_sequence(target, _alphabet(sequence_type))
        total_residues += len(target)
        if total_residues > max_total_residues:
            raise ValueError("Reference pack exceeds max_total_residues limit")
        if target == normalized_query:
            hits.append({
                "reference_id": record.identifier,
                "identity": 1.0,
                "query_coverage": 1.0,
                "reference_coverage": 1.0,
                "score": float(len(normalized_query)),
                "evalue": None,
                "evidence_type": "exact_sequence",
                "source_coordinates": None,
            })

    return {
        "schema_version": 1,
        "query": {
            "sequence_sha256": query_hash,
            "length": len(normalized_query),
            "alphabet": sequence_type,
            "sequence_type": {
                "DNA": "gene", "RNA": "transcript", "protein": "protein"
            }[sequence_type],
        },
        "search": {
            "algorithm": "exact-full-length-match-v1",
            "parameters": {
                "case_normalization": "uppercase",
                "whitespace": "removed",
                "partial_matches": False,
                "similarity_search": False,
                "max_records": max_records,
                "max_total_residues": max_total_residues,
                "max_query_residues": max_query_residues,
            },
            "reference_packs": [{
                "name": reference_pack.name,
                "version": reference_pack.version,
                "license": reference_pack.license,
                "source": reference_pack.source,
                "content_sha256": reference_pack.content_sha256,
            }],
        },
        "hits": hits,
        "conclusion": {
            "annotation_status": "supported" if hits else "no_hit",
            "novelty_status": "not_established",
            "confidence": "not_calibrated",
            "abstention_reasons": [] if hits else [
                "No exact full-length match in the supplied reference pack",
                "Similarity, homology, family and domain searches were not performed",
                "Reference-pack scope and completeness are not established",
            ],
        },
        "limitations": [
            "Exact full-length matching only; no local alignment or homology inference",
            "A no-hit result is not evidence that a sequence is novel",
            "No gene function, protein function, pathogenicity or clinical interpretation",
            "Reference pack license, version and hash are caller-supplied and must be independently verified",
        ],
    }



def exact_reference_search_fasta(
    query: str,
    fasta_bytes: bytes,
    *,
    sequence_type: SequenceType,
    reference_pack: ReferencePack,
    max_fasta_bytes: int = 512 * 1024 * 1024,
    max_records: int = 100_000,
    max_total_residues: int = 50_000_000,
    max_query_residues: int = 5_000_000,
) -> dict[str, object]:
    """Verify exact FASTA bytes against pack provenance, then search records.

    The byte digest is computed from the supplied raw payload before UTF-8
    decoding. FASTA records are parsed incrementally; no homology or novelty
    inference is performed. The caller remains responsible for acquiring the
    bytes under the source's licence and pinning the correct release.
    """
    reference_pack.validate()
    if not isinstance(fasta_bytes, bytes):
        raise TypeError("fasta_bytes must be bytes")
    if (
        not isinstance(max_fasta_bytes, int)
        or isinstance(max_fasta_bytes, bool)
        or max_fasta_bytes < 1
    ):
        raise ValueError("max_fasta_bytes must be a positive integer")
    if len(fasta_bytes) > max_fasta_bytes:
        raise ValueError("FASTA payload exceeds max_fasta_bytes limit")
    actual_sha256 = sha256(fasta_bytes).hexdigest()
    if actual_sha256 != reference_pack.content_sha256:
        raise ValueError("FASTA payload SHA-256 does not match reference-pack metadata")
    try:
        stream = TextIOWrapper(BytesIO(fasta_bytes), encoding="utf-8", errors="strict")
        records = iter_fasta_records(stream)
        return exact_reference_search(
            query,
            records,
            sequence_type=sequence_type,
            reference_pack=reference_pack,
            max_records=max_records,
            max_total_residues=max_total_residues,
            max_query_residues=max_query_residues,
        )
    except UnicodeDecodeError as exc:
        raise ValueError("FASTA payload must be valid UTF-8 text") from exc
