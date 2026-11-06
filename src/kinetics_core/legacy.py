"""Explicit adapters for importing legacy paired-target CSV records.

The old preprocessing workflow stores Km and kcat in one row. The research
core stores one independently measured target per observation. This adapter
bridges those shapes without inventing source identifiers or dropping a valid
single-target measurement.
"""
from __future__ import annotations

from typing import Any

import pandas as pd

from .records import KineticObservation


def paired_frame_to_observations(
    frame: pd.DataFrame,
    *,
    source: str,
    source_record_id_column: str,
    km_unit: str = "mM",
    kcat_unit: str = "s^-1",
    source_version: str | None = None,
    license_id: str | None = None,
    sequence_column: str = "sequence",
    smiles_column: str = "smiles",
) -> list[KineticObservation]:
    """Convert legacy paired rows into independent canonical observations.

    A stable source record ID is mandatory. Missing Km or kcat values are
    handled independently, so a valid measurement is retained when its paired
    target is absent. Invalid non-missing measurements fail with row context.
    """
    if not isinstance(source, str) or not source.strip():
        raise ValueError("source must be a non-empty string")
    if frame.empty:
        raise ValueError("Legacy frame contains no rows")
    required = {
        source_record_id_column, "km", "kcat",
        sequence_column, smiles_column,
    }
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Legacy frame is missing required columns: {sorted(missing)}")

    observations: list[KineticObservation] = []
    for row_index, row in frame.iterrows():
        raw_record_id = row[source_record_id_column]
        if pd.isna(raw_record_id) or not str(raw_record_id).strip():
            raise ValueError(f"row {row_index}: source record ID is missing")
        record_id = str(raw_record_id).strip()
        sequence = None if pd.isna(row[sequence_column]) else str(row[sequence_column])
        smiles = None if pd.isna(row[smiles_column]) else str(row[smiles_column])

        row_observations = 0
        for target, column, unit in (
            ("km", "km", km_unit),
            ("kcat", "kcat", kcat_unit),
        ):
            raw_value = row[column]
            if pd.isna(raw_value):
                continue
            try:
                observation = KineticObservation(
                    target=target,
                    value=float(raw_value),
                    unit=unit,
                    source=source.strip(),
                    source_record_id=record_id,
                    sequence=sequence,
                    smiles=smiles,
                    source_version=source_version,
                    license_id=license_id,
                )
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"row {row_index}, target {target!r}, source record "
                    f"{record_id!r}: {exc}"
                ) from exc
            observations.append(observation)
            row_observations += 1

        if row_observations == 0:
            raise ValueError(
                f"row {row_index}, source record {record_id!r}: "
                "both Km and kcat measurements are missing"
            )
    return observations


def paired_frame_to_records(
    frame: pd.DataFrame,
    **kwargs: Any,
) -> list[dict[str, Any]]:
    """Return canonical dictionaries suitable for CSV/Parquet serialization."""
    return [observation.as_dict() for observation in paired_frame_to_observations(frame, **kwargs)]
