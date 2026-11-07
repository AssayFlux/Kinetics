#!/usr/bin/env python3
"""R0 placeholder for reproducible paper-evidence generation."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
JOBS_FILE = ROOT / "validation" / "reproduction_jobs.yaml"


def main() -> int:
    try:
        config = yaml.safe_load(JOBS_FILE.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        print(f"Cannot read reproduction job registry: {exc}", file=sys.stderr)
        return 2
    jobs = config.get("jobs", [])
    if not isinstance(jobs, list):
        print("Invalid reproduction job registry: jobs must be a list", file=sys.stderr)
        return 2
    if not jobs:
        print(
            "No reproduction jobs registered; no paper evidence was generated "
            "(expected in R0)."
        )
        return 0
    print(
        "Jobs are registered, but the R0 stub cannot execute them. "
        "Implement the evidence runner first.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
