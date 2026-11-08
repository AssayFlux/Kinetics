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

    wrapper_properties = root / "android/gradle/wrapper/gradle-wrapper.properties"
    try:
        wrapper = wrapper_properties.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Gradle wrapper properties could not be read: {exc}")
        wrapper = ""
    if "gradle-8.13-bin.zip" not in wrapper:
        errors.append("Gradle wrapper distribution must be pinned to 8.13")
    if "distributionSha256Sum=20f1b1176237254a6fc204d8434196fa11a4cfb387567519c61556e8710aed78" not in wrapper:
        errors.append("Gradle wrapper must verify the official Gradle 8.13 SHA-256")
    local_build = root / "scripts/build_android_local.sh"
    try:
        build_source = local_build.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Local Android build script could not be read: {exc}")
        build_source = ""
    for marker in (
        'CHAQUOPY_COMMIT="1f63c93d8beaf7062fbe51888ab9235475df3bb8"',
        'BIOPYTHON_COMMIT="d7e4b8b19399668b09442a5b35765d9186b5f665"',
        'GRADLE_SHA256="20f1b1176237254a6fc204d8434196fa11a4cfb387567519c61556e8710aed78"',
        'NDK_VERSION="28.2.13676358"',
        'PYTHON_TARGET="3.11.17-0"',
    ):
        if marker not in build_source:
            errors.append(f"Local build inputs must remain pinned: {marker}")

    rust_toolchain = root / "rust-toolchain.toml"
    cargo_lock = root / "android/native-rust/Cargo.lock"
    if not rust_toolchain.is_file() or 'channel = "1.88.0"' not in rust_toolchain.read_text(encoding="utf-8"):
        errors.append("Native Rust toolchain must be pinned to 1.88.0")
    if not cargo_lock.is_file():
        errors.append("Native Rust Cargo.lock is required for --locked builds")

    manifest_path = root / "android/app/src/main/AndroidManifest.xml"
    try:
        manifest = manifest_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Android manifest could not be read: {exc}")
        manifest = ""
    if 'android:allowBackup="false"' not in manifest:
        errors.append("Android backup must remain disabled for local research data")
    if 'android:usesCleartextTraffic="false"' not in manifest:
        errors.append("Android cleartext traffic must remain disabled")
    if "android.permission.INTERNET" in manifest:
        errors.append("Android application must not request INTERNET permission")

    package_init = root / "python/kinetics/__init__.py"
    runtime_probe = root / "android/app/src/main/python/kinetics_probe.py"
    if not package_init.is_file():
        errors.append("Repository kinetics Python package is missing")
    try:
        probe_source = runtime_probe.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Embedded Python runtime probe could not be read: {exc}")
        probe_source = ""
    if "import kinetics" not in probe_source:
        errors.append("Embedded Python runtime probe must import the packaged kinetics module")

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
