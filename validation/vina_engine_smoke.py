"""Pinned AutoDock Vina engine smoke check; not scientific redocking validation."""
from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from jsonschema import Draft202012Validator

from kinetics.docking_vina import run_vina_docking


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "validation" / "fixtures" / "vina"


def _run() -> dict[str, object]:
    receptor_path = FIXTURES / "1iep_receptor.pdbqt"
    ligand_path = FIXTURES / "1iep_ligand.pdbqt"
    receptor = receptor_path.read_text(encoding="utf-8")
    ligand = ligand_path.read_text(encoding="utf-8")
    return run_vina_docking(
        receptor,
        ligand,
        center_angstrom=[15.664, 53.212, 15.545],
        box_size_angstrom=[20.0, 20.0, 20.0],
        seed=20261111,
        exhaustiveness=4,
        n_poses=3,
        cpu=1,
    )


def main() -> None:
    schema = json.loads(
        (ROOT / "api" / "insilico-result.schema.json").read_text(encoding="utf-8")
    )
    first = _run()
    second = _run()
    Draft202012Validator(schema).validate(first)
    first_poses = first["poses"]
    second_poses = second["poses"]
    deterministic = (
        [pose["score"] for pose in first_poses]
        == [pose["score"] for pose in second_poses]
        and [pose["pose_sha256"] for pose in first_poses]
        == [pose["pose_sha256"] for pose in second_poses]
    )
    if not deterministic:
        raise SystemExit("Pinned Vina replay was not deterministic on the single-CPU fixture")
    receptor_bytes = (FIXTURES / "1iep_receptor.pdbqt").read_bytes()
    ligand_bytes = (FIXTURES / "1iep_ligand.pdbqt").read_bytes()
    report = {
        "validation_id": "vina-1iep-engine-smoke-v1",
        "overall_pass": True,
        "validation_scope": "engine availability, deterministic replay, result schema and provenance",
        "scientific_redocking_validation": False,
        "engine": first["engine"],
        "fixture_source": {
            "repository": "https://github.com/forlilab/AutoDock-Vina",
            "tag": "v1.2.7",
            "commit": "8eb40404f4f45608acb3b01427587ac049f27c1f",
            "pdb_entry": "1IEP",
            "receptor_sha256": sha256(receptor_bytes).hexdigest(),
            "ligand_sha256": sha256(ligand_bytes).hexdigest(),
        },
        "protocol": first["protocol"],
        "pose_count": len(first_poses),
        "scores_kcal_per_mol_engine_output": [pose["score"] for pose in first_poses],
        "pose_hashes": [pose["pose_sha256"] for pose in first_poses],
        "deterministic_replay": deterministic,
        "limitations": [
            "Smoke test only; no symmetry-corrected crystal-pose RMSD or decoy enrichment",
            "No prospective or independent cross-docking benchmark",
            "Engine score is not experimental binding free energy or affinity",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
