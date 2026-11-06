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
        temperature_c_column=None,
        assay_id_column="assay",
        source_version="fixture-v1",
        license_id="CC-BY-4.0",
    )

    accepted = pd.read_csv(accepted_path, dtype={"source_record_id": "string"})
    rejected = pd.read_csv(rejected_path, dtype={"source_record_id": "string"})
    manifest = json.loads(manifest_path.read_text())

    assert accepted["source_record_id"].tolist() == ["0007", "0008"]
    assert accepted["canonical_value"].tolist() == [2.5e-6, 4.0e-6]
    assert accepted["measurement_kind"].tolist() == ["source_aggregated", "source_aggregated"]
    assert accepted["aggregation_method"].iloc[0].startswith("geometric_mean")
    assert accepted["ph"].tolist() == [7.0, 6.5]
    assert accepted["temperature_k"].tolist() == [298.15, 310.0]
    assert accepted["assay_id"].tolist() == ["assay-a", "assay-b"]
    assert accepted["publication_doi"].tolist() == [
        "10.1/example-a", "10.1/example-b"
    ]
    assert len(rejected) == 1
    assert "ph is not numeric" in rejected.loc[0, "reason"]
    assert manifest["mapping"]["ph"] == "ph"
    assert manifest["mapping"]["temperature_k"] == "temp_k"
    assert manifest["mapping"]["assay_id"] == "assay"
    assert manifest["input_rows"] == 3
    assert manifest["accepted_rows"] == 2
    assert manifest["rejected_rows"] == 1



def test_published_catpred_schema_uses_celsius_and_content_addressed_row_locator(tmp_path):
    source = tmp_path / "catpred-km.csv"
    pd.DataFrame({
        "sequence": ["ACDEFG", "ACDEFGH"],
        "sequence_source": ["brenda", "sabio"],
        "uniprot": ["Q12345", "P01234"],
        "substrate_smiles": ["CCO", "CCN"],
        "value": [0.003, 0.02],
        "log10_value": [-2.5229, -1.6990],
        "temperature": [25.0, 37.0],
        "ph": [7.0, 6.5],
        "ec": ["1.1.1.1", "2.7.1.1"],
        "taxonomy_id": [9606, 562],
        "group": ["train", "test"],
        "sequence_40cluster": [11, 12],
    }).to_csv(source, index=False)
    accepted_path, rejected_path, manifest_path = normalize_catpred_csv(
        source, tmp_path / "normalized", target="km", unit="mM",
        source_version="hf-main-fixture", license_id="CC-BY-4.0",
        doi_column=None, assay_id_column=None,
    )
    accepted = pd.read_csv(accepted_path, dtype={"source_record_id": "string"})
    manifest = json.loads(manifest_path.read_text())
    assert len(accepted) == 2
    assert accepted["measurement_kind"].eq("source_aggregated").all()
    assert accepted["aggregation_method"].iloc[0].startswith("geometric_mean")
    assert accepted["temperature_k"].tolist() == [298.15, 310.15]
    assert accepted["protein_accession"].tolist() == ["Q12345", "P01234"]
    assert accepted["smiles"].tolist() == ["CCO", "CCN"]
    assert manifest["mapping"]["substrate_smiles"] == "substrate_smiles"
    assert accepted["source_ec"].tolist() == ["1.1.1.1", "2.7.1.1"]
    assert accepted["source_sequence_40cluster"].tolist() == [11, 12]
    assert accepted["source_record_id"].str.startswith("catpred:").all()
    assert manifest["record_id_origin"] == "generated_content_addressed_file_row_locator"
    assert manifest["mapping"]["temperature_c"] == "temperature"
    assert manifest["mapping"]["doi"] is None
    assert len(pd.read_csv(rejected_path)) == 0


def test_catpred_rejects_ki_and_missing_unit_declaration(tmp_path):
    source = tmp_path / "source.csv"
    pd.DataFrame({"value": [1.0]}).to_csv(source, index=False)
    import pytest

    with pytest.raises(ValueError, match="only km and kcat"):
        normalize_catpred_csv(source, tmp_path / "ki", target="ki", unit="mM")
    with pytest.raises(ValueError, match="units must be verified"):
        normalize_catpred_csv(source, tmp_path / "km", target="km")



def test_catpred_kcat_uses_maximum_aggregate_and_reactant_smiles(tmp_path):
    source = tmp_path / "catpred-kcat.csv"
    pd.DataFrame({
        "sequence": ["ACDEFG"],
        "uniprot": ["Q12345"],
        "reactant_smiles": ["CCO.O"],
        "value": [0.0036],
        "temperature": [30.0],
        "ph": [7.2],
        "ec": ["1.1.1.1"],
        "taxonomy_id": [9606],
    }).to_csv(source, index=False)
    accepted_path, _, manifest_path = normalize_catpred_csv(
        source, tmp_path / "normalized", target="kcat", unit="s^-1",
        source_version="44409e6", license_id="CC-BY-4.0",
    )
    accepted = pd.read_csv(accepted_path)
    manifest = json.loads(manifest_path.read_text())
    assert accepted.loc[0, "smiles"] == "CCO.O"
    assert accepted.loc[0, "canonical_unit"] == "s^-1"
    assert accepted.loc[0, "aggregation_method"].startswith("maximum")
    assert manifest["aggregation_method"].startswith("maximum")
