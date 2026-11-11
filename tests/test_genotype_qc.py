from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from kinetics.genotype_qc import aggregate_synthetic_vcf_qc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (ROOT / "api" / "synthetic-genotype-qc.schema.json").read_text(encoding="utf-8")
)

VCF = """##fileformat=VCFv4.3
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYN_A\tSYN_B\tSYN_C
chrSynthetic1\t2\t.\tA\tG\t60\tPASS\t.\tGT:GQ\t0/1:99\t1|1:80\t./.:.
chrSynthetic1\t5\t.\tC\tT,G\t50\tPASS\t.\tGT\t0/2\t0/0\t1/2
"""


def _run(document: str = VCF) -> dict:
    return aggregate_synthetic_vcf_qc(
        document,
        fixture_id="tiny-synthetic-cohort",
        data_classification="public_non_patient_synthetic",
    )


def test_synthetic_vcf_qc_returns_aggregate_only_and_valid_schema() -> None:
    result = _run()
    Draft202012Validator.check_schema(SCHEMA)
    Draft202012Validator(SCHEMA).validate(result)
    assert result["sample_count"] == 3
    assert result["variant_count"] == 2
    assert result["variants"][0]["called_sample_count"] == 2
    assert result["variants"][0]["missing_sample_count"] == 1
    assert result["variants"][0]["heterozygous_sample_count"] == 1
    assert result["variants"][0]["alternate_allele_count"] == 3
    assert result["variants"][1]["alternate_allele_count"] == 3
    assert "samples" not in result
    assert all("genotypes" not in variant for variant in result["variants"])


def test_qc_digest_is_deterministic_and_changes_with_input() -> None:
    first = _run()
    second = _run()
    changed = _run(VCF.replace("60", "61", 1))
    assert first["input_sha256"] == second["input_sha256"]
    assert first["input_sha256"] != changed["input_sha256"]


def test_rejects_non_synthetic_classification_and_bad_fixture_id() -> None:
    with pytest.raises(ValueError, match="Only explicitly synthetic"):
        aggregate_synthetic_vcf_qc(
            VCF, fixture_id="fixture", data_classification="public_non_patient"
        )
    with pytest.raises(ValueError, match="kebab-case"):
        aggregate_synthetic_vcf_qc(
            VCF, fixture_id="Not Valid", data_classification="public_non_patient_synthetic"
        )


@pytest.mark.parametrize(
    "document, message",
    [
        (VCF.replace("0/1:99", "0/3:99"), "exceeds ALT count"),
        (VCF.replace("0/1:99", "x/.:99"), "malformed genotype allele index"),
        (VCF.replace("0/1:99", "0/1|1:99"), "mixes phased and unphased"),
        (VCF.replace("GT:GQ", "DP:GQ", 1), "one unique GT field"),
        (VCF.replace("T,G", "<DEL>,G"), "literal A/C/G/T"),
    ],
)
def test_rejects_malformed_or_unsupported_genotypes(document: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        _run(document)


def test_enforces_resource_limits_and_requires_sample_columns() -> None:
    with pytest.raises(ValueError, match="max_input_bytes"):
        aggregate_synthetic_vcf_qc(
            VCF,
            fixture_id="tiny-synthetic-cohort",
            data_classification="public_non_patient_synthetic",
            max_input_bytes=10,
        )
    header_only = "\n".join(VCF.splitlines()[:2]) + "\n"
    with pytest.raises(ValueError, match="at least one variant"):
        _run(header_only)
    no_samples = VCF.splitlines()[0] + "\n" + "\t".join(
        VCF.splitlines()[1].split("\t")[:8]
    ) + "\n" + "\t".join(VCF.splitlines()[2].split("\t")[:8])
    with pytest.raises(ValueError, match="at least one sample"):
        _run(no_samples)


def test_partial_missing_genotype_is_counted_as_missing() -> None:
    result = _run(VCF.replace("0/1:99", "0/.:99"))
    assert result["variants"][0]["called_sample_count"] == 1
    assert result["variants"][0]["missing_sample_count"] == 2



@pytest.mark.parametrize("genotype", ["0", "0/1/1", "0/1/2", "0|1|1"])
def test_rejects_unsupported_haploid_and_polyploid_calls(genotype: str) -> None:
    document = VCF.replace("0/1:99", f"{genotype}:99", 1)
    with pytest.raises(ValueError, match="unsupported ploidy"):
        _run(document)
