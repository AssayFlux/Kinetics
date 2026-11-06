import json
import sqlite3

import pandas as pd
import pytest

from kinetics_core.cli import main
from kinetics_core.persistence import persist_observation_csv


def test_import_audit_persist_pipeline_preserves_independent_targets_and_provenance(tmp_path):
    raw = tmp_path / "paired.csv"
    canonical = tmp_path / "canonical.csv"
    audited_dir = tmp_path / "audited"
    database = tmp_path / "research.sqlite3"
    pd.DataFrame({
        "source_id": ["00017", "00018"],
        "sequence": ["ACDEFG", "MKWVTF"],
        "smiles": ["CCO", "CCN"],
        "km": [250.0, None],
        "kcat": [120.0, 60.0],
    }).to_csv(raw, index=False)

    assert main([
        "import-legacy", "--input", str(raw), "--output", str(canonical),
        "--source", "fixture-source", "--source-record-id-column", "source_id",
        "--km-unit", "uM", "--kcat-unit", "min^-1",
        "--source-version", "release-1", "--license-id", "CC-BY-4.0",
    ]) == 0
    assert main([
        "audit", "--input", str(canonical), "--output-dir", str(audited_dir),
    ]) == 0
    audited = audited_dir / "observations_audited.csv"
    assert main([
        "persist", "--input", str(audited), "--database", str(database),
        "--dataset-id", "fixture-release-1", "--name", "Fixture dataset",
        "--source", "fixture-source", "--version", "release-1",
        "--license-id", "CC-BY-4.0", "--citation", "doi:10.example/fixture",
    ]) == 0

    with sqlite3.connect(database) as connection:
        dataset = connection.execute(
            "SELECT checksum_sha256, license FROM datasets WHERE dataset_id = ?",
            ("fixture-release-1",),
        ).fetchone()
        measurements = connection.execute(
            "SELECT measurement_type, value, unit, metadata_json "
            "FROM measurements ORDER BY measurement_type, measurement_id"
        ).fetchall()
        events = connection.execute(
            "SELECT event_type FROM provenance_events WHERE subject_id = ?",
            ("fixture-release-1",),
        ).fetchall()

    assert len(dataset[0]) == 64
    assert dataset[1] == "CC-BY-4.0"
    assert len(measurements) == 3
    assert {row[0] for row in measurements} == {"km", "kcat"}
    km = next(row for row in measurements if row[0] == "km")
    assert km[1] == pytest.approx(250e-6)
    assert km[2] == "M"
    metadata = json.loads(km[3])
    assert metadata["source_record_id"] == "00017"
    assert metadata["original_value"] == 250.0
    assert metadata["original_unit"] == "uM"
    assert metadata["license_id"] == "CC-BY-4.0"
    assert events == [("canonical_observation_import",)]


def test_persistence_is_idempotent_and_rejects_changed_snapshot(tmp_path):
    source = tmp_path / "observations.csv"
    pd.DataFrame({
        "source": ["fixture"], "source_record_id": ["001"],
        "target": ["km"], "value": [2.0], "unit": ["uM"],
        "canonical_value": [2e-6], "canonical_unit": ["M"],
    }).to_csv(source, index=False)
    database = tmp_path / "research.sqlite3"
    args = {
        "dataset_id": "snapshot-1", "name": "Snapshot", "source": "fixture",
        "license_id": "CC0-1.0",
    }

    first = persist_observation_csv(source, database, **args)
    second = persist_observation_csv(source, database, **args)
    assert first["n_inserted"] == 1
    assert second["n_inserted"] == 0
    assert second["idempotent_replay"] is True

    frame = pd.read_csv(source)
    frame.loc[0, "canonical_value"] = 3e-6
    frame.to_csv(source, index=False)
    with pytest.raises(ValueError, match="different source metadata or content"):
        persist_observation_csv(source, database, **args)
