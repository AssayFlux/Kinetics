"""OpenMM CPU engine smoke test with a synthetic harmonic molecule only."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import openmm
from openmm import app, unit
from openmm.vec3 import Vec3
from jsonschema import Draft202012Validator

from kinetics.md_openmm import run_openmm_dynamics


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    topology = app.Topology()
    chain = topology.addChain("A")
    residue = topology.addResidue("MOL", chain)
    atom_a = topology.addAtom("C1", app.element.carbon, residue)
    atom_b = topology.addAtom("C2", app.element.carbon, residue)
    topology.addBond(atom_a, atom_b)

    system = openmm.System()
    system.addParticle(12.011 * unit.amu)
    system.addParticle(12.011 * unit.amu)
    bond = openmm.HarmonicBondForce()
    bond.addBond(
        0, 1, 0.15 * unit.nanometer,
        1000.0 * unit.kilojoule_per_mole / unit.nanometer**2,
    )
    system.addForce(bond)
    positions = [Vec3(0.0, 0.0, 0.0), Vec3(0.18, 0.0, 0.0)] * unit.nanometer
    parameter_manifest = (
        "synthetic two-carbon harmonic bond; equilibrium=0.15 nm; "
        "force_constant=1000 kJ/mol/nm^2; not a chemical force field"
    )
    topology_manifest = "two atoms C1,C2 in synthetic residue MOL, connected by one bond"
    coordinate_manifest = "initial positions: (0,0,0) and (0.18,0,0) nm"
    result = run_openmm_dynamics(
        system,
        topology,
        positions,
        coordinates_sha256=hashlib.sha256(coordinate_manifest.encode()).hexdigest(),
        topology_sha256=hashlib.sha256(topology_manifest.encode()).hexdigest(),
        force_field_name="synthetic harmonic test system",
        force_field_version="1",
        parameter_source_sha256=hashlib.sha256(parameter_manifest.encode()).hexdigest(),
        temperature_kelvin=300.0,
        pressure_bar=None,
        timestep_fs=1.0,
        steps=100,
        equilibration_steps=10,
        replicas=2,
        seed=20261111,
        report_interval=10,
        cpu_threads=1,
    )
    schema = json.loads(
        (ROOT / "api" / "insilico-result.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(schema).validate(result)
    if len(result["replicas"]) != 2:
        raise SystemExit("Expected two independent MD replicas")
    report = {
        "validation_id": "openmm-synthetic-harmonic-cpu-smoke-v1",
        "overall_pass": True,
        "scientific_validation": False,
        "engine": result["engine"],
        "protocol": result["protocol"],
        "replicas": [
            {
                "replica_id": item["replica_id"],
                "steps_completed": item["steps_completed"],
                "initial_potential_energy_kj_per_mol": item["initial_potential_energy"],
                "final_potential_energy_kj_per_mol": item["final_potential_energy"],
                "trajectory_sha256": item["trajectory_sha256"],
                "trajectory_bytes": len(item["trajectory_dcd_base64"]) * 3 // 4,
            }
            for item in result["replicas"]
        ],
        "limitations": [
            "Synthetic two-particle harmonic system only; not a biomolecular model",
            "Smoke check verifies engine execution, DCD output, provenance and schema only",
            "No force-field, protein, ligand, solvent, energy-conservation or ensemble validation",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
