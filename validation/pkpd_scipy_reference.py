"""Independent SciPy ODE comparison for the closed-form PK reference model."""
from __future__ import annotations

import json

import numpy as np
from scipy.integrate import solve_ivp

from kinetics.pkpd import one_compartment_oral_pk


def compare_case(*, ka: float, ke: float) -> dict[str, object]:
    dose = 100.0
    bioavailability = 0.75
    volume = 20.0
    times = np.asarray([0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0])
    result = one_compartment_oral_pk(
        times.tolist(),
        dose_amount_mg=dose,
        bioavailability_fraction=bioavailability,
        absorption_rate_per_h=ka,
        elimination_rate_per_h=ke,
        apparent_volume_l=volume,
    )
    initial = [bioavailability * dose, 0.0]

    def derivative(_time: float, state: list[float]) -> list[float]:
        depot, central = state
        return [-ka * depot, ka * depot - ke * central]

    reference = solve_ivp(
        derivative,
        (0.0, float(times[-1])),
        initial,
        t_eval=times,
        method="DOP853",
        rtol=1e-11,
        atol=1e-12,
    )
    if not reference.success:
        raise SystemExit(f"SciPy reference integration failed: {reference.message}")
    reference_concentration = reference.y[1] / volume
    analytic_concentration = np.asarray(
        [row["concentration_mg_per_l"] for row in result["observations"]]
    )
    absolute_error = np.abs(analytic_concentration - reference_concentration)
    max_absolute_error = float(np.max(absolute_error))
    passed = bool(np.allclose(analytic_concentration, reference_concentration, rtol=1e-8, atol=1e-10))
    return {
        "ka_per_h": ka,
        "ke_per_h": ke,
        "max_absolute_error_mg_per_l": max_absolute_error,
        "relative_tolerance": 1e-8,
        "absolute_tolerance_mg_per_l": 1e-10,
        "pass": passed,
    }


def main() -> None:
    cases = [
        compare_case(ka=1.5, ke=0.2),
        compare_case(ka=0.5, ke=0.5),
        compare_case(ka=0.2, ke=1.5),
    ]
    report = {
        "validation_id": "pkpd-oral-one-compartment-scipy-ode-v1",
        "overall_pass": all(case["pass"] for case in cases),
        "reference": "SciPy solve_ivp DOP853 two-state depot/central ODE",
        "cases": cases,
        "limitations": [
            "Numerical software cross-check only; not experimental PK validation",
            "Does not validate caller-supplied dose, bioavailability, rates or volume",
            "No population, species, compound, safety or clinical applicability is established",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["overall_pass"]:
        raise SystemExit("Closed-form PK result disagreed with independent SciPy ODE reference")


if __name__ == "__main__":
    main()
