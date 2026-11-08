#!/usr/bin/env python3
"""Static guardrails for the local-only Android build and offline app manifest."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID_NS = "{http://schemas.android.com/apk/res/android}"
FORBIDDEN_CI_TASKS = (
    "assembleDebug", "assembleRelease", "bundleDebug", "bundleRelease",
    "connectedAndroidTest", "managedDevice",
)


def validate_android_config(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    manifest_path = root / "android/app/src/main/AndroidManifest.xml"
    gradle_path = root / "android/app/build.gradle.kts"
    cmake_path = root / "android/app/src/main/cpp/CMakeLists.txt"
    workflow_path = root / ".github/workflows/ci.yml"
    try:
        manifest = ET.parse(manifest_path).getroot()
    except (OSError, ET.ParseError) as exc:
        return [f"Android manifest could not be parsed: {exc}"]

    permissions = {
        node.get(ANDROID_NS + "name", "")
        for node in manifest.findall("uses-permission")
    }
    if "android.permission.INTERNET" in permissions:
        errors.append("offline Research Mode must not request INTERNET permission")
    application = manifest.find("application")
    if application is None:
        errors.append("Android manifest is missing application")
    else:
        if application.get(ANDROID_NS + "allowBackup") != "false":
            errors.append("application must disable Android backup")
        if application.get(ANDROID_NS + "usesCleartextTraffic") != "false":
            errors.append("application must disable cleartext traffic")

    try:
        gradle = gradle_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Android Gradle config could not be read: {exc}")
        gradle = ""
    required_gradle = {
        'srcDir("../../python")': "Chaquopy must package the repository's kinetics Python modules",
        'minSdk = 29': "Android minimum SDK must remain API 29",
        'targetSdk = 36': "Android target SDK must remain explicitly pinned to API 36",
        'ndkVersion = "28.2.13676358"': "Android NDK version must match the local build script",
        'abiFilters += "arm64-v8a"': "Android ABI must remain arm64-v8a only",
        'useLegacyPackaging = false': "JNI libraries must use modern uncompressed packaging",
    }
    for marker, message in required_gradle.items():
        if marker not in gradle:
            errors.append(message)

    try:
        cmake = cmake_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Native CMake config could not be read: {exc}")
        cmake = ""
    if "-Wl,-z,max-page-size=16384" not in cmake:
        errors.append("Native linker must request 16 KB maximum page alignment")

    try:
        workflow = workflow_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"GitHub workflow could not be read: {exc}")
        workflow = ""
    for task in FORBIDDEN_CI_TASKS:
        if task in workflow:
            errors.append(f"GitHub Actions must not invoke Android build/device task {task}")
    if "workflow_dispatch:" not in workflow:
        errors.append("Android/source CI must remain manual-dispatch only during test deferral")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate_android_config(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Android offline/build-first configuration guardrails are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
