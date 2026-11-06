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
