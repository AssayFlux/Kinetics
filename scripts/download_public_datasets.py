#!/usr/bin/env python3
"""Download pinned CatPred-DB tables without modifying upstream data."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

HF_DATA_FILES = {
    "km/km_train.csv": "km/km_train.csv",
    "km/km_val.csv": "km/km_val.csv",
    "km/km_test.csv": "km/km_test.csv",
    "kcat/kcat_train.csv": "kcat/kcat_train.csv",
    "kcat/kcat_val.csv": "kcat/kcat_val.csv",
    "kcat/kcat_test.csv": "kcat/kcat_test.csv",
}
SEQUENCE_CLUSTER_TESTS = {
    "kcat-seq_test_sequence_20cluster.csv": "kcat-seq_test_sequence_20cluster.csv",
    "kcat-seq_test_sequence_40cluster.csv": "kcat-seq_test_sequence_40cluster.csv",
    "kcat-seq_test_sequence_60cluster.csv": "kcat-seq_test_sequence_60cluster.csv",
    "kcat-seq_test_sequence_80cluster.csv": "kcat-seq_test_sequence_80cluster.csv",
    "kcat-seq_test_sequence_99cluster.csv": "kcat-seq_test_sequence_99cluster.csv",
    "km-seq_test_sequence_40cluster.csv": "km-seq_test_sequence_40cluster.csv",
    "km-seq_test_sequence_60cluster.csv": "km-seq_test_sequence_60cluster.csv",
    "km-seq_test_sequence_80cluster.csv": "km-seq_test_sequence_80cluster.csv",
    "km-seq_test_sequence_99cluster.csv": "km-seq_test_sequence_99cluster.csv",
}
CATPRED_REVISION = "44409e6"
CATPRED_PROCESSING_REVISION = "931583821ff875e873002730fbbdf1047acfde77"
CATPRED_BASE_URL = "https://huggingface.co/datasets/RosettaCommons/CatPred-DB/resolve"
CATPRED_GITHUB_RAW = "https://raw.githubusercontent.com/maranasgroup/CatPred-DB"


def is_catpred_hf_url(url: str) -> bool:
    """Return whether a URL is on the exact gated dataset origin and path."""
    parsed = urlsplit(url)
    return (
        parsed.scheme == "https"
        and parsed.hostname == "huggingface.co"
        and parsed.port in (None, 443)
        and parsed.username is None
        and parsed.password is None
        and parsed.path.startswith("/datasets/RosettaCommons/CatPred-DB/")
    )


def request_headers(url: str, token: str | None = None) -> dict[str, str]:
    """Attach credentials only to the exact Hugging Face dataset origin."""
    headers = {"User-Agent": "AssayFlux-Kinetics/0.1"}
    if token and is_catpred_hf_url(url):
        headers["Authorization"] = f"Bearer {token}"
    return headers


class _SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Never forward a bearer token to a different redirect origin."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected is not None and req.has_header("Authorization"):
            if not is_catpred_hf_url(newurl):
                redirected.remove_header("Authorization")
        return redirected


def download(url: str, destination: Path, token: str | None = None) -> dict:
    request = urllib.request.Request(url, headers=request_headers(url, token))
    digest = hashlib.sha256()
    size = 0
    temporary = destination.with_suffix(destination.suffix + ".part")
    temporary.unlink(missing_ok=True)
    try:
        with (
            urllib.request.build_opener(_SafeRedirectHandler()).open(
                request, timeout=60
            ) as response,
            temporary.open("wb") as output,
        ):
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
    except urllib.error.HTTPError as exc:
        temporary.unlink(missing_ok=True)
        if (
            exc.code in (401, 403)
            and is_catpred_hf_url(url)
        ):
            raise RuntimeError(
                "CatPred-DB rejected this download (HTTP "
                f"{exc.code}). Open the dataset page in a browser, sign in, "
                "review and accept its access conditions, and obtain access. "
                "Then set HF_TOKEN to a read token for that same account and retry. "
                "The token is sent only to the Hugging Face dataset host and is "
                "never written to the manifest."
            ) from exc
        raise
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
    parser.add_argument(
        "--revision", default=CATPRED_REVISION,
        help="Pinned Hugging Face dataset revision",
    )
    parser.add_argument("--processing-revision", default=CATPRED_PROCESSING_REVISION)
    parser.add_argument(
        "--hf-token-env",
        default="HF_TOKEN",
        help="Environment variable containing a Hugging Face read token (default: HF_TOKEN)",
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-fA-F]{7,40}", args.revision):
        raise ValueError("--revision must be an immutable Git commit SHA, not a branch name")
    if not re.fullmatch(r"[0-9a-fA-F]{7,40}", args.processing_revision):
        raise ValueError("--processing-revision must be an immutable Git commit SHA")
    token = os.environ.get(args.hf_token_env)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    if manifest_path.exists() and not args.overwrite:
        raise FileExistsError(
            f"Download manifest exists: {manifest_path}; pass --overwrite or use a new directory"
        )
    manifest = {
        "dataset": "CatPred-DB",
        "repository": "https://github.com/maranasgroup/CatPred-DB",
        "source_revision": args.revision,
        "processing_code_revision": args.processing_revision,
        "dataset_card": "https://huggingface.co/datasets/RosettaCommons/CatPred-DB",
        "citation": (
            "Boorla and Maranas, Nature Communications 16, 2072 (2025), "
            "doi:10.1038/s41467-025-57215-9"
        ),
        "license_note": (
            "Pinned Hugging Face dataset card declares CC-BY-4.0; verify exact "
            "revision and underlying-source terms before redistribution."
        ),
        "authentication": {
            "required_if_gated": True,
            "token_environment_variable": args.hf_token_env if token else None,
            "token_value_recorded": False,
        },
        "files": [],
    }
    file_specs = [
        {
            "file": filename,
            "url": f"{CATPRED_BASE_URL}/{args.revision}/{relative_path}",
            "source": "huggingface_dataset",
        }
        for filename, relative_path in HF_DATA_FILES.items()
    ] + [
        {
            "file": f"sequence_cluster_tests/{filename}",
            "url": (
                f"{CATPRED_GITHUB_RAW}/{args.processing_revision}/"
                f"datasets/splits/{relative_path}"
            ),
            "source": "github_sequence_cluster_test",
        }
        for filename, relative_path in SEQUENCE_CLUSTER_TESTS.items()
    ]
    for spec in file_specs:
        filename = spec["file"]
        url = spec["url"]
        destination = output_dir / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and not args.overwrite:
            digest = hashlib.sha256(destination.read_bytes()).hexdigest()
            manifest["files"].append({
                "file": filename, "source": spec["source"],
                "source_url": url, "bytes": destination.stat().st_size,
                "sha256": digest, "status": "already_present_not_overwritten",
            })
            print(f"Keeping existing {destination}")
            continue
        print(f"Downloading {filename} ...", flush=True)
        record = download(url, destination, token=token)
        record["file"] = filename
        record["source"] = spec["source"]
        manifest["files"].append(record)
        print(f"Saved {destination} ({record['bytes']:,} bytes)")
        time.sleep(0.2)
    manifest["manifest_created_at"] = datetime.now(timezone.utc).isoformat()
    temporary_manifest = manifest_path.with_suffix(".json.tmp")
    temporary_manifest.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary_manifest.replace(manifest_path)
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
