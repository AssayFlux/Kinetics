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


def test_import_legacy_cli_writes_canonical_csv_and_provenance_manifest(tmp_path):
    import json

    from kinetics_core.cli import main

    source = tmp_path / "legacy.csv"
    output = tmp_path / "canonical" / "observations.csv"
    pd.DataFrame({
        "source_id": ["row-1", "row-2"],
        "sequence": ["ACDEFG", "MKWVTF"],
        "smiles": ["CCO", "CCN"],
        "km": [100.0, None],
        "kcat": [60.0, 120.0],
    }).to_csv(source, index=False)

    exit_code = main([
        "import-legacy",
        "--input", str(source),
        "--output", str(output),
        "--source", "legacy-dataset",
        "--source-record-id-column", "source_id",
        "--km-unit", "uM",
        "--kcat-unit", "min^-1",
        "--source-version", "v1",
        "--license-id", "CC-BY-4.0",
    ])

    assert exit_code == 0
    canonical = pd.read_csv(output)
    assert canonical["target"].tolist() == ["km", "kcat", "kcat"]
    assert canonical["canonical_unit"].tolist() == ["M", "s^-1", "s^-1"]
    manifest = json.loads(output.with_suffix(".csv.manifest.json").read_text())
    assert manifest["n_input_rows"] == 2
    assert manifest["n_observations"] == 3
    assert manifest["target_counts"] == {"kcat": 2, "km": 1}
    assert len(manifest["input"]["sha256"]) == 64
    assert len(manifest["output"]["sha256"]) == 64


def test_import_legacy_cli_refuses_to_overwrite_raw_input(tmp_path):
    from kinetics_core.cli import main

    source = tmp_path / "legacy.csv"
    pd.DataFrame({
        "source_id": ["row-1"], "sequence": ["ACDEFG"], "smiles": ["CCO"],
        "km": [1.0], "kcat": [2.0],
    }).to_csv(source, index=False)

    with pytest.raises(ValueError, match="differ from the raw input"):
        main([
            "import-legacy", "--input", str(source), "--output", str(source),
            "--source", "legacy-dataset", "--source-record-id-column", "source_id",
        ])


def test_legacy_adapter_rejects_empty_input():
    with pytest.raises(ValueError, match="contains no rows"):
        paired_frame_to_observations(
            pd.DataFrame(columns=["record_id", "sequence", "smiles", "km", "kcat"]),
            source="legacy-csv", source_record_id_column="record_id",
        )
