from __future__ import annotations

import pytest

from kinetics.genomics import fastq_quality_summary, parse_sam, parse_vcf


def test_sam_parses_valid_record_and_optional_tag() -> None:
    rows = parse_sam("read1\t0\tchr1\t1\t60\t4M\t*\t0\t0\tACGT\t!!!!\tNM:i:0")
    assert len(rows) == 1
    assert rows[0].query_name == "read1"
    assert rows[0].cigar == "4M"


@pytest.mark.parametrize(
    "record",
    [
        "read1\t65536\tchr1\t1\t60\t4M\t*\t0\t0\tACGT\t!!!!",
        "read1\t0\tchr1\t1\t60\t4Q\t*\t0\t0\tACGT\t!!!!",
        "read1\t0\tchr1\t1\t60\t4M\t*\t0\t0\tACGT\t!!!",
        "read1\t0\tchr1\t1\t60\t4M\t*\t0\t0\tACGT\t!!!!\tNM:x:0",
    ],
)
def test_sam_rejects_malformed_records(record: str) -> None:
    with pytest.raises(ValueError):
        parse_sam(record)


def test_vcf_parses_header_and_sample_columns() -> None:
    text = (
        "##fileformat=VCFv4.3\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\n"
        "chr1\t10\t.\tA\tG\t50\tPASS\t.\tGT\t0/1\n"
    )
    result = parse_vcf(text)
    assert result[0]["pos"] == 10
    assert result[0]["samples"] == ["S1"]
    assert result[0]["genotypes"] == ["0/1"]


@pytest.mark.parametrize(
    "text",
    [
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\nchr1\t0\t.\tA\tG\t.\tPASS\t.\n",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\nchr1\t1\t.\tA\tG\tNaN\tPASS\t.\n",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\nchr1\t1\t.\tA\tG\t.\tPASS\t.\textra\n",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\nchr1\t1\t.\tA\tG\t.\tPASS\t.\tGT\n",
    ],
)
def test_vcf_rejects_invalid_position_quality_and_column_counts(text: str) -> None:
    with pytest.raises(ValueError):
        parse_vcf(text)


def test_fastq_quality_summary_requires_explicit_supported_offset() -> None:
    assert fastq_quality_summary(["IIII"], offset=33)["mean_phred"] == 40
    with pytest.raises(ValueError):
        fastq_quality_summary(["IIII"], offset=0)
