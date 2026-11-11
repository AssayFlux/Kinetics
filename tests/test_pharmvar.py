from __future__ import annotations

import hashlib

import pytest

from kinetics.pharmvar import match_pharmvar_haplotype, parse_pharmvar_tsv

TSV = (
    "Haplotype Identifier\tGene Symbol\tdbSNP rsID\tReference Sequence\t"
    "Variant Start\tVariant Stop\tReference Allele\tVariant Allele\t"
    "Variant Type\n"
    "*1\tSYN1\t.\tNG_SYNTHETIC.1\t0\t0\tREFERENCE\t.\treference\n"
    "*2\tSYN1\trsSynthetic1\tNG_SYNTHETIC.1\t2\t2\tA\tG\tsnv\n"
)


def defs():
    return parse_pharmvar_tsv(
        TSV,
        source_release="fixture-1",
        source_url="https://example.invalid/source",
        source_sha256=hashlib.sha256(TSV.encode()).hexdigest(),
        license_id="CC0 synthetic test only",
        expected_release="fixture-1",
    )


def test_pharmvar_exact_byte_digest_and_accession_preservation():
    definitions = defs()
    assert len(definitions) == 2 and definitions[0].is_reference
    assert next(iter(definitions[1].variants)).reference_accession == "NG_SYNTHETIC.1"


def test_pharmvar_exact_haplotype_match_and_unphased_abstention():
    definitions = defs()
    variant = next(iter(definitions[1].variants))
    matched = match_pharmvar_haplotype(
        "SYN1",
        "NG_SYNTHETIC.1",
        [variant],
        definitions,
        phase_confirmed=True,
        call_complete=True,
    )
    assert matched.status == "matched" and matched.haplotype == "*2"
    unphased = match_pharmvar_haplotype(
        "SYN1",
        "NG_SYNTHETIC.1",
        [variant],
        definitions,
        phase_confirmed=False,
        call_complete=True,
    )
    assert unphased.status == "no_call_unphased" and unphased.haplotype is None


def test_pharmvar_rejects_digest_release_and_accession_mismatch():
    digest = hashlib.sha256(TSV.encode()).hexdigest()
    with pytest.raises(ValueError, match="checksum"):
        parse_pharmvar_tsv(
            TSV,
            source_release="fixture-1",
            source_url="https://example.invalid/source",
            source_sha256="0" * 64,
            license_id="test",
            expected_release="fixture-1",
        )
    with pytest.raises(ValueError, match="release"):
        parse_pharmvar_tsv(
            TSV,
            source_release="fixture-1",
            source_url="https://example.invalid/source",
            source_sha256=digest,
            license_id="test",
            expected_release="fixture-2",
        )
    with pytest.raises(ValueError, match="different reference accession"):
        match_pharmvar_haplotype(
            "SYN1",
            "OTHER",
            [next(iter(defs()[1].variants))],
            defs(),
            phase_confirmed=True,
            call_complete=True,
        )
