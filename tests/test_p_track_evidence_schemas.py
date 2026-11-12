from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]


def check(name, record):
    schema = json.loads((ROOT / "api" / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(record)


def test_guideline_schema_requires_research_only_not_cds():
    record = {
        "schema_version": 1,
        "evidence_id": "synthetic-guideline",
        "gene_symbol": "SYN1",
        "guideline_name": "Synthetic",
        "guideline_version": "fixture-1",
        "source_url": "https://example.invalid/g",
        "source_license_status": "verify_before_use",
        "source_release_date": "2026-01-01",
        "genome_build": "synthetic-v1",
        "recommendation_scope": "research_reference_only",
        "clinical_decision_support": False,
        "evidence_level": "not_assessed",
        "review_status": "draft",
        "reviewer": {
            "role": "synthetic-reviewer",
            "review_date": "2026-01-01",
            "evidence_url": "https://example.invalid/review",
        },
    }
    check("pgx-guideline-evidence.schema.json", record)
    record["clinical_decision_support"] = True
    with pytest.raises(ValidationError):
        check("pgx-guideline-evidence.schema.json", record)


def test_curation_schema_requires_second_review_and_no_autonomous_call():
    record = {
        "schema_version": 1,
        "record_id": "synthetic-record",
        "evidence_id": "e1",
        "source_url": "https://example.invalid/s",
        "source_release": "fixture-1",
        "source_sha256": "a" * 64,
        "license_status": "verify_before_use",
        "curation_outcome": "uncertain",
        "curator_role": "synthetic-curator",
        "curated_at": "2026-01-01T00:00:00Z",
        "second_review_required": True,
        "second_review_status": "pending",
        "autonomous_final_classification": False,
        "clinical_use": False,
    }
    check("pgx-curation-record.schema.json", record)
    record["autonomous_final_classification"] = True
    with pytest.raises(ValidationError):
        check("pgx-curation-record.schema.json", record)


def test_risk_contract_prohibits_patient_data():
    record = {
        "schema_version": 1,
        "risk_id": "P-001",
        "hazard": "fixture",
        "initial_severity": "not_assessed",
        "initial_likelihood": "not_assessed",
        "control": "synthetic only",
        "verification_status": "not_tested",
        "residual_risk_status": "unassessed",
        "owner_role": "engineering",
        "patient_data_scope": "prohibited_until_p0_approval",
    }
    check("p-track-risk-control.schema.json", record)


def test_jurisdiction_contract_cannot_enable_patient_or_clinical_use():
    record = {
        "schema_version": 1,
        "jurisdiction": "synthetic-jurisdiction",
        "intended_use_version": "draft-1",
        "review_status": "not_started",
        "reviewer_role": "unassigned",
        "review_date": "2026-01-01",
        "patient_data_authorized": False,
        "clinical_mode_authorized": False,
    }
    check("p-track-jurisdiction-review.schema.json", record)
    record["patient_data_authorized"] = True
    with pytest.raises(ValidationError):
        check("p-track-jurisdiction-review.schema.json", record)



def test_accepted_curation_requires_completed_evidenced_second_review():
    record = {
        "schema_version": 1,
        "record_id": "synthetic-accepted-record",
        "evidence_id": "e1",
        "source_url": "https://example.invalid/s",
        "source_release": "fixture-1",
        "source_sha256": "b" * 64,
        "license_status": "approved_for_research",
        "curation_outcome": "accepted_for_research",
        "curator_role": "synthetic-curator",
        "curated_at": "2026-01-01T00:00:00Z",
        "second_review_required": True,
        "second_review_status": "pending",
        "autonomous_final_classification": False,
        "clinical_use": False,
    }
    with pytest.raises(ValidationError):
        check("pgx-curation-record.schema.json", record)
    record.update({
        "second_review_status": "completed",
        "second_reviewer_role": "independent-synthetic-reviewer",
        "second_reviewed_at": "2026-01-02T00:00:00Z",
        "second_review_evidence_url": "https://example.invalid/review",
    })
    check("pgx-curation-record.schema.json", record)
    record.pop("second_review_evidence_url")
    with pytest.raises(ValidationError):
        check("pgx-curation-record.schema.json", record)
