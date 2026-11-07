#!/usr/bin/env python3
"""Restore verified corpus objects from the GitHub Release batches in the manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/corpus-manifests/metadata_index.json"
OBJECT_PREFIX = PurePosixPath("data/corpus/objects")


def gh(args: list[str]) -> None:
    subprocess.run(["gh", *args], cwd=ROOT, check=True, text=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--max-releases", type=int, default=1000)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    records = data.get("items", {})
    expected = {
        record["path"]: record["sha256"]
        for record in records.values()
        if record.get("status") == "downloaded" and record.get("release_uploaded")
        and record.get("path") and record.get("sha256")
    }
    releases: dict[str, str] = {}
    for record in records.values():
        if record.get("release_uploaded") and record.get("release_tag") and record.get("release_asset"):
            releases[record["release_tag"]] = record["release_asset"]
    if len(releases) > args.max_releases:
        raise RuntimeError(f"Manifest has {len(releases)} releases; limit is {args.max_releases}")

    restored = 0
    with tempfile.TemporaryDirectory(prefix="kinetics-release-restore-") as temp:
        temp_dir = Path(temp)
        for tag, asset_name in sorted(releases.items()):
            download_dir = temp_dir / tag
            download_dir.mkdir(parents=True, exist_ok=True)
            gh(["release", "download", tag, "--pattern", asset_name, "--dir", str(download_dir)])
            archives = list(download_dir.glob(asset_name))
            if len(archives) != 1:
                raise RuntimeError(f"Expected one archive for {tag}, found {len(archives)}")
            with tarfile.open(archives[0], "r:gz") as archive:
                for member in archive.getmembers():
                    member_path = PurePosixPath(member.name)
                    if (not member.isfile() or member.issym() or member.islnk()
                            or member_path.is_absolute() or ".." in member_path.parts
                            or member_path.parts[:3] != OBJECT_PREFIX.parts):
                        raise RuntimeError(f"Unsafe archive member rejected: {member.name}")
                    relative = member_path.as_posix()
                    digest_expected = expected.get(relative)
                    if not digest_expected:
                        raise RuntimeError(f"Archive member is absent from manifest: {relative}")
                    source = archive.extractfile(member)
                    if source is None:
                        raise RuntimeError(f"Cannot read archive member: {relative}")
                    payload = source.read(20 * 1024 * 1024 + 1)
                    if len(payload) > 20 * 1024 * 1024:
                        raise RuntimeError(f"Archive member exceeds 20 MiB: {relative}")
                    digest = hashlib.sha256(payload).hexdigest()
                    if digest != digest_expected:
                        raise RuntimeError(f"SHA-256 mismatch for restored object: {relative}")
                    target = (ROOT / relative).resolve()
                    if ROOT not in target.parents:
                        raise RuntimeError(f"Restore path escaped repository: {relative}")
                    target.parent.mkdir(parents=True, exist_ok=True)
                    temporary_target = target.with_suffix(target.suffix + ".restore")
                    temporary_target.write_bytes(payload)
                    temporary_target.replace(target)
                    restored += 1
    print(f"Restored and verified {restored} corpus objects from {len(releases)} releases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
