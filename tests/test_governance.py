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


def test_security_and_data_flow_inventories_have_complete_stable_ids() -> None:
    from pathlib import Path
    import re

    root = Path(__file__).resolve().parents[1]
    security = (root / "docs/track-g/security-verification-matrix.md").read_text()
    flows = (root / "docs/track-g/data-flow-inventory.md").read_text()
    security_ids = re.findall(r"\|\s*(SEC-\d{3})\s*\|", security)
    flow_ids = re.findall(r"\|\s*(DF-\d{2})\s*\|", flows)
    assert set(security_ids) == {f"SEC-{number:03d}" for number in range(1, 17)}
    assert len(security_ids) == len(set(security_ids)) == 16
    assert set(flow_ids) == {f"DF-{number:02d}" for number in range(1, 9)}
    assert len(flow_ids) == len(set(flow_ids)) == 8


def test_operational_templates_keep_exercise_status_and_evidence_explicit() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    controls = (root / "docs/track-g/operational-controls.md").read_text()
    assert "No exercise is marked complete by this template" in controls
    for exercise in ("OPS-TT-01", "OPS-TT-02", "OPS-TT-03", "OPS-TT-04", "OPS-TT-05"):
        rows = [line for line in controls.splitlines() if line.startswith("|") and exercise in line]
        assert len(rows) == 1
        status = rows[0].strip("|").split("|")[-1].strip()
        assert status == "NOT RUN" or status.startswith("COMPLETED — evidence:")
