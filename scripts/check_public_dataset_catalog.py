#!/usr/bin/env python3
"""Validate public non-patient dataset metadata; never downloads data or lifts P0."""
from __future__ import annotations
import argparse, re, sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "data" / "public-dataset-catalog.yaml"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FORBIDDEN = ("diagnos", "treatment recommendation", "dosing recommendation",
             "clinical decision support", "patient stratification", "individual risk score")

def _https(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)

def _aware(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None

def _safe_use(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not any(
        term in value.casefold() for term in FORBIDDEN
    )

def validate_catalog(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["catalogue root must be a mapping"]
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("data_classification") != "public_non_patient_only":
        errors.append("data_classification must be public_non_patient_only")
    if not isinstance(data.get("purpose"), str) or not data["purpose"].strip():
        errors.append("purpose must be non-empty")
    candidates = data.get("candidate_sources")
    if not isinstance(candidates, list):
        errors.append("candidate_sources must be a list")
        candidates = []
    seen: set[str] = set()
    for i, item in enumerate(candidates):
        p = f"candidate_sources[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{p} must be a mapping")
            continue
        sid = item.get("source_id")
        if not isinstance(sid, str) or not SLUG.fullmatch(sid):
            errors.append(f"{p}.source_id must be lowercase kebab-case")
        elif sid in seen:
            errors.append(f"duplicate candidate source_id: {sid}")
        else:
            seen.add(sid)
        for field in ("title", "candidate_use", "notes"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{p}.{field} must be non-empty")
        if not _https(item.get("source_url")):
            errors.append(f"{p}.source_url must be HTTPS")
        if item.get("license_review_status") != "verify_before_intake":
            errors.append(f"{p}.license_review_status must remain verify_before_intake")
        if item.get("patient_data") is not False:
            errors.append(f"{p}.patient_data must be false")
        if not _safe_use(item.get("candidate_use")):
            errors.append(f"{p}.candidate_use contains prohibited intended-use language")
    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("entries must be a list")
        entries = []
    seen_entries: set[str] = set()
    for i, item in enumerate(entries):
        p = f"entries[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{p} must be a mapping")
            continue
        did = item.get("dataset_id")
        if not isinstance(did, str) or not SLUG.fullmatch(did):
            errors.append(f"{p}.dataset_id must be lowercase kebab-case")
        elif did in seen_entries:
            errors.append(f"duplicate dataset_id: {did}")
        else:
            seen_entries.add(did)
        for field in ("title", "accession_or_version", "license", "intended_use"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{p}.{field} must be non-empty")
        for field in ("source_url", "license_url"):
            if not _https(item.get(field)):
                errors.append(f"{p}.{field} must be HTTPS")
        if item.get("license_review_status") not in {"not_reviewed", "approved_for_research", "prohibited"}:
            errors.append(f"{p}.license_review_status is invalid")
        if item.get("patient_data") is not False:
            errors.append(f"{p}.patient_data must be false")
        if not isinstance(item.get("content_sha256"), str) or not SHA256.fullmatch(item["content_sha256"]):
            errors.append(f"{p}.content_sha256 must be a lowercase SHA-256 digest")
        if not _aware(item.get("retrieved_at")):
            errors.append(f"{p}.retrieved_at must be timezone-aware ISO-8601")
        if not _safe_use(item.get("intended_use")):
            errors.append(f"{p}.intended_use contains prohibited intended-use language")
        if item.get("license_review_status") == "approved_for_research":
            review = item.get("license_review")
            if not isinstance(review, dict):
                errors.append(f"{p}.license_review is required for approved_for_research")
            else:
                for field in ("reviewer", "approved_scope"):
                    if not isinstance(review.get(field), str) or not review[field].strip():
                        errors.append(f"{p}.license_review.{field} must be non-empty")
                if not _aware(review.get("reviewed_at")):
                    errors.append(f"{p}.license_review.reviewed_at must be timezone-aware")
                if not _https(review.get("evidence_url")):
                    errors.append(f"{p}.license_review.evidence_url must be HTTPS")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()
    try:
        data = yaml.safe_load(args.catalog.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"catalogue load failed: {exc}", file=sys.stderr)
        return 2
    errors = validate_catalog(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Public dataset catalogue valid: {len(data['candidate_sources'])} candidate(s), "
          f"{len(data['entries'])} acquired metadata entr(y/ies); patient-data intake remains disabled.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
