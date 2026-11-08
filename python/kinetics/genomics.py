"""Text SAM/VCF parsing and read-quality utilities; BAM requires a separate engine."""
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean


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
        if flag < 0 or position < 0 or not 0 <= mapq <= 255:
            raise ValueError(f"SAM line {line_number}: numeric field out of range")
        if fields[9] != "*" and fields[10] != "*" and len(fields[9]) != len(fields[10]):
            raise ValueError(f"SAM line {line_number}: sequence/quality length mismatch")
        records.append(SamRecord(fields[0], flag, fields[2], position, mapq,
                                 fields[5], fields[9], fields[10]))
    return records


def parse_vcf(text: str) -> list[dict[str, object]]:
    samples: list[str] = []
    variants: list[dict[str, object]] = []
    header_seen = False
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line or line.startswith("##"):
            continue
        if line.startswith("#CHROM"):
            samples = line.split("\t")[9:]
            header_seen = True
            continue
        if line.startswith("#"):
            continue
        if not header_seen:
            raise ValueError("VCF data encountered before #CHROM header")
        fields = line.split("\t")
        if len(fields) < 8:
            raise ValueError(f"VCF line {line_number}: expected at least 8 columns")
        try:
            position = int(fields[1])
        except ValueError as exc:
            raise ValueError(f"VCF line {line_number}: invalid POS") from exc
        if position < 1:
            raise ValueError(f"VCF line {line_number}: POS must be >=1")
        variants.append({"chrom": fields[0], "pos": position, "id": fields[2],
                         "ref": fields[3], "alt": fields[4], "qual": fields[5],
                         "filter": fields[6], "info": fields[7], "samples": samples,
                         "genotypes": fields[9:]})
    if not header_seen:
        raise ValueError("VCF #CHROM header missing")
    return variants


def fastq_quality_summary(qualities: list[str], *, offset: int = 33) -> dict[str, float | int]:
    if not qualities or offset not in (33, 64):
        raise ValueError("Provide qualities and an explicit Phred offset of 33 or 64")
    scores = [ord(char) - offset for read in qualities for char in read]
    if not scores or min(scores) < 0 or max(scores) > 93:
        raise ValueError("Quality character outside supported Phred range")
    return {"bases": len(scores), "mean_phred": mean(scores),
            "q20_fraction": sum(score >= 20 for score in scores) / len(scores),
            "q30_fraction": sum(score >= 30 for score in scores) / len(scores)}
