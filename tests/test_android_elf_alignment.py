from __future__ import annotations

import struct

import pytest

from scripts.check_android_elf_alignment import PAGE_ALIGNMENT, inspect_elf


def make_elf(*, alignment: int = PAGE_ALIGNMENT, file_offset: int = 0,
             virtual_address: int = 0, machine: int = 183, include_load: bool = True) -> bytes:
    payload = bytearray(64 + 56)
    payload[:7] = b"\\x7fELF\\x02\\x01\\x01"
    struct.pack_into("<H", payload, 18, machine)
    struct.pack_into("<Q", payload, 32, 64)
    struct.pack_into("<HHH", payload, 52, 64, 56, 1)
    struct.pack_into("<I", payload, 64, 1 if include_load else 0)
    struct.pack_into("<QQ", payload, 72, file_offset, virtual_address)
    struct.pack_into("<Q", payload, 112, alignment)
    return bytes(payload)


def test_accepts_16kb_aligned_aarch64_load_segment() -> None:
    result = inspect_elf("valid.so", make_elf())
    assert result["pass"] is True


def test_rejects_load_segment_below_16kb() -> None:
    result = inspect_elf("small-align.so", make_elf(alignment=4096))
    assert result["pass"] is False


def test_rejects_incongruent_file_and_virtual_offsets() -> None:
    result = inspect_elf(
        "incongruent.so",
        make_elf(file_offset=0, virtual_address=4096),
    )
    assert result["pass"] is False
    assert "not congruent" in result["failures"][0]  # type: ignore[index]


def test_rejects_non_aarch64_and_missing_load_segments() -> None:
    with pytest.raises(ValueError, match="AArch64"):
        inspect_elf("wrong-arch.so", make_elf(machine=62))
    with pytest.raises(ValueError, match="no PT_LOAD"):
        inspect_elf("no-load.so", make_elf(include_load=False))
