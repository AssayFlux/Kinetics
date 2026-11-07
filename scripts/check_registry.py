#!/usr/bin/env python3
"""Validate the JSON-compatible YAML capability registry and domain references."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "capabilities" / "registry.yaml"
DOMAINS = ROOT / "domains"
VALID_STATUSES = {"planned", "implemented", "validated"}


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: {exc}") from exc


def main() -> int:
    registry = load(REGISTRY)
    tools = {item["id"] for item in registry.get("tools", [])}
    engines = {item["id"] for item in registry.get("engines", [])}
    packs = {item["id"] for item in registry.get("data_packs", [])}
    errors: list[str] = []
    files = sorted(DOMAINS.glob("*.yaml"))
    seen: set[str] = set()

    for path in files:
        domain = load(path)
        domain_id = domain.get("id")
        if not domain_id or domain_id in seen:
            errors.append(f"{path.name}: missing or duplicate domain id {domain_id!r}")
        seen.add(domain_id)
        if path.stem != domain_id:
            errors.append(f"{path.name}: filename must match id {domain_id!r}")
        if domain.get("status") not in VALID_STATUSES:
            errors.append(f"{path.name}: invalid status {domain.get('status')!r}")
        for field, known in (("tools", tools), ("engines", engines), ("data_packs", packs)):
            for ref in domain.get(field, []):
                if ref not in known:
                    errors.append(f"{path.name}: unknown {field[:-1]} reference {ref!r}")
        if domain.get("status") == "validated":
            errors.append(f"{path.name}: validated domain requires a validation record and benchmark mapping")

    registry_ids = {item.get("id") for item in registry.get("domains", [])}
    if registry_ids != seen:
        errors.append(
            f"registry domain set differs from files: {len(registry_ids)} registry ids, "
            f"{len(seen)} files"
        )
    if len(files) != 160:
        errors.append(f"expected 160 domain files, found {len(files)}")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Registry OK: {len(files)} domains; {len(tools)} tools; "
          f"{len(engines)} engines; {len(packs)} data packs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
