#!/usr/bin/env python3
"""Inspect downloaded public CSV files before any schema conversion."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

def inspect(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        samples = []
        count = 0
        for row in reader:
            count += 1
            if len(samples) < 3:
                samples.append({key: (value[:160] if isinstance(value, str) else value)
                                for key, value in row.items()})
    return {"file": path.name, "rows": count, "columns": columns, "sample_rows": samples}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="data/public/catpred-db")
    args = parser.parse_args()
    root = Path(args.input_dir)
    if not root.is_dir():
        raise SystemExit(f"Directory not found: {root}. Download the data first.")
    reports = [inspect(path) for path in sorted(root.glob("*.csv"))]
    if not reports:
        raise SystemExit(f"No CSV files found in {root}")
    print(json.dumps(reports, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
