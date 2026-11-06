"""Explicit, auditable conversion of source tables into kinetic observations.

Column mappings are supplied by the caller. This avoids guessing that similarly
named columns from unrelated sources have identical scientific meaning.
"""
from __future__ import annotations

import math
from typing import Any

import pandas as pd

from .records import KineticObservation


def normalize_observation_table(
    frame: pd.DataFrame,
    *,
    target: str,
    source: str,
    source_record_id_column: str,
    value_column: str,
    unit: str | None = None,
    unit_column: str | None = None,
    sequence_column: str | None = None,
    smiles_column: str | None = None,
    accession_column: str | None = None,
    organism_column: str | None = None,
    ph_column: str | None = None,
    temperature_k_column: str | None = None,
    assay_id_column: str | None = None,
    doi_column: str | None = None,
    source_version: str | None = None,
    license_id: str | None = None,
    measurement_kind: str = "individual_measurement",
    aggregation_method: str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return accepted canonical observations and a row-level rejection audit.

    The original row number and source fields are retained in the accepted output.
    Missing optional metadata remains missing; no identifiers or assay conditions
    are inferred. Km and kcat tables are normalized separately.
    """
    if target not in ("km", "kcat"):
        raise ValueError("target must be 'km' or 'kcat'")
    required = [source_record_id_column, value_column]
    optional = [
        sequence_column, smiles_column, accession_column, organism_column,
        ph_column, temperature_k_column, assay_id_column, doi_column,
    ]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required source columns: {missing}")
    if unit is None and unit_column is None:
        raise ValueError("Provide a fixed unit or a source unit_column")
    if unit is not None and unit_column is not None:
        raise ValueError("Provide either unit or unit_column, not both")
    if unit_column is not None and unit_column not in frame.columns:
        raise ValueError(f"Configured unit column does not exist: {unit_column}")
    for column in optional:
        if column is not None and column not in frame.columns:
            raise ValueError(f"Configured metadata column does not exist: {column}")

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for row_number, row in frame.iterrows():
        try:
            raw_record_id = row[source_record_id_column]
            if pd.isna(raw_record_id):
                raise ValueError("missing source record identifier")
            record_id = str(raw_record_id).strip()
            if not record_id or record_id.lower() in {"nan", "none", "<na>"}:
                raise ValueError("missing source record identifier")
            value = float(row[value_column])
            if not math.isfinite(value) or value <= 0:
                raise ValueError("measurement is non-finite or non-positive")
            row_unit = str(row[unit_column]).strip() if unit_column else str(unit)
            if unit_column and (pd.isna(row[unit_column]) or not row_unit):
                raise ValueError("missing measurement unit")
            observation = KineticObservation(
                target=target,
                value=value,
                unit=row_unit,
                source=source,
                source_record_id=record_id,
                sequence=_optional_text(row, sequence_column),
                smiles=_optional_text(row, smiles_column),
                protein_accession=_optional_text(row, accession_column),
                organism=_optional_text(row, organism_column),
                ph=_optional_float(row, ph_column),
                temperature_k=_optional_float(row, temperature_k_column),
                assay_id=_optional_text(row, assay_id_column),
                publication_doi=_optional_text(row, doi_column),
                source_version=source_version,
                license_id=license_id,
                measurement_kind=measurement_kind,
                aggregation_method=aggregation_method,
            )
            item = observation.as_dict()
            item["source_row_number"] = int(row_number) if isinstance(row_number, int) else str(row_number)
            accepted.append(item)
        except (TypeError, ValueError, OverflowError) as exc:
            rejected.append({
                "source_row_number": int(row_number) if isinstance(row_number, int) else str(row_number),
                "source_record_id": str(row.get(source_record_id_column, "")),
                "reason": str(exc),
            })
    accepted_columns = [
        *KineticObservation.__dataclass_fields__,
        "canonical_value",
        "canonical_unit",
        "source_row_number",
    ]
    rejected_columns = ["source_row_number", "source_record_id", "reason"]
    return (
        pd.DataFrame(accepted, columns=accepted_columns),
        pd.DataFrame(rejected, columns=rejected_columns),
    )


def _optional_text(row: pd.Series, column: str | None) -> str | None:
    if column is None or pd.isna(row[column]):
        return None
    value = str(row[column]).strip()
    return value or None


def _optional_float(row: pd.Series, column: str | None) -> float | None:
    if column is None or pd.isna(row[column]):
        return None
    value = float(row[column])
    if not math.isfinite(value):
        raise ValueError(f"{column} is non-finite")
    return value
