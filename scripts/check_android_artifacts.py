#!/usr/bin/env python3
"""Report the owner-directed local-only Android build boundary in source CI."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID = ROOT / "android"


def main() -> int:
    artifacts = list(ANDROID.rglob("*.apk")) + list(ANDROID.rglob("*.aab"))
    if not artifacts:
        print(
            "NOT RUN IN GITHUB ACTIONS by owner instruction: APK/AAB builds and "
            "Android runtime tests are local-only. Use docs/local-android-build.md."
        )
        return 0
    print(
        "Android artifacts found in the checkout, but this source-only CI job "
        "does not inspect or validate them. Use the local build procedure and "
        "record the results in docs/android-feasibility.md."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
