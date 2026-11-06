"""Normalize CatPred-DB target tables without inventing upstream record identifiers.

CatPred-DB publishes target-specific Km, kcat and Ki tables. This adapter accepts
only Km and kcat, preserves source metadata, and uses a content-addressed file-row
locator when the published table has no native record identifier.
"""
# ruff: noqa: I001
from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import tempfile

import numpy as np
import pandas as pd

from .curation import normalize_observation_table
from .provenance import file_record, write_json_atomic


CATPRED_SOURCE = "CatPred-DB"
CATPRED_DATASET_URL = "https://huggingface.co/datasets/RosettaCommons/CatPred-DB"
CATPRED_PROCESSING_REVISION = "931583821ff875e873002730fbbdf1047acfde77"


def normalize_catpred_csv(
    input_csv: str | pathlib.Path,
    output_dir: str | pathlib.Path,
    *,
    target: str,
    aggregate_log10_column: str | None = None,
    unit: str,
    record_id_column: str | None = None,
    sequence_column: str | None = "sequence",
    smiles_column: str | None = None,
    accession_column: str | None = "uniprot",
    organism_column: str | None = None,
    doi_column: str | None = None,
    ph_column: str | None = "ph",
    temperature_k_column: str | None = None,
    temperature_c_column: str | None = "temperature",
    assay_id_column: str | None = None,
    source_version: str,
    license_id: str,
    processing_revision: str = CATPRED_PROCESSING_REVISION,
) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
    if target not in ("km", "kcat"):
        raise ValueError("CatPred-DB adapter supports only km and kcat; Ki is not Km or kcat")
    if not re.fullmatch(r"[0-9a-fA-F]{7,40}", source_version):
        raise ValueError("source_version must be the pinned Hugging Face commit SHA")
    if not re.fullmatch(r"[0-9a-fA-F]{7,40}", processing_revision):
        raise ValueError("processing_revision must be the pinned GitHub commit SHA")
    if not license_id.strip():
        raise ValueError("CatPred imports require a non-empty license_id")
    source_path = pathlib.Path(input_csv)
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    expected_unit = "mM" if target == "km" else "s^-1"
    if unit != expected_unit:
        raise ValueError(
            f"CatPred {target} aggregate values must use the published "
            f"{expected_unit} convention"
        )
    if aggregate_log10_column is None:
        aggregate_log10_column = "log10km_mean" if target == "km" else "log10kcat_max"
    raw = pd.read_csv(
        source_path,
        dtype={column: "string" for column in (record_id_column, accession_column) if column},
    )
    if aggregate_log10_column not in raw.columns:
        raise ValueError(
            f"Missing CatPred aggregate target column: {aggregate_log10_column}"
        )
    raw["__kinetics_aggregate_linear_value"] = np.power(
        10.0, pd.to_numeric(raw[aggregate_log10_column], errors="coerce")
    )
    if smiles_column is None:
        if target == "km" and "substrate_smiles" in raw.columns:
            smiles_column = "substrate_smiles"
        elif "reactant_smiles" in raw.columns:
            smiles_column = "reactant_smiles"
        elif "substrate_smiles" in raw.columns:
            smiles_column = "substrate_smiles"
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
            raise ValueError(
                f"Configured temperature Celsius column does not exist: {temperature_c_column}"
            )
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
        value_column="__kinetics_aggregate_linear_value",
        unit=unit,
        unit_column=None,
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
        measurement_kind="source_aggregated",
        aggregation_method=(
            "maximum_over_source_measurements_for_sequence_substrate_pair"
            if target == "kcat"
            else "geometric_mean_over_source_measurements_for_sequence_substrate_pair"
        ),
    )
    # Preserve every upstream column verbatim; split/cluster labels remain source
    # annotations and are never presented as newly calculated identities.
    preserved_columns = [
        column for column in raw.columns if not column.startswith("__kinetics_")
    ]
    for column in preserved_columns:
        accepted[f"source_{column}"] = [
            raw.iloc[int(index)][column] for index in accepted["source_row_number"]
        ]
    output = pathlib.Path(output_dir).resolve()
    if output.exists():
        raise FileExistsError("CatPred output directory exists; choose a new output directory")
    if output == source_path.resolve().parent or output in source_path.resolve().parents:
        raise ValueError("CatPred output directory must not contain the raw source file")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = pathlib.Path(tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=output.parent))
    normalized_path = staging / f"{target}_observations.csv"
    rejected_path = staging / f"{target}_rejected_rows.csv"
    manifest_path = staging / f"{target}_curation_manifest.json"
    accepted.to_csv(normalized_path, index=False)
    rejected.to_csv(rejected_path, index=False)
    manifest = {
        "schema_version": "2.0",
        "dataset": CATPRED_SOURCE,
        "dataset_url": CATPRED_DATASET_URL,
        "target": target,
        "canonical_unit": "M" if target == "km" else "s^-1",
        "source_aggregate_log10_column": aggregate_log10_column,
        "source_aggregate_unit": unit,
        "source_value_semantics": (
            "As-published representative row value; it is not the aggregate target "
            "and reflects upstream clipping."
        ),
        "source_clipping_policy": (
            {"lower": 1e-8, "upper": 1e4, "unit": "mM"}
            if target == "km"
            else {"lower": 1e-6, "upper": 1e6, "unit": "s^-1"}
        ),
        "source_unit_basis": (
            "CatPred processing convention: Km in mM and kcat in s^-1; per-row "
            "underlying source units are not retained in the aggregate table."
        ),
        "unit_quality_warning": (
            "BRENDA num_value values are carried through the upstream merge without "
            "per-row unit metadata. SABIO kcat conversion multiplies min^-1 by 60, "
            "which appears opposite to the standard min^-1 to s^-1 conversion. "
            "Audit original source records before treating kcat as an absolute reference."
            if target == "kcat"
            else "BRENDA num_value values are carried through the upstream merge without "
            "per-row unit metadata; the aggregate table does not permit independent "
            "record-level unit verification."
        ),
        "source_processing_revision": processing_revision,
        "source_processing_refs": [
            f"https://github.com/maranasgroup/CatPred-DB/blob/{processing_revision}/scripts/processing/process_sabio.py",
            f"https://github.com/maranasgroup/CatPred-DB/blob/{processing_revision}/scripts/processing/merge.py",
        ],
        "measurement_kind": "source_aggregated",
        "aggregation_method": (
            "geometric_mean_over_source_measurements_for_sequence_substrate_pair"
            if target == "km"
            else "maximum_over_source_measurements_for_sequence_substrate_pair"
        ),
        "source_file": file_record(source_path, CATPRED_DATASET_URL),
        "source_version": source_version,
        "license_note": license_id,
        "record_id_origin": record_id_origin,
        "record_id_column": record_id_column,
        "mapping": {
            "source_row_value": "value",
            "source_row_log10_value": "log10_value",
            "aggregate_log10": aggregate_log10_column,
            "aggregate_linearized_value": "__kinetics_aggregate_linear_value",
            "unit": unit,
            "sequence": sequence_column, "substrate_smiles": smiles_column,
            "accession": accession_column, "organism": organism_column,
            "doi": doi_column, "ph": ph_column,
            "temperature_k": temperature_k_column,
            "temperature_c": temperature_c_column,
            "assay_id": assay_id_column,
            "source_context_preserved": preserved_columns,
        },
        "input_rows": int(len(raw)),
        "accepted_rows": int(len(accepted)),
        "rejected_rows": int(len(rejected)),
        "normalized_file": normalized_path.name,
        "rejected_file": rejected_path.name,
        "policy": (
            "CatPred values are source aggregates (Km geometric mean; kcat maximum), "
            "not individual assays. "
            "Generated row locators are not upstream "
            "record IDs. CatPred temperature Celsius is converted to kelvin. Raw source "
            "values and source columns are retained; no DOI, organism, or assay ID inferred."
        ),
    }
    manifest["outputs"] = {
        path.name: {
            "sha256": file_record(path)["sha256"],
            "size_bytes": path.stat().st_size,
        }
        for path in (normalized_path, rejected_path)
    }
    try:
        write_json_atomic(manifest, manifest_path)
        staging.rename(output)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return (
        output / normalized_path.name,
        output / rejected_path.name,
        output / manifest_path.name,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", default="data/processed/catpred-db")
    parser.add_argument("--target", choices=["km", "kcat"], required=True)
    parser.add_argument("--record-id-column")
    parser.add_argument("--aggregate-log10-column")
    parser.add_argument("--unit", choices=["mM", "s^-1"], required=True)
    parser.add_argument("--sequence-column", default="sequence")
    parser.add_argument("--smiles-column")
    parser.add_argument("--accession-column", default="uniprot")
    parser.add_argument("--organism-column")
    parser.add_argument("--doi-column")
    parser.add_argument("--ph-column", default="ph")
    parser.add_argument("--temperature-k-column")
    parser.add_argument("--temperature-c-column", default="temperature")
    parser.add_argument("--assay-id-column")
    parser.add_argument("--source-version", required=True)
    parser.add_argument("--license-id", required=True)
    parser.add_argument("--processing-revision", default=CATPRED_PROCESSING_REVISION)
    args = parser.parse_args()
    outputs = normalize_catpred_csv(
        args.input, args.output_dir, target=args.target,
        record_id_column=args.record_id_column,
        aggregate_log10_column=args.aggregate_log10_column, unit=args.unit,
        sequence_column=args.sequence_column, smiles_column=args.smiles_column,
        accession_column=args.accession_column, organism_column=args.organism_column,
        doi_column=args.doi_column, ph_column=args.ph_column,
        temperature_k_column=args.temperature_k_column,
        temperature_c_column=args.temperature_c_column,
        assay_id_column=args.assay_id_column,
        source_version=args.source_version, license_id=args.license_id,
        processing_revision=args.processing_revision,
    )
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
