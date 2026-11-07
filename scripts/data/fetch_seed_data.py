#!/usr/bin/env python3
"""Fetch explicitly enabled small public reference packs into the repository.

Bulk datasets are never downloaded implicitly. The catalog controls eligibility;
every file is streamed, SHA-256 verified, and accompanied by a provenance manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "database/sources/catalog.json"
SEED = ROOT / "database/seed"
USER_AGENT = "Kinetics-Scientific-Data-Importer/0.1 (+https://github.com/AssayFlux/Kinetics)"
CHUNK = 1024 * 1024
MAX_STARTER_BYTES = 250 * 1024 * 1024


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch(source: dict, force: bool = False) -> dict:
    if not source.get("enabled") or source.get("redistribution") != "allowed":
        raise RuntimeError(f"{source['id']}: source is not explicitly enabled for redistribution")
    url = source.get("download_or_api_url", "")
    if not url.startswith("https://") or not url.lower().endswith((".obo", ".obo.gz")):
        raise RuntimeError(f"{source['id']}: starter downloader only accepts HTTPS OBO files")
    suffix = ".obo.gz" if url.endswith(".obo.gz") else ".obo"
    target = SEED / f"{source['id']}{suffix}"
    partial = target.with_suffix(target.suffix + ".part")
    if target.exists() and not force:
        return {"id": source["id"], "path": str(target.relative_to(ROOT)), "sha256": sha256(target), "status": "already_present"}

    SEED.mkdir(parents=True, exist_ok=True)
    offset = partial.stat().st_size if partial.exists() else 0
    headers = {"User-Agent": USER_AGENT, "Accept-Encoding": "identity"}
    if offset:
        headers["Range"] = f"bytes={offset}-"
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request, timeout=45)
    except urllib.error.HTTPError as exc:
        if offset and exc.code == 416:
            partial.unlink(missing_ok=True)
            return fetch(source, force=True)
        raise

    status = getattr(response, "status", 200)
    if offset and status != 206:
        offset = 0
        partial.unlink(missing_ok=True)
    mode = "ab" if offset else "wb"
    length = response.headers.get("Content-Length")
    expected = int(length) + offset if length and length.isdigit() else None
    if expected and expected > MAX_STARTER_BYTES:
        response.close()
        raise RuntimeError(f"{source['id']}: starter pack exceeds {MAX_STARTER_BYTES} byte safety limit")

    written = offset
    with response, partial.open(mode) as output:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            written += len(chunk)
            if written > MAX_STARTER_BYTES:
                raise RuntimeError(f"{source['id']}: download exceeded starter pack size limit")
            output.write(chunk)
            output.flush()
            os.fsync(output.fileno())

    partial.replace(target)
    return {
        "id": source["id"], "name": source["name"],
        "url": url, "license_id": source.get("license_id"),
        "attribution": source.get("attribution"),
        "retrieved_unix": int(time.time()), "bytes": target.stat().st_size,
        "sha256": sha256(target), "path": str(target.relative_to(ROOT)),
        "status": "downloaded"
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", dest="sources", help="source id; repeatable")
    parser.add_argument("--force", action="store_true", help="replace existing starter pack")
    args = parser.parse_args()
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    selected = args.sources or [item["id"] for item in catalog["sources"] if item.get("enabled")]
    by_id = {item["id"]: item for item in catalog["sources"]}
    manifest_path = ROOT / "database/seed/MANIFEST.json"
    manifest = {"catalog_version": catalog["catalog_version"], "files": []}
    if manifest_path.exists() and not args.force:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    existing = {entry.get("id"): entry for entry in manifest.get("files", [])}
    failures = 0
    for source_id in selected:
        source = by_id.get(source_id)
        if source is None:
            print(f"Unknown source: {source_id}", file=sys.stderr)
            failures += 1
            continue
        try:
            result = fetch(source, args.force)
            existing[source_id] = result
            print(f"{source_id}: {result['status']} ({result['bytes'] if 'bytes' in result else 'cached'} bytes)")
        except Exception as exc:
            failures += 1
            print(f"{source_id}: ERROR: {exc}", file=sys.stderr)
    manifest["files"] = sorted(existing.values(), key=lambda item: item.get("id", ""))
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
