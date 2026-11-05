"""Leakage-aware dataset partition helpers.

These functions only create and describe partitions; they do not fit models.
Use source-published cluster labels when available and retain the resulting
split manifest with every downstream experiment.
"""
from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


def grouped_holdout(
    frame: pd.DataFrame,
    *,
    group_column: str,
    test_fraction: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """Split by groups so no group identifier appears in both partitions."""
    if group_column not in frame:
        raise ValueError(f"Missing grouping column: {group_column}")
    if not 0.0 < test_fraction < 1.0:
        raise ValueError("test_fraction must be strictly between 0 and 1")
    groups = frame[group_column]
    if groups.isna().any():
        raise ValueError(f"Grouping column {group_column} contains missing values")
    unique_groups = groups.nunique()
    if unique_groups < 2:
        raise ValueError("At least two distinct groups are required")
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_fraction, random_state=random_state)
    train_idx, test_idx = next(splitter.split(frame, groups=groups))
    train, test = frame.iloc[train_idx].copy(), frame.iloc[test_idx].copy()
    train_groups, test_groups = set(train[group_column]), set(test[group_column])
    overlap = train_groups.intersection(test_groups)
    if overlap:
        raise RuntimeError("Group leakage detected after split")
    manifest = {
        "strategy": "grouped_holdout",
        "group_column": group_column,
        "test_fraction_requested": test_fraction,
        "random_state": random_state,
        "train_rows": len(train),
        "test_rows": len(test),
        "train_groups": len(train_groups),
        "test_groups": len(test_groups),
        "group_overlap": 0,
    }
    return train, test, manifest


def double_cold_holdout(
    frame: pd.DataFrame,
    *,
    protein_group_column: str,
    substrate_group_column: str,
    test_fraction: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """Create strict protein-and-substrate cold partitions.

    Test rows contain only held-out protein groups AND held-out substrate groups.
    Training rows contain neither held-out group. Cross-quadrant rows are returned
    separately as excluded rows, preventing them from leaking into either set.
    """
    for column in (protein_group_column, substrate_group_column):
        if column not in frame:
            raise ValueError(f"Missing grouping column: {column}")
        if frame[column].isna().any():
            raise ValueError(f"Grouping column {column} contains missing values")
    if not 0.0 < test_fraction < 1.0:
        raise ValueError("test_fraction must be strictly between 0 and 1")
    protein_groups = frame[protein_group_column].drop_duplicates().to_numpy()
    substrate_groups = frame[substrate_group_column].drop_duplicates().to_numpy()
    if len(protein_groups) < 2 or len(substrate_groups) < 2:
        raise ValueError("At least two unique protein and substrate groups are required")

    from sklearn.model_selection import train_test_split
    _, held_proteins = train_test_split(
        protein_groups, test_size=test_fraction, random_state=random_state
    )
    _, held_substrates = train_test_split(
        substrate_groups, test_size=test_fraction, random_state=random_state + 1
    )
    protein_is_held = frame[protein_group_column].isin(set(held_proteins))
    substrate_is_held = frame[substrate_group_column].isin(set(held_substrates))
    test_mask = protein_is_held & substrate_is_held
    train_mask = ~protein_is_held & ~substrate_is_held
    excluded_mask = ~(test_mask | train_mask)
    train = frame.loc[train_mask].copy()
    test = frame.loc[test_mask].copy()
    excluded = frame.loc[excluded_mask].copy()
    if train.empty or test.empty:
        raise ValueError(
            "Double-cold split produced an empty train or test partition; "
            "adjust the holdout fraction or grouping granularity."
        )
    manifest = {
        "strategy": "double_cold_holdout",
        "protein_group_column": protein_group_column,
        "substrate_group_column": substrate_group_column,
        "test_fraction_requested_per_axis": test_fraction,
        "random_state": random_state,
        "held_out_protein_groups": sorted(map(str, held_proteins)),
        "held_out_substrate_groups": sorted(map(str, held_substrates)),
        "train_rows": len(train),
        "test_rows": len(test),
        "excluded_cross_quadrant_rows": len(excluded),
    }
    return train, test, excluded, manifest
