#!/usr/bin/env python3
"""Acquire explicitly redistributable books and papers in bounded, resumable batches.

The script stores binary objects outside Git history and commits only metadata
manifests by default. It never treats API accessibility as a redistribution
license. See docs/KNOWLEDGE_INGESTION.md before enabling a public mirror.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import tarfile
import tempfile
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data/corpus-manifests/metadata_index.json"
DEFAULT_OBJECTS = ROOT / "data/corpus/objects"
DOMAIN_FILE = ROOT / "docs/SCIENCE_DOMAIN_CATALOGUE_100.md"
DOMAIN_SYNONYMS_FILE = ROOT / "database/domains/domain_synonyms.json"
SOURCE_REGISTRY_FILE = ROOT / "database/sources/knowledge_sources.json"
USER_AGENT = "Kinetics-KnowledgeIngestion/1.0 (research; contact: repository-maintainer)"
MAX_FILE_BYTES = 100 * 1024 * 1024
DEFAULT_BATCH_BYTES = 80 * 1024 * 1024
ALLOWED_LICENSES = (
    "creativecommons.org/licenses/by/4.0",
    "creativecommons.org/licenses/by-sa/4.0",
    "creativecommons.org/publicdomain/zero/1.0",
    "creativecommons.org/publicdomain/mark/1.0",
    "creativecommons.org/licenses/by/3.0",
    "creativecommons.org/licenses/by-sa/3.0",
    "creativecommons.org/licenses/by/2.0",
    "creativecommons.org/licenses/by-sa/2.0",
)
LOG = logging.getLogger("kinetics.fetch")


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=5, connect=5, read=5, status=5,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(("GET", "HEAD")),
        respect_retry_after_header=True,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=4, pool_maxsize=4)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "*/*"})
    return session


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "created_at": utcnow(), "items": {}, "cursor": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or not isinstance(data.get("items"), dict):
            raise ValueError("Unsupported or malformed manifest schema")
        data.setdefault("cursor", {})
        return data
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError(f"Cannot safely resume from manifest {path}: {exc}") from exc


def save_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest["updated_at"] = utcnow()
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def domain_catalogue() -> list[str]:
    if not DOMAIN_FILE.exists():
        raise FileNotFoundError(f"Canonical domain catalogue missing: {DOMAIN_FILE}")
    pattern = re.compile(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|", re.MULTILINE)
    names = pattern.findall(DOMAIN_FILE.read_text(encoding="utf-8"))
    names = list(dict.fromkeys(name.strip() for name in names if name.strip()))
    if len(names) < 100:
        raise RuntimeError(f"Expected at least 100 canonical domains; parsed {len(names)}")
    extension_path = ROOT / "database/domains/extended_domains.json"
    if extension_path.exists():
        extension = json.loads(extension_path.read_text(encoding="utf-8"))
        names.extend(str(name).strip() for name in extension.get("domains", []) if str(name).strip())
    names = list(dict.fromkeys(names))
    if len(names) < 150:
        raise RuntimeError(f"Expected at least 150 acquisition domains; loaded {len(names)}")
    return names


def domain_search_terms(domain: str) -> list[str]:
    terms = [domain]
    if DOMAIN_SYNONYMS_FILE.exists():
        data = json.loads(DOMAIN_SYNONYMS_FILE.read_text(encoding="utf-8"))
        configured = data.get("domains", {}).get(domain, [])
        terms.extend(str(value).strip() for value in configured if str(value).strip())
    return list(dict.fromkeys(terms))


def load_source_registry() -> dict[str, dict[str, Any]]:
    if not SOURCE_REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Source registry missing: {SOURCE_REGISTRY_FILE}")
    data = json.loads(SOURCE_REGISTRY_FILE.read_text(encoding="utf-8"))
    entries = data.get("sources", [])
    registry = {entry["id"]: entry for entry in entries if entry.get("id")}
    supported = {"internet_archive": "scripts/fetch_corpus.py",
                 "europe_pmc_oa": "scripts/fetch_corpus.py"}
    for source_id, entry in registry.items():
        if entry.get("enabled") and source_id not in supported:
            raise RuntimeError(f"Source {source_id} is enabled but has no implemented adapter")
    return registry


def safe_category(domain: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "_", domain.lower()).strip("_")
    if any(term in key for term in ("engineering", "robotics", "device", "material", "instrument", "computer", "software", "data_science", "machine_learning", "cybersecurity", "cloud", "distributed", "database", "signal", "control", "mathematics", "statistics", "physics", "energy", "geoscience", "photonics", "quantum", "industrial", "manufacturing", "systems_engineering", "agricultural", "food_science", "climate", "environmental")):
        return "engineering"
    if any(term in key for term in ("medicine", "clinical", "health", "cardio", "oncology",
                                     "pathology", "surgery", "pediatrics", "pharmacology")):
        return "medicine"
    return "biomedical"


def license_allowed(value: str | None) -> bool:
    if not value:
        return False
    normalized = value.strip().lower().replace(" ", "")
    if any(token in normalized for token in ("ccby-nc", "ccby-nd", "noncommercial", "allrightsreserved")):
        return False
    if normalized in ("publicdomain", "public-domain", "pd", "cc0", "ccby", "ccby4.0",
                      "ccby-sa", "ccby-sa4.0"):
        return True
    return any(fragment in normalized for fragment in ALLOWED_LICENSES)


def stream_download(session: requests.Session, url: str, destination: Path,
                    remaining_bytes: int, per_file_limit: int) -> tuple[int, str]:
    if not url.startswith("https://"):
        raise ValueError("Only HTTPS source URLs are accepted")
    destination.parent.mkdir(parents=True, exist_ok=True)
    part = destination.with_suffix(destination.suffix + ".part")
    offset = part.stat().st_size if part.exists() else 0
    digest = hashlib.sha256()
    if offset:
        with part.open("rb") as existing:
            for block in iter(lambda: existing.read(1024 * 1024), b""):
                digest.update(block)
    total = offset
    request_headers = {"Range": f"bytes={offset}-"} if offset else {}
    try:
        with session.get(url, stream=True, timeout=(15, 90), allow_redirects=True,
                         headers=request_headers) as response:
            response.raise_for_status()
            if not response.url.startswith("https://"):
                raise ValueError("Refusing a non-HTTPS redirect target")
            if offset and response.status_code == 200:
                # Origin ignored Range: restart rather than append a duplicate body.
                offset = 0
                total = 0
                digest = hashlib.sha256()
            elif offset and response.status_code == 206:
                content_range = response.headers.get("Content-Range", "")
                if not content_range.startswith(f"bytes {offset}-"):
                    raise ValueError("Origin returned an invalid Content-Range")
            length = response.headers.get("Content-Length")
            if length and total + int(length) > min(remaining_bytes, per_file_limit):
                raise ValueError("Remote object exceeds configured byte budget")
            with part.open("ab" if offset else "wb") as output:
                for block in response.iter_content(chunk_size=256 * 1024):
                    if not block:
                        continue
                    total += len(block)
                    if total > min(remaining_bytes, per_file_limit):
                        raise ValueError("Stream exceeded configured byte budget")
                    output.write(block)
                    digest.update(block)
        if total == 0:
            raise ValueError("Source returned an empty object")
        part.replace(destination)
        return total, digest.hexdigest()
    except requests.RequestException as exc:
        # A stale partial can receive 416 when the remote object changed or was
        # already complete. Clear it so the next invocation starts cleanly.
        if getattr(getattr(exc, "response", None), "status_code", None) == 416:
            part.unlink(missing_ok=True)
        # Keep other verified prefixes so a later run can request the remaining range.
        raise
    except Exception:
        part.unlink(missing_ok=True)
        raise


def local_record_is_valid(record: dict[str, Any]) -> bool:
    try:
        path = (ROOT / record["path"]).resolve()
        return (ROOT in path.parents and path.is_file()
                and path.stat().st_size == int(record["bytes"])
                and hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"])
    except (KeyError, OSError, TypeError, ValueError):
        return False


def persist_record(session: requests.Session, item_id: str, title: str, source: str,
                   domain: str, license_value: str, source_url: str, file_url: str,
                   extension: str, manifest: dict[str, Any], objects: Path,
                   remaining_bytes: int, citation_metadata: dict[str, Any] | None = None) -> tuple[dict[str, Any] | None, int]:
    if not license_allowed(license_value):
        return None, 0
    if extension not in (".pdf", ".epub", ".xml", ".nxml", ".html", ".txt"):
        return None, 0
    safe_id = re.sub(r"[^A-Za-z0-9._-]", "_", item_id)[:140]
    category = safe_category(domain)
    staging_path = objects / category / f".{safe_id}{extension}.staging"
    size, digest = stream_download(session, file_url, staging_path, remaining_bytes, MAX_FILE_BYTES)
    content_path = objects / category / digest[:2] / f"{digest}{extension}"
    content_path.parent.mkdir(parents=True, exist_ok=True)
    if content_path.exists():
        staging_path.unlink(missing_ok=True)
    else:
        staging_path.replace(content_path)
    if os.name == "posix":
        content_path.chmod(0o600)
    rel = content_path.relative_to(ROOT).as_posix()
    record = {
        "item_id": item_id, "title": title[:1000], "source": source,
        "source_url": source_url, "file_url": file_url, "domain": domain,
        "category": category, "license": license_value, "path": rel,
        "format": extension.lstrip("."), "bytes": size, "sha256": digest,
        "retrieved_at": utcnow(), "citation_metadata": citation_metadata or {}, "status": "downloaded",
    }
    manifest["items"][item_id] = record
    return record, size


def fetch_internet_archive(session: requests.Session, domain: str, manifest: dict[str, Any],
                           objects: Path, remaining_bytes: int, remaining_items: int) -> tuple[int, int]:
    terms = domain_search_terms(domain)
    clauses = " OR ".join(f'(subject:"{term}" OR title:"{term}")' for term in terms)
    query = f"mediatype:texts AND ({clauses})"
    cursor = manifest.setdefault("cursor", {})
    pages = cursor.setdefault("ia_pages", {})
    page = int(pages.get(domain, 1))
    params = {"q": query, "fl[]": ["identifier", "title"], "rows": min(100, remaining_items * 4),
              "page": page, "output": "json", "sort[]": "downloads desc"}
    response = session.get("https://archive.org/advancedsearch.php", params=params, timeout=(15, 45))
    response.raise_for_status()
    docs = response.json().get("response", {}).get("docs", [])
    pages[domain] = page + 1 if docs else 1
    count = 0
    used = 0
    for hit in docs:
        if count >= remaining_items or used >= remaining_bytes:
            break
        identifier = hit.get("identifier")
        if not identifier:
            continue
        prior = manifest["items"].get(identifier, {})
        if prior.get("status") == "skipped_license":
            continue
        if prior.get("status") == "downloaded" and (prior.get("release_uploaded") or local_record_is_valid(prior)):
            continue
        meta_response = session.get(f"https://archive.org/metadata/{quote(identifier, safe='')}",
                                    timeout=(15, 45))
        meta_response.raise_for_status()
        metadata = meta_response.json()
        md = metadata.get("metadata", {})
        license_value = str(md.get("licenseurl") or md.get("rights") or "")
        if not license_allowed(license_value):
            manifest["items"][identifier] = {
                "item_id": identifier, "source": "internet_archive",
                "status": "skipped_license", "license": license_value,
                "checked_at": utcnow(), "domain": domain,
            }
            continue
        files = metadata.get("files", [])
        candidates = []
        for file_info in files:
            name = str(file_info.get("name", ""))
            ext = Path(name).suffix.lower()
            if ext in (".pdf", ".epub") and not file_info.get("private"):
                size = int(file_info.get("size") or 0)
                if size and size <= MAX_FILE_BYTES:
                    candidates.append((size, name, ext))
        if not candidates:
            continue
        candidates.sort(key=lambda row: (row[0], row[2] != ".pdf"))
        _, name, ext = candidates[0]
        url = f"https://archive.org/download/{quote(identifier, safe='')}/{quote(name, safe='/')}"
        try:
            record, size = persist_record(session, identifier, str(md.get("title") or hit.get("title") or identifier),
                "internet_archive", domain, license_value, f"https://archive.org/details/{identifier}",
                url, ext, manifest, objects, remaining_bytes - used,
                {"creator": md.get("creator"), "date": md.get("date"),
                 "doi": md.get("doi"), "identifier": md.get("identifier")})
            if record:
                count += 1
                used += size
        except (requests.RequestException, OSError, ValueError) as exc:
            LOG.warning("IA item %s failed: %s", identifier, exc)
            manifest["items"][identifier] = {"item_id": identifier, "status": "error",
                "source": "internet_archive", "error": str(exc)[:500], "checked_at": utcnow()}
    return count, used


def fetch_europe_pmc(session: requests.Session, domain: str, manifest: dict[str, Any],
                     objects: Path, remaining_bytes: int, remaining_items: int) -> tuple[int, int]:
    terms = domain_search_terms(domain)
    clauses = " OR ".join(f'TITLE_ABS:"{term}"' for term in terms)
    query = f"OPEN_ACCESS:Y AND ({clauses})"
    cursor = manifest.setdefault("cursor", {})
    pages = cursor.setdefault("epmc_pages", {})
    page = int(pages.get(domain, 1))
    params = {"query": query, "format": "json", "pageSize": min(100, remaining_items * 5),
              "page": page, "resultType": "core"}
    response = session.get("https://www.ebi.ac.uk/europepmc/webservices/rest/search",
                           params=params, timeout=(15, 45))
    response.raise_for_status()
    results = response.json().get("resultList", {}).get("result", [])
    pages[domain] = page + 1 if results else 1
    count = 0
    used = 0
    for item in results:
        if count >= remaining_items or used >= remaining_bytes:
            break
        pmcid = item.get("pmcid")
        license_value = str(item.get("license") or "")
        if not pmcid or not license_allowed(license_value):
            continue
        prior = manifest["items"].get(pmcid, {})
        if prior.get("status") == "skipped_license":
            continue
        if prior.get("status") == "downloaded" and (prior.get("release_uploaded") or local_record_is_valid(prior)):
            continue
        oa = session.get("https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi",
                         params={"id": pmcid}, timeout=(15, 45))
        oa.raise_for_status()
        try:
            root = ET.fromstring(oa.text)
        except ET.ParseError:
            continue
        link = next((node for node in root.iter("link")
                     if node.attrib.get("format") == "tgz" and node.attrib.get("href")), None)
        if link is None:
            continue
        package_url = link.attrib["href"]
        if package_url.startswith("ftp://"):
            package_url = "https://" + package_url[6:]
        with tempfile.TemporaryDirectory(prefix="kinetics-pmc-") as temp_dir:
            archive = Path(temp_dir) / "package.tar.gz"
            try:
                size, _ = stream_download(session, package_url, archive,
                                          remaining_bytes - used, MAX_FILE_BYTES)
                used += size
                with tarfile.open(archive, "r:gz") as tar:
                    members = [m for m in tar.getmembers() if m.isfile()
                               and Path(m.name).suffix.lower() in (".pdf", ".xml", ".nxml")]
                    members.sort(key=lambda m: (Path(m.name).suffix.lower() != ".pdf", m.size))
                    selected = next((m for m in members if m.size <= MAX_FILE_BYTES), None)
                    if selected is None:
                        continue
                    source = tar.extractfile(selected)
                    if source is None:
                        continue
                    ext = Path(selected.name).suffix.lower()
                    payload = source.read(MAX_FILE_BYTES + 1)
                    if len(payload) > MAX_FILE_BYTES:
                        continue
                    digest = hashlib.sha256(payload).hexdigest()
                    target = objects / "biomedical" / digest[:2] / f"{digest}{ext}"
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if (not target.exists()
                            or hashlib.sha256(target.read_bytes()).hexdigest() != digest):
                        temporary_target = target.with_suffix(target.suffix + ".tmp")
                        temporary_target.write_bytes(payload)
                        temporary_target.replace(target)
                    if os.name == "posix":
                        target.chmod(0o600)
                    rel = target.relative_to(ROOT).as_posix()
                    manifest["items"][pmcid] = {
                        "item_id": pmcid, "title": item.get("title", pmcid),
                        "source": "europe_pmc_oa", "source_url": f"https://europepmc.org/articles/{pmcid}",
                        "file_url": package_url, "domain": domain, "category": "biomedical",
                        "license": license_value, "path": rel, "format": ext.lstrip("."),
                        "bytes": len(payload), "sha256": digest, "retrieved_at": utcnow(),
                        "package_bytes": size,
                        "citation_metadata": {
                            "doi": item.get("doi"), "pmid": item.get("pmid"),
                            "author_string": item.get("authorString"),
                            "journal_title": item.get("journalTitle"),
                            "first_publication_date": item.get("firstPublicationDate"),
                        },
                        "status": "downloaded",
                    }
                    count += 1
            except (requests.RequestException, OSError, tarfile.TarError, ValueError) as exc:
                LOG.warning("PMC item %s failed: %s", pmcid, exc)
                manifest["items"][pmcid] = {"item_id": pmcid, "status": "error",
                    "source": "europe_pmc_oa", "error": str(exc)[:500], "checked_at": utcnow()}
    return count, used


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-size", type=int, default=30)
    parser.add_argument("--max-batch-mb", type=int, default=80)
    parser.add_argument("--max-file-mb", type=int, default=100,
                        help="Maximum size per downloaded source object (1-200 MiB)")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--objects", type=Path, default=DEFAULT_OBJECTS)
    parser.add_argument("--source", choices=("all", "ia", "europe-pmc"), default="all")
    parser.add_argument("--max-domains", type=int, default=8,
                        help="Rotate through at most this many domains per run")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.batch_size <= 50:
        parser.error("--batch-size must be between 1 and 50")
    if not 1 <= args.max_batch_mb <= 80:
        parser.error("--max-batch-mb must be between 1 and 80")
    if not 1 <= args.max_file_mb <= 200:
        parser.error("--max-file-mb must be between 1 and 200")
    global MAX_FILE_BYTES
    MAX_FILE_BYTES = args.max_file_mb * 1024 * 1024
    if not 1 <= args.max_domains <= 200:
        parser.error("--max-domains must be between 1 and 200")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    manifest = load_manifest(args.manifest)
    domains = domain_catalogue()
    source_registry = load_source_registry()
    enabled_ia = bool(source_registry.get("internet_archive", {}).get("enabled"))
    enabled_epmc = bool(source_registry.get("europe_pmc_oa", {}).get("enabled"))
    start = int(manifest.get("cursor", {}).get("domain_index", 0)) % len(domains)
    selected = [domains[(start + offset) % len(domains)] for offset in range(args.max_domains)]
    budget = args.max_batch_mb * 1024 * 1024
    if args.dry_run:
        print(json.dumps({"selected_domains": selected, "known_items": len(manifest["items"]),
                          "batch_size": args.batch_size, "max_batch_bytes": budget,
                          "max_file_bytes": MAX_FILE_BYTES,
                          "enabled_sources": [key for key, value in source_registry.items() if value.get("enabled")]}, indent=2))
        return 0

    args.objects.mkdir(parents=True, exist_ok=True)
    session = make_session()
    total_count = 0
    total_bytes = 0
    processed_domains = 0
    try:
        for domain in selected:
            if total_count >= args.batch_size or total_bytes >= budget:
                break
            remaining_items = args.batch_size - total_count
            remaining_bytes = budget - total_bytes
            if args.source in ("all", "ia") and enabled_ia:
                try:
                    n, b = fetch_internet_archive(session, domain, manifest, args.objects,
                                                  remaining_bytes, remaining_items)
                except requests.RequestException as exc:
                    LOG.warning("Internet Archive query failed for %s: %s", domain, exc)
                    n, b = 0, 0
                total_count += n
                total_bytes += b
            if args.source in ("all", "europe-pmc") and enabled_epmc and total_count < args.batch_size and total_bytes < budget:
                try:
                    n, b = fetch_europe_pmc(session, domain, manifest, args.objects,
                                            budget - total_bytes, args.batch_size - total_count)
                except requests.RequestException as exc:
                    LOG.warning("Europe PMC query failed for %s: %s", domain, exc)
                    n, b = 0, 0
                total_count += n
                total_bytes += b
            processed_domains += 1
            time.sleep(0.1)
            save_manifest(args.manifest, manifest)
        manifest.setdefault("cursor", {})["domain_index"] = (start + processed_domains) % len(domains)
        manifest["last_batch"] = {"items": total_count, "bytes": total_bytes,
                                  "domains": selected, "completed_at": utcnow()}
        save_manifest(args.manifest, manifest)
    finally:
        session.close()
    LOG.info("Batch complete: %d files, %.2f MiB; manifest=%s",
             total_count, total_bytes / (1024 * 1024), args.manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
