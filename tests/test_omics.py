from __future__ import annotations

import math

import pytest

from kinetics.omics import (
    clr_transform, cpm, cross_omics_correlation, logistic_growth,
    log2_fold_change, pearson, shannon_diversity, simpson_diversity,
)


def test_count_normalisation_and_compositional_transform() -> None:
    values = cpm([[10, 30], [30, 70]])
    assert [sum(row[j] for row in values) for j in range(2)] == pytest.approx([1e6, 1e6])
    transformed = clr_transform([[1, 2], [3, 4]])
    assert [sum(row[j] for row in transformed) for j in range(2)] == pytest.approx([0, 0])


def test_diversity_metrics_use_relative_abundance() -> None:
    assert shannon_diversity([1, 1]) == pytest.approx(math.log(2))
    assert simpson_diversity([1, 1]) == pytest.approx(0.5)
    assert simpson_diversity([0.25, 0.25, 0.5]) == pytest.approx(0.625)


def test_omics_models_and_cross_matrix_correlation() -> None:
    assert log2_fold_change([4, 4], [2, 2]) > 0
    assert pearson([1, 2, 3], [2, 4, 6]) == pytest.approx(1)
    matrix = cross_omics_correlation([[1, 2, 3]], [[3, 2, 1], [1, 2, 3]])
    assert matrix[0] == pytest.approx([-1, 1])
    assert logistic_growth([0, 1], [1, 2], carrying_capacity=100, growth_rate=0.5, initial=1)[0] == 1


@pytest.mark.parametrize("bad", [float("nan"), float("inf")])
def test_omics_rejects_non_finite_inputs(bad: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        cpm([[1, bad]])
    with pytest.raises(ValueError, match="finite"):
        pearson([1, 2, bad], [1, 2, 3])
    with pytest.raises(ValueError, match="finite"):
        logistic_growth([0, bad], [1, 2], carrying_capacity=10, growth_rate=1, initial=1)


def test_omics_rejects_zero_library_and_constant_correlation() -> None:
    with pytest.raises(ValueError, match="zero-library"):
        cpm([[0, 1], [0, 2]])
    with pytest.raises(ValueError, match="constant"):
        pearson([1, 1, 1], [1, 2, 3])
