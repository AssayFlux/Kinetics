#!/usr/bin/env python3
"""Check that all declared release-version sources and the candidate manifest agree."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    try:
        import tomli as tomllib
    except ModuleNotFoundError as exc:
        raise SystemExit("Python 3.10 requires the declared tomli development dependency") from exc

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "pyproject.toml").open("rb") as handle:
    python_version = str(tomllib.load(handle)["project"]["version"])

package_source = (ROOT / "python/kinetics/__init__.py").read_text(encoding="utf-8")
package_match = re.search(r'^__version__\\s*=\\s*["\\']([^"\\']+)["\\']', package_source, re.MULTILINE)
if package_match is None:
    raise SystemExit("python/kinetics/__init__.py does not declare __version__")

android_source = (ROOT / "android/app/build.gradle.kts").read_text(encoding="utf-8")
android_match = re.search(r'versionName\\s*=\\s*"([^"]+)"', android_source)
code_match = re.search(r'versionCode\\s*=\\s*(\\d+)', android_source)
if android_match is None or code_match is None:
    raise SystemExit("Android versionName/versionCode are not declared")

manifest = json.loads((ROOT / "release-baseline.json").read_text(encoding="utf-8"))
manifest_versions = {
    "manifest.release": str(manifest.get("release", "")),
    "manifest.android_version_name": str(manifest.get("android_version_name", "")),
    "manifest.python_distribution_version": str(manifest.get("python_distribution_version", "")),
    "manifest.python_package_version": str(manifest.get("python_package_version", "")),
}
versions = {
    "pyproject.toml": python_version,
    "python/kinetics/__init__.py": package_match.group(1),
    "android/app/build.gradle.kts": android_match.group(1),
    **manifest_versions,
}
if len(set(versions.values())) != 1:
    raise SystemExit(f"Release version mismatch: {versions}")

android_code = int(code_match.group(1))
if android_code != int(manifest.get("android_version_code", -1)):
    raise SystemExit(
        f"Android versionCode mismatch: gradle={android_code}, "
        f"manifest={manifest.get('android_version_code')}"
    )

if manifest.get("status") not in {"candidate_not_frozen", "frozen"}:
    raise SystemExit("release-baseline.json status must be candidate_not_frozen or frozen")
if manifest.get("status") == "frozen":
    required = [manifest.get("source_commit"), manifest.get("immutable_tag"),
                manifest.get("apk", {}).get("sha256"), manifest.get("apk", {}).get("build_run_id")]
    if not all(required):
        raise SystemExit("A frozen baseline requires source commit, immutable tag, APK SHA-256 and build run ID")
    if not all(manifest.get("acceptance", {}).values()):
        raise SystemExit("A frozen baseline requires every acceptance gate to be true")

print(f"Release versions aligned: {python_version} (Android versionCode {android_code})")
