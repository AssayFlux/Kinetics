#!/usr/bin/env python3
"""Keep the Android capability integration summary consistent with its row-level matrix."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "docs/track-u/android-capability-integration-matrix.md"
text = PATH.read_text(encoding="utf-8")

def section(start: str, end: str) -> str:
    try:
        return text.split(start, 1)[1].split(end, 1)[0]
    except IndexError as exc:
        raise SystemExit(f"Missing matrix section boundary: {start!r} / {end!r}") from exc

summary = section("## Summary", "## Connected Android workflows")
mapping = section("## Complete catalogue mapping", "## Remaining engineering work")
connected_section = section("## Connected Android workflows", "## Complete catalogue mapping")

def summary_count(label: str) -> int:
    match = re.search(rf"- {re.escape(label)}: \\*\\*(\\d+)\\*\\*", summary)
    if match is None:
        raise SystemExit(f"Missing numeric summary: {label}")
    return int(match.group(1))

rows = []
for line in mapping.splitlines():
    if not line.startswith("| `") or "| `python/" not in line:
        continue
    cells = [cell.strip() for cell in line.strip("|").split("|")]
    if len(cells) != 3:
        raise SystemExit(f"Malformed capability row: {line}")
    capability_id = cells[0].strip("`")
    status = cells[2]
    if status.startswith("Connected —"):
        rows.append((capability_id, True))
    elif status.startswith("Not connected —"):
        rows.append((capability_id, False))
    else:
        raise SystemExit(f"Unknown integration status for {capability_id}: {status}")

ids = [item[0] for item in rows]
if len(ids) != len(set(ids)):
    raise SystemExit("Duplicate capability IDs in integration matrix")
total = len(rows)
connected = sum(1 for _, is_connected in rows if is_connected)
not_connected = total - connected
expected = {
    "Catalogue entries": total,
    "Catalogue entries connected to Android workflows": connected,
    "Catalogue entries not yet connected to Android": not_connected,
}
for label, actual in expected.items():
    declared = summary_count(label)
    if declared != actual:
        raise SystemExit(f"{label}: summary says {declared}, row-level matrix says {actual}")

listed = set()
for line in connected_section.splitlines():
    if not line.startswith("| `"):
        continue
    capability_id = line.split("|", 2)[1].strip().strip("`")
    if capability_id != "Capability ID" and capability_id != "public.reference_databases":
        listed.add(capability_id)
actual_connected = {capability_id for capability_id, is_connected in rows if is_connected}
if listed != actual_connected:
    missing = sorted(actual_connected - listed)
    extra = sorted(listed - actual_connected)
    raise SystemExit(f"Connected workflow list mismatch; missing={missing}, extra={extra}")

print(f"Android capability matrix consistent: {total} catalogue entries, "
      f"{connected} connected, {not_connected} not connected")
