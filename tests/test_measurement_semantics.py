import pytest

from kinetics_core.records import KineticObservation


def test_source_aggregated_observation_requires_declared_method():
    with pytest.raises(ValueError, match="require aggregation_method"):
        KineticObservation(
            target="km", value=1.0, unit="mM", source="CatPred-DB",
            source_record_id="file-row-1", measurement_kind="source_aggregated",
        )


def test_individual_observation_cannot_claim_aggregation_method():
    with pytest.raises(ValueError, match="cannot declare"):
        KineticObservation(
            target="km", value=1.0, unit="mM", source="fixture",
            source_record_id="row-1", aggregation_method="geometric_mean",
        )


def test_source_aggregated_observation_preserves_method():
    record = KineticObservation(
        target="km", value=1.0, unit="mM", source="CatPred-DB",
        source_record_id="file-row-1", measurement_kind="source_aggregated",
        aggregation_method="geometric_mean",
    )
    assert record.as_dict()["measurement_kind"] == "source_aggregated"
    assert record.as_dict()["aggregation_method"] == "geometric_mean"
