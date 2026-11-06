#!/usr/bin/env python3
"""Download public CatPred-DB tables without modifying upstream data."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CATPRED_FILES = {
    "km/km_train.csv": "km/km_train.csv",
    "km/km_val.csv": "km/km_val.csv",
    "km/km_test.csv": "km/km_test.csv",
    "kcat/kcat_train.csv": "kcat/kcat_train.csv",
    "kcat/kcat_val.csv": "kcat/kcat_val.csv",
    "kcat/kcat_test.csv": "kcat/kcat_test.csv",
}
CATPRED_REVISION = "44409e6"
CATPRED_BASE_URL = "https://huggingface.co/datasets/RosettaCommons/CatPred-DB/resolve"

def download(url: str, destination: Path) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "AssayFlux-Kinetics/0.1"})
    digest = hashlib.sha256()
    size = 0
    temporary = destination.with_suffix(destination.suffix + ".part")
    try:
        with urllib.request.urlopen(request, timeout=60) as response, temporary.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)
                digest.update(chunk)
                size += len(chunk)
        if size == 0:
            raise RuntimeError("Downloaded an empty file")
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return {
        "file": destination.name,
        "source_url": url,
        "bytes": size,
        "sha256": digest.hexdigest(),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=["catpred-db"], default="catpred-db")
    parser.add_argument("--output-dir", default="data/public/catpred-db")
    parser.add_argument("--revision", default=CATPRED_REVISION, help="Pinned Hugging Face dataset revision")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest = {
        "dataset": "CatPred-DB",
        "repository": "https://github.com/maranasgroup/CatPred-DB",
        "source_revision": args.revision,
        "dataset_card": "https://huggingface.co/datasets/RosettaCommons/CatPred-DB",
        "license_note": "Pinned Hugging Face dataset card declares CC-BY-4.0; verify exact revision and redistribution terms.",
        "files": [],
    }
    for filename, relative_path in CATPRED_FILES.items():
        destination = output_dir / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        url = f"{CATPRED_BASE_URL}/{args.revision}/{relative_path}"
        if destination.exists() and not args.overwrite:
            digest = hashlib.sha256(destination.read_bytes()).hexdigest()
            manifest["files"].append({
                "file": filename, "source_url": url, "bytes": destination.stat().st_size,
                "sha256": digest, "status": "already_present_not_overwritten",
            })
            print(f"Keeping existing {destination}")
            continue
        print(f"Downloading {filename} ...", flush=True)
        record = download(url, destination)
        manifest["files"].append(record)
        print(f"Saved {destination} ({record['bytes']:,} bytes)")
        time.sleep(0.2)
    manifest["manifest_created_at"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest: {manifest_path}")

if __name__ == "__main__":
    main()
