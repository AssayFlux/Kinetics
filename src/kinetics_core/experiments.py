"""Reproducible experiment manifests and artifact provenance."""
from __future__ import annotations

from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any

from .provenance import environment_record, file_record, write_json_atomic


DEFAULT_PACKAGES = ("numpy", "pandas", "scikit-learn", "xgboost", "torch", "transformers", "rdkit")


def package_versions(packages: tuple[str, ...] = DEFAULT_PACKAGES) -> dict[str, str | None]:
    """Return installed package versions without failing on optional dependencies."""
    versions: dict[str, str | None] = {}
    for package in packages:
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = None
    return versions


def build_experiment_manifest(
    *,
    experiment_id: str,
    research_question: str,
    inputs: list[str | Path],
    configuration: dict[str, Any],
    outputs: list[str | Path] | None = None,
    dataset_citations: list[str] | None = None,
    git_revision: str | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    """Build a self-describing manifest for a computational research run."""
    if not experiment_id.strip() or not research_question.strip():
        raise ValueError("experiment_id and research_question are required")
    input_records = [file_record(path) for path in inputs]
    output_records = [file_record(path) for path in (outputs or [])]
    return {
        "schema_version": "1.0",
        "experiment_id": experiment_id,
        "research_question": research_question,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "git_revision": git_revision,
        "inputs": input_records,
        "outputs": output_records,
        "configuration": configuration,
        "dataset_citations": dataset_citations or [],
        "environment": environment_record(),
        "package_versions": package_versions(),
        "notes": notes or [],
    }


def save_experiment_manifest(manifest: dict[str, Any], destination: str | Path) -> Path:
    """Persist a manifest as stable, human-readable JSON."""
    return write_json_atomic(manifest, destination)
