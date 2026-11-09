from __future__ import annotations
import copy, runpy
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATE = runpy.run_path(str(ROOT / "scripts" / "check_public_dataset_catalog.py"))["validate_catalog"]

def _catalog() -> dict:
    return yaml.safe_load((ROOT / "data" / "public-dataset-catalog.yaml").read_text(encoding="utf-8"))

def _entry() -> dict:
    return {
        "dataset_id": "synthetic-public-reference",
        "title": "Synthetic non-patient reference fixture",
        "source_url": "https://example.org/reference",
        "accession_or_version": "fixture-v1",
        "license": "CC0-1.0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "license_review_status": "not_reviewed",
        "intended_use": "Non-clinical software test fixture and parser regression testing",
        "retrieved_at": "2026-11-09T00:00:00Z",
        "content_sha256": "a" * 64,
        "patient_data": False,
        "notes": "Synthetic test metadata only; no external dataset is represented.",
    }

def test_committed_catalog_passes_and_has_no_acquired_records() -> None:
    catalog = _catalog()
    assert VALIDATE(catalog) == []
    assert catalog["entries"] == []
    assert all(item["patient_data"] is False for item in catalog["candidate_sources"])

def test_rejects_patient_data_and_duplicate_candidate_ids() -> None:
    catalog = _catalog()
    catalog["candidate_sources"].append(copy.deepcopy(catalog["candidate_sources"][0]))
    catalog["candidate_sources"][0]["patient_data"] = True
    errors = VALIDATE(catalog)
    assert any("patient_data must be false" in error for error in errors)
    assert any("duplicate candidate source_id" in error for error in errors)

def test_rejects_bad_hash_and_timezone_free_timestamp() -> None:
    catalog = _catalog()
    entry = _entry()
    entry["content_sha256"] = "not-a-digest"
    entry["retrieved_at"] = "2026-11-09T00:00:00"
    catalog["entries"] = [entry]
    errors = VALIDATE(catalog)
    assert any("content_sha256" in error for error in errors)
    assert any("retrieved_at" in error for error in errors)

def test_research_approval_requires_review_evidence() -> None:
    catalog = _catalog()
    entry = _entry()
    entry["license_review_status"] = "approved_for_research"
    catalog["entries"] = [entry]
    assert any("license_review is required" in error for error in VALIDATE(catalog))
    entry["license_review"] = {
        "reviewer": "Independent licence reviewer",
        "reviewed_at": "2026-11-09T00:00:00Z",
        "approved_scope": "Local non-clinical research use only",
        "evidence_url": "https://example.org/license-review",
    }
    assert VALIDATE(catalog) == []

def test_rejects_clinical_intended_use_language() -> None:
    catalog = _catalog()
    entry = _entry()
    entry["intended_use"] = "Clinical decision support for patient stratification"
    catalog["entries"] = [entry]
    assert any("prohibited" in error for error in VALIDATE(catalog))
