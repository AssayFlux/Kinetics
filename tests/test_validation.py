import numpy as np
import pytest

from kinetics_core.validation import bootstrap_regression_intervals


def test_bootstrap_intervals_are_reproducible_and_well_formed():
    truth = np.asarray([-3.0, -2.5, -2.0, -1.5, -1.0])
    prediction = np.asarray([-2.9, -2.7, -1.8, -1.6, -1.2])
    first = bootstrap_regression_intervals(
        truth, prediction, target="km", n_resamples=200, random_state=17,
    )
    second = bootstrap_regression_intervals(
        truth, prediction, target="km", n_resamples=200, random_state=17,
    )
    assert first == second
    assert first["sample_size"] == 5
    assert first["method"] == "paired_row_percentile_bootstrap"
    for metric in ("mae", "rmse"):
        interval = first["log10_metric_intervals"][metric]
        assert interval["lower"] <= interval["upper"]
        assert np.isfinite([interval["lower"], interval["upper"]]).all()


@pytest.mark.parametrize("kwargs", [
    {"n_resamples": 99},
    {"confidence_level": 1.0},
])
def test_bootstrap_rejects_invalid_configuration(kwargs):
    with pytest.raises(ValueError):
        bootstrap_regression_intervals([1, 2], [1, 2], target="km", **kwargs)


def test_bootstrap_rejects_nonfinite_or_misaligned_data():
    with pytest.raises(ValueError, match="equal length"):
        bootstrap_regression_intervals([1, 2], [1], target="kcat")
    with pytest.raises(ValueError, match="finite"):
        bootstrap_regression_intervals([1, np.nan], [1, 2], target="kcat")


def test_cluster_bootstrap_intervals_are_reproducible_and_group_aware():
    from kinetics_core.validation import bootstrap_cluster_regression_intervals

    truth = np.asarray([-3.0, -2.8, -2.5, -1.8, -1.5, -1.2])
    prediction = np.asarray([-2.9, -2.7, -2.6, -1.9, -1.4, -1.1])
    clusters = np.asarray(["p1", "p1", "p1", "p2", "p2", "p2"])
    first = bootstrap_cluster_regression_intervals(
        truth, prediction, clusters, target="km", n_resamples=200, random_state=9,
    )
    second = bootstrap_cluster_regression_intervals(
        truth, prediction, clusters, target="km", n_resamples=200, random_state=9,
    )
    assert first == second
    assert first["cluster_count"] == 2
    assert first["method"] == "paired_cluster_percentile_bootstrap"
    for metric in ("mae", "rmse"):
        interval = first["log10_metric_intervals"][metric]
        assert interval["lower"] <= interval["upper"]
        assert np.isfinite([interval["lower"], interval["upper"]]).all()


def test_cluster_bootstrap_rejects_bad_groups():
    from kinetics_core.validation import bootstrap_cluster_regression_intervals

    with pytest.raises(ValueError, match="align"):
        bootstrap_cluster_regression_intervals([1, 2], [1, 2], ["a"], target="km")
    with pytest.raises(ValueError, match="at least two clusters"):
        bootstrap_cluster_regression_intervals([1, 2], [1, 2], ["a", "a"], target="km")
