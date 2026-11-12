from __future__ import annotations

from scripts.check_governance import validate
from scripts.generate_governance_claims import render


def test_track_g_governance_registers_are_structurally_complete() -> None:
    assert validate() == []


def test_capability_claim_matrix_is_conservative_and_reproducible() -> None:
    rendered = render()
    assert rendered.startswith("capability_id,capability_name,")
    assert "no scientific validity is implied" in rendered
    assert "device_status,license_status" in rendered
