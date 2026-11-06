import pytest

from kinetics_core.release_gate import REQUIRED_GATES, evaluate_release


def manifest(state="passed"):
    return {
        "version": "0.3.0",
        "source_commit": "a" * 40,
        "gates": [
            {"gate_id": gate, "state": state, "evidence": [f"evidence:{gate}"]}
            for gate in REQUIRED_GATES
        ],
    }


def test_all_required_gates_with_evidence_produce_go_but_not_signoff():
    result = evaluate_release(manifest())
    assert result["decision"] == "GO"
    assert result["release_signoff"] is False


@pytest.mark.parametrize("state", ["not_run", "blocked", "failed"])
def test_any_incomplete_or_failed_gate_is_no_go(state):
    candidate = manifest()
    candidate["gates"][0]["state"] = state
    assert evaluate_release(candidate)["decision"] == "NO-GO"


def test_missing_gate_is_rejected():
    candidate = manifest()
    candidate["gates"].pop()
    with pytest.raises(ValueError, match="missing required"):
        evaluate_release(candidate)


def test_critical_gate_cannot_be_waived():
    candidate = manifest()
    candidate["gates"][0] = {"gate_id": REQUIRED_GATES[0], "state": "waived",
                             "approver": "reviewer", "rationale": "reason",
                             "expires_on": "2026-12-01",
                             "compensating_control": "manual review"}
    with pytest.raises(ValueError, match="cannot be waived"):
        evaluate_release(candidate)


def test_complete_noncritical_waiver_is_conditional():
    candidate = manifest()
    candidate["gates"][0] = {"gate_id": REQUIRED_GATES[0], "state": "waived",
                             "severity": "non_critical", "approver": "reviewer",
                             "rationale": "temporary limitation", "expires_on": "2026-12-01",
                             "compensating_control": "manual review"}
    assert evaluate_release(candidate)["decision"] == "CONDITIONAL"


def test_bad_source_commit_is_rejected():
    candidate = manifest()
    candidate["source_commit"] = "main"
    with pytest.raises(ValueError, match="commit SHA"):
        evaluate_release(candidate)


def test_evidence_must_be_a_list_of_unique_nonempty_references():
    candidate = manifest()
    candidate["gates"][0]["evidence"] = "not-a-list"
    with pytest.raises(ValueError, match="list of non-empty"):
        evaluate_release(candidate)
    candidate = manifest()
    candidate["gates"][0]["evidence"] = ["evidence:build", "evidence:build"]
    with pytest.raises(ValueError, match="unique"):
        evaluate_release(candidate)


def test_waiver_expiry_must_be_iso_date():
    candidate = manifest()
    candidate["gates"][0] = {
        "gate_id": REQUIRED_GATES[0], "state": "waived",
        "severity": "non_critical", "approver": "reviewer",
        "rationale": "temporary limitation", "expires_on": "next month",
        "compensating_control": "manual review",
    }
    with pytest.raises(ValueError, match="ISO date"):
        evaluate_release(candidate)


def test_gate_id_must_be_nonempty_text():
    candidate = manifest()
    candidate["gates"][0]["gate_id"] = None
    with pytest.raises(ValueError, match="gate_id"):
        evaluate_release(candidate)
