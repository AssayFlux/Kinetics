#!/usr/bin/env python3
"""Validate Track G governance registers and evidence-index integrity."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL_ID = re.compile(r"\bG[0-7]-\d{2}\b")


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path.relative_to(ROOT)} has no CSV header")
        return list(reader.fieldnames), list(reader)


def validate() -> list[str]:
    errors: list[str] = []
    required = [
        "docs/track-g/implementation-plan.md",
        "docs/track-g/control-evidence-register.md",
        "docs/track-g/roles-and-review-cadence.md",
        "docs/track-g/requirements-traceability.csv",
        "docs/track-g/capa-register.csv",
        "docs/track-g/data-flow-inventory.md",
        "docs/track-g/security-verification-matrix.md",
        "docs/track-g/publication-integrity.md",
        "docs/track-g/operational-controls.md",
        "docs/security-threat-model.md",
        "SECURITY.md",
        "PRIVACY.md",
        "docs/release-checklist.md",
        "paper/claim-evidence-ledger.csv",
        "capabilities/registry.yaml",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            errors.append(f"Missing required governance artifact: {relative}")

    register_path = ROOT / "docs/track-g/control-evidence-register.md"
    trace_path = ROOT / "docs/track-g/requirements-traceability.csv"
    if register_path.is_file() and trace_path.is_file():
        register = register_path.read_text(encoding="utf-8")
        controls = set(CONTROL_ID.findall(register))
        expected = {
            f"G{group}-{number:02d}"
            for group, count in enumerate((6, 4, 4, 4, 3, 3, 3, 3))
            for number in range(1, count + 1)
        }
        missing = sorted(expected - controls)
        if missing:
            errors.append("Control register is missing IDs: " + ", ".join(missing))
        headers, rows = _read_csv(trace_path)
        if not {"requirement_id", "control_ids", "status"}.issubset(headers):
            errors.append("Requirements traceability CSV is missing required columns")
        else:
            mapped = set()
            requirement_ids = []
            for row in rows:
                requirement_ids.append(row["requirement_id"])
                mapped.update(CONTROL_ID.findall(row["control_ids"]))
            if len(requirement_ids) != len(set(requirement_ids)):
                errors.append("Duplicate requirement_id in traceability CSV")
            unmapped = sorted(expected - mapped)
            if unmapped:
                errors.append("Controls missing traceability rows: " + ", ".join(unmapped))

    capa_path = ROOT / "docs/track-g/capa-register.csv"
    if capa_path.is_file():
        headers, _ = _read_csv(capa_path)
        required_columns = {
            "record_id", "record_type", "severity", "description", "containment",
            "root_cause", "corrective_action", "effectiveness_check", "owner",
            "reviewer", "status", "linked_controls", "evidence_uri",
        }
        if not required_columns.issubset(headers):
            errors.append("CAPA register is missing required columns")

    security_path = ROOT / "docs/track-g/security-verification-matrix.md"
    if security_path.is_file():
        security = security_path.read_text(encoding="utf-8")
        test_ids = re.findall(r"\|\s*(SEC-\d{3})\s*\|", security)
        if len(test_ids) != len(set(test_ids)):
            errors.append("Duplicate security verification test IDs")
        if not test_ids:
            errors.append("Security verification matrix contains no test IDs")

    claim_path = ROOT / "paper/claim-evidence-ledger.csv"
    if claim_path.is_file():
        headers, rows = _read_csv(claim_path)
        required_columns = {
            "claim_id", "claim_text", "implementation_commit", "validation_protocol",
            "reference_dataset", "metric", "measured_value", "uncertainty",
            "artifact_path", "artifact_sha256", "independent_review", "status",
            "limitations",
        }
        if not required_columns.issubset(headers):
            errors.append("Manuscript claim ledger is missing required columns")
        if any(row.get("status", "").strip().lower() == "validated" and
               not row.get("independent_review", "").strip() for row in rows):
            errors.append("Validated manuscript claim lacks independent-review evidence")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Track G governance structure and register checks passed.")
    print("This validates document/register structure only; it is not external assurance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
