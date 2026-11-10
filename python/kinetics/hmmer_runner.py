"""Bounded local HMMER execution and evidence parsing.

No downloads, shell expansion, or implicit executable/profile discovery occur.
The caller supplies explicit local paths and SHA-256 digests for both artifacts.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Mapping

from .hmmer import parse_hmmscan_domtblout


def _child_file_limit(max_bytes: int) -> Callable[[], None] | None:
    """Apply a kernel-enforced output-file ceiling on POSIX child processes."""
    if sys.platform == "win32":
        return None

    def apply_limit() -> None:
        import resource

        resource.setrlimit(resource.RLIMIT_FSIZE, (max_bytes, max_bytes))

    return apply_limit


def _sha256_file(path: Path, *, max_bytes: int) -> tuple[str, int]:
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"Artifact exceeds byte limit: {path.name}")
            digest.update(chunk)
    return digest.hexdigest(), total


def run_local_hmmscan(
    sequences_fasta: str,
    *,
    executable_path: str,
    executable_sha256: str,
    profile_path: str,
    profile_pack: Mapping[str, str],
    max_input_bytes: int = 64 * 1024 * 1024,
    max_profile_bytes: int = 512 * 1024 * 1024,
    max_executable_bytes: int = 512 * 1024 * 1024,
    max_output_bytes: int = 64 * 1024 * 1024,
    timeout_seconds: int = 300,
    max_domains: int = 1_000_000,
) -> dict[str, object]:
    """Run a locally installed hmmscan against one explicitly pinned HMM file."""
    if not isinstance(sequences_fasta, str) or not sequences_fasta.strip():
        raise ValueError("sequences_fasta must be non-empty text")
    fasta_bytes = sequences_fasta.encode("utf-8")
    if len(fasta_bytes) > max_input_bytes:
        raise ValueError("FASTA input exceeds max_input_bytes")
    if not sequences_fasta.lstrip().startswith(">"):
        raise ValueError("FASTA input must begin with a record header")
    for name, value in (
        ("max_input_bytes", max_input_bytes),
        ("max_profile_bytes", max_profile_bytes),
        ("max_executable_bytes", max_executable_bytes),
        ("max_output_bytes", max_output_bytes),
        ("timeout_seconds", timeout_seconds),
        ("max_domains", max_domains),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    expected_executable_hash = executable_sha256
    if (
        not isinstance(expected_executable_hash, str)
        or len(expected_executable_hash) != 64
        or any(c not in "0123456789abcdef" for c in expected_executable_hash)
    ):
        raise ValueError("executable_sha256 must be lowercase SHA-256 hex")

    executable = Path(executable_path).expanduser().resolve(strict=True)
    profile = Path(profile_path).expanduser().resolve(strict=True)
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise ValueError("HMMER executable_path must be an executable regular file")
    if not profile.is_file():
        raise ValueError("profile_path must be a regular file")
    executable_hash, _ = _sha256_file(
        executable, max_bytes=max_executable_bytes,
    )
    if executable_hash != expected_executable_hash:
        raise ValueError("HMMER executable SHA-256 does not match approved digest")
    profile_hash, _ = _sha256_file(profile, max_bytes=max_profile_bytes)
    if dict(profile_pack).get("content_sha256") != profile_hash:
        raise ValueError("HMM profile SHA-256 does not match profile-pack metadata")

    with tempfile.TemporaryDirectory(prefix="kinetics-hmmscan-") as work_dir:
        work = Path(work_dir)
        fasta_path = work / "queries.fasta"
        output_path = work / "domains.tbl"
        stderr_path = work / "hmmscan.stderr"
        fasta_path.write_bytes(fasta_bytes)
        env = {
            "HOME": str(work),
            "TMPDIR": str(work),
            "TEMP": str(work),
            "TMP": str(work),
            "LANG": "C",
            "LC_ALL": "C",
        }
        try:
            with stderr_path.open("wb") as stderr_handle:
                run_result = subprocess.run(
                    [
                        str(executable),
                        "--noali",
                        "--domtblout",
                        str(output_path),
                        str(profile),
                        str(fasta_path),
                    ],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=stderr_handle,
                    cwd=work,
                    env=env,
                    check=False,
                    timeout=timeout_seconds,
                    shell=False,
                    preexec_fn=_child_file_limit(max_output_bytes),
                )
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError("Local hmmscan exceeded timeout_seconds") from exc

        if run_result.returncode != 0:
            raise RuntimeError(f"hmmscan exited with status {run_result.returncode}")
        if stderr_path.stat().st_size > max_output_bytes:
            raise ValueError("HMMER diagnostic output exceeds max_output_bytes")
        stderr_text = stderr_path.read_text(encoding="utf-8", errors="replace")
        if not output_path.exists():
            raise RuntimeError(
                f"hmmscan did not create domtblout (diagnostics: {stderr_text[-2000:]})"
            )
        if output_path.stat().st_size > max_output_bytes:
            raise ValueError("HMMER domtblout exceeds max_output_bytes")
        if not output_path.is_file():
            raise RuntimeError("hmmscan domtblout is not a regular file")
        # HMMER's version output is requested from the same pinned executable.
        version_result = subprocess.run(
            [str(executable), "-h"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=work,
            env=env,
            check=False,
            timeout=min(timeout_seconds, 30),
            shell=False,
        )
        if version_result.returncode != 0:
            raise RuntimeError("Pinned executable failed the HMMER version check")
        version_text = version_result.stdout[:65536].decode("utf-8", errors="replace")
        version_line = next(
            (line.strip() for line in version_text.splitlines()
             if line.startswith("# HMMER") or "HMMER " in line),
            "",
        )
        if not version_line:
            raise RuntimeError("Pinned executable did not identify itself as HMMER")
        if not stderr_text.strip() and output_path.stat().st_size == 0:
            # An empty valid result is allowed, but still parsed as an empty evidence set.
            pass
        with output_path.open("r", encoding="utf-8", errors="strict") as handle:
            evidence = parse_hmmscan_domtblout(
                handle,
                hmmer_version=version_line,
                profile_pack=dict(profile_pack),
                max_lines=max_output_bytes,
                max_line_bytes=min(max_output_bytes, 16_384),
                max_domains=max_domains,
            )
        return {
            "schema": "kinetics.local-hmmscan-run.v1",
            "execution_mode": "local",
            "executable_sha256": executable_hash,
            "profile_pack_sha256": profile_hash,
            "evidence": evidence,
            "diagnostics": stderr_text[-2000:],
            "limitations": [
                "The host must approve HMMER executable and profile-pack licenses.",
                "The caller is responsible for validating profile provenance and thresholds.",
                "Profile hits are candidates, not validated protein-family or function assignments.",
                "No network access is requested; the host must enforce OS-level network isolation.",
            ],
        }
