#!/usr/bin/env python3
"""Validate registry references and evidence claims; never infer validation."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from typing import Any
import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "capabilities" / "registry.yaml"
COLLECTIONS = ("tools", "engines", "data_packs", "domains", "device_logs")
STATUSES = {"planned", "implemented", "validated"}
EVIDENCE = {"none", "benchmark", "reference-concordance", "clinical-study"}

def _ids(items: Any, collection: str, errors: list[str]) -> set[str]:
    if not isinstance(items, list):
        errors.append(f"{collection} must be a list")
        return set()
    found: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{collection}[{index}] must be a mapping")
            continue
        identifier = item.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            errors.append(f"{collection}[{index}] requires a non-empty id")
        elif identifier in found:
            errors.append(f"duplicate {collection} id: {identifier}")
        else:
            found.add(identifier)
    return found

def validate_registry(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["registry root must be a mapping"]
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    known = {name: _ids(data.get(name, []), name, errors) for name in COLLECTIONS}
    tools = data.get("tools", [])
    if not isinstance(tools, list):
        tools = []
    for tool in tools:
        if not isinstance(tool, dict):
            continue
        tid = str(tool.get("id", "<unknown>"))
        status = tool.get("status", "planned")
        evidence = tool.get("evidence_level", "none")
        if status not in STATUSES:
            errors.append(f"tool {tid}: invalid status {status!r}")
        if evidence not in EVIDENCE:
            errors.append(f"tool {tid}: invalid evidence_level {evidence!r}")
        for field, collection in (("engine_ids", "engines"), ("data_pack_ids", "data_packs"), ("domain_ids", "domains")):
            refs = tool.get(field, [])
            if not isinstance(refs, list):
                errors.append(f"tool {tid}: {field} must be a list")
                continue
            for ref in refs:
                if ref not in known[collection]:
                    errors.append(f"tool {tid}: {field} references missing {collection} id {ref!r}")
        if status == "validated":
            records = tool.get("validation_records", [])
            if not isinstance(records, list) or not records:
                errors.append(f"tool {tid}: validated status requires validation_records")
            if evidence == "none":
                errors.append(f"tool {tid}: validated status requires non-none evidence_level")
        if tool.get("device_verified", False):
            logs = tool.get("device_log_ids", [])
            if not isinstance(logs, list) or not logs:
                errors.append(f"tool {tid}: device_verified requires device_log_ids")
            elif any(log not in known["device_logs"] for log in logs):
                errors.append(f"tool {tid}: device_verified references a missing device log")
        if tool.get("clinical", False):
            gate = data.get("clinical_gate", {})
            if not isinstance(gate, dict) or gate.get("enabled") is not True:
                errors.append(f"tool {tid}: clinical capability requires clinical_gate.enabled")
            elif not gate.get("part12_evidence"):
                errors.append(f"tool {tid}: clinical capability requires Part 12 evidence")
    if not isinstance(data.get("clinical_gate", {}), dict):
        errors.append("clinical_gate must be a mapping")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    args = parser.parse_args()
    try:
        data = yaml.safe_load(args.registry.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"registry load failed: {exc}", file=sys.stderr)
        return 2
    errors = validate_registry(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Registry valid: {args.registry}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
