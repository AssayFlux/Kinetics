#!/usr/bin/env python3
"""Report Android artifact checks as blocked until R1 creates real artifacts."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ANDROID = ROOT / "android"

def main() -> int:
    artifacts = list(ANDROID.rglob("*.apk")) + list(ANDROID.rglob("*.aab"))
    if not artifacts:
        print("BLOCKED / NOT APPLICABLE in R0: no APK/AAB exists; 16 KB alignment and package-size checks require R1 toolchains and artifacts.")
        return 0
    print("Android artifacts found, but alignment and package-size validation is not implemented; artifact presence is not a pass.")
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
