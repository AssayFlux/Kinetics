from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from kinetics.hmmer import parse_hmmscan_domtblout
from test_hmmer import PACK, ROW


def test_hmmscan_evidence_matches_versioned_schema() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads((root / "api" / "hmmscan-domain-evidence.schema.json").read_text())
    result = parse_hmmscan_domtblout(
        [ROW], hmmer_version="3.4", profile_pack=PACK,
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(result)
