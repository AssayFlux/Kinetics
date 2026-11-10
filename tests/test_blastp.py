from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

from kinetics.blastp import hash_blast_protein_database, run_local_blastp


def _artifacts(tmp_path: Path) -> tuple[Path, Path, dict[str, str]]:
    executable = tmp_path / "blastp.py"
    script = [
        "#!" + sys.executable,
        "import pathlib, sys",
        "if '-version' in sys.argv:",
        " print('blastp: 2.16.0+')",
        " raise SystemExit(0)",
        "args=sys.argv[1:]",
        "out=pathlib.Path(args[args.index('-out')+1])",
        "out.write_text('q1\\\\ts1\\\\t98.0\\\\t10\\\\t0\\\\t0\\\\t1\\\\t10\\\\t5\\\\t14\\\\t1e-20\\\\t42.0\\\\t10\\\\t100\\\\n')",
    ]
    executable.write_text("\n".join(script) + "\n", encoding="utf-8")
    executable.chmod(0o755)
    prefix = tmp_path / "protein_db"
    digests: dict[str, str] = {}
    for suffix in (".pin", ".phr", ".psq"):
        artifact = Path(str(prefix) + suffix)
        artifact.write_bytes(("db" + suffix).encode("ascii"))
        digests[suffix] = hashlib.sha256(artifact.read_bytes()).hexdigest()
    return executable, prefix.with_suffix(".pin"), digests


def test_local_blastp_runs_against_hash_pinned_database(tmp_path: Path) -> None:
    executable, pin_file, digests = _artifacts(tmp_path)
    prefix = str(pin_file)[:-4]
    result = run_local_blastp(
        ">q1\nACDEFGHIKL\n",
        executable_path=str(executable),
        executable_sha256=hashlib.sha256(executable.read_bytes()).hexdigest(),
        database_prefix=prefix,
        database_file_sha256=digests,
        database_id="synthetic-db",
        database_version="1",
        database_license="CC0-1.0",
        database_source="https://example.org/db",
    )
    assert result["hit_count"] == 1
    assert result["conclusion"] == "candidate_homology_hits_require_review"


def test_local_blastp_rejects_database_tampering_and_bad_query(
    tmp_path: Path,
) -> None:
    executable, pin_file, digests = _artifacts(tmp_path)
    prefix = str(pin_file)[:-4]
    with pytest.raises(ValueError, match="FASTA"):
        run_local_blastp(
            "ACDEFGHIKL",
            executable_path=str(executable),
            executable_sha256=hashlib.sha256(executable.read_bytes()).hexdigest(),
            database_prefix=prefix,
            database_file_sha256=digests,
            database_id="synthetic-db",
            database_version="1",
            database_license="CC0-1.0",
            database_source="https://example.org/db",
        )
    (Path(prefix + ".psq")).write_bytes(b"tampered")
    with pytest.raises(ValueError, match="digest mismatch"):
        hash_blast_protein_database(prefix, digests)
