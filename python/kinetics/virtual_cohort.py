"""Synthetic-only aggregate genotype frequency simulation for research software tests.

This module does not read patient data, infer ancestry, estimate clinical risk or
model variant effects. Hardy-Weinberg equilibrium is an explicit assumption.
"""
from __future__ import annotations

import random
from math import isfinite


def simulate_hardy_weinberg_cohort(
    allele_frequencies: dict[str, float],
    *,
    sample_size: int,
    seed: int,
) -> dict[str, object]:
    """Generate aggregate synthetic diploid genotype counts for independent loci."""
    valid_size = (
        isinstance(sample_size, int)
        and not isinstance(sample_size, bool)
        and 1 <= sample_size <= 1_000_000
    )
    if not valid_size:
        raise ValueError("sample_size must be an integer between 1 and 1000000")
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= 2**32 - 1:
        raise ValueError("seed must be an unsigned 32-bit integer")
    if (
        not isinstance(allele_frequencies, dict)
        or not allele_frequencies
        or len(allele_frequencies) > 1000
    ):
        raise ValueError("allele_frequencies must contain 1 to 1000 loci")
    normalized: dict[str, float] = {}
    for locus, frequency in allele_frequencies.items():
        if not isinstance(locus, str) or not locus or len(locus) > 128:
            raise ValueError(
                "locus identifiers must be non-empty strings of at most 128 characters"
            )
        if (
            not isinstance(frequency, (int, float))
            or isinstance(frequency, bool)
            or not isfinite(frequency)
        ):
            raise ValueError(f"allele frequency for {locus} must be finite")
        if not 0.0 <= frequency <= 1.0:
            raise ValueError(f"allele frequency for {locus} must be between 0 and 1")
        normalized[locus] = float(frequency)

    if sample_size * len(normalized) > 10_000_000:
        raise ValueError("sample_size times locus count must not exceed 10000000")

    rng = random.Random(seed)
    results: list[dict[str, object]] = []
    for locus in sorted(normalized):
        p = normalized[locus]
        q = 1.0 - p
        observed = [0, 0, 0]
        for _ in range(sample_size):
            genotype = int(rng.random() < p) + int(rng.random() < p)
            observed[genotype] += 1
        expected = [sample_size * q * q, sample_size * 2.0 * p * q, sample_size * p * p]
        results.append({
            "locus_id": locus,
            "alternate_allele_frequency": p,
            "reference_allele_frequency": q,
            "genotype_order": ["reference_homozygous", "heterozygous", "alternate_homozygous"],
            "observed_synthetic_counts": observed,
            "expected_hardy_weinberg_counts": expected,
        })
    return {
        "schema_version": 1,
        "simulation": "independent-locus Hardy-Weinberg synthetic aggregate cohort",
        "data_classification": "synthetic_non_patient",
        "sample_size": sample_size,
        "seed": seed,
        "loci": results,
        "assumptions": [
            "Diploid autosomal loci with caller-supplied allele frequencies",
            "Hardy-Weinberg equilibrium within the synthetic population",
            "Independent loci; linkage disequilibrium and haplotypes are not modelled",
            "No ancestry, population structure, relatedness, selection or missingness",
        ],
        "limitations": [
            "Synthetic aggregate counts only; no individual-level genotypes are returned",
            "No variant-effect, disease-risk, penetrance or phenotype model is implemented",
            "Not representative of any real population or cohort",
            "No clinical interpretation, diagnosis, treatment or risk estimate",
        ],
        "provenance": {
            "generator": "Kinetics synthetic HWE generator",
            "seeded_prng": "Python random.Random",
        },
    }
