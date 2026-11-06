"""Persist audited canonical observations and their provenance in SQLite."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

from .provenance import sha256_file
from .quality import audit_observations
from .storage import KineticsSQLite


def _json_safe(value: Any) -> Any:
    """Convert pandas/numpy scalar values into strict JSON-compatible values."""
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def persist_observation_csv(
    input_path: str | Path,
    database_path: str | Path,
    *,
    dataset_id: str,
    name: str,
    source: str,
    version: str | None = None,
    license_id: str | None = None,
    citation: str | None = None,
) -> dict[str, Any]:
    """Audit and atomically persist a canonical observation CSV.

    The dataset ID identifies an immutable import snapshot. Re-importing the
    same file under the same ID is idempotent; reusing that ID for changed
    content or metadata is rejected. Every measurement retains its source
    record ID and original row metadata in JSON.
    """
    for field, value in (("dataset_id", dataset_id), ("name", name), ("source", source)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")

    source_path = Path(input_path)
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    checksum = sha256_file(source_path)
    frame = pd.read_csv(source_path, dtype={"source_record_id": "string"})
    audited, _, report = audit_observations(frame)
    if "canonical_unit" not in audited:
        raise ValueError("canonical observations must include canonical_unit")
    expected_units = audited["target"].map({"km": "M", "kcat": "s^-1"})
    if not audited["canonical_unit"].eq(expected_units).all():
        raise ValueError("canonical_unit does not match the target's required unit")

    store = KineticsSQLite(database_path)
    store.initialize()
    dataset_metadata = {
        "schema": "kinetics-canonical-observation-v1",
        "n_observations": int(len(audited)),
        "quality_report": report,
    }
    measurement_rows = []
    for row_index, row in audited.iterrows():
        record = {key: _json_safe(value) for key, value in row.to_dict().items()}
        identity = "|".join(
            (dataset_id, checksum, str(row_index), str(row["source_record_id"]),
             str(row["target"]))
        )
        measurement_id = hashlib.sha256(identity.encode("utf-8")).hexdigest()
        metadata = {
            "dataset_id": dataset_id,
            "source": source,
            "source_record_id": str(row["source_record_id"]),
            "source_version": version or record.get("source_version"),
            "license_id": license_id or record.get("license_id"),
            "original_value": record.get("value"),
            "original_unit": record.get("unit"),
            "canonical_value": float(row["canonical_value"]),
            "canonical_unit": str(row["canonical_unit"]),
            "source_observation": record,
        }
        measurement_rows.append((
            measurement_id, str(row["target"]), float(row["canonical_value"]),
            str(row["canonical_unit"]), store.json_dumps(metadata),
        ))

    with store.transaction() as connection:
        existing = connection.execute(
            "SELECT name, source, version, license, citation, checksum_sha256 "
            "FROM datasets WHERE dataset_id = ?", (dataset_id,)
        ).fetchone()
        expected_dataset = (
            name, source, version, license_id, citation, checksum
        )
        if existing is not None:
            actual_dataset = tuple(existing)
            if actual_dataset != expected_dataset:
                raise ValueError(
                    "dataset_id already exists with different source metadata or content; "
                    "use a new immutable dataset_id for a new snapshot"
                )
            existing_count = connection.execute(
                "SELECT COUNT(*) FROM measurements WHERE json_extract(metadata_json, "
                "'$.dataset_id') = ?", (dataset_id,)
            ).fetchone()[0]
            if existing_count != len(measurement_rows):
                raise RuntimeError(
                    "Existing dataset snapshot has an incomplete or inconsistent "
                    "measurement count; refusing to append or repair implicitly"
                )
            inserted = 0
        else:
            connection.execute(
                "INSERT INTO datasets(dataset_id, name, source, version, license, "
                "citation, checksum_sha256, local_path, metadata_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    dataset_id, name, source, version, license_id, citation,
                    checksum, str(source_path.resolve()),
                    store.json_dumps(dataset_metadata),
                ),
            )
            connection.executemany(
                "INSERT INTO measurements(measurement_id, measurement_type, value, "
                "unit, metadata_json) VALUES (?, ?, ?, ?, ?)",
                measurement_rows,
            )
            event_id = hashlib.sha256(
                f"dataset-import|{dataset_id}|{checksum}".encode("utf-8")
            ).hexdigest()
            connection.execute(
                "INSERT INTO provenance_events(event_id, event_type, subject_id, "
                "source, details_json) VALUES (?, ?, ?, ?, ?)",
                (
                    event_id, "canonical_observation_import", dataset_id, source,
                    store.json_dumps({
                        "sha256": checksum,
                        "n_observations": len(measurement_rows),
                        "database_schema_version": 1,
                    }),
                ),
            )
            inserted = len(measurement_rows)

    return {
        "dataset_id": dataset_id,
        "database": str(store.path.resolve()),
        "input_sha256": checksum,
        "n_observations": len(measurement_rows),
        "n_inserted": inserted,
        "idempotent_replay": inserted == 0,
        "quality_report": report,
    }
