"""End-to-end preparation of protein/scaffold double-cold train/calibration/test partitions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from .provenance import file_record, write_json_atomic
from .splitting import double_cold_holdout


def prepare_target_partitions(
    observations_csv: str | Path,
    output_dir: str | Path,
    *,
    target: str,
    protein_group_column: str = "protein_cluster_id",
    substrate_group_column: str = "scaffold_id",
    test_fraction: float = 0.2,
    calibration_fraction: float = 0.2,
    random_state: int = 42,
) -> dict[str, Any]:
    """Create train/calibration/test partitions cold on both protein and scaffold.

    The first double-cold split reserves the final test set. A second double-cold
    split within the remaining development pool reserves calibration data.
    Cross-quadrant observations from both splits are kept in a separate excluded
    CSV and never silently reassigned to train, calibration, or test.
    """
    if target not in ("km", "kcat"):
        raise ValueError("target must be 'km' or 'kcat'")
    if not 0.0 < test_fraction < 1.0 or not 0.0 < calibration_fraction < 1.0:
        raise ValueError("test_fraction and calibration_fraction must be between 0 and 1")
    source = Path(observations_csv)
    if not source.is_file():
        raise FileNotFoundError(source)
    frame = pd.read_csv(
        source, dtype={"source_record_id": "string", "source": "string"}
    )
    required = {
        "target", "source", "source_record_id", "canonical_value",
        protein_group_column, substrate_group_column,
    }
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Normalized observations are missing columns: {sorted(missing)}")
    selected = frame.loc[frame["target"] == target].copy().reset_index(drop=True)
    if selected.empty:
        raise ValueError(f"No normalized observations for target {target}")
    if selected.duplicated(subset=["source", "source_record_id"]).any():
        raise ValueError(
            "Duplicate source_record_id values remain; review the quality audit and "
            "resolve replicate/conflict policy before partitioning"
        )

    development_pool, test, excluded_test, test_manifest = double_cold_holdout(
        selected,
        protein_group_column=protein_group_column,
        substrate_group_column=substrate_group_column,
        test_fraction=test_fraction,
        random_state=random_state,
    )
    train, calibration, excluded_calibration, calibration_manifest = double_cold_holdout(
        development_pool,
        protein_group_column=protein_group_column,
        substrate_group_column=substrate_group_column,
        test_fraction=calibration_fraction,
        random_state=random_state + 1009,
    )
    if train.empty or calibration.empty or test.empty:
        raise ValueError("Partitioning produced an empty train, calibration, or test set")

    for axis in (protein_group_column, substrate_group_column):
        train_groups = set(train[axis].astype(str))
        calibration_groups = set(calibration[axis].astype(str))
        test_groups = set(test[axis].astype(str))
        if train_groups.intersection(calibration_groups):
            raise RuntimeError(f"Train/calibration leakage detected on {axis}")
        if train_groups.intersection(test_groups) or calibration_groups.intersection(test_groups):
            raise RuntimeError(f"Test leakage detected on {axis}")

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "train": output / f"{target}_train.csv",
        "calibration": output / f"{target}_calibration.csv",
        "test": output / f"{target}_test.csv",
        "excluded": output / f"{target}_excluded_cross_quadrant.csv",
    }
    train.to_csv(paths["train"], index=False)
    calibration.to_csv(paths["calibration"], index=False)
    test.to_csv(paths["test"], index=False)
    pd.concat([excluded_test, excluded_calibration], ignore_index=True).to_csv(
        paths["excluded"], index=False
    )
    manifest = {
        "schema_version": "1.0",
        "target": target,
        "source_file": file_record(source),
        "split_strategy": "nested_double_cold_protein_and_scaffold",
        "protein_group_column": protein_group_column,
        "substrate_group_column": substrate_group_column,
        "test_fraction_requested": test_fraction,
        "calibration_fraction_requested_within_development_pool": calibration_fraction,
        "random_state": random_state,
        "rows": {
            "source_target_rows": int(len(selected)),
            "train": int(len(train)),
            "calibration": int(len(calibration)),
            "test": int(len(test)),
            "excluded_cross_quadrant": int(len(excluded_test) + len(excluded_calibration)),
        },
        "group_counts": {
            partition: {
                "protein": int(data[protein_group_column].nunique()),
                "substrate": int(data[substrate_group_column].nunique()),
            }
            for partition, data in (
                ("train", train), ("calibration", calibration), ("test", test)
            )
        },
        "train_test_split_manifest": test_manifest,
        "train_calibration_split_manifest": calibration_manifest,
        "outputs": {name: path.name for name, path in paths.items()},
        "leakage_checks": {
            axis: {
                "train_calibration_overlap": 0,
                "train_test_overlap": 0,
                "calibration_test_overlap": 0,
            }
            for axis in (protein_group_column, substrate_group_column)
        },
        "policy": (
            "Excluded cross-quadrant observations are retained separately. "
            "No record is duplicated across train, calibration, and test."
        ),
    }
    manifest_path = output / f"{target}_split_manifest.json"
    write_json_atomic(manifest, manifest_path)
    return {
        "manifest": manifest,
        "manifest_path": str(manifest_path),
        **{key: str(value) for key, value in paths.items()},
    }
