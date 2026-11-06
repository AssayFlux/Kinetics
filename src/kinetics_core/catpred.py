"""Normalize CatPred-DB target tables without inventing upstream record identifiers.

CatPred-DB publishes target-specific Km, kcat and Ki tables. This adapter accepts
only Km and kcat, preserves source metadata, and uses a content-addressed file-row
locator when the published table has no native record identifier.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pandas as pd

from .curation import normalize_observation_table
from .provenance import file_record, write_json_atomic


CATPRED_SOURCE = "CatPred-DB"
CATPRED_DATASET_URL = "https://huggingface.co/datasets/RosettaCommons/CatPred-DB"
_SOURCE_CONTEXT_COLUMNS = (
    "sequence_source", "ec", "taxonomy_id", "group", "sequence_20cluster",
    "sequence_40cluster", "sequence_60cluster", "sequence_80cluster",
    "sequence_99cluster", "reactant_smiles", "reaction_smiles", "product_smiles",
    "log10_value", "log10km_mean", "pdbpath",
)


def normalize_catpred_csv(
    input_csv: str | Path,
    output_dir: str | Path,
    *,
    target: str,
    value_column: str = "value",
    unit: str | None = None,
    unit_column: str | None = None,
    record_id_column: str | None = None,
    sequence_column: str | None = "sequence",
    smiles_column: str | None = "reactant_smiles",
    accession_column: str | None = "uniprot",
    organism_column: str | None = None,
    doi_column: str | None = None,
    ph_column: str | None = "ph",
    temperature_k_column: str | None = None,
    temperature_c_column: str | None = "temperature",
    assay_id_column: str | None = None,
    source_version: str | None = None,
    license_id: str | None = None,
) -> tuple[Path, Path, Path]:
    if target not in ("km", "kcat"):
        raise ValueError("CatPred-DB adapter supports only km and kcat; Ki is not Km or kcat")
    source_path = Path(input_csv)
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    if unit is None and unit_column is None:
        raise ValueError("CatPred-DB raw value units must be verified and supplied explicitly")
    if unit is not None and unit_column is not None:
        raise ValueError("Provide either unit or unit_column, not both")
    raw = pd.read_csv(
        source_path,
        dtype={column: "string" for column in (record_id_column, accession_column) if column},
    )
    input_hash = file_record(source_path, CATPRED_DATASET_URL)["sha256"]
    if record_id_column is None:
        raw["__kinetics_source_row_locator"] = [
            f"catpred:{input_hash}:{target}:row:{index}" for index in range(len(raw))
        ]
        record_id_column = "__kinetics_source_row_locator"
        record_id_origin = "generated_content_addressed_file_row_locator"
    else:
        record_id_origin = "upstream_column"
    if temperature_c_column and temperature_k_column:
        raise ValueError("Map temperature in either Celsius or kelvin, not both")
    if temperature_c_column:
        if temperature_c_column not in raw.columns:
            raise ValueError(f"Configured temperature Celsius column does not exist: {temperature_c_column}")
        def to_kelvin(value):
            if pd.isna(value) or str(value).strip() == "":
                return None
            try:
                return float(value) + 273.15
            except (TypeError, ValueError):
                return "invalid_temperature_c"
        raw["__kinetics_temperature_k"] = raw[temperature_c_column].map(to_kelvin)
        temperature_k_column = "__kinetics_temperature_k"
    accepted, rejected = normalize_observation_table(
        raw,
        target=target,
        source=CATPRED_SOURCE,
        source_record_id_column=record_id_column,
        value_column=value_column,
        unit=unit,
        unit_column=unit_column,
        sequence_column=sequence_column,
        smiles_column=smiles_column,
        accession_column=accession_column,
        organism_column=organism_column,
        doi_column=doi_column,
        ph_column=ph_column,
        temperature_k_column=temperature_k_column,
        assay_id_column=assay_id_column,
        source_version=source_version,
        license_id=license_id,
    )
    # Preserve source-specific fields verbatim; do not reinterpret split labels or
    # cluster IDs as newly calculated identities.
    for column in _SOURCE_CONTEXT_COLUMNS:
        if column in raw.columns:
            accepted[f"source_{column}"] = [
                raw.iloc[int(index)][column] for index in accepted["source_row_number"]
            ]
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    normalized_path = output / f"{target}_observations.csv"
    rejected_path = output / f"{target}_rejected_rows.csv"
    manifest_path = output / f"{target}_curation_manifest.json"
    if any(path.exists() for path in (normalized_path, rejected_path, manifest_path)):
        raise FileExistsError("CatPred output exists; choose a new output directory")
    accepted.to_csv(normalized_path, index=False)
    rejected.to_csv(rejected_path, index=False)
    manifest = {
        "schema_version": "2.0",
        "dataset": CATPRED_SOURCE,
        "dataset_url": CATPRED_DATASET_URL,
        "target": target,
        "canonical_unit": "M" if target == "km" else "s^-1",
        "source_file": file_record(source_path, CATPRED_DATASET_URL),
        "source_version": source_version,
        "license_note": license_id,
        "record_id_origin": record_id_origin,
        "record_id_column": record_id_column,
        "mapping": {
            "value": value_column, "unit": unit, "unit_column": unit_column,
            "sequence": sequence_column, "substrate_smiles": smiles_column,
            "accession": accession_column, "organism": organism_column,
            "doi": doi_column, "ph": ph_column,
            "temperature_k": temperature_k_column,
            "temperature_c": temperature_c_column,
            "assay_id": assay_id_column,
            "source_context_preserved": [c for c in _SOURCE_CONTEXT_COLUMNS if c in raw.columns],
        },
        "input_rows": int(len(raw)),
        "accepted_rows": int(len(accepted)),
        "rejected_rows": int(len(rejected)),
        "normalized_file": normalized_path.name,
        "rejected_file": rejected_path.name,
        "policy": (
            "Km and kcat imported independently. Generated row locators are not upstream "
            "record IDs. CatPred temperature Celsius is converted to kelvin. Raw source "
            "values and source columns are retained; no DOI, organism, or assay ID inferred."
        ),
    }
    write_json_atomic(manifest, manifest_path)
    return normalized_path, rejected_path, manifest_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", default="data/processed/catpred-db")
    parser.add_argument("--target", choices=["km", "kcat"], required=True)
    parser.add_argument("--record-id-column")
    parser.add_argument("--value-column", default="value")
    parser.add_argument("--unit")
    parser.add_argument("--unit-column")
    parser.add_argument("--sequence-column", default="sequence")
    parser.add_argument("--smiles-column", default="reactant_smiles")
    parser.add_argument("--accession-column", default="uniprot")
    parser.add_argument("--organism-column")
    parser.add_argument("--doi-column")
    parser.add_argument("--ph-column", default="ph")
    parser.add_argument("--temperature-k-column")
    parser.add_argument("--temperature-c-column", default="temperature")
    parser.add_argument("--assay-id-column")
    parser.add_argument("--source-version", required=True)
    parser.add_argument("--license-id", required=True)
    args = parser.parse_args()
    outputs = normalize_catpred_csv(
        args.input, args.output_dir, target=args.target,
        record_id_column=args.record_id_column, value_column=args.value_column,
        unit=args.unit, unit_column=args.unit_column,
        sequence_column=args.sequence_column, smiles_column=args.smiles_column,
        accession_column=args.accession_column, organism_column=args.organism_column,
        doi_column=args.doi_column, ph_column=args.ph_column,
        temperature_k_column=args.temperature_k_column,
        temperature_c_column=args.temperature_c_column,
        assay_id_column=args.assay_id_column,
        source_version=args.source_version, license_id=args.license_id,
    )
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
