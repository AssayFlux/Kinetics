from __future__ import annotations
from scripts.check_registry import validate_registry

def base_registry() -> dict[str, object]:
    return {"schema_version": 1, "tools": [], "engines": [{"id": "engine-a"}],
            "data_packs": [{"id": "pack-a"}], "domains": [{"id": "domain-a"}],
            "device_logs": [{"id": "device-log-a"}],
            "clinical_gate": {"enabled": False, "part12_evidence": []}}

def test_empty_r0_registry_is_valid() -> None:
    assert validate_registry(base_registry()) == []

def test_missing_engine_reference_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "status": "planned", "engine_ids": ["missing"]}]
    assert any("missing engines id" in error for error in validate_registry(data))

def test_validated_without_record_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "status": "validated", "evidence_level": "benchmark"}]
    assert any("requires validation_records" in error for error in validate_registry(data))

def test_device_verified_without_log_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "device_verified": True}]
    assert any("requires device_log_ids" in error for error in validate_registry(data))

def test_device_verified_with_unknown_log_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "device_verified": True, "device_log_ids": ["missing"]}]
    assert any("missing device log" in error for error in validate_registry(data))

def test_clinical_capability_without_part12_gate_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "clinical": True}]
    assert any("clinical_gate.enabled" in error for error in validate_registry(data))

def test_clinical_capability_without_part12_evidence_is_rejected() -> None:
    data = base_registry()
    data["clinical_gate"] = {"enabled": True, "part12_evidence": []}
    data["tools"] = [{"id": "tool-a", "clinical": True}]
    assert any("Part 12 evidence" in error for error in validate_registry(data))

def test_invalid_status_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "status": "shipped"}]
    assert any("invalid status" in error for error in validate_registry(data))
