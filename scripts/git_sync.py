#!/usr/bin/env python3
"""Synchronize compact manifests and durable public corpus batches to GitHub."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/corpus-manifests/metadata_index.json"


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=check)


def save_manifest(data: dict) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    tmp = MANIFEST.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(MANIFEST)


def create_release_batch(manifest: dict) -> int:
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    repository = os.getenv("GITHUB_REPOSITORY")
    if not token or not repository:
        raise RuntimeError("Release mode requires GH_TOKEN/GITHUB_TOKEN and GITHUB_REPOSITORY")
    pending = []
    for item_id, record in manifest.get("items", {}).items():
        if record.get("status") != "downloaded" or record.get("release_uploaded"):
            continue
        path = (ROOT / record.get("path", "")).resolve()
        if ROOT not in path.parents or not path.is_file():
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != record.get("sha256"):
            raise RuntimeError(f"SHA-256 mismatch for {item_id}; refusing release upload")
        pending.append((item_id, record, path))
    if not pending:
        print("No new corpus objects to attach to a release")
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_id = os.getenv("GITHUB_RUN_ID", "local")
    tag = f"corpus-batch-{stamp}-{run_id}"
    archive_path = ROOT / f"kinetics-corpus-{tag}.tar.gz"
    try:
        with tarfile.open(archive_path, "w:gz") as archive:
            for _, record, path in pending:
                archive.add(path, arcname=record["path"], recursive=False)
        if archive_path.stat().st_size > 100 * 1024 * 1024:
            raise RuntimeError("Release archive exceeds 100 MiB safety ceiling")
        run(["gh", "release", "create", tag, str(archive_path),
             "--title", f"Kinetics corpus batch {tag}",
             "--notes", "Licensed public-domain/Creative Commons corpus batch. "
                        "See repository data manifest for per-item provenance and rights."])
        for item_id, record, _ in pending:
            record["release_uploaded"] = True
            record["release_tag"] = tag
            record["release_asset"] = archive_path.name
        save_manifest(manifest)
        print(f"Published {len(pending)} objects in https://github.com/{repository}/releases/tag/{tag}")
        return len(pending)
    finally:
        archive_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", default=os.getenv("GITHUB_REF_NAME", "main"))
    parser.add_argument("--mode", choices=("manifest", "lfs", "release"), default="manifest")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()
    if not (ROOT / ".git").exists():
        raise RuntimeError("Run this command inside a Git checkout")

    if args.mode == "release":
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        create_release_batch(manifest)
    elif args.mode == "lfs":
        run(["git", "lfs", "install", "--local"])
        run(["git", "lfs", "track", "*.pdf", "*.epub"])
        run(["git", "add", ".gitattributes"])
        run(["git", "add", "-f", "data/corpus/objects"])
    run(["git", "add", "data/corpus-manifests"])

    status = run(["git", "status", "--porcelain"]).stdout.strip()
    if not status:
        print("No manifest changes to commit")
        return 0
    run(["git", "config", "user.name", "github-actions[bot]"])
    run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"])
    run(["git", "commit", "-m", "data: ingest licensed knowledge batch [skip ci]"])
    if args.push:
        token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
        if not token:
            raise RuntimeError("Set GH_TOKEN or GITHUB_TOKEN to push")
        basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
        run(["git", "-c", f"http.extraheader=AUTHORIZATION: basic {basic}",
             "push", "origin", f"HEAD:{args.branch}"])
    print("Corpus synchronization complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
