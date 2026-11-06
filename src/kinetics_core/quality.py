"""Non-destructive quality audit for normalized kinetic observations.

Repeated records are annotated, never silently discarded or averaged. Identical
source record IDs with differing measurements are surfaced as conflicts for
curator review. Similar protein/substrate pairs across sources are not assumed
to be duplicate experiments.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

import numpy as np
import pandas as pd


_REQUIRED = {"target", "source", "source_record_id", "canonical_value", "canonical_unit"}


def audit_observations(
    frame: pd.DataFrame,
    *,
    log10_tolerance: float = 1e-8,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """Annotate duplicate source IDs and return row-level and group-level audits."""
    missing = _REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"Observation table is missing required columns: {sorted(missing)}")
    if log10_tolerance < 0 or not np.isfinite(log10_tolerance):
        raise ValueError("log10_tolerance must be finite and non-negative")
    result = frame.copy().reset_index(drop=True)
    values = pd.to_numeric(result["canonical_value"], errors="coerce").to_numpy(float)
    if not np.isfinite(values).all() or np.any(values <= 0):
        raise ValueError("canonical_value must be finite and strictly positive")
    if not result["target"].isin(["km", "kcat"]).all():
        raise ValueError("target values must be km or kcat")

    group_columns = ["source", "source_record_id", "target"]
    if result[group_columns].isna().any().any():
        raise ValueError("source, source_record_id, and target cannot be missing")
    for column in group_columns:
        if result[column].astype(str).str.strip().eq("").any():
            raise ValueError(f"{column} cannot contain empty identifiers")
    result["duplicate_group_id"] = [
        hashlib.sha256(
            "|".join(map(str, (source, record_id, target))).encode("utf-8")
        ).hexdigest()
        for source, record_id, target in result[group_columns].itertuples(index=False, name=None)
    ]
    result["duplicate_status"] = "unique"
    audit_rows = []
    for group_id, indices in result.groupby("duplicate_group_id", sort=False).groups.items():
        if len(indices) < 2:
            continue
        group_values = result.loc[indices, "canonical_value"].astype(float).to_numpy()
        log_values = np.log10(group_values)
        conflict = float(np.max(log_values) - np.min(log_values)) > log10_tolerance
        status = "conflicting_duplicate" if conflict else "exact_duplicate"
        result.loc[indices, "duplicate_status"] = status
        first = result.loc[indices[0]]
        audit_rows.append({
            "duplicate_group_id": group_id,
            "source": str(first["source"]),
            "source_record_id": str(first["source_record_id"]),
            "target": str(first["target"]),
            "n_rows": int(len(indices)),
            "n_distinct_canonical_values": int(np.unique(group_values).size),
            "canonical_values": json.dumps(group_values.tolist()),
            "status": status,
            "review_required": bool(conflict),
        })
    audit = pd.DataFrame(audit_rows)
    counts = result["duplicate_status"].value_counts().to_dict()
    report = {
        "n_rows": int(len(result)),
        "n_km": int((result["target"] == "km").sum()),
        "n_kcat": int((result["target"] == "kcat").sum()),
        "n_unique_source_records": int(result["duplicate_group_id"].nunique()),
        "n_duplicate_groups": int(len(audit)),
        "n_conflicting_groups": int(
            (audit["status"] == "conflicting_duplicate").sum()
        ) if not audit.empty else 0,
        "optional_metadata_missing_fraction": {
            column: float(result[column].isna().mean())
            for column in ("sequence", "smiles", "protein_accession", "organism", "ph", "temperature_k", "assay_id", "publication_doi")
            if column in result
        },
        "duplicate_status_counts": {str(key): int(value) for key, value in counts.items()},
        "policy": (
            "No observations were removed or averaged. Review conflicts and decide "
            "replicate handling using source assay metadata and a predeclared protocol."
        ),
    }
    return result, audit, report



def review_potential_duplicate_observations(
    frame: pd.DataFrame,
    *,
    log10_precision: int = 8,
) -> pd.DataFrame:
    """Report cross-record exact-context candidates without removing or merging rows.

    Candidate matching requires at least one protein, substrate, accession, or DOI
    identity. Source is deliberately excluded so cross-source matches can be reviewed.
    """
    required = {"target", "canonical_value", "source_record_id"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Observation table is missing required columns: {sorted(missing)}")
    if log10_precision < 0:
        raise ValueError("log10_precision must be non-negative")
    candidates = frame.copy().reset_index(drop=True)
    identity_columns = [
        column for column in (
            "sequence_normalized", "sequence", "protein_accession",
            "smiles_canonical", "smiles", "publication_doi",
        ) if column in candidates.columns
    ]
    if not identity_columns:
        return pd.DataFrame()
    rows = []
    for index, row in candidates.iterrows():
        identities = {
            column: _identity_text(row[column])
            for column in identity_columns
        }
        if not any(identities.values()):
            continue
        value = float(row["canonical_value"])
        if not np.isfinite(value) or value <= 0:
            continue
        context = {
            "target": str(row["target"]),
            "log10_value": round(float(np.log10(value)), log10_precision),
            "ph": _rounded_optional(row.get("ph"), 3),
            "temperature_k": _rounded_optional(row.get("temperature_k"), 2),
            "organism": _identity_text(row.get("organism")),
            **identities,
        }
        fingerprint = hashlib.sha256(
            json.dumps(context, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        rows.append({
            "fingerprint": fingerprint,
            "source_record_id": str(row["source_record_id"]),
            "source": str(row.get("source", "")),
            "target": str(row["target"]),
            "canonical_value": value,
            "row_index": index,
        })
    if not rows:
        return pd.DataFrame()
    indexed = pd.DataFrame(rows)
    groups = []
    for fingerprint, group in indexed.groupby("fingerprint", sort=False):
        if len(group) < 2:
            continue
        groups.append({
            "candidate_group_id": fingerprint,
            "n_rows": int(len(group)),
            "sources": json.dumps(sorted(set(group["source"]))),
            "source_record_ids": json.dumps(group["source_record_id"].tolist()),
            "targets": json.dumps(group["target"].tolist()),
            "canonical_values": json.dumps(group["canonical_value"].tolist()),
            "row_indices": json.dumps(group["row_index"].tolist()),
            "review_required": True,
            "policy": "Candidate only; retain all observations pending curator review.",
        })
    return pd.DataFrame(groups)


def _identity_text(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    return text or None


def _rounded_optional(value: Any, digits: int) -> float | None:
    if value is None or pd.isna(value):
        return None
    numeric = float(value)
    return round(numeric, digits) if np.isfinite(numeric) else None
