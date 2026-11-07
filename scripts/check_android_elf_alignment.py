#!/usr/bin/env python3
"""Verify every packaged Android native library is 16 KB ELF-page compatible."""
from __future__ import annotations

import argparse
import json
import struct
import sys
import zipfile
from pathlib import Path

PAGE_ALIGNMENT = 16 * 1024
EM_AARCH64 = 183
PT_LOAD = 1


def inspect_elf(name: str, payload: bytes) -> dict[str, object]:
    if payload[:4] != b"\x7fELF":
        raise ValueError(f"{name}: not an ELF file")
    if len(payload) < 64 or payload[4] != 2 or payload[5] != 1:
        raise ValueError(f"{name}: expected ELF64 little-endian")
    machine = struct.unpack_from("<H", payload, 18)[0]
    if machine != EM_AARCH64:
        raise ValueError(f"{name}: expected AArch64 (e_machine=183), got {machine}")
    phoff = struct.unpack_from("<Q", payload, 32)[0]
    phentsize, phnum = struct.unpack_from("<HH", payload, 54)
    if phentsize < 56 or phoff + phentsize * phnum > len(payload):
        raise ValueError(f"{name}: invalid program-header table")
    aligns: list[int] = []
    for index in range(phnum):
        offset = phoff + index * phentsize
        if struct.unpack_from("<I", payload, offset)[0] == PT_LOAD:
            aligns.append(struct.unpack_from("<Q", payload, offset + 48)[0])
    if not aligns:
        raise ValueError(f"{name}: no PT_LOAD segments")
    minimum = min(aligns)
    return {
        "path": name,
        "load_segment_alignments": sorted(set(aligns)),
        "minimum_load_alignment": minimum,
        "pass": minimum >= PAGE_ALIGNMENT,
    }


def inspect_archive(path: Path) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    with zipfile.ZipFile(path) as archive:
        native = [item for item in archive.infolist() if item.filename.endswith(".so")]
        if not native:
            raise ValueError(f"{path}: no packaged .so files found")
        for item in native:
            results.append(inspect_elf(f"{path}!/{item.filename}", archive.read(item)))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", nargs="+", type=Path, help="APK and/or AAB files")
    args = parser.parse_args()
    results: list[dict[str, object]] = []
    for archive in args.archives:
        results.extend(inspect_archive(archive))
    failures = [item for item in results if not item["pass"]]
    print(json.dumps({"native_libraries_checked": len(results), "failures": failures,
                      "results": results}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
