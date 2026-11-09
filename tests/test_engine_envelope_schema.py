from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (ROOT / "api" / "engine-envelope-v1.schema.json").read_text(encoding="utf-8")
)
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def _base(kind: str) -> dict:
    message = {
        "schema": "kinetics.engine-envelope.v1",
        "schema_version": 1,
        "kind": kind,
        "request_id": "7c3d2a91-4d66-4e6a-9c43-12b1d70a2e81",
        "created_at_utc": "2026-11-09T02:00:00Z",
        "operation": "sequence.fasta.qc",
        "engine": {"id": "kinetics.python.sequence", "version": "1.0.0"},
        "source_sha256": "a" * 64,
        "units": {"sequence_length": "base"},
    }
    if kind == "request":
        message["input"] = {"sequence": ">seq\nACGT"}
    elif kind == "result":
        message["output"] = {"record_count": 1, "total_bases": 4}
    else:
        message["error"] = {
            "code": "INVALID_ARGUMENT",
            "retryable": False,
            "message": "Input did not satisfy the FASTA contract.",
        }
    return message


def test_engine_envelope_schema_is_valid_draft_2020_12() -> None:
    Draft202012Validator.check_schema(SCHEMA)


@pytest.mark.parametrize("kind", ["request", "result", "error"])
def test_valid_message_kinds_follow_one_shared_envelope(kind: str) -> None:
    assert list(VALIDATOR.iter_errors(_base(kind))) == []


def test_rejects_unknown_schema_version_and_malformed_digest() -> None:
    message = _base("request")
    message["schema_version"] = 2
    message["source_sha256"] = "NOT-A-SHA256"
    errors = list(VALIDATOR.iter_errors(message))
    assert any(list(error.path) == ["schema_version"] for error in errors)
    assert any(list(error.path) == ["source_sha256"] for error in errors)


def test_rejects_payload_for_wrong_message_kind() -> None:
    message = _base("request")
    message["output"] = {"record_count": 1}
    assert list(VALIDATOR.iter_errors(message))


def test_rejects_timezone_free_timestamp_and_invalid_request_id() -> None:
    message = _base("request")
    message["created_at_utc"] = "2026-11-09T02:00:00"
    message["request_id"] = "not-a-uuid"
    errors = list(VALIDATOR.iter_errors(message))
    assert any(list(error.path) == ["created_at_utc"] for error in errors)
    assert any(list(error.path) == ["request_id"] for error in errors)
