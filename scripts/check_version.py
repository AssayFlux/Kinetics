#!/usr/bin/env python3
"""Check that all declared release-version sources and the candidate manifest agree."""
from __future__ import annotations

import json
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

package_lines = (ROOT / "python/kinetics/__init__.py").read_text(encoding="utf-8").splitlines()
package_line = next((line for line in package_lines if line.startswith("__version__")), "")
if '"' not in package_line:
    raise SystemExit("python/kinetics/__init__.py does not declare __version__")
package_version = package_line.split('"')[1]

android_lines = (ROOT / "android/app/build.gradle.kts").read_text(encoding="utf-8").splitlines()
version_name_line = next((line for line in android_lines if "versionName" in line), "")
version_code_line = next((line for line in android_lines if "versionCode" in line), "")
if '"' not in version_name_line or "=" not in version_code_line:
    raise SystemExit("Android versionName/versionCode are not declared")
android_version = version_name_line.split('"')[1]
android_code = int(version_code_line.split("=", 1)[1].strip())

manifest = json.loads((ROOT / "release-baseline.json").read_text(encoding="utf-8"))
versions = {
    "pyproject.toml": python_version,
    "python/kinetics/__init__.py": package_version,
    "android/app/build.gradle.kts": android_version,
    "manifest.release": str(manifest.get("release", "")),
    "manifest.android_version_name": str(manifest.get("android_version_name", "")),
    "manifest.python_distribution_version": str(manifest.get("python_distribution_version", "")),
    "manifest.python_package_version": str(manifest.get("python_package_version", "")),
}
if len(set(versions.values())) != 1:
    raise SystemExit(f"Release version mismatch: {versions}")

if android_code != int(manifest.get("android_version_code", -1)):
    raise SystemExit(
        f"Android versionCode mismatch: gradle={android_code}, "
        f"manifest={manifest.get('android_version_code')}"
    )

if manifest.get("status") not in {"candidate_not_frozen", "frozen"}:
    raise SystemExit("release-baseline.json status must be candidate_not_frozen or frozen")
if manifest.get("status") == "frozen":
    apk = manifest.get("apk", {})
    required = [
        manifest.get("source_commit"),
        manifest.get("immutable_tag"),
        apk.get("sha256"),
        apk.get("build_run_id"),
    ]
    if not all(required):
        raise SystemExit(
            "A frozen baseline requires source commit, immutable tag, APK SHA-256 and build run ID"
        )
    if not all(manifest.get("acceptance", {}).values()):
        raise SystemExit("A frozen baseline requires every acceptance gate to be true")

print(f"Release versions aligned: {python_version} (Android versionCode {android_code})")
