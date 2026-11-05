"""File hashing and machine-readable provenance helpers."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
from typing import Any


def sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    """Compute a streaming SHA-256 digest without loading the full file into memory."""
    source = Path(path)
    digest = hashlib.sha256()
    with source.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: str | Path, source_url: str | None = None) -> dict[str, Any]:
    """Describe a local source artifact and its content hash."""
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)
    return {
        "path": str(source),
        "name": source.name,
        "size_bytes": source.stat().st_size,
        "sha256": sha256_file(source),
        "source_url": source_url,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }


def environment_record() -> dict[str, str]:
    """Capture minimal runtime metadata useful for reproducing a computational run."""
    return {
        "python": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "executable": sys.executable,
        "working_directory": os.getcwd(),
    }


def write_json_atomic(payload: dict[str, Any], destination: str | Path) -> Path:
    """Write JSON via a temporary file and atomic replace to avoid partial manifests."""
    output = Path(destination)
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output.name}.", suffix=".tmp", dir=output.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
        Path(temporary_name).replace(output)
    except Exception:
        Path(temporary_name).unlink(missing_ok=True)
        raise
    return output
