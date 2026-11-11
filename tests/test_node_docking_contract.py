from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


def test_private_node_worker_request_schema_requires_explicit_owner_approval() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "api" / "docking-execution.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    request = {
        "schema_version": 1,
        "job_type": "docking",
        "execution_authorized": True,
        "owner_approval": True,
        "engine": {
            "engine_id": "AutoDock Vina",
            "version": "1.2.7",
            "source_license_status": "apache-2.0-source-reviewed",
            "dependency_audit_status": "pending",
        },
        "receptor_pdbqt": "ATOM      1  C   ALA A   1       0.000   0.000   0.000  1.00  0.00     0.000 C\n",
        "ligand_pdbqt": "ATOM      1  C1  UNL     1       1.000   1.000   1.000  1.00  0.00     0.000 C\n",
        "center_angstrom": [0, 0, 0],
        "box_size_angstrom": [20, 20, 20],
        "seed": 1,
        "exhaustiveness": 8,
        "n_poses": 3,
        "cpu": 1,
        "scoring_function": "vina",
        "energy_range_kcal_per_mol": 3.0,
    }
    assert validator.is_valid(request)
    assert not validator.is_valid({**request, "owner_approval": False})
    assert not validator.is_valid({**request, "engine": {**request["engine"], "version": "latest"}})
    assert not validator.is_valid({**request, "box_size_angstrom": [20, 0, 20]})
