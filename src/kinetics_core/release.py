"""Immutable, license-gated dataset releases with verifiable artifact hashes."""
from __future__ import annotations

import json
import shutil
import tempfile
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from .provenance import environment_record, sha256_file, write_json_atomic
from .quality import audit_observations, review_potential_duplicate_observations


def create_dataset_release(
    observations_csv: str | Path,
    rejected_csv: str | Path | Sequence[str | Path],
    output_dir: str | Path,
    *,
    dataset_id: str,
    dataset_name: str,
    source: str,
    source_version: str,
    license_id: str,
    citation: str,
    source_url: str | None = None,
    source_manifests: Sequence[str | Path] = (),
) -> dict[str, Any]:
    """Create a new immutable release; require explicit license and citation metadata."""
    required = {
        "dataset_id": dataset_id,
        "dataset_name": dataset_name,
        "source": source,
        "source_version": source_version,
        "license_id": license_id,
        "citation": citation,
    }
    missing = [
        key for key, value in required.items()
        if not isinstance(value, str) or not value.strip()
    ]
    if missing:
        raise ValueError(f"Release requires verified non-empty metadata: {missing}")
    observations = Path(observations_csv).resolve()
    rejected_paths = (
        [Path(path).resolve() for path in rejected_csv]
        if isinstance(rejected_csv, (list, tuple))
        else [Path(rejected_csv).resolve()]
    )
    if not rejected_paths or len(set(rejected_paths)) != len(rejected_paths):
        raise ValueError("Provide one or more distinct rejection audit files")
    manifest_paths = [Path(path).resolve() for path in source_manifests]
    if len(set(manifest_paths)) != len(manifest_paths):
        raise ValueError("Source manifest paths must be distinct")
    destination = Path(output_dir).resolve()
    for path in [observations, *rejected_paths, *manifest_paths]:
        if not path.is_file():
            raise FileNotFoundError(path)
        if destination == path or destination in path.parents:
            raise ValueError("Release directory must not contain or overwrite source artifacts")
    if any(not path.is_file() for path in manifest_paths):
        raise FileNotFoundError("A supplied source manifest does not exist")
    if (
        observations in rejected_paths
        or observations in manifest_paths
        or set(rejected_paths).intersection(manifest_paths)
    ):
        raise ValueError("Observations and rejection audit must be separate files")
    if destination.exists():
        raise FileExistsError(f"Immutable release already exists: {destination}")

    frame = pd.read_csv(observations, dtype={"source_record_id": "string"})
    audited, duplicates, quality = audit_observations(frame)
    potential_duplicates = review_potential_duplicate_observations(audited)
    if audited.empty:
        raise ValueError("Cannot release an empty canonical observation dataset")
    if not set(audited["target"]).issubset({"km", "kcat"}):
        raise ValueError("Release contains unsupported kinetic targets")
    expected = audited["target"].map({"km": "M", "kcat": "s^-1"})
    if "canonical_unit" not in audited or not audited["canonical_unit"].eq(expected).all():
        raise ValueError("Release contains target-incompatible canonical units")

    rejection_frames = [pd.read_csv(path) for path in rejected_paths]
    rejected_frame = pd.concat(rejection_frames, ignore_index=True, sort=False)
    rejected_count = int(len(rejected_frame))
    aggregation_methods = sorted(
        str(value)
        for value in audited.get("aggregation_method", pd.Series(dtype=str)).dropna().unique()
    )
    measurement_kinds = sorted(
        str(value)
        for value in audited.get("measurement_kind", pd.Series(["individual_measurement"])).unique()
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.staging-", dir=destination.parent)
    )
    try:
        shutil.copy2(observations, staging / "observations.csv")
        rejected_frame.to_csv(staging / "rejected_rows.csv", index=False)
        audited.to_csv(staging / "observations_audited.csv", index=False)
        duplicates.to_csv(staging / "duplicate_audit.csv", index=False)
        potential_duplicates.to_csv(staging / "potential_duplicate_audit.csv", index=False)
        write_json_atomic(quality, staging / "quality_report.json")
        manifest_artifacts = []
        if manifest_paths:
            manifest_dir = staging / "source_manifests"
            manifest_dir.mkdir()
            for index, source_manifest in enumerate(manifest_paths, start=1):
                name = f"source_manifest_{index}.json"
                destination_manifest = manifest_dir / name
                shutil.copy2(source_manifest, destination_manifest)
                manifest_artifacts.append({
                    "name": f"source_manifests/{name}",
                    "sha256": sha256_file(destination_manifest),
                })
        (staging / "DATA_CARD.md").write_text(
            f"# {dataset_name}\n\n"
            f"- Dataset ID: {dataset_id}\n"
            f"- Source: {source}\n"
            f"- Source version: {source_version}\n"
            f"- License (operator supplied): {license_id}\n"
            f"- Citation: {citation}\n"
            f"- Observations: {len(audited)}\n"
            f"- Rejected rows: {rejected_count}\n"
            f"- Duplicate groups: {quality.get('n_duplicate_groups', 0)}\n"
            f"- Conflicting groups: {quality.get('n_conflicting_groups', 0)}\n\n"
            "This release contains in-vitro enzyme kinetic observations. "
            "Conflicts are disclosed, not averaged. License terms require manual review "
            "against the exact upstream snapshot. Verify the manifest before use.\n",
            encoding="utf-8",
        )
        artifact_names = (
            "observations.csv",
            "rejected_rows.csv",
            "observations_audited.csv",
            "duplicate_audit.csv",
            "potential_duplicate_audit.csv",
            "quality_report.json",
            "DATA_CARD.md",
        )
        artifacts = {
            name: {
                "sha256": sha256_file(staging / name),
                "size_bytes": (staging / name).stat().st_size,
            }
            for name in artifact_names
        }
        for source_manifest in manifest_artifacts:
            manifest_path = staging / source_manifest["name"]
            artifacts[source_manifest["name"]] = {
                "sha256": source_manifest["sha256"],
                "size_bytes": manifest_path.stat().st_size,
            }
        manifest = {
            "schema_version": "kinetics-kdb-release-v1",
            "dataset_id": dataset_id,
            "dataset_name": dataset_name,
            "source": source,
            "source_url": source_url,
            "source_version": source_version,
            "source_manifests": manifest_artifacts,
            "rejection_sources": [
                {"name": path.name, "sha256": sha256_file(path)} for path in rejected_paths
            ],
            "license": {
                "identifier": license_id,
                "status": "operator_supplied_requires_manual_source_terms_review",
            },
            "citation": citation,
            "measurement_kinds": measurement_kinds,
            "aggregation_methods": aggregation_methods,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "environment": environment_record(),
            "counts": {
                "observations": int(len(audited)),
                "rejected_rows": rejected_count,
                "duplicate_groups": int(quality.get("n_duplicate_groups", 0)),
                "conflicting_groups": int(quality.get("n_conflicting_groups", 0)),
                "potential_duplicate_groups": int(len(potential_duplicates)),
            },
            "artifacts": artifacts,
            "policy": (
                "Rows are retained; duplicates and conflicts are reported, never averaged "
                "or overwritten. Km and kcat remain independent observations."
            ),
        }
        write_json_atomic(manifest, staging / "release_manifest.json")
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
        relative_path = Path(name)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"Unsafe release artifact path: {name}")
        path = root / relative_path
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Release artifact escapes release directory: {name}")
        if not path.is_file():
            raise ValueError(f"Release artifact is missing: {name}")
        actual = sha256_file(path)
        if actual != expected.get("sha256"):
            raise ValueError(f"Release artifact checksum mismatch: {name}")
        if path.stat().st_size != expected.get("size_bytes"):
            raise ValueError(f"Release artifact size mismatch: {name}")
        verified.append(name)
    return {
        "dataset_id": manifest["dataset_id"],
        "verified": True,
        "artifacts_verified": verified,
    }
