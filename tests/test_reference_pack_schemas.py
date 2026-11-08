from __future__ import annotations

import json

import yaml
from pathlib import Path


def test_local_reference_pack_schema_is_strict_and_content_addressed() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "api" / "local-reference-pack.schema.json").read_text(encoding="utf-8")
    )
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == {
        "schema_version", "name", "version", "license", "source",
        "sequence_type", "format", "content_sha256",
    }
    assert schema["properties"]["content_sha256"]["pattern"] == "^[0-9a-f]{64}$"
    assert schema["properties"]["sequence_type"]["enum"] == ["DNA", "RNA", "protein"]


def test_public_dataset_catalog_is_empty_and_non_patient_by_default() -> None:
    root = Path(__file__).resolve().parents[1]
    catalog = (root / "data" / "public-dataset-catalog.yaml").read_text(encoding="utf-8")
    assert "data_classification: public_non_patient_only" in catalog
    assert "entries: []" in catalog
    schema = json.loads(
        (root / "api" / "public-dataset-catalog.schema.json").read_text(encoding="utf-8")
    )
    assert schema["properties"]["data_classification"]["const"] == "public_non_patient_only"
    assert schema["properties"]["entries"]["items"]["properties"]["patient_data"]["const"] is False


def test_public_candidate_sources_are_explicitly_unapproved_and_non_patient() -> None:
    root = Path(__file__).resolve().parents[1]
    catalog = yaml.safe_load(
        (root / "data" / "public-dataset-catalog.yaml").read_text(encoding="utf-8")
    )
    schema = json.loads(
        (root / "api" / "public-dataset-catalog.schema.json").read_text(encoding="utf-8")
    )
    assert catalog["entries"] == []
    assert catalog["data_classification"] == "public_non_patient_only"
    assert catalog["candidate_sources"]
    candidate_schema = schema["properties"]["candidate_sources"]["items"]
    assert candidate_schema["properties"]["license_review_status"]["const"] == "verify_before_intake"
    assert candidate_schema["properties"]["patient_data"]["const"] is False
    for candidate in catalog["candidate_sources"]:
        assert candidate["license_review_status"] == "verify_before_intake"
        assert candidate["patient_data"] is False
