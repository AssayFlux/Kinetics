#!/usr/bin/env python3
"""Verify that the Android CI build produced non-empty APK and AAB artifacts."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID = ROOT / "android"
EXPECTED = (
    ANDROID / "app/build/outputs/apk/debug/app-debug.apk",
    ANDROID / "app/build/outputs/bundle/debug/app-debug.aab",
)


def main() -> int:
    missing = [path for path in EXPECTED if not path.is_file() or path.stat().st_size == 0]
    if missing:
        for path in missing:
            print(f"ERROR: required Android artifact is missing or empty: {path}", file=sys.stderr)
        return 1

    for path in EXPECTED:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"OK: {path.relative_to(ROOT)} size={path.stat().st_size} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
