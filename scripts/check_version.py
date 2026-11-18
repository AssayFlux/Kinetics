#!/usr/bin/env python3
"""Check that the Python package and Android application share one release version."""
from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "pyproject.toml").open("rb") as handle:
    python_version = str(tomllib.load(handle)["project"]["version"])

package_source = (ROOT / "python/kinetics/__init__.py").read_text(encoding="utf-8")
package_match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', package_source, re.MULTILINE)
if package_match is None:
    raise SystemExit("python/kinetics/__init__.py does not declare __version__")

android_source = (ROOT / "android/app/build.gradle.kts").read_text(encoding="utf-8")
android_match = re.search(r'versionName\s*=\s*"([^"]+)"', android_source)
if android_match is None:
    raise SystemExit("android/app/build.gradle.kts does not declare versionName")

versions = {
    "pyproject.toml": python_version,
    "python/kinetics/__init__.py": package_match.group(1),
    "android/app/build.gradle.kts": android_match.group(1),
}
if len(set(versions.values())) != 1:
    raise SystemExit(f"Release version mismatch: {versions}")

print(f"Release versions aligned: {python_version}")
