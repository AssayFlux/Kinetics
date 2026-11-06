"""Narrow, provenance-preserving bridge to the native molecular scene inspector."""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Any

SCENE_SCHEMA = "kinetics.molecular-scene/1.0"
SUPPORTED_SIMULATION_ENGINES = {"openmm", "gromacs"}


def sha256_file(path: str | Path) -> str:
    """Hash a file in bounded memory."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_structure(
    structure_path: str | Path,
    *,
    executable: str | Path,
    timeout_seconds: float = 30.0,
) -> dict[str, Any]:
    """Inspect a PDB with the C++ engine and attach immutable input provenance."""
    source = Path(structure_path)
    binary = Path(executable)
    if not source.is_file():
        raise FileNotFoundError(f"structure file does not exist: {source}")
    if not binary.is_file():
        raise FileNotFoundError(f"native inspector does not exist: {binary}")
    if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be finite and positive")

    import tempfile

    with tempfile.TemporaryDirectory(prefix="kinetics-native-") as temporary:
        output_path = Path(temporary) / "scene.json"
        completed = subprocess.run(
            [str(binary), str(source), str(output_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            shell=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or "native inspector failed")
        try:
            scene = json.loads(output_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError("native inspector did not produce valid scene JSON") from exc

    if scene.get("schema_version") != SCENE_SCHEMA:
        raise ValueError("unsupported native molecular scene schema")
    if scene.get("coordinate_unit") != "angstrom":
        raise ValueError("native scene coordinates must be expressed in angstrom")
    atoms, bonds = scene.get("atoms"), scene.get("bonds")
    if not isinstance(atoms, list) or not atoms:
        raise ValueError("native scene must contain at least one atom")
    if not isinstance(bonds, list):
        raise ValueError("native scene bonds must be a list")

    serials: set[int] = set()
    for atom in atoms:
        if not isinstance(atom, dict) or not isinstance(atom.get("serial"), int):
            raise ValueError("native scene atom serial is invalid")
        serial = atom["serial"]
        if serial <= 0 or serial in serials:
            raise ValueError("native scene atom serials must be unique positive integers")
        serials.add(serial)
        position = atom.get("position")
        if (
            not isinstance(position, list)
            or len(position) != 3
            or any(
                not isinstance(value, (int, float)) or not math.isfinite(value)
                for value in position
            )
        ):
            raise ValueError("native scene atom coordinates must be three finite numbers")
    for bond in bonds:
        if not isinstance(bond, dict):
            raise ValueError("native scene bond is invalid")
        left, right = bond.get("atom_serial_a"), bond.get("atom_serial_b")
        if left not in serials or right not in serials or left == right:
            raise ValueError("native scene bond references an invalid atom")

    scene["provenance"] = {
        "source_file_name": source.name,
        "source_sha256": sha256_file(source),
        "native_engine_version": scene.get("engine_version"),
        "native_scene_schema": SCENE_SCHEMA,
        "source_coordinate_unit": "angstrom",
    }
    return scene


def build_simulation_plan(
    structure_path: str | Path,
    *,
    engine: str,
    engine_version: str,
    force_field: str,
    water_model: str,
    integrator: str,
    timestep_fs: float,
    steps: int,
    temperature_kelvin: float,
    random_seed: int,
    pressure_bar: float | None = None,
) -> dict[str, Any]:
    """Create a parameterized, provenance-bound plan; never launch a simulation."""
    source = Path(structure_path)
    if not source.is_file():
        raise FileNotFoundError(f"structure file does not exist: {source}")
    normalized_engine = engine.strip().lower()
    if normalized_engine not in SUPPORTED_SIMULATION_ENGINES:
        raise ValueError(f"engine must be one of {sorted(SUPPORTED_SIMULATION_ENGINES)}")
    required = {
        "engine_version": engine_version,
        "force_field": force_field,
        "water_model": water_model,
        "integrator": integrator,
    }
    if any(not isinstance(value, str) or not value.strip() for value in required.values()):
        raise ValueError("engine version, force field, water model and integrator are required")
    if not isinstance(steps, int) or isinstance(steps, bool) or steps <= 0:
        raise ValueError("steps must be a positive integer")
    if (
        not isinstance(random_seed, int)
        or isinstance(random_seed, bool)
        or not 0 <= random_seed <= 2**32 - 1
    ):
        raise ValueError("random_seed must be an unsigned 32-bit integer")
    numeric = {"timestep_fs": timestep_fs, "temperature_kelvin": temperature_kelvin}
    if any(
        not isinstance(value, (int, float)) or not math.isfinite(value)
        for value in numeric.values()
    ):
        raise ValueError("timestep and temperature must be finite numbers")
    if not 0 < timestep_fs <= 10:
        raise ValueError("timestep_fs must be in (0, 10]")
    if not 0 < temperature_kelvin <= 1000:
        raise ValueError("temperature_kelvin must be in (0, 1000]")
    if pressure_bar is not None and (
        not isinstance(pressure_bar, (int, float))
        or not math.isfinite(pressure_bar)
        or pressure_bar < 0
    ):
        raise ValueError("pressure_bar must be finite and non-negative when supplied")

    return {
        "schema_version": "kinetics.simulation-plan/1.0",
        "execution_status": "planned_not_executed",
        "engine": normalized_engine,
        "engine_version": engine_version.strip(),
        "input_structure": {
            "file_name": source.name,
            "sha256": sha256_file(source),
            "coordinate_unit": "angstrom",
        },
        "force_field": force_field.strip(),
        "water_model": water_model.strip(),
        "integrator": integrator.strip(),
        "timestep": {"value": float(timestep_fs), "unit": "femtosecond"},
        "steps": steps,
        "temperature": {"value": float(temperature_kelvin), "unit": "kelvin"},
        "pressure": None if pressure_bar is None else {
            "value": float(pressure_bar), "unit": "bar"
        },
        "random_seed": random_seed,
        "outputs": {
            "trajectory": "trajectory.xtc" if normalized_engine == "gromacs" else "trajectory.dcd",
            "final_structure": "final_structure.pdb",
            "logs": "simulation.log",
        },
        "warning": (
            "Plan only: no simulation engine was launched and no physical result is implied. "
            "Engine-specific input generation and execution require a reviewed adapter."
        ),
    }
