"""Strict text SAM/VCF parsing and read-quality utilities; BAM/CRAM need native engines."""
from __future__ import annotations

import re
from dataclasses import dataclass
from math import isfinite
from statistics import mean
from typing import BinaryIO, Iterator

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
        if sequence == "*" and quality != "*":
            raise ValueError(f"SAM line {line_number}: QUAL must be '*' when SEQ is unavailable")
        if sequence != "*":
            if any(base not in _DNA_IUPAC for base in sequence.upper()):
                raise ValueError(f"SAM line {line_number}: invalid SEQ symbol")
            if quality != "*" and len(sequence) != len(quality):
                raise ValueError(f"SAM line {line_number}: sequence/quality length mismatch")
            if quality != "*" and any(not 33 <= ord(char) <= 126 for char in quality):
                raise ValueError(f"SAM line {line_number}: invalid QUAL character")
            if cigar != "*":
                query_length = sum(
                    int(length) for length, operation in re.findall(r"([1-9][0-9]*)([MIDNSHP=X])", cigar)
                    if operation in {"M", "I", "S", "=", "X"}
                )
                if query_length != len(sequence):
                    raise ValueError(f"SAM line {line_number}: CIGAR query length does not match SEQ")
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
            # Remove the shared right anchor, then prepend the preceding
            # reference base. This permits shifting out of a repeat tract
            # to its left-most valid VCF representation.
            ref_allele = ref_allele[:-1]
            alt_allele = alt_allele[:-1]
            previous = reference[start - 1]
            ref_allele = previous + ref_allele
            alt_allele = previous + alt_allele
            start -= 1

    return {
        "chrom": chrom,
        "pos": start + 1,
        "ref": ref_allele,
        "alt": alt_allele,
        "normalization": "minimal-left-aligned-biallelic-small-variant",
        "reference_checked": True,
    }

def iter_bam_records(
    source: BinaryIO, *, max_records: int = 10_000_000,
    max_total_bases: int = 500_000_000,
    max_header_bytes: int = 64 * 1024 * 1024,
) -> Iterator[SamRecord]:
    """Lazily decode core BAM fields under explicit record/base resource limits.

    BGZF is a concatenated gzip format, so Python's gzip reader handles its block
    stream. Auxiliary tags are deliberately skipped, and CRAM is not supported.
    The caller owns the binary source stream. Limits count decoded records and
    query bases across the entire stream; exceeding either raises ValueError.
    """

    import gzip
    import struct
    if not hasattr(source, "read"):
        raise TypeError("BAM source must be an open binary stream")
    if (
        isinstance(max_records, bool) or not isinstance(max_records, int)
        or max_records <= 0
    ):
        raise ValueError("max_records must be a positive integer")
    if (
        isinstance(max_total_bases, bool) or not isinstance(max_total_bases, int)
        or max_total_bases <= 0
    ):
        raise ValueError("max_total_bases must be a positive integer")
    if (
        isinstance(max_header_bytes, bool) or not isinstance(max_header_bytes, int)
        or max_header_bytes <= 0
    ):
        raise ValueError("max_header_bytes must be a positive integer")
    stream = gzip.GzipFile(fileobj=source, mode="rb")
    if stream.read(4) != b"BAM\x01":
        raise ValueError("Invalid BAM magic; input must be BGZF-compressed BAM")
    raw = stream.read(4)
    if len(raw) != 4:
        raise ValueError("Truncated BAM header text length")
    text_length = struct.unpack("<i", raw)[0]
    if text_length < 0 or text_length > max_header_bytes:
        raise ValueError("BAM header text length outside configured max_header_bytes")
    header_bytes = text_length
    header_text = stream.read(text_length)
    if len(header_text) != text_length:
        raise ValueError("Truncated BAM header text")
    raw = stream.read(4)
    if len(raw) != 4:
        raise ValueError("Truncated BAM reference count")
    reference_count = struct.unpack("<i", raw)[0]
    if not 0 <= reference_count <= 1_000_000:
        raise ValueError("BAM reference count outside supported bounds")
    references: list[str] = []
    for _ in range(reference_count):
        raw = stream.read(4)
        if len(raw) != 4:
            raise ValueError("Truncated BAM reference name length")
        name_length = struct.unpack("<i", raw)[0]
        if not 2 <= name_length <= 1_000_000:
            raise ValueError("Invalid BAM reference name length")
        if name_length + 4 > max_header_bytes - header_bytes:
            raise ValueError("BAM reference dictionary exceeds configured max_header_bytes")
        header_bytes += name_length + 8
        name = stream.read(name_length)
        raw = stream.read(4)
        if len(name) != name_length or name[-1:] != b"\x00" or len(raw) != 4:
            raise ValueError("Truncated or malformed BAM reference entry")
        references.append(name[:-1].decode("utf-8", errors="strict"))
        reference_length = struct.unpack("<i", raw)[0]
        if reference_length < 0:
            raise ValueError("Negative BAM reference length")

    sequence_codes = "=ACMGRSVTWYHKDBN"
    cigar_codes = "MIDNSHP=X"
    record_count = 0
    total_bases = 0
    while True:
        raw = stream.read(4)
        if not raw:
            return
        if len(raw) != 4:
            raise ValueError("Truncated BAM record block size")
        block_size = struct.unpack("<i", raw)[0]
        if block_size < 32 or block_size > 64 * 1024 * 1024:
            raise ValueError("BAM record block size outside supported bounds")
        block = stream.read(block_size)
        if len(block) != block_size:
            raise ValueError("Truncated BAM record block")
        ref_id, pos, bin_mq_nl, flag_nc, sequence_length, _next_ref, _next_pos, _template_length = (
            struct.unpack_from("<iiIIiiii", block, 0)
        )
        name_length = bin_mq_nl & 0xFF
        mapq = (bin_mq_nl >> 8) & 0xFF
        cigar_count = flag_nc & 0xFFFF
        flag = (flag_nc >> 16) & 0xFFFF
        if name_length < 2 or sequence_length < 0:
            raise ValueError("Invalid BAM query name or sequence length")
        if record_count >= max_records:
            raise ValueError("BAM record count exceeds configured max_records")
        if sequence_length > max_total_bases - total_bases:
            raise ValueError("BAM query bases exceed configured max_total_bases")
        cursor = 32
        if cursor + name_length > block_size:
            raise ValueError("BAM query name exceeds record block")
        query_name_raw = block[cursor:cursor + name_length]
        cursor += name_length
        if query_name_raw[-1:] != b"\x00":
            raise ValueError("BAM query name is not NUL-terminated")
        query_name = query_name_raw[:-1].decode("utf-8", errors="strict")

        cigar_end = cursor + 4 * cigar_count
        if cigar_end > block_size:
            raise ValueError("BAM CIGAR exceeds record block")
        cigar_parts = []
        query_consumption = 0
        for index in range(cigar_count):
            encoded = struct.unpack_from("<I", block, cursor + index * 4)[0]
            length, operation_code = encoded >> 4, encoded & 0xF
            if length <= 0 or operation_code >= len(cigar_codes):
                raise ValueError("Invalid BAM CIGAR operation")
            operation = cigar_codes[operation_code]
            cigar_parts.append(str(length) + operation)
            if operation in "MIS=X":
                query_consumption += length
        cursor = cigar_end

        packed_length = (sequence_length + 1) // 2
        if cursor + packed_length + sequence_length > block_size:
            raise ValueError("BAM sequence/quality exceeds record block")
        packed = block[cursor:cursor + packed_length]
        cursor += packed_length
        sequence = "".join(
            sequence_codes[(packed[i // 2] >> (4 if i % 2 == 0 else 0)) & 0xF]
            for i in range(sequence_length)
        )
        qualities = block[cursor:cursor + sequence_length]
        if qualities and all(value == 0xFF for value in qualities):
            quality = "*"
        elif any(value == 0xFF or value > 93 for value in qualities):
            raise ValueError("Invalid BAM Phred quality array")
        else:
            quality = "".join(chr(value + 33) for value in qualities)
        if cigar_parts and query_consumption != sequence_length:
            raise ValueError("BAM CIGAR query length does not match sequence length")
        if ref_id < -1 or ref_id >= len(references):
            raise ValueError("BAM reference ID outside header dictionary")
        if ref_id >= 0 and pos < 0:
            raise ValueError("Mapped BAM record has negative position")
        record_count += 1
        total_bases += sequence_length
        yield SamRecord(
            query_name, flag, references[ref_id] if ref_id >= 0 else "*",
            pos + 1 if pos >= 0 else 0, mapq,
            "".join(cigar_parts) if cigar_parts else "*", sequence or "*", quality,
        )

