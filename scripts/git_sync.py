#!/usr/bin/env python3
"""Safely commit corpus manifests and optionally Git-LFS-managed public objects."""
from __future__ import annotations

import argparse
import base64
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str], *, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, env=env, text=True, capture_output=True, check=check)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", default=os.getenv("GITHUB_REF_NAME", "main"))
    parser.add_argument("--mode", choices=("manifest", "lfs"), default="manifest")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()
    if not (ROOT / ".git").exists():
        raise RuntimeError("Run this command inside a Git checkout")
    if args.mode == "lfs":
        run(["git", "lfs", "install", "--local"])
        run(["git", "lfs", "track", "*.pdf", "*.epub"])
        run(["git", "add", ".gitattributes"])
        run(["git", "add", "data/corpus/objects"])
    else:
        run(["git", "add", "data/corpus-manifests"])
    status = run(["git", "status", "--porcelain"]).stdout.strip()
    if not status:
        print("No corpus changes to commit")
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
