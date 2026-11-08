from __future__ import annotations

import hashlib
import json

import pytest

from kinetics.sequence_pack import (
    load_local_fasta_reference_pack,
    search_local_fasta_reference,
)


def write_pack(tmp_path, fasta: bytes, **overrides):
    fasta_path = tmp_path / "reference.fasta"
    manifest_path = tmp_path / "manifest.json"
    fasta_path.write_bytes(fasta)
    manifest = {
        "schema_version": 1,
        "name": "synthetic",
        "version": "1.0",
        "license": "CC0-1.0",
        "source": "https://example.org/reference",
        "sequence_type": "DNA",
        "format": "fasta",
        "content_sha256": hashlib.sha256(fasta).hexdigest(),
    }
    manifest.update(overrides)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return fasta_path, manifest_path


def test_local_pack_verifies_bytes_and_loads_records(tmp_path) -> None:
    fasta = b">gene-a example\nACGT\n>gene-b\nTTAA\n"
    fasta_path, manifest_path = write_pack(tmp_path, fasta)
    loaded = load_local_fasta_reference_pack(fasta_path, manifest_path)
    assert loaded.metadata.content_sha256 == hashlib.sha256(fasta).hexdigest()
    assert loaded.sequence_type == "DNA"
    assert [(record.identifier, record.sequence) for record in loaded.records] == [
        ("gene-a", "ACGT"), ("gene-b", "TTAA"),
    ]


def test_local_pack_rejects_hash_mismatch(tmp_path) -> None:
    fasta_path, manifest_path = write_pack(tmp_path, b">gene\nACGT\n")
    fasta_path.write_bytes(b">gene\nTGCA\n")
    with pytest.raises(ValueError, match="SHA-256"):
        load_local_fasta_reference_pack(fasta_path, manifest_path)


@pytest.mark.parametrize("overrides, message", [
    ({"license": ""}, "non-empty"),
    ({"sequence_type": "unknown"}, "sequence_type"),
    ({"format": "genbank"}, "FASTA"),
    ({"unexpected": True}, "keys mismatch"),
])
def test_manifest_rejects_invalid_metadata(tmp_path, overrides, message) -> None:
    fasta_path, manifest_path = write_pack(tmp_path, b">gene\nACGT\n", **overrides)
    with pytest.raises(ValueError, match=message):
        load_local_fasta_reference_pack(fasta_path, manifest_path)


def test_local_pack_enforces_record_residue_and_byte_limits(tmp_path) -> None:
    fasta_path, manifest_path = write_pack(
        tmp_path, b">a\nACGT\n>b\nTTAA\n",
    )
    with pytest.raises(ValueError, match="max_records"):
        load_local_fasta_reference_pack(fasta_path, manifest_path, max_records=1)
    with pytest.raises(ValueError, match="max_total_residues"):
        load_local_fasta_reference_pack(
            fasta_path, manifest_path, max_total_residues=7,
        )
    with pytest.raises(ValueError, match="max_pack_bytes"):
        load_local_fasta_reference_pack(fasta_path, manifest_path, max_pack_bytes=2)


def test_local_pack_rejects_duplicate_ids_invalid_alphabet_and_symlinks(tmp_path) -> None:
    fasta_path, manifest_path = write_pack(tmp_path, b">same\nACGT\n>same\nTTAA\n")
    with pytest.raises(ValueError, match="unique"):
        load_local_fasta_reference_pack(fasta_path, manifest_path)

    fasta_path, manifest_path = write_pack(tmp_path, b">gene\nACGU\n")
    with pytest.raises(ValueError, match="Invalid symbols"):
        load_local_fasta_reference_pack(fasta_path, manifest_path)

    link_path = tmp_path / "linked.fasta"
    link_path.symlink_to(fasta_path)
    with pytest.raises(ValueError, match="symbolic link"):
        load_local_fasta_reference_pack(link_path, manifest_path)



def test_local_pack_search_verifies_pack_and_returns_exact_evidence(tmp_path) -> None:
    fasta_path, manifest_path = write_pack(tmp_path, b">gene-a\nACGT\n")
    result = search_local_fasta_reference("ACGT", fasta_path, manifest_path)
    assert result["hits"][0]["reference_id"] == "gene-a"
    assert result["conclusion"]["novelty_status"] == "not_established"
    assert result["search"]["reference_packs"][0]["content_sha256"] == hashlib.sha256(
        b">gene-a\nACGT\n"
    ).hexdigest()
