#!/usr/bin/env python3
"""Run deterministic small-molecule sanity fixtures against the optional RDKit adapter.

This is an I1 engineering check, not an ADMET/biological-activity validation.
"""
from __future__ import annotations

import json
import math
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from kinetics.chemistry import graph_descriptors, parse_sdf_record
from kinetics.chemistry_rdkit import analyze_molblock, analyze_smiles, rdkit_backend_info

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
        for key in ("formula", "atom_count", "bond_count", "ring_count", "h_bond_donors", "h_bond_acceptors", "rotatable_bonds", "formal_charge", "heavy_atom_count", "aromatic_atom_count", "aliphatic_ring_count", "aromatic_ring_count"):
            checks[key] = observed[key] == expected[key]
        for key, tolerance_key in (
            ("molecular_weight", "molecular_weight_da"),
            ("exact_molecular_weight", "exact_molecular_weight_da"),
            ("tpsa_angstrom2", "tpsa_angstrom2"),
            ("crippen_logp", "crippen_logp"),
            ("fraction_csp3", "fraction_csp3"),
        ):
            checks[key] = _close(observed[key], expected[key], tolerances[tolerance_key])
        checks["descriptor_schema_version"] = observed["descriptor_schema_version"] == 2
        checks["input_sha256"] = observed["input_provenance"]["sha256_utf8"] == sha256(
            molecule["smiles"].encode("utf-8")
        ).hexdigest()
        checks["fingerprint_configuration"] = (
            observed["morgan_fingerprint"]["algorithm"] == "Morgan"
            and observed["morgan_fingerprint"]["radius"] == 2
            and observed["morgan_fingerprint"]["bits"] == 2048
        )
        checks["fingerprint_nonempty"] = bool(observed["morgan_fingerprint"]["on_bits"])
        results.append({
            "id": molecule["id"],
            "checks": checks,
            "pass": all(checks.values()),
            "observed": {key: observed[key] for key in expected},
        })
    # Reject hostile text before invoking the chemistry parser.
    input_guard_checks: dict[str, bool] = {}
    for label, value in (
        ("embedded_nul", "CCO\\x00"),
        ("invalid_unicode", "CCO\\ud800"),
    ):
        try:
            analyze_smiles(value)
        except ValueError:
            input_guard_checks[label] = True
        else:
            input_guard_checks[label] = False
    try:
        analyze_smiles("é" * 600_000)
    except ValueError:
        input_guard_checks["utf8_byte_limit"] = True
    else:
        input_guard_checks["utf8_byte_limit"] = False
    if not all(input_guard_checks.values()):
        raise AssertionError(f"RDKit input guard failure: {input_guard_checks}")

    # A small explicit-atom SDF ring compares the conservative graph parser
    # against RDKit's independently parsed/sanitized molecular graph.
    counts = f"{3:3d}{3:3d}  0  0  0  0            999 V2000"
    coordinates = [(0.0, 0.0, 0.0), (1.5, 0.0, 0.0), (0.75, 1.3, 0.0)]
    atom_lines = [
        f"{x:10.4f}{y:10.4f}{z:10.4f} {'C':>3s}"
        for x, y, z in coordinates
    ]
    bond_lines = [
        f"{1:3d}{2:3d}{1:3d}",
        f"{2:3d}{3:3d}{1:3d}",
        f"{3:3d}{1:3d}{1:3d}",
    ]
    molblock = "\n".join([
        "cyclopropane", "Kinetics reference", "", counts,
        *atom_lines, *bond_lines, "M  END",
    ])
    local = parse_sdf_record(molblock)
    local_graph = graph_descriptors(local)
    adapter = analyze_molblock(molblock)
    from rdkit import Chem
    reference_molecule = Chem.MolFromMolBlock(
        molblock, sanitize=True, removeHs=False, strictParsing=True,
    )
    if reference_molecule is None:
        raise RuntimeError("RDKit could not parse the SDF graph reference fixture")
    reference_conformer = reference_molecule.GetConformer()
    max_coordinate_delta = 0.0
    element_match = local["atom_count"] == reference_molecule.GetNumAtoms()
    if element_match:
        for index, atom in enumerate(local["atoms"]):
            reference_atom = reference_molecule.GetAtomWithIdx(index)
            element_match = element_match and atom["element"] == reference_atom.GetSymbol()
            point = reference_conformer.GetAtomPosition(index)
            max_coordinate_delta = max(
                max_coordinate_delta,
                math.sqrt(
                    (float(atom["x"]) - point.x) ** 2
                    + (float(atom["y"]) - point.y) ** 2
                    + (float(atom["z"]) - point.z) ** 2
                ),
            )
    bond_match = local["bond_count"] == reference_molecule.GetNumBonds()
    if bond_match:
        for first, second, order in local["bonds"]:
            reference_bond = reference_molecule.GetBondBetweenAtoms(first, second)
            bond_match = bond_match and reference_bond is not None
            if reference_bond is not None:
                bond_match = bond_match and reference_bond.GetBondTypeAsDouble() == order
    graph_comparison = {
        "fixture": "explicit-atom cyclopropane V2000",
        "pass": (
            element_match and bond_match
            and local_graph["cycle_rank"] == reference_molecule.GetRingInfo().NumRings()
            and max_coordinate_delta <= 1e-4
            and adapter["atom_count"] == reference_molecule.GetNumAtoms()
            and adapter["bond_count"] == reference_molecule.GetNumBonds()
        ),
        "local_atom_count": local["atom_count"],
        "rdkit_atom_count": reference_molecule.GetNumAtoms(),
        "local_bond_count": local["bond_count"],
        "rdkit_bond_count": reference_molecule.GetNumBonds(),
        "local_cycle_rank": local_graph["cycle_rank"],
        "rdkit_ring_count": reference_molecule.GetRingInfo().NumRings(),
        "element_match": element_match,
        "bond_order_match": bond_match,
        "max_coordinate_delta_angstrom": max_coordinate_delta,
        "coordinate_tolerance_angstrom": 1e-4,
        "rdkit_formula_including_implicit_hydrogens": adapter["formula"],
        "note": "The local formula counts explicit SDF atoms only; implicit-hydrogen formula equality is intentionally not asserted.",
    }
    return {
        "validation_id": fixture["validation_id"],
        "schema_version": fixture["schema_version"],
        "engine": backend,
        "fixture_reference_basis": fixture["reference_basis"],
        "results": results,
        "input_guard_checks": input_guard_checks,
        "graph_parser_comparison": graph_comparison,
        "overall_pass": all(result["pass"] for result in results) and graph_comparison["pass"],
        "limitations": fixture["limitations"] + [
            "The SDF comparison is a synthetic explicit-atom graph/coordinate concordance check only.",
            "It does not validate stereochemistry, aromaticity models, implicit-hydrogen inference, tautomer/protonation behavior or Android RDKit feasibility.",
        ],
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["overall_pass"]:
        raise SystemExit(1)
