from __future__ import annotations

import pytest

from kinetics.virtual_cohort import simulate_hardy_weinberg_cohort


def test_synthetic_cohort_is_reproducible_aggregate_and_conserves_counts() -> None:
    args = {"rsSynthetic1": 0.2, "rsSynthetic2": 0.5}
    first = simulate_hardy_weinberg_cohort(args, sample_size=5000, seed=42)
    second = simulate_hardy_weinberg_cohort(args, sample_size=5000, seed=42)
    assert first == second
    assert first["data_classification"] == "synthetic_non_patient"
    for locus in first["loci"]:
        assert sum(locus["observed_synthetic_counts"]) == 5000
        assert len(locus["expected_hardy_weinberg_counts"]) == 3
    assert "No variant-effect" in first["limitations"][1]


@pytest.mark.parametrize(
    ("frequencies", "sample_size", "seed"),
    [
        ({}, 10, 1),
        ({"rs1": -0.1}, 10, 1),
        ({"rs1": 1.1}, 10, 1),
        ({"rs1": float("nan")}, 10, 1),
        ({"rs1": 0.5}, 0, 1),
        ({"rs1": 0.5}, 10, -1),
        ({"rs1": 0.5}, 10, True),
    ],
)
def test_synthetic_cohort_rejects_invalid_inputs(
    frequencies: dict[str, float], sample_size: int, seed: int
) -> None:
    with pytest.raises(ValueError):
        simulate_hardy_weinberg_cohort(frequencies, sample_size=sample_size, seed=seed)


def test_synthetic_cohort_caps_total_genotype_draws() -> None:
    with pytest.raises(ValueError, match="locus count"):
        simulate_hardy_weinberg_cohort(
            {f"locus_{index}": 0.5 for index in range(11)},
            sample_size=1_000_000,
            seed=1,
        )
