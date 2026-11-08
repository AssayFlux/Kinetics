from __future__ import annotations

import hashlib

import pytest

from kinetics.sequence import SequenceRecord
from kinetics.sequence_reference import ReferencePack, exact_reference_search


def pack() -> ReferencePack:
    return ReferencePack(
        name="synthetic-test-pack",
        version="1.0",
        license="CC0-1.0",
        source="https://example.org/reference-pack",
        content_sha256=hashlib.sha256(b"fixture-pack").hexdigest(),
    )


def test_exact_reference_search_emits_provenance_and_match_evidence() -> None:
    result = exact_reference_search(
        " acgt ", [SequenceRecord("ref-1", "ACGT")],
        sequence_type="DNA", reference_pack=pack(),
    )
    assert result["query"]["sequence_sha256"] == hashlib.sha256(b"ACGT").hexdigest()
    assert result["hits"][0]["identity"] == 1.0
    assert result["conclusion"]["annotation_status"] == "supported"
    assert result["conclusion"]["novelty_status"] == "not_established"
    assert result["search"]["reference_packs"][0]["license"] == "CC0-1.0"


def test_no_hit_abstains_and_never_claims_novelty() -> None:
    result = exact_reference_search(
        "ACGA", [SequenceRecord("ref-1", "ACGT")],
        sequence_type="DNA", reference_pack=pack(),
    )
    assert result["hits"] == []
    assert result["conclusion"]["annotation_status"] == "no_hit"
    assert result["conclusion"]["novelty_status"] == "not_established"
    assert len(result["conclusion"]["abstention_reasons"]) >= 1


@pytest.mark.parametrize("kwargs", [
    {"max_records": 0},
    {"max_total_residues": 0},
])
def test_search_rejects_invalid_resource_limits(kwargs: dict[str, int]) -> None:
    with pytest.raises(ValueError):
        exact_reference_search(
            "ACGT", [], sequence_type="DNA", reference_pack=pack(), **kwargs,
        )


def test_search_rejects_invalid_pack_hash_and_duplicate_reference_ids() -> None:
    bad = ReferencePack("pack", "1", "CC0", "https://example.org", "not-a-hash")
    with pytest.raises(ValueError, match="SHA-256"):
        exact_reference_search("ACGT", [], sequence_type="DNA", reference_pack=bad)
    with pytest.raises(ValueError, match="unique"):
        exact_reference_search(
            "ACGT", [SequenceRecord("dup", "ACGT"), SequenceRecord("dup", "ACGT")],
            sequence_type="DNA", reference_pack=pack(),
        )


def test_protein_exact_match_uses_protein_alphabet() -> None:
    result = exact_reference_search(
        "MKWVTF", [SequenceRecord("p1", "MKWVTF")],
        sequence_type="protein", reference_pack=pack(),
    )
    assert result["hits"][0]["evidence_type"] == "exact_sequence"
    assert result["query"]["alphabet"] == "protein"



def test_exact_reference_search_bounds_query_and_validates_integer_limits() -> None:
    from kinetics.sequence_reference import ReferencePack, exact_reference_search
    from kinetics.sequence import SequenceRecord

    pack = ReferencePack(
        name="fixture", version="1", license="CC0-1.0",
        source="https://example.org/reference",
        content_sha256="a" * 64,
    )
    refs = [SequenceRecord(identifier="r1", sequence="ATG")]
    with pytest.raises(ValueError, match="max_query_residues"):
        exact_reference_search(
            "ATGATG", refs, sequence_type="DNA", reference_pack=pack,
            max_query_residues=5,
        )
    with pytest.raises(ValueError, match="positive integer"):
        exact_reference_search(
            "ATG", refs, sequence_type="DNA", reference_pack=pack,
            max_records=True,
        )
    with pytest.raises(ValueError, match="positive integer"):
        exact_reference_search(
            "ATG", refs, sequence_type="DNA", reference_pack=pack,
            max_total_residues=1.5,
        )
