from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

from kinetics.s4_process import (
    PinnedSubprocessPredictionEngine,
    run_pinned_local_prediction,
)


def _fixture(tmp_path: Path) -> tuple[Path, Path, str, str]:
    weights = tmp_path / "weights.bin"
    weights.write_bytes(b"synthetic weights")
    executable = tmp_path / "engine.py"
    executable.write_text(
        "#!" + sys.executable + "\n"
        "import json, pathlib, sys\n"
        "args = sys.argv[1:]\n"
        "request = pathlib.Path(args[args.index('--kinetics-request') + 1])\n"
        "response = pathlib.Path(args[args.index('--kinetics-response') + 1])\n"
        "data = json.loads(request.read_text())\n"
        "seq = data['sequence']\n"
        "response.write_text(json.dumps({\n"
        " 'schema': 'kinetics.structure-prediction.v1',\n"
        " 'input_sequence_sha256': __import__('hashlib').sha256(seq.encode()).hexdigest(),\n"
        " 'sequence_length': len(seq), 'model': data['model'], 'node': data['node'],\n"
        " 'created_at': '2026-11-10T00:00:00Z',\n"
        " 'predicted_structure': {'schema':'kinetics.structure-view.v1', 'source_format':'pdb', 'coordinate_unit':'angstrom', 'atom_count':1, 'atoms':[{'serial':1,'name':'CA','residue':'ALA','chain':'A','residue_number':1,'element':'C','xyz':[0.0,0.0,0.0]}], 'limitations':['synthetic fixture']},\n"
        " 'confidence': {'plddt_per_residue':[50.0]*len(seq), 'mean_plddt':50.0,\n"
        "  'pae_mean_angstrom':None, 'pae_max_angstrom':None},\n"
        " 'limitations':['synthetic fixture only']\n"
        "}))\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    return (
        executable,
        weights,
        hashlib.sha256(executable.read_bytes()).hexdigest(),
        hashlib.sha256(weights.read_bytes()).hexdigest(),
    )


def _engine(tmp_path: Path) -> PinnedSubprocessPredictionEngine:
    executable, weights, executable_hash, weights_hash = _fixture(tmp_path)
    return PinnedSubprocessPredictionEngine(
        executable_path=str(executable),
        executable_sha256=executable_hash,
        weights_path=str(weights),
        weights_sha256=weights_hash,
        model_name="synthetic",
        model_version="1",
        model_license="CC0-1.0",
        engine_id="fixture-engine",
        software_version="1",
        node_id="local-test",
        run_id="fixture-run-1",
    )


def test_pinned_local_prediction_process_validates_full_envelope(
    tmp_path: Path,
) -> None:
    result = run_pinned_local_prediction("AG", _engine(tmp_path))
    assert result["execution_mode"] == "local"
    assert result["validation"]["status"] == "unverified_prediction"


def test_pinned_local_prediction_rejects_artifact_hash_mismatch(
    tmp_path: Path,
) -> None:
    executable, weights, _, weights_hash = _fixture(tmp_path)
    with pytest.raises(ValueError, match="executable SHA-256"):
        PinnedSubprocessPredictionEngine(
            executable_path=str(executable),
            executable_sha256="0" * 64,
            weights_path=str(weights),
            weights_sha256=weights_hash,
            model_name="synthetic",
            model_version="1",
            model_license="CC0-1.0",
            engine_id="fixture-engine",
            software_version="1",
            node_id="local-test",
            run_id="fixture-run-1",
        )


def test_pinned_local_prediction_rejects_nonzero_exit_and_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = _engine(tmp_path)
    import kinetics.s4_process as module

    class Failed:
        returncode = 2

    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: Failed())
    with pytest.raises(RuntimeError, match="status 2"):
        engine.predict("AG")
