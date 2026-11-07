#!/usr/bin/env python3
"""Acquire openly redistributable books and research datasets from Zenodo.

Only records with explicit CC0, CC-BY or CC-BY-SA licenses are mirrored.
Downloads are bounded, content-addressed, resumable at the workflow level and
recorded in the shared corpus manifest with citation/provenance metadata.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
DOMAIN_FILE = ROOT / "docs/SCIENCE_DOMAIN_CATALOGUE_100.md"
SYNONYMS_FILE = ROOT / "database/domains/domain_synonyms.json"
MANIFEST_FILE = ROOT / "data/corpus-manifests/metadata_index.json"
OBJECTS = ROOT / "data/corpus/objects"
API = "https://zenodo.org/api/records"
USER_AGENT = "Kinetics-ResearchCorpus/1.0 (open research; https://github.com/AssayFlux/Kinetics)"
ALLOWED_LICENSES = {
    "cc0-1.0", "cc0", "public-domain-mark", "publicdomain",
    "cc-by-4.0", "cc-by-3.0", "cc-by-2.0",
    "cc-by-sa-4.0", "cc-by-sa-3.0", "cc-by-sa-2.0",
}
ALLOWED_EXTENSIONS = {
    ".pdf", ".epub", ".txt", ".html", ".xml", ".csv", ".tsv", ".json",
    ".fasta", ".fa", ".fna", ".faa", ".gb", ".gbk", ".genbank",
    ".pdb", ".cif", ".mmcif",
}
LOG = logging.getLogger("kinetics.zenodo")


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def license_allowed(value: str | None) -> bool:
    if not value:
        return False
    normalized = value.strip().lower().replace("_", "-").replace(" ", "")
    if any(token in normalized for token in ("-nc", "-nd", "noncommercial", "allrightsreserved")):
        return False
    if normalized in ALLOWED_LICENSES:
        return True
    return any(f"/{license_id}/" in normalized for license_id in ALLOWED_LICENSES)


def load_manifest(path: Path) -> dict[str, Any]:
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or not isinstance(data.get("items"), dict):
            raise RuntimeError("Unsupported or malformed shared corpus manifest")
        data.setdefault("cursor", {})
        return data
    return {"schema_version": 1, "created_at": utcnow(), "items": {}, "cursor": {}}


def save_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest["updated_at"] = utcnow()
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def domains() -> list[str]:
    text = DOMAIN_FILE.read_text(encoding="utf-8")
    names = re.findall(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|", text, re.M)
    names = list(dict.fromkeys(name.strip() for name in names))
    extension = json.loads((ROOT / "database/domains/extended_domains.json").read_text())
    names.extend(extension.get("domains", []))
    names = list(dict.fromkeys(names))
    if len(names) < 150:
        raise RuntimeError(f"Expected 150+ domains, found {len(names)}")
    return names


def search_terms(domain: str) -> list[str]:
    terms = [domain]
    if SYNONYMS_FILE.exists():
        aliases = json.loads(SYNONYMS_FILE.read_text(encoding="utf-8")).get("domains", {}).get(domain, [])
        terms.extend(str(term).strip() for term in aliases if str(term).strip())
    return list(dict.fromkeys(terms))


def category(domain: str) -> str:
    key = domain.lower()
    if any(word in key for word in ("engineering", "computer", "software", "physics", "mathematics",
                                     "statistics", "climate", "geoscience", "energy", "robotics")):
        return "engineering"
    if any(word in key for word in ("medicine", "clinical", "health", "cardio", "oncology")):
        return "medicine"
    return "biomedical"


def make_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(total=4, connect=4, read=4, status=4, backoff_factor=1.2,
                  status_forcelist=(429, 500, 502, 503, 504),
                  allowed_methods=frozenset(("GET",)), respect_retry_after_header=True)
    session.mount("https://", HTTPAdapter(max_retries=retry, pool_connections=2, pool_maxsize=2))
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json, */*"})
    return session


def download(session: requests.Session, url: str, target: Path,
             remaining_bytes: int, per_file_bytes: int) -> tuple[int, str]:
    if not url.startswith("https://"):
        raise ValueError("Only HTTPS downloads are allowed")
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_suffix(target.suffix + ".part")
    size = 0
    digest = hashlib.sha256()
    with session.get(url, stream=True, timeout=(20, 120), allow_redirects=True) as response:
        response.raise_for_status()
        if not response.url.startswith("https://"):
            raise ValueError("Refusing non-HTTPS redirect")
        length = response.headers.get("Content-Length")
        if length and int(length) > min(remaining_bytes, per_file_bytes):
            raise ValueError("Zenodo file exceeds configured byte budget")
        with temp.open("wb") as output:
            for block in response.iter_content(256 * 1024):
                if not block:
                    continue
                size += len(block)
                if size > min(remaining_bytes, per_file_bytes):
                    raise ValueError("Zenodo stream exceeded configured byte budget")
                output.write(block)
                digest.update(block)
    if size == 0:
        temp.unlink(missing_ok=True)
        raise ValueError("Zenodo returned an empty file")
    temp.replace(target)
    return size, digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-size", type=int, default=15)
    parser.add_argument("--max-batch-mb", type=int, default=40)
    parser.add_argument("--max-file-mb", type=int, default=40)
    parser.add_argument("--max-domains", type=int, default=8)
    parser.add_argument("--manifest", type=Path, default=MANIFEST_FILE)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.batch_size <= 30 or not 1 <= args.max_domains <= 160:
        parser.error("batch-size must be 1-30 and max-domains 1-160")
    if not 1 <= args.max_batch_mb <= 80 or not 1 <= args.max_file_mb <= 80:
        parser.error("byte limits must be 1-80 MiB")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    manifest = load_manifest(args.manifest)
    all_domains = domains()
    cursor = manifest.setdefault("cursor", {})
    start = int(cursor.get("zenodo_domain_index", 0)) % len(all_domains)
    selected = [all_domains[(start + i) % len(all_domains)] for i in range(args.max_domains)]
    if args.dry_run:
        print(json.dumps({"source": "zenodo", "selected_domains": selected,
                          "known_items": len(manifest["items"]),
                          "license_policy": sorted(ALLOWED_LICENSES),
                          "max_batch_mb": args.max_batch_mb}, indent=2))
        return 0

    session = make_session()
    budget = args.max_batch_mb * 1024 * 1024
    per_file = args.max_file_mb * 1024 * 1024
    total_items = total_bytes = processed = 0
    pages = cursor.setdefault("zenodo_pages", {})
    try:
        for domain in selected:
            if total_items >= args.batch_size or total_bytes >= budget:
                break
            terms = search_terms(domain)
            query = " OR ".join(f'"{term}"' for term in terms[:8])
            page = int(pages.get(domain, 1))
            response = session.get(API, params={"q": query, "size": min(50, args.batch_size * 3),
                                                "page": page, "sort": "mostviewed"},
                                   timeout=(20, 60))
            response.raise_for_status()
            hits = response.json().get("hits", {}).get("hits", [])
            pages[domain] = page + 1 if hits else 1
            for hit in hits:
                if total_items >= args.batch_size or total_bytes >= budget:
                    break
                metadata = hit.get("metadata", {})
                license_obj = metadata.get("license") or {}
                license_id = str(license_obj.get("id") or license_obj.get("url") or "")
                if not license_allowed(license_id):
                    continue
                files = hit.get("files", [])
                candidates = []
                for item in files:
                    filename = str(item.get("key") or "")
                    ext = Path(filename).suffix.lower()
                    size = int(item.get("size") or 0)
                    link = (item.get("links") or {}).get("self") or (item.get("links") or {}).get("download")
                    if ext in ALLOWED_EXTENSIONS and link and 0 < size <= per_file:
                        candidates.append((filename, ext, size, link))
                if not candidates:
                    continue
                # Prefer a complete book/paper or a structured dataset over previews.
                candidates.sort(key=lambda row: (
                    0 if row[1] in (".pdf", ".epub") else
                    1 if row[1] in (".csv", ".tsv", ".json") else 2,
                    -row[2], row[0]))
                filename, ext, declared_size, file_url = candidates[0]
                record_id = str(hit.get("id") or "")
                item_id = f"zenodo:{record_id}:{filename}"
                prior = manifest["items"].get(item_id, {})
                if prior.get("status") == "downloaded":
                    path = (ROOT / prior.get("path", "")).resolve()
                    if ROOT in path.parents and path.is_file():
                        if hashlib.sha256(path.read_bytes()).hexdigest() == prior.get("sha256"):
                            continue
                digest_hint = hashlib.sha256(item_id.encode()).hexdigest()[:12]
                staging = OBJECTS / category(domain) / ".staging" / f"{digest_hint}{ext}"
                try:
                    size, digest = download(session, file_url, staging, budget - total_bytes, per_file)
                    target = OBJECTS / category(domain) / digest[:2] / f"{digest}{ext}"
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if target.exists():
                        staging.unlink(missing_ok=True)
                    else:
                        staging.replace(target)
                    if __import__("os").name == "posix":
                        target.chmod(0o600)
                    creators = metadata.get("creators", [])
                    manifest["items"][item_id] = {
                        "item_id": item_id,
                        "title": str(metadata.get("title") or filename)[:1000],
                        "source": "zenodo",
                        "source_url": hit.get("links", {}).get("html"),
                        "file_url": file_url,
                        "domain": domain,
                        "category": category(domain),
                        "license": license_id,
                        "path": target.relative_to(ROOT).as_posix(),
                        "format": ext.lstrip("."),
                        "bytes": size,
                        "sha256": digest,
                        "retrieved_at": utcnow(),
                        "status": "downloaded",
                        "citation_metadata": {
                            "doi": hit.get("doi"),
                            "conceptdoi": hit.get("conceptdoi"),
                            "creators": creators,
                            "publication_date": metadata.get("publication_date"),
                            "description": str(metadata.get("description") or "")[:4000],
                            "keywords": metadata.get("keywords", []),
                            "version": metadata.get("version"),
                            "record_id": record_id,
                            "filename": filename,
                            "declared_file_size": declared_size,
                        },
                    }
                    total_items += 1
                    total_bytes += size
                except (requests.RequestException, OSError, ValueError) as exc:
                    LOG.warning("Zenodo record %s failed: %s", record_id, exc)
                    manifest["items"][item_id] = {"item_id": item_id, "source": "zenodo",
                        "status": "error", "error": str(exc)[:500], "checked_at": utcnow(),
                        "domain": domain}
            processed += 1
            save_manifest(args.manifest, manifest)
            time.sleep(0.25)
        cursor["zenodo_domain_index"] = (start + processed) % len(all_domains)
        manifest["last_zenodo_batch"] = {"items": total_items, "bytes": total_bytes,
            "domains": selected[:processed], "completed_at": utcnow()}
        save_manifest(args.manifest, manifest)
    finally:
        session.close()
    LOG.info("Zenodo batch complete: %d files, %.2f MiB", total_items, total_bytes / 1048576)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
