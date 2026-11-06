import json

import pandas as pd
import pytest

from kinetics_core.identity import normalize_biomolecular_identities
from kinetics_core.release import create_dataset_release, verify_dataset_release
from kinetics_core.quality import review_potential_duplicate_observations


def _observations(path):
    pd.DataFrame({
        "target": ["km", "km", "kcat"],
        "value": [2.0, 2.0, 4.0],
        "unit": ["uM", "uM", "s^-1"],
        "canonical_value": [2e-6, 2e-6, 4.0],
        "canonical_unit": ["M", "M", "s^-1"],
        "source": ["fixture"] * 3,
        "source_record_id": ["a", "a", "c"],
    }).to_csv(path, index=False)


def test_identity_normalization_is_deterministic_and_audits_invalid_inputs():
    frame = pd.DataFrame({
        "source_record_id": ["one", "two"],
        "sequence": [" acd ef ", "ACD*"],
        "smiles": ["CCO", "not-smiles"],
    })
    accepted, rejected = normalize_biomolecular_identities(frame)
    assert len(accepted) == 1
    assert accepted.iloc[0]["sequence_normalized"] == "ACDEF"
    assert len(accepted.iloc[0]["protein_content_id"]) == 64
    assert accepted.iloc[0]["smiles_canonical"] == "CCO"
    assert len(rejected) == 1
    assert "invalid amino-acid" in rejected.iloc[0]["reason"]


def test_release_requires_license_and_citation(tmp_path):
    observations, rejected = tmp_path / "observations.csv", tmp_path / "rejected.csv"
    _observations(observations)
    pd.DataFrame(columns=["source_row_number", "reason"]).to_csv(rejected, index=False)
    with pytest.raises(ValueError, match="license_id"):
        create_dataset_release(
            observations, rejected, tmp_path / "release",
            dataset_id="fixture-v1", dataset_name="Fixture", source="fixture",
            source_version="v1", license_id="", citation="fixture citation",
        )


def test_release_manifest_verifies_and_detects_tampering(tmp_path):
    observations, rejected = tmp_path / "observations.csv", tmp_path / "rejected.csv"
    _observations(observations)
    pd.DataFrame(columns=["source_row_number", "reason"]).to_csv(rejected, index=False)
    release = tmp_path / "release-v1"
    result = create_dataset_release(
        observations, rejected, release,
        dataset_id="fixture-v1", dataset_name="Fixture", source="fixture",
        source_version="v1", license_id="MIT", citation="fixture citation",
    )
    assert result["verified"] is True
    manifest = json.loads((release / "release_manifest.json").read_text())
    assert manifest["counts"]["observations"] == 3
    assert manifest["counts"]["duplicate_groups"] >= 1
    with pytest.raises(FileExistsError):
        create_dataset_release(
            observations, rejected, release,
            dataset_id="fixture-v1", dataset_name="Fixture", source="fixture",
            source_version="v1", license_id="MIT", citation="fixture citation",
        )
    (release / "observations.csv").write_text("tampered")
    with pytest.raises(ValueError, match="checksum mismatch"):
        verify_dataset_release(release)



def test_cross_source_duplicate_candidates_are_reported_not_removed():
    frame = pd.DataFrame({
        "target": ["km", "km", "km"],
        "source": ["source-a", "source-b", "source-c"],
        "source_record_id": ["a-1", "b-9", "c-2"],
        "canonical_value": [1e-3, 1e-3, 2e-3],
        "canonical_unit": ["M", "M", "M"],
        "sequence_normalized": ["ACDEFG", "ACDEFG", "ACDEFG"],
        "smiles_canonical": ["CCO", "CCO", "CCN"],
        "ph": [7.0, 7.0, 7.0],
        "temperature_k": [298.15, 298.15, 298.15],
    })
    candidates = review_potential_duplicate_observations(frame)
    assert len(candidates) == 1
    assert candidates.iloc[0]["sources"] == '["source-a", "source-b"]'
    assert bool(candidates.iloc[0]["review_required"])
    assert len(frame) == 3



def test_identity_cli_writes_manifest_and_row_level_rejections(tmp_path):
    from kinetics_core.cli import main

    source = tmp_path / "observations.csv"
    pd.DataFrame({
        "source_record_id": ["valid", "invalid"],
        "sequence": ["ACDEFG", "ACD*"],
        "smiles": ["CCO", "CCN"],
    }).to_csv(source, index=False)
    output = tmp_path / "identities"
    assert main([
        "normalize-identities", "--input", str(source), "--output-dir", str(output)
    ]) == 0
    accepted = pd.read_csv(output / "observations_with_identities.csv")
    rejected = pd.read_csv(output / "identity_rejected_rows.csv")
    manifest = json.loads((output / "identity_manifest.json").read_text())
    assert len(accepted) == 1
    assert len(rejected) == 1
    assert manifest["input_rows"] == 2
    assert len(manifest["outputs"]["observations_with_identities.csv"]["sha256"]) == 64
