import numpy as np
import pandas as pd
import pytest

from kinetics_core.applicability import ApplicabilityDomain
from kinetics_core.context import AssayContextEncoder
from kinetics_core.uncertainty import conformal_interval, conformal_quantile


def test_context_encoder_ignores_unselected_identifier_and_handles_unknown_category():
    train = pd.DataFrame({
        "ph": [6.0, 7.0, None],
        "temperature_k": [298.0, 303.0, 310.0],
        "organism": ["A", "B", "A"],
        "source_record_id": ["r1", "r2", "r3"],
    })
    encoder = AssayContextEncoder(
        numeric_columns=("ph", "temperature_k"),
        categorical_columns=("organism",),
    ).fit(train)
    test = pd.DataFrame({
        "ph": [6.5],
        "temperature_k": [300.0],
        "organism": ["unseen"],
        "source_record_id": ["test-id"],
    })
    encoded = encoder.transform(test)
    assert encoded.shape[0] == 1
    assert np.isfinite(encoded).all()
    assert "source_record_id" not in " ".join(encoder.get_feature_names_out())


def test_context_encoder_rejects_missing_configured_column():
    encoder = AssayContextEncoder(
        numeric_columns=("ph",), categorical_columns=()
    )
    with pytest.raises(ValueError, match="missing configured"):
        encoder.fit(pd.DataFrame({"temperature_k": [298.0, 300.0]}))


def test_conformal_quantile_and_original_unit_interval():
    q = conformal_quantile([1.0, 2.0, 3.0], [1.1, 1.8, 3.2], alpha=0.1)
    assert q == pytest.approx(0.2)
    result = conformal_interval(np.asarray([2.0]), q, target="km")
    assert result["canonical_unit"] == "M"
    assert result["lower"][0] == pytest.approx(10**1.8)
    assert result["upper"][0] == pytest.approx(10**2.2)


def test_applicability_domain_flags_far_query():
    reference = np.asarray([[0.0, 0.0], [0.1, 0.0], [0.0, 0.1], [0.1, 0.1]])
    monitor = ApplicabilityDomain(quantile=0.75).fit(reference)
    near = monitor.score([[0.05, 0.05]])
    far = monitor.score([[100.0, 100.0]])
    assert bool(near["within_domain"][0])
    assert not bool(far["within_domain"][0])
    assert "not a probability" in near["interpretation"]
