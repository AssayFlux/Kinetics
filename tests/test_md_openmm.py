from __future__ import annotations

import pytest

from kinetics.md_openmm import run_openmm_dynamics


def _arguments() -> dict[str, object]:
    return {
        "coordinates_sha256": "a" * 64,
        "topology_sha256": "b" * 64,
        "force_field_name": "synthetic",
        "force_field_version": "1",
        "parameter_source_sha256": "c" * 64,
        "temperature_kelvin": 300.0,
        "timestep_fs": 1.0,
        "steps": 100,
        "equilibration_steps": 10,
        "replicas": 2,
        "seed": 1,
        "report_interval": 10,
    }


@pytest.mark.parametrize(
    ("key", "value", "message"),
    [
        ("coordinates_sha256", "bad", "SHA-256"),
        ("timestep_fs", 5.0, "timestep_fs"),
        ("temperature_kelvin", 0.0, "temperature_kelvin"),
        ("steps", 0, "steps"),
        ("replicas", 1, "replicas"),
        ("seed", 2**32 - 1, "seed"),
        ("report_interval", 101, "report_interval"),
        ("cpu_threads", 0, "cpu_threads"),
        ("pressure_bar", 0.0, "pressure_bar"),
    ],
)
def test_openmm_runner_rejects_invalid_protocol_before_loading_engine(
    key: str, value: object, message: str
) -> None:
    arguments = _arguments()
    arguments[key] = value
    with pytest.raises(ValueError, match=message):
        run_openmm_dynamics(object(), object(), object(), **arguments)  # type: ignore[arg-type]
