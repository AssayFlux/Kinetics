"""Machine-readable release evidence validation for Step 10.

A valid manifest is a review aid, not a deployment, security certification, or sign-off.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from typing import Any, Literal

EvidenceState = Literal["not_run", "blocked", "passed", "failed", "waived"]
REQUIRED_GATES = (
    "build_compatibility",
    "scientific_reproducibility",
    "security_privacy",
    "runtime_resilience",
    "user_acceptance",
    "operations_documentation",
)
_STATES = {"not_run", "blocked", "passed", "failed", "waived"}
_SHA = re.compile(r"^[0-9a-f]{40}$")
_SEMVER = re.compile(
    r"^v?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:[-+][0-9A-Za-z.-]+)?$"
)


@dataclass(frozen=True, slots=True)
class GateResult:
    gate_id: str
    state: EvidenceState
    evidence: tuple[str, ...] = ()
    severity: Literal["critical", "non_critical"] = "critical"
    approver: str | None = None
    rationale: str | None = None
    expires_on: str | None = None
    compensating_control: str | None = None

    def validate(self) -> None:
        if not self.gate_id.strip():
            raise ValueError("gate_id is required")
        if self.state not in _STATES:
            raise ValueError(f"unsupported evidence state: {self.state}")
        if self.severity not in ("critical", "non_critical"):
            raise ValueError("severity must be critical or non_critical")
        if self.state == "passed" and not self.evidence:
            raise ValueError(f"passed gate {self.gate_id} requires evidence references")
        if self.state == "waived":
            if self.severity != "non_critical":
                raise ValueError(f"critical gate {self.gate_id} cannot be waived")
            for name in ("approver", "rationale", "expires_on", "compensating_control"):
                value = getattr(self, name)
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"waived gate {self.gate_id} requires {name}")
            try:
                date.fromisoformat(self.expires_on)
            except ValueError as exc:
                raise ValueError(
                    f"waived gate {self.gate_id} expires_on must be an ISO date"
                ) from exc


def evaluate_release(manifest: dict[str, Any]) -> dict[str, Any]:
    """Validate a candidate manifest and return a conservative GO/CONDITIONAL/NO-GO result."""
    if not isinstance(manifest, dict):
        raise TypeError("release manifest must be an object")
    version = manifest.get("version")
    commit = manifest.get("source_commit")
    if not isinstance(version, str) or not _SEMVER.fullmatch(version):
        raise ValueError("version must be semantic version text")
    if not isinstance(commit, str) or not _SHA.fullmatch(commit):
        raise ValueError("source_commit must be a 40-character lowercase commit SHA")
    gates = manifest.get("gates")
    if not isinstance(gates, list):
        raise ValueError("gates must be a list")
    parsed: dict[str, GateResult] = {}
    for item in gates:
        if not isinstance(item, dict):
            raise ValueError("each gate must be an object")
        gate_id = item.get("gate_id")
        evidence = item.get("evidence", [])
        if not isinstance(gate_id, str) or not gate_id.strip():
            raise ValueError("gate_id must be non-empty text")
        if not isinstance(evidence, list) or any(
            not isinstance(ref, str) or not ref.strip() for ref in evidence
        ):
            raise ValueError(f"gate {gate_id} evidence must be a list of non-empty references")
        if len(set(evidence)) != len(evidence):
            raise ValueError(f"gate {gate_id} evidence references must be unique")
        gate = GateResult(
            gate_id=gate_id,
            state=item.get("state", "not_run"),
            evidence=tuple(evidence),
            severity=item.get("severity", "critical"),
            approver=item.get("approver"),
            rationale=item.get("rationale"),
            expires_on=item.get("expires_on"),
            compensating_control=item.get("compensating_control"),
        )
        gate.validate()
        if gate.gate_id in parsed:
            raise ValueError(f"duplicate gate_id: {gate.gate_id}")
        parsed[gate.gate_id] = gate

    missing = sorted(set(REQUIRED_GATES) - parsed.keys())
    if missing:
        raise ValueError(f"missing required release gates: {missing}")
    incomplete = sorted(
        gate.gate_id for gate in parsed.values()
        if gate.state in {"not_run", "blocked", "failed"}
    )
    waived = sorted(gate.gate_id for gate in parsed.values() if gate.state == "waived")
    decision = "NO-GO" if incomplete else ("CONDITIONAL" if waived else "GO")
    return {
        "manifest_schema": "kinetics.release-candidate/1.0",
        "version": version,
        "source_commit": commit,
        "decision": decision,
        "missing_gates": missing,
        "incomplete_gates": incomplete,
        "waived_gates": waived,
        "release_signoff": False,
        "notice": "Automated gate evaluation is not an accountable human release sign-off.",
    }
