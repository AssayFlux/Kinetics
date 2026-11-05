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
