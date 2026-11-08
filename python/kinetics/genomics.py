"""Strict text SAM/VCF parsing and read-quality utilities; BAM/CRAM need native engines."""
from __future__ import annotations

import re
from dataclasses import dataclass
from math import isfinite
from statistics import mean

_CIGAR = re.compile(r"(?:[1-9][0-9]*[MIDNSHP=X])+")
_DNA_IUPAC = set("=ACMGRSVTWYHKDBN")


@dataclass(frozen=True)
class SamRecord:
    query_name: str
    flag: int
    reference: str
    position: int
    mapq: int
    cigar: str
    sequence: str
    quality: str


def parse_sam(text: str) -> list[SamRecord]:
    """Parse SAM text records and validate mandatory fields and optional tag syntax."""
    records: list[SamRecord] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line or line.startswith("@"):
            continue
        fields = line.split("\t")
        if len(fields) < 11:
            raise ValueError(f"SAM line {line_number}: expected at least 11 fields")
        try:
            flag, position, mapq = int(fields[1]), int(fields[3]), int(fields[4])
        except ValueError as exc:
            raise ValueError(f"SAM line {line_number}: invalid numeric field") from exc
        if not fields[0] or flag < 0 or flag > 65535 or position < 0 or not 0 <= mapq <= 255:
            raise ValueError(f"SAM line {line_number}: mandatory field out of range")
        cigar, sequence, quality = fields[5], fields[9], fields[10]
        if cigar != "*" and not _CIGAR.fullmatch(cigar):
            raise ValueError(f"SAM line {line_number}: malformed CIGAR")
        if (sequence == "*") != (quality == "*"):
            raise ValueError(f"SAM line {line_number}: SEQ and QUAL must both be '*' or both present")
        if sequence != "*":
            if any(base not in _DNA_IUPAC for base in sequence.upper()):
                raise ValueError(f"SAM line {line_number}: invalid SEQ symbol")
            if len(sequence) != len(quality):
                raise ValueError(f"SAM line {line_number}: sequence/quality length mismatch")
            if any(not 33 <= ord(char) <= 126 for char in quality):
                raise ValueError(f"SAM line {line_number}: invalid QUAL character")
        for tag in fields[11:]:
            parts = tag.split(":", 2)
            if len(parts) != 3 or not re.fullmatch(r"[A-Za-z][A-Za-z0-9]", parts[0]):
                raise ValueError(f"SAM line {line_number}: malformed optional tag")
            if parts[1] not in {"A", "i", "f", "Z", "H", "B"}:
                raise ValueError(f"SAM line {line_number}: unsupported optional tag type")
            if parts[1] == "f":
                try:
                    number = float(parts[2])
                except ValueError as exc:
                    raise ValueError(f"SAM line {line_number}: invalid float tag") from exc
                if not isfinite(number):
                    raise ValueError(f"SAM line {line_number}: non-finite float tag")
        records.append(SamRecord(fields[0], flag, fields[2], position, mapq,
                                 cigar, sequence, quality))
    return records


def parse_vcf(text: str) -> list[dict[str, object]]:
    """Parse VCF tabular records with header/column and core scalar validation."""
    header: list[str] | None = None
    variants: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line:
            continue
        if line.startswith("##"):
            continue
        if line.startswith("#CHROM"):
            if header is not None:
                raise ValueError("VCF contains more than one #CHROM header")
            header = line.split("\t")
            if len(header) < 8 or header[:8] != [
                "#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"
            ]:
                raise ValueError("VCF #CHROM header has invalid mandatory columns")
            if len(header) == 9:
                raise ValueError("VCF FORMAT column requires at least one sample column")
            if len(header) > 9 and header[8] != "FORMAT":
                raise ValueError("VCF ninth column must be FORMAT when samples are present")
            if len(set(header[9:])) != len(header[9:]):
                raise ValueError("VCF sample names must be unique")
            continue
        if line.startswith("#"):
            continue
        if header is None:
            raise ValueError("VCF data encountered before #CHROM header")
        fields = line.split("\t")
        if len(fields) != len(header):
            raise ValueError(
                f"VCF line {line_number}: expected {len(header)} columns, found {len(fields)}"
            )
        try:
            position = int(fields[1])
        except ValueError as exc:
            raise ValueError(f"VCF line {line_number}: invalid POS") from exc
        if position < 1 or not fields[0] or not fields[3] or not fields[4]:
            raise ValueError(f"VCF line {line_number}: invalid CHROM, POS, REF or ALT")
        if fields[5] != ".":
            try:
                quality = float(fields[5])
            except ValueError as exc:
                raise ValueError(f"VCF line {line_number}: invalid QUAL") from exc
            if not isfinite(quality) or quality < 0:
                raise ValueError(f"VCF line {line_number}: QUAL must be finite and non-negative")
        samples = header[9:]
        genotypes = fields[9:]
        if samples and (not fields[8] or any(not value for value in genotypes)):
            raise ValueError(f"VCF line {line_number}: FORMAT/sample value is empty")
        variants.append({
            "chrom": fields[0], "pos": position, "id": fields[2], "ref": fields[3],
            "alt": fields[4], "qual": fields[5], "filter": fields[6], "info": fields[7],
            "samples": samples, "format": fields[8] if samples else None,
            "genotypes": genotypes,
        })
    if header is None:
        raise ValueError("VCF #CHROM header missing")
    return variants


def fastq_quality_summary(qualities: list[str], *, offset: int = 33) -> dict[str, float | int]:
    if not qualities or offset not in (33, 64):
        raise ValueError("Provide qualities and an explicit Phred offset of 33 or 64")
    scores = [ord(char) - offset for read in qualities for char in read]
    if not scores or min(scores) < 0 or max(scores) > 93:
        raise ValueError("Quality character outside supported Phred range")
    return {
        "bases": len(scores), "mean_phred": mean(scores),
        "q20_fraction": sum(score >= 20 for score in scores) / len(scores),
        "q30_fraction": sum(score >= 30 for score in scores) / len(scores),
    }

def normalize_small_variant(
    chrom: str, position: int, ref: str, alt: str, reference_sequence: str,
) -> dict[str, object]:
    """Validate and left-normalize one biallelic small variant against a reference.

    Coordinates are 1-based. Only literal A/C/G/T alleles are accepted; symbolic,
    spanning-deletion, breakend and multi-allelic records require dedicated handling.
    This helper does not perform transcript mapping or variant interpretation.
    """
    if not chrom or position < 1:
        raise ValueError("Chromosome and positive 1-based position are required")
    reference = reference_sequence.upper()
    ref_allele, alt_allele = ref.upper(), alt.upper()
    if not reference or any(base not in "ACGTN" for base in reference):
        raise ValueError("Reference sequence must contain only A/C/G/T/N")
    if not ref_allele or not alt_allele or any(
        base not in "ACGT" for base in ref_allele + alt_allele
    ):
        raise ValueError("REF and ALT must be non-empty literal A/C/G/T alleles")
    if ref_allele == alt_allele:
        raise ValueError("REF and ALT must differ")
    start = position - 1
    end = start + len(ref_allele)
    if end > len(reference):
        raise ValueError("Variant REF extends beyond supplied reference sequence")
    if reference[start:end] != ref_allele:
        raise ValueError("Variant REF does not match supplied reference sequence")

    # Trim shared suffix and prefix while preserving an anchor base in each allele.
    while len(ref_allele) > 1 and len(alt_allele) > 1 and ref_allele[-1] == alt_allele[-1]:
        ref_allele, alt_allele = ref_allele[:-1], alt_allele[:-1]
    while len(ref_allele) > 1 and len(alt_allele) > 1 and ref_allele[0] == alt_allele[0]:
        ref_allele, alt_allele = ref_allele[1:], alt_allele[1:]
        start += 1

    # For repeat-associated indels, rotate the anchored alleles left across
    # matching preceding reference bases. Re-check the reference at every step.
    if len(ref_allele) != len(alt_allele):
        while start > 0 and ref_allele[-1] == alt_allele[-1]:
            previous = reference[start - 1]
            if previous != ref_allele[-1]:
                break
            ref_allele = previous + ref_allele[:-1]
            alt_allele = previous + alt_allele[:-1]
            start -= 1

    return {
        "chrom": chrom,
        "pos": start + 1,
        "ref": ref_allele,
        "alt": alt_allele,
        "normalization": "minimal-left-aligned-biallelic-small-variant",
        "reference_checked": True,
    }

