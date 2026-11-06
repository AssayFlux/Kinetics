from __future__ import annotations

import json
from pathlib import Path

import pytest

from kinetics_core.native_molecule import (
    build_simulation_plan,
    inspect_structure,
    sha256_file,
)


def test_simulation_plan_is_complete_and_explicit(tmp_path: Path) -> None:
    structure = tmp_path / "input.pdb"
    structure.write_text("ATOM fixture\n", encoding="utf-8")
    plan = build_simulation_plan(
        structure,
        engine="OpenMM",
        engine_version="8.2.0",
        force_field="amber14-all.xml",
        water_model="amber14/tip3p",
        integrator="LangevinMiddleIntegrator",
        timestep_fs=2.0,
        steps=10000,
        temperature_kelvin=300.0,
        random_seed=1234,
        pressure_bar=1.0,
    )
    assert plan["execution_status"] == "planned_not_executed"
    assert plan["engine"] == "openmm"
    assert plan["input_structure"]["sha256"] == sha256_file(structure)
    assert plan["timestep"] == {"value": 2.0, "unit": "femtosecond"}
    assert plan["pressure"] == {"value": 1.0, "unit": "bar"}


@pytest.mark.parametrize(
    "overrides",
    [
        {"steps": 0},
        {"random_seed": -1},
        {"timestep_fs": 0},
        {"temperature_kelvin": float("nan")},
        {"pressure_bar": -1.0},
        {"engine": "unknown"},
        {"force_field": ""},
    ],
)
def test_simulation_plan_rejects_invalid_parameters(tmp_path: Path, overrides: dict) -> None:
    structure = tmp_path / "input.pdb"
    structure.write_text("ATOM fixture\n", encoding="utf-8")
    parameters = {
        "engine": "gromacs",
        "engine_version": "2024.1",
        "force_field": "amber99sb-ildn",
        "water_model": "tip3p",
        "integrator": "md",
        "timestep_fs": 2.0,
        "steps": 1000,
        "temperature_kelvin": 300.0,
        "random_seed": 7,
    }
    parameters.update(overrides)
    with pytest.raises(ValueError):
        build_simulation_plan(structure, **parameters)


def test_native_bridge_checks_scene_and_records_source_hash(tmp_path: Path) -> None:
    source = tmp_path / "source.pdb"
    source.write_text("fixture structure\n", encoding="utf-8")
    executable = tmp_path / "inspector.py"
    scene = {
        "schema_version": "kinetics.molecular-scene/1.0",
        "engine_version": "0.1.0",
        "coordinate_unit": "angstrom",
        "atoms": [
            {"serial": 1, "position": [0.0, 0.0, 0.0]},
            {"serial": 2, "position": [1.0, 0.0, 0.0]},
        ],
        "bonds": [{"atom_serial_a": 1, "atom_serial_b": 2}],
    }
    executable.write_text(
        "#!/usr/bin/env python3\n"
        "import json, pathlib, sys\n"
        f"scene = json.loads({json.dumps(scene)!r})\n"
        "pathlib.Path(sys.argv[2]).write_text(json.dumps(scene), encoding='utf-8')\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    result = inspect_structure(source, executable=executable)
    assert result["provenance"]["source_sha256"] == sha256_file(source)
    assert result["provenance"]["native_engine_version"] == "0.1.0"


def test_native_bridge_rejects_bad_bond_reference(tmp_path: Path) -> None:
    source = tmp_path / "source.pdb"
    source.write_text("fixture structure\n", encoding="utf-8")
    executable = tmp_path / "inspector.py"
    scene = {
        "schema_version": "kinetics.molecular-scene/1.0",
        "engine_version": "0.1.0",
        "coordinate_unit": "angstrom",
        "atoms": [{"serial": 1, "position": [0.0, 0.0, 0.0]}],
        "bonds": [{"atom_serial_a": 1, "atom_serial_b": 99}],
    }
    executable.write_text(
        "#!/usr/bin/env python3\n"
        "import json, pathlib, sys\n"
        f"scene = {json.dumps(scene)!r}\n"
        "pathlib.Path(sys.argv[2]).write_text(json.dumps(scene), encoding='utf-8')\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    with pytest.raises(ValueError, match="bond references"):
        inspect_structure(source, executable=executable)
