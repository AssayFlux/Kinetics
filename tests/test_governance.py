from __future__ import annotations

import csv
import io

from scripts.check_governance import validate
from scripts.generate_governance_claims import render


def test_track_g_governance_registers_are_structurally_complete() -> None:
    assert validate() == []


def test_capability_claim_matrix_is_conservative_and_reproducible() -> None:
    rendered = render()
    assert rendered.startswith("capability_id,capability_name,")
    assert "no scientific validity is implied" in rendered
    assert "device_status,license_status" in rendered
    rows = list(csv.DictReader(io.StringIO(rendered)))
    capability_ids = [row["capability_id"] for row in rows]
    assert len(rows) == 68
    assert len(capability_ids) == len(set(capability_ids))
    assert all(row["device_status"] == "OPEN" for row in rows)
    assert all(row["license_status"] == "OPEN" for row in rows)


def test_dependency_register_never_implies_unreviewed_clearance() -> None:
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / (
        "docs/track-g/dependency-decision-register.csv"
    )
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows
    assert all(row["license_status"] for row in rows)
    assert all(row["redistribution_status"] for row in rows)
    assert all(row["reviewer"] for row in rows)
