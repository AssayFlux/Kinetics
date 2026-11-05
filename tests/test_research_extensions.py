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


from kinetics_core.quality import audit_observations


def test_quality_audit_flags_conflicting_duplicate_without_dropping_rows():
    frame = pd.DataFrame({
        "target": ["km", "km", "kcat"],
        "source": ["db", "db", "db"],
        "source_record_id": ["r1", "r1", "r1"],
        "canonical_value": [1e-3, 2e-3, 2.0],
        "canonical_unit": ["M", "M", "s^-1"],
        "sequence": ["AAAA", "AAAA", None],
    })
    annotated, audit, report = audit_observations(frame)
    assert len(annotated) == 3
    assert len(audit) == 1
    assert audit.iloc[0]["status"] == "conflicting_duplicate"
    assert report["n_conflicting_groups"] == 1
    assert annotated.loc[0, "duplicate_status"] == "conflicting_duplicate"
    assert annotated.loc[2, "duplicate_status"] == "unique"
