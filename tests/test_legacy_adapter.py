import pandas as pd
import pytest

from kinetics_core.legacy import paired_frame_to_observations, paired_frame_to_records


def test_legacy_adapter_expands_paired_row_into_independent_targets():
    frame = pd.DataFrame({
        "record_id": ["source-17"],
        "sequence": ["ACDEFG"],
        "smiles": ["CCO"],
        "km": [250.0],
        "kcat": [120.0],
    })

    observations = paired_frame_to_observations(
        frame, source="legacy-csv", source_record_id_column="record_id",
        km_unit="uM", kcat_unit="min^-1",
        source_version="2026-01", license_id="CC-BY-4.0",
    )

    assert [item.target for item in observations] == ["km", "kcat"]
    assert [item.canonical_value() for item in observations] == pytest.approx(
        [250e-6, 2.0]
    )
    assert {item.source_record_id for item in observations} == {"source-17"}
    assert {item.source_version for item in observations} == {"2026-01"}
    assert {item.license_id for item in observations} == {"CC-BY-4.0"}
    assert all(item.sequence == "ACDEFG" and item.smiles == "CCO" for item in observations)


def test_legacy_adapter_preserves_single_available_target():
    frame = pd.DataFrame({
        "record_id": ["source-18"],
        "sequence": ["ACDEFG"],
        "smiles": ["CCO"],
        "km": [None],
        "kcat": [3.0],
    })

    observations = paired_frame_to_observations(
        frame, source="legacy-csv", source_record_id_column="record_id"
    )

    assert len(observations) == 1
    assert observations[0].target == "kcat"


def test_legacy_adapter_requires_explicit_source_record_identity():
    frame = pd.DataFrame({
        "record_id": [None], "sequence": ["ACDEFG"], "smiles": ["CCO"],
        "km": [1.0], "kcat": [2.0],
    })
    with pytest.raises(ValueError, match="source record ID is missing"):
        paired_frame_to_observations(
            frame, source="legacy-csv", source_record_id_column="record_id"
        )


def test_legacy_adapter_reports_invalid_measurement_with_row_context():
    frame = pd.DataFrame({
        "record_id": ["source-19"], "sequence": ["ACDEFG"], "smiles": ["CCO"],
        "km": [0.0], "kcat": [2.0],
    })
    with pytest.raises(ValueError, match="row 0, target 'km'"):
        paired_frame_to_observations(
            frame, source="legacy-csv", source_record_id_column="record_id"
        )


def test_legacy_adapter_exports_canonical_records():
    frame = pd.DataFrame({
        "record_id": ["source-20"], "sequence": ["ACDEFG"], "smiles": ["CCO"],
        "km": [1.0], "kcat": [2.0],
    })
    records = paired_frame_to_records(
        frame, source="legacy-csv", source_record_id_column="record_id"
    )
    assert records[0]["canonical_unit"] == "M"
    assert records[1]["canonical_unit"] == "s^-1"
