import json

import pandas as pd

from kinetics_core.catpred import normalize_catpred_csv


def test_catpred_adapter_preserves_opaque_ids_and_assay_context(tmp_path):
    source = tmp_path / "km.csv"
    pd.DataFrame({
        "record_id": ["0007", "0008", "0009"],
        "measurement": [2.5, 4.0, 1.0],
        "unit": ["uM", "uM", "uM"],
        "sequence": ["AAAA", "BBBB", "CCCC"],
        "smiles": ["CCO", "CCN", "CCC"],
        "ph": [7.0, 6.5, "not-reported"],
        "temp_k": [298.15, 310.0, 300.0],
        "assay": ["assay-a", "assay-b", "assay-c"],
        "doi": ["10.1/example-a", "10.1/example-b", "10.1/example-c"],
    }).to_csv(source, index=False)

    accepted_path, rejected_path, manifest_path = normalize_catpred_csv(
        source,
        tmp_path / "normalized",
        target="km",
        record_id_column="record_id",
        value_column="measurement",
        unit_column="unit",
        sequence_column="sequence",
        smiles_column="smiles",
        doi_column="doi",
        ph_column="ph",
        temperature_k_column="temp_k",
        assay_id_column="assay",
        source_version="fixture-v1",
        license_id="CC-BY-4.0",
    )

    accepted = pd.read_csv(accepted_path, dtype={"source_record_id": "string"})
    rejected = pd.read_csv(rejected_path, dtype={"source_record_id": "string"})
    manifest = json.loads(manifest_path.read_text())

    assert accepted["source_record_id"].tolist() == ["0007", "0008"]
    assert accepted["canonical_value"].tolist() == [2.5e-6, 4.0e-6]
    assert accepted["ph"].tolist() == [7.0, 6.5]
    assert accepted["temperature_k"].tolist() == [298.15, 310.0]
    assert accepted["assay_id"].tolist() == ["assay-a", "assay-b"]
    assert accepted["publication_doi"].tolist() == [
        "10.1/example-a", "10.1/example-b"
    ]
    assert len(rejected) == 1
    assert "ph is non-finite" in rejected.loc[0, "reason"]
    assert manifest["mapping"]["ph"] == "ph"
    assert manifest["mapping"]["temperature_k"] == "temp_k"
    assert manifest["mapping"]["assay_id"] == "assay"
    assert manifest["input_rows"] == 3
    assert manifest["accepted_rows"] == 2
    assert manifest["rejected_rows"] == 1
