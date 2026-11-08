#!/usr/bin/env python3
"""Run deterministic small-molecule sanity fixtures against the optional RDKit adapter.

This is an I1 engineering check, not an ADMET/biological-activity validation.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from kinetics.chemistry_rdkit import analyze_smiles, rdkit_backend_info

FIXTURE = ROOT / "validation" / "chemistry-reference-fixtures.json"


def _close(actual: Any, expected: Any, tolerance: float) -> bool:
    return isinstance(actual, (int, float)) and math.isfinite(float(actual)) and abs(float(actual) - float(expected)) <= tolerance


def run() -> dict[str, Any]:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    backend = rdkit_backend_info()
    if backend.get("available") != "true":
        raise SystemExit(backend.get("status", "RDKit is unavailable"))
    tolerances = fixture["tolerances"]
    results = []
    for molecule in fixture["molecules"]:
        observed = analyze_smiles(molecule["smiles"])
        expected = molecule["expected"]
        checks: dict[str, bool] = {}
        for key in ("formula", "atom_count", "bond_count", "ring_count", "h_bond_donors", "h_bond_acceptors", "rotatable_bonds"):
            checks[key] = observed[key] == expected[key]
        for key, tolerance_key in (
            ("molecular_weight", "molecular_weight_da"),
            ("exact_molecular_weight", "exact_molecular_weight_da"),
            ("tpsa_angstrom2", "tpsa_angstrom2"),
            ("crippen_logp", "crippen_logp"),
        ):
            checks[key] = _close(observed[key], expected[key], tolerances[tolerance_key])
        results.append({
            "id": molecule["id"],
            "checks": checks,
            "pass": all(checks.values()),
            "observed": {key: observed[key] for key in expected},
        })
    return {
        "validation_id": fixture["validation_id"],
        "schema_version": fixture["schema_version"],
        "engine": backend,
        "fixture_reference_basis": fixture["reference_basis"],
        "results": results,
        "overall_pass": all(result["pass"] for result in results),
        "limitations": fixture["limitations"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
