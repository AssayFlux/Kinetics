"""Normalize one CatPred-DB target table using explicit source-column mappings.

CatPred-DB publishes Km and kcat as separate tables. Run this adapter separately
for each target; it intentionally does not join those tables.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .curation import normalize_observation_table
from .provenance import file_record, write_json_atomic


CATPRED_SOURCE = "CatPred-DB"
CATPRED_DATASET_URL = "https://huggingface.co/datasets/RosettaCommons/CatPred-DB"


def normalize_catpred_csv(
    input_csv: str | Path,
    output_dir: str | Path,
    *,
    target: str,
    record_id_column: str,
    value_column: str,
    unit: str,
    sequence_column: str | None = None,
    smiles_column: str | None = None,
    accession_column: str | None = None,
    organism_column: str | None = None,
    doi_column: str | None = None,
    source_version: str | None = None,
    license_id: str = "CC-BY-4.0 (verify current source terms)",
) -> tuple[Path, Path, Path]:
    source_path = Path(input_csv)
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    raw = pd.read_csv(source_path)
    accepted, rejected = normalize_observation_table(
        raw,
        target=target,
        source=CATPRED_SOURCE,
        source_record_id_column=record_id_column,
        value_column=value_column,
        unit=unit,
        sequence_column=sequence_column,
        smiles_column=smiles_column,
        accession_column=accession_column,
        organism_column=organism_column,
        doi_column=doi_column,
        source_version=source_version,
        license_id=license_id,
    )
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    normalized_path = output / f"{target}_observations.csv"
    rejected_path = output / f"{target}_rejected_rows.csv"
    manifest_path = output / f"{target}_curation_manifest.json"
    accepted.to_csv(normalized_path, index=False)
    rejected.to_csv(rejected_path, index=False)
    manifest = {
        "schema_version": "1.0",
        "dataset": CATPRED_SOURCE,
        "dataset_url": CATPRED_DATASET_URL,
        "target": target,
        "canonical_unit": "M" if target == "km" else "s^-1",
        "source_file": file_record(source_path),
        "source_version": source_version,
        "license_note": license_id,
        "mapping": {
            "record_id": record_id_column,
            "value": value_column,
            "unit": unit,
            "sequence": sequence_column,
            "smiles": smiles_column,
            "accession": accession_column,
            "organism": organism_column,
            "doi": doi_column,
        },
        "input_rows": int(len(raw)),
        "accepted_rows": int(len(accepted)),
        "rejected_rows": int(len(rejected)),
        "normalized_file": normalized_path.name,
        "rejected_file": rejected_path.name,
        "policy": "No inferred pairing between Km and kcat; original source file is unchanged.",
    }
    write_json_atomic(manifest, manifest_path)
    return normalized_path, rejected_path, manifest_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", default="data/processed/catpred-db")
    parser.add_argument("--target", choices=["km", "kcat"], required=True)
    parser.add_argument("--record-id-column", required=True)
    parser.add_argument("--value-column", required=True)
    parser.add_argument("--unit", required=True)
    parser.add_argument("--sequence-column")
    parser.add_argument("--smiles-column")
    parser.add_argument("--accession-column")
    parser.add_argument("--organism-column")
    parser.add_argument("--doi-column")
    parser.add_argument("--source-version")
    parser.add_argument("--license-id", default="CC-BY-4.0 (verify current source terms)")
    args = parser.parse_args()
    outputs = normalize_catpred_csv(
        args.input, args.output_dir, target=args.target,
        record_id_column=args.record_id_column, value_column=args.value_column,
        unit=args.unit, sequence_column=args.sequence_column,
        smiles_column=args.smiles_column, accession_column=args.accession_column,
        organism_column=args.organism_column, doi_column=args.doi_column,
        source_version=args.source_version, license_id=args.license_id,
    )
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
