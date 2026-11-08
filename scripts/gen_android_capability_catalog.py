#!/usr/bin/env python3
"""Generate the Android Explore catalogue from the canonical capability registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "capabilities" / "registry.yaml"
OUTPUT = ROOT / "android" / "app" / "src" / "main" / "assets" / "capability-catalog.json"

DOMAIN_LABELS = {
    "sequence": "Sequence analysis",
    "genome": "Genome analysis",
    "genomics": "Genomics",
    "transcriptomics": "Transcriptomics",
    "protein": "Protein analysis",
    "structure": "Structural biology",
    "chemistry": "Computational chemistry",
    "molecular": "Molecular biology",
    "phylo": "Phylogenetics",
    "omics": "Omics & statistics",
    "microbiome": "Microbiome analysis",
    "kinetics": "Kinetics & modelling",
    "genes": "Gene reference data",
    "pharmacogenomics": "Pharmacogenomics",
}


def build_catalogue(registry: dict[str, Any]) -> list[dict[str, str]]:
    tools = registry.get("tools", [])
    if not isinstance(tools, list):
        raise ValueError("registry tools must be a list")
    catalogue: list[dict[str, str]] = []
    for tool in tools:
        if not isinstance(tool, dict):
            raise ValueError("every registry tool must be a mapping")
        identifier = tool.get("id")
        if not isinstance(identifier, str) or "." not in identifier:
            raise ValueError(f"tool has invalid domain-qualified id: {identifier!r}")
        domain_key = identifier.split(".", 1)[0]
        implementation = tool.get("implementation")
        if not isinstance(implementation, str) or not implementation:
            raise ValueError(f"tool {identifier} has no implementation path")
        catalogue.append(
            {
                "id": identifier,
                "name": str(tool.get("name", identifier)),
                "status": str(tool.get("status", "planned")),
                "implementation": implementation,
                "evidence_level": str(tool.get("evidence_level", "none")),
                "domain": DOMAIN_LABELS.get(
                    domain_key, domain_key.replace("_", " ").title()
                ),
            }
        )
    return catalogue


def render_catalogue(registry: dict[str, Any]) -> str:
    return json.dumps(build_catalogue(registry), ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the committed asset is stale")
    args = parser.parse_args()
    import yaml

    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    rendered = render_catalogue(registry)
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit("Android capability catalogue is stale; regenerate it")
        print(f"Android capability catalogue is current: {OUTPUT}")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(rendered, encoding="utf-8")
        print(f"Generated {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
