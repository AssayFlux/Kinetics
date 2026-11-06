"""Immutable, license-gated dataset releases with verifiable artifact hashes."""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import tempfile
from typing import Any

import pandas as pd

from .provenance import environment_record, sha256_file, write_json_atomic
from .quality import audit_observations


def create_dataset_release(
    observations_csv: str | Path,
    rejected_csv: str | Path,
    output_dir: str | Path,
    *,
    dataset_id: str,
    dataset_name: str,
    source: str,
    source_version: str,
    license_id: str,
    citation: str,
    source_url: str | None = None,
) -> dict[str, Any]:
    """Create a new immutable release; require explicit license and citation metadata."""
    required = {
        "dataset_id": dataset_id, "dataset_name": dataset_name, "source": source,
        "source_version": source_version, "license_id": license_id, "citation": citation,
    }
    missing = [key for key, value in required.items() if not isinstance(value, str) or not value.strip()]
    if missing:
        raise ValueError(f"Release requires verified non-empty metadata: {missing}")
    observations = Path(observations_csv).resolve()
    rejected = Path(rejected_csv).resolve()
    destination = Path(output_dir).resolve()
    for path in (observations, rejected):
        if not path.is_file():
            raise FileNotFoundError(path)
        if destination == path or destination in path.parents:
            raise ValueError("Release directory must not contain or overwrite source artifacts")
    if observations == rejected:
        raise ValueError("Observations and rejection audit must be separate files")
    if destination.exists():
        raise FileExistsError(f"Immutable release already exists: {destination}")

    frame = pd.read_csv(observations, dtype={"source_record_id": "string"})
    audited, duplicates, quality = audit_observations(frame)
    if audited.empty:
        raise ValueError("Cannot release an empty canonical observation dataset")
    if "target" not in audited or not set(audited["target"]).issubset({"km", "kcat"}):
        raise ValueError("Release contains unsupported kinetic targets")
    expected = audited["target"].map({"km": "M", "kcat": "s^-1"})
    if "canonical_unit" not in audited or not audited["canonical_unit"].eq(expected).all():
        raise ValueError("Release contains target-incompatible canonical units")

    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{destination.name}.staging-", dir=destination.parent))
    try:
        shutil.copy2(observations, staging / "observations.csv")
        shutil.copy2(rejected, staging / "rejected_rows.csv")
        audited.to_csv(staging / "observations_audited.csv", index=False)
        duplicates.to_csv(staging / "duplicate_audit.csv", index=False)
        write_json_atomic(quality, staging / "quality_report.json")
        artifacts = {
            name: {"sha256": sha256_file(staging / name), "size_bytes": (staging / name).stat().st_size}
            for name in (
                "observations.csv", "rejected_rows.csv", "observations_audited.csv",
                "duplicate_audit.csv", "quality_report.json",
            )
        }
        manifest = {
            "schema_version": "kinetics-kdb-release-v1",
            "dataset_id": dataset_id,
            "dataset_name": dataset_name,
            "source": source,
            "source_url": source_url,
            "source_version": source_version,
            "license": {"identifier": license_id, "verified_by_release_operator": True},
            "citation": citation,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "environment": environment_record(),
            "counts": {
                "observations": int(len(audited)),
                "rejected_rows": int(len(pd.read_csv(rejected))),
                "duplicate_groups": int(quality.get("n_duplicate_groups", 0)),
                "conflicting_groups": int(quality.get("n_conflicting_groups", 0)),
            },
            "artifacts": artifacts,
            "policy": (
                "Rows are retained; duplicates and conflicts are reported, never averaged "
                "or overwritten. Km and kcat remain independent observations."
            ),
        }
        write_json_atomic(manifest, staging / "release_manifest.json")
        (staging / "DATA_CARD.md").write_text(
            f"# {dataset_name}\n\n"
            f"- Dataset ID: {dataset_id}\n- Source: {source}\n"
            f"- Source version: {source_version}\n- License: {license_id}\n"
            f"- Citation: {citation}\n- Observations: {len(audited)}\n"
            f"- Rejected rows: {manifest['counts']['rejected_rows']}\n"
            f"- Duplicate groups: {manifest['counts']['duplicate_groups']}\n"
            f"- Conflicting groups: {manifest['counts']['conflicting_groups']}\n\n"
            "This release contains in-vitro enzyme kinetic observations. "
            "Conflicts are disclosed, not averaged. Verify the manifest before use.\n",
            encoding="utf-8",
        )
        staging.rename(destination)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return verify_dataset_release(destination)


def verify_dataset_release(release_dir: str | Path) -> dict[str, Any]:
    """Verify every artifact in a release manifest; fail closed on missing or altered files."""
    root = Path(release_dir)
    manifest_path = root / "release_manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "kinetics-kdb-release-v1":
        raise ValueError("Unsupported dataset release manifest schema")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict) or not artifacts:
        raise ValueError("Release manifest has no artifact inventory")
    verified = []
    for name, expected in artifacts.items():
        path = root / name
        if not path.is_file():
            raise ValueError(f"Release artifact is missing: {name}")
        actual = sha256_file(path)
        if actual != expected.get("sha256"):
            raise ValueError(f"Release artifact checksum mismatch: {name}")
        if path.stat().st_size != expected.get("size_bytes"):
            raise ValueError(f"Release artifact size mismatch: {name}")
        verified.append(name)
    return {"dataset_id": manifest["dataset_id"], "verified": True, "artifacts_verified": verified}
