#!/usr/bin/env python3
"""Generate a conservative capability-to-evidence claims matrix from the registry."""
from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/track-g/capability-claims-matrix.csv"
FIELDS = [
    "capability_id", "capability_name", "implementation_path",
    "implementation_status", "evidence_level", "validation_status",
    "device_status", "license_status", "permitted_claim", "limitations",
]


def render(registry_path: Path = ROOT / "capabilities/registry.yaml") -> str:
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    tools = registry.get("tools", [])
    rows = []
    for tool in tools:
        status = str(tool.get("status", "unknown"))
        evidence = str(tool.get("evidence_level", "none"))
        validated = evidence.lower() in {"validated", "independently_validated"}
        rows.append({
            "capability_id": str(tool.get("id", "")),
            "capability_name": str(tool.get("name", "")),
            "implementation_path": str(tool.get("implementation", "")),
            "implementation_status": status,
            "evidence_level": evidence,
            "validation_status": "EVIDENCE-RECORDED-REVIEW-REQUIRED" if validated else "OPEN",
            "device_status": "OPEN",
            "license_status": "OPEN",
            "permitted_claim": (
                "Independently validated only within the linked protocol scope"
                if validated else
                "Software implementation is recorded; no scientific validity is implied"
            ),
            "limitations": (
                "Inspect exact validation record, reviewer, source terms and device evidence"
                if validated else
                "No independent validation, device verification or redistribution approval inferred"
            ),
        })
    rows.sort(key=lambda row: row["capability_id"])
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != expected:
            print(f"Capability claims matrix is stale: {args.output}")
            return 1
        print(f"Capability claims matrix is reproducible: {args.output}")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(expected, encoding="utf-8", newline="")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
