"""Validate raw enzyme records, transform targets, and create reproducible splits.

Input units are explicit: km is converted to mM and kcat to s^-1 before log10.
The default assumes km is already in mM and kcat in s^-1.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from Bio.SeqUtils.ProtParamData import (  # noqa: F401 - Biopython dependency sanity check
    kd,
)
from rdkit import Chem
from sklearn.model_selection import train_test_split

LOG = logging.getLogger("kinetics.preprocess")
STANDARD_AA = set("ACDEFGHIKLMNPQRSTVWY")
REQUIRED_COLUMNS = {"sequence", "smiles", "km", "kcat"}
KM_TO_MM = {"mM": 1.0, "uM": 1e-3, "µM": 1e-3, "nM": 1e-6, "M": 1e3}
KCAT_TO_PER_S = {"s^-1": 1.0, "min^-1": 1.0 / 60.0, "h^-1": 1.0 / 3600.0}


def _valid_sequence(value: object) -> bool:
    if not isinstance(value, str):
        return False
    sequence = value.strip().upper()
    return bool(sequence) and set(sequence) <= STANDARD_AA


def _canonical_smiles(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        mol = Chem.MolFromSmiles(value.strip())
        return Chem.MolToSmiles(mol, canonical=True) if mol is not None else None
    except Exception:
        return None


def clean_dataframe(
    frame: pd.DataFrame,
    km_unit: str = "mM",
    kcat_unit: str = "s^-1",
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Return validated records with log10 targets and counts for each rejection."""
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {sorted(missing)}")
    if km_unit not in KM_TO_MM:
        raise ValueError(f"Unsupported km unit {km_unit!r}; choose {sorted(KM_TO_MM)}")
    if kcat_unit not in KCAT_TO_PER_S:
        raise ValueError(f"Unsupported kcat unit {kcat_unit!r}; choose {sorted(KCAT_TO_PER_S)}")

    data = frame.loc[:, ["sequence", "smiles", "km", "kcat"]].copy()
    data["sequence"] = data["sequence"].map(
        lambda x: x.strip().upper() if isinstance(x, str) else ""
    )
    data["smiles"] = data["smiles"].map(_canonical_smiles)
    data["km"] = pd.to_numeric(data["km"], errors="coerce") * KM_TO_MM[km_unit]
    data["kcat"] = pd.to_numeric(data["kcat"], errors="coerce") * KCAT_TO_PER_S[kcat_unit]

    seq_ok = data["sequence"].map(_valid_sequence)
    smiles_ok = data["smiles"].notna()
    target_ok = (
        np.isfinite(data["km"]) & np.isfinite(data["kcat"])
        & (data["km"] > 0) & (data["kcat"] > 0)
    )
    stats = {
        "input_rows": int(len(data)),
        "invalid_sequences": int((~seq_ok).sum()),
        "invalid_smiles": int((~smiles_ok).sum()),
        "invalid_or_nonpositive_targets": int((~target_ok).sum()),
    }
    data = data.loc[seq_ok & smiles_ok & target_ok].copy()
    data["log10_km"] = np.log10(data["km"].astype(float))
    data["log10_kcat"] = np.log10(data["kcat"].astype(float))
    data = data.reset_index(drop=True)
    stats["kept_rows"] = int(len(data))
    if len(data) < 2:
        raise ValueError("Fewer than two valid rows remain; cannot create a train/test split.")
    return data, stats


def preprocess_csv(
    input_csv: str | Path,
    output_dir: str | Path = "data",
    test_size: float = 0.2,
    random_state: int = 42,
    km_unit: str = "mM",
    kcat_unit: str = "s^-1",
) -> tuple[Path, Path]:
    """Clean a CSV and persist train.csv/test.csv plus a cleaning report."""
    if not 0.0 < test_size < 1.0:
        raise ValueError("test_size must be strictly between 0 and 1.")
    input_path, out = Path(input_csv), Path(output_dir)
    if not input_path.is_file():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")
    out.mkdir(parents=True, exist_ok=True)
    cleaned, stats = clean_dataframe(
        pd.read_csv(input_path), km_unit=km_unit, kcat_unit=kcat_unit
    )
    train, test = train_test_split(
        cleaned, test_size=test_size, random_state=random_state, shuffle=True
    )
    train_path, test_path = out / "train.csv", out / "test.csv"
    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)
    pd.Series(stats, name="count").to_csv(out / "preprocessing_report.csv")
    LOG.info("Kept %d/%d rows; train=%d test=%d", len(cleaned), stats["input_rows"], len(train), len(test))
    LOG.info("Saved %s and %s", train_path, test_path)
    return train_path, test_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Raw CSV path")
    parser.add_argument("--output-dir", default="data")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--km-unit", choices=KM_TO_MM, default="mM")
    parser.add_argument("--kcat-unit", choices=KCAT_TO_PER_S, default="s^-1")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    preprocess_csv(args.input, args.output_dir, args.test_size, args.seed, args.km_unit, args.kcat_unit)


if __name__ == "__main__":
    main()
