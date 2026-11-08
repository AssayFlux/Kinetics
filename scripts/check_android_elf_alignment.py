#!/usr/bin/env python3
"""Verify packaged Android native libraries have 16 KB-compatible ELF load segments."""
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
ELF_HEADER_SIZE = 64
PROGRAM_HEADER_SIZE = 56


def inspect_elf(name: str, payload: bytes) -> dict[str, object]:
    if len(payload) < ELF_HEADER_SIZE or payload[:4] != b"\\x7fELF":
        raise ValueError(f"{name}: truncated or invalid ELF header")
    if payload[4] != 2 or payload[5] != 1 or payload[6] != 1:
        raise ValueError(f"{name}: expected ELF64 little-endian version 1")
    machine = struct.unpack_from("<H", payload, 18)[0]
    if machine != EM_AARCH64:
        raise ValueError(f"{name}: expected AArch64 (e_machine=183), got {machine}")
    phoff = struct.unpack_from("<Q", payload, 32)[0]
    ehsize, phentsize, phnum = struct.unpack_from("<HHH", payload, 52)
    if ehsize < ELF_HEADER_SIZE or phentsize < PROGRAM_HEADER_SIZE:
        raise ValueError(f"{name}: invalid ELF/program-header entry size")
    if phoff < ehsize or phoff + phentsize * phnum > len(payload):
        raise ValueError(f"{name}: invalid program-header table")

    segments: list[dict[str, int]] = []
    for index in range(phnum):
        offset = phoff + index * phentsize
        if struct.unpack_from("<I", payload, offset)[0] != PT_LOAD:
            continue
        file_offset, virtual_address, alignment = struct.unpack_from("<QQ", payload, offset + 8)[0], struct.unpack_from("<Q", payload, offset + 16)[0], struct.unpack_from("<Q", payload, offset + 48)[0]
        segments.append({
            "index": index,
            "file_offset": file_offset,
            "virtual_address": virtual_address,
            "alignment": alignment,
        })

    if not segments:
        raise ValueError(f"{name}: no PT_LOAD segments")

    failures: list[str] = []
    for segment in segments:
        alignment = segment["alignment"]
        if alignment < PAGE_ALIGNMENT:
            failures.append(f"PT_LOAD[{segment['index']}] p_align={alignment} is below 16 KB")
            continue
        if alignment & (alignment - 1):
            failures.append(f"PT_LOAD[{segment['index']}] p_align={alignment} is not a power of two")
        if segment["file_offset"] % alignment != segment["virtual_address"] % alignment:
            failures.append(
                f"PT_LOAD[{segment['index']}] p_offset and p_vaddr are not congruent modulo p_align"
            )

    return {
        "path": name,
        "load_segments": segments,
        "pass": not failures,
        "failures": failures,
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
