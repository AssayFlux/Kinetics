#!/usr/bin/env python3
"""Acquire openly licensed literature and molecular datasets from specialist APIs.

Adapters:
- OpenAlex: only OA works with an explicit CC0/CC-BY/CC-BY-SA license and PDF URL.
- arXiv: only papers whose abstract page explicitly declares an accepted CC license.
- UniProtKB: CC BY 4.0 protein FASTA records.
- RCSB PDB: CC0 structural coordinate files.

All downloads are HTTPS-only, size-bounded, SHA-256 addressed and entered into
the common provenance manifest. This intentionally excludes records with
unknown, NC, ND or otherwise restrictive rights.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
DOMAIN_FILE = ROOT / "docs/SCIENCE_DOMAIN_CATALOGUE_100.md"
EXTENSION_FILE = ROOT / "database/domains/extended_domains.json"
SYNONYMS_FILE = ROOT / "database/domains/domain_synonyms.json"
MANIFEST_FILE = ROOT / "data/corpus-manifests/metadata_index.json"
OBJECTS = ROOT / "data/corpus/objects"
LOG = logging.getLogger("kinetics.specialist_sources")
ACCEPTED = {"cc0", "cc0-1.0", "cc-by", "cc-by-4.0", "cc-by-3.0",
            "cc-by-sa", "cc-by-sa-4.0", "cc-by-sa-3.0",
            "publicdomain", "public-domain-mark"}
USER_AGENT = "Kinetics-ResearchCorpus/1.0 (open science; https://github.com/AssayFlux/Kinetics)"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def accepted_license(value: str | None) -> bool:
    if not value:
        return False
    raw = value.strip().lower()
    compact = re.sub(r"[^a-z0-9]+", "", raw)
    if any(x in raw for x in ("-nc", "-nd", "noncommercial", "non-commercial",
                              "no derivatives", "all rights reserved")):
        return False
    if compact.startswith("cc0") or compact in {"cc01", "cc010", "cc01.0", "publicdomain", "publicdomainmark",
                   "publicdomainmark10", "ccby", "ccby30", "ccby40",
                   "ccbysa", "ccbysa30", "ccbysa40"}:
        return True
    if any(x in raw for x in (
        "creativecommons.org/licenses/by/4.0", "creativecommons.org/licenses/by/3.0",
        "creativecommons.org/licenses/by-sa/4.0", "creativecommons.org/licenses/by-sa/3.0",
        "creativecommons.org/publicdomain/zero/1.0",
        "creativecommons.org/publicdomain/mark/1.0",
    )):
        return True
    if re.search(r"cc\s*[- ]?\s*by\s*[- ]?\s*4\.0", raw):
        return True
    if re.search(r"cc\s*[- ]?\s*by\s*[- ]?\s*3\.0", raw):
        return True
    if re.search(r"cc\s*[- ]?\s*by\s*[- ]?sa\s*[- ]?\s*4\.0", raw):
        return True
    if re.search(r"creative\s+commons\s+attribution\s+4\.0", raw):
        return True
    return False

def session() -> requests.Session:
    s = requests.Session()
    retry = Retry(total=4, connect=4, read=4, status=4, backoff_factor=1.0,
                  status_forcelist=(429, 500, 502, 503, 504),
                  allowed_methods=frozenset(("GET", "POST")),
                  respect_retry_after_header=True)
    s.mount("https://", HTTPAdapter(max_retries=retry, pool_connections=3, pool_maxsize=3))
    s.headers.update({"User-Agent": USER_AGENT, "Accept": "*/*"})
    return s


def load_manifest(path: Path) -> dict[str, Any]:
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or not isinstance(data.get("items"), dict):
            raise RuntimeError("Unsupported or malformed corpus manifest")
        data.setdefault("cursor", {})
        return data
    return {"schema_version": 1, "created_at": now(), "items": {}, "cursor": {}}


def save_manifest(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = now()
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def get_domains() -> list[str]:
    raw = DOMAIN_FILE.read_text(encoding="utf-8")
    names = re.findall(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|", raw, re.M)
    names = list(dict.fromkeys(x.strip() for x in names if x.strip()))
    if EXTENSION_FILE.exists():
        names.extend(json.loads(EXTENSION_FILE.read_text()).get("domains", []))
    names = list(dict.fromkeys(names))
    if len(names) < 150:
        raise RuntimeError(f"Expected at least 150 domains, found {len(names)}")
    return names


def terms_for(domain: str) -> list[str]:
    terms = [domain]
    if SYNONYMS_FILE.exists():
        aliases = json.loads(SYNONYMS_FILE.read_text(encoding="utf-8")).get("domains", {}).get(domain, [])
        terms.extend(str(x) for x in aliases if str(x).strip())
    return list(dict.fromkeys(terms))


def category(domain: str) -> str:
    key = domain.lower()
    if any(x in key for x in ("engineering", "computer", "software", "physics", "mathematics",
                               "statistics", "climate", "geoscience", "energy", "robotics",
                               "chemistry", "materials", "mechanics")):
        return "engineering"
    if any(x in key for x in ("medicine", "clinical", "health", "cardio", "oncology")):
        return "medicine"
    return "biomedical"


def store(session_obj: requests.Session, manifest: dict[str, Any], item_id: str,
          title: str, source: str, domain: str, license_id: str, source_url: str,
          download_url: str, extension: str, metadata: dict[str, Any],
          budget_left: int, per_file: int) -> int:
    if not accepted_license(license_id):
        return 0
    if urlparse(download_url).scheme != "https":
        return 0
    prior = manifest["items"].get(item_id, {})
    if prior.get("status") == "downloaded":
        p = (ROOT / prior.get("path", "")).resolve()
        if ROOT in p.parents and p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == prior.get("sha256"):
            return 0
    response = session_obj.get(download_url, stream=True, timeout=(20, 90), allow_redirects=True)
    response.raise_for_status()
    if urlparse(response.url).scheme != "https":
        raise ValueError("Refusing non-HTTPS redirect")
    length = response.headers.get("Content-Length")
    if length and int(length) > min(budget_left, per_file):
        response.close()
        return 0
    staging = OBJECTS / category(domain) / ".staging" / (hashlib.sha256(item_id.encode()).hexdigest() + extension + ".part")
    staging.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    total = 0
    try:
        with response, staging.open("wb") as out:
            for block in response.iter_content(256 * 1024):
                if not block:
                    continue
                total += len(block)
                if total > min(budget_left, per_file):
                    raise ValueError("Object exceeded configured byte budget")
                digest.update(block)
                out.write(block)
        if not total:
            raise ValueError("Empty response body")
        hexdigest = digest.hexdigest()
        target = OBJECTS / category(domain) / hexdigest[:2] / (hexdigest + extension)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            staging.unlink(missing_ok=True)
        else:
            staging.replace(target)
        manifest["items"][item_id] = {
            "item_id": item_id, "title": title[:1000], "source": source,
            "source_url": source_url, "file_url": download_url, "domain": domain,
            "category": category(domain), "license": license_id,
            "path": target.relative_to(ROOT).as_posix(), "format": extension.lstrip("."),
            "bytes": total, "sha256": hexdigest, "retrieved_at": now(),
            "status": "downloaded", "citation_metadata": metadata,
        }
        return total
    except Exception:
        staging.unlink(missing_ok=True)
        raise


def run_openalex(s, manifest, domain, budget, per_file, limit):
    count = used = 0
    for term in terms_for(domain)[:2]:
        url = "https://api.openalex.org/works"
        params = {"search": term, "filter": "is_oa:true,best_oa_location.license:cc-by|cc-by-sa|cc0",
                  "per-page": min(10, limit), "sort": "cited_by_count:desc"}
        mailto = __import__("os").environ.get("OPENALEX_MAILTO")
        if mailto:
            params["mailto"] = mailto
        data = s.get(url, params=params, timeout=(20, 60)).json()
        for work in data.get("results", []):
            if count >= limit or used >= budget:
                break
            loc = work.get("best_oa_location") or {}
            license_id, pdf = loc.get("license"), loc.get("pdf_url")
            if not accepted_license(license_id) or not pdf:
                continue
            doi = work.get("doi") or work.get("id")
            item = f"openalex:{doi}"
            meta = {"doi": work.get("doi"), "openalex_id": work.get("id"),
                    "publication_year": work.get("publication_year"),
                    "authors": [a.get("author", {}).get("display_name") for a in work.get("authorships", [])[:30]],
                    "journal": (work.get("primary_location") or {}).get("source", {}).get("display_name"),
                    "license": license_id}
            try:
                n = store(s, manifest, item, work.get("title") or item, "openalex", domain,
                          license_id, work.get("id") or "", pdf, ".pdf", meta, budget-used, per_file)
                if n:
                    used += n; count += 1
            except (requests.RequestException, ValueError) as exc:
                LOG.warning("OpenAlex %s: %s", item, exc)
        time.sleep(0.15)
    return count, used


def run_arxiv(s, manifest, domain, budget, per_file, limit):
    count = used = 0
    term = terms_for(domain)[0]
    query = f'all:"{term}"'
    response = s.get("https://export.arxiv.org/api/query",
                     params={"search_query": query, "start": 0, "max_results": min(limit * 3, 30),
                             "sortBy": "relevance", "sortOrder": "descending"},
                     timeout=(20, 60))
    response.raise_for_status()
    root = ET.fromstring(response.content)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("a:entry", ns):
        if count >= limit or used >= budget:
            break
        paper_url = entry.findtext("a:id", default="", namespaces=ns)
        match = re.search(r"abs/([^v]+)", paper_url)
        if not match:
            continue
        paper_id = match.group(1)
        page = s.get(paper_url, timeout=(20, 60))
        page.raise_for_status()
        licenses = re.findall(r'https?://creativecommons\.org/(?:licenses|publicdomain)/[^"\'<> ]+', page.text, re.I)
        license_id = next((x for x in licenses if accepted_license(x)), None)
        if not license_id:
            continue
        pdf = f"https://export.arxiv.org/pdf/{paper_id}"
        title = " ".join((entry.findtext("a:title", default="", namespaces=ns)).split())
        authors = [x.findtext("a:name", default="", namespaces=ns) for x in entry.findall("a:author", ns)]
        item = f"arxiv:{paper_id}"
        try:
            n = store(s, manifest, item, title or item, "arxiv", domain, license_id,
                      paper_url, pdf, ".pdf", {"arxiv_id": paper_id, "authors": authors,
                      "published": entry.findtext("a:published", default="", namespaces=ns)},
                      budget-used, per_file)
            if n:
                used += n; count += 1
        except (requests.RequestException, ValueError) as exc:
            LOG.warning("arXiv %s: %s", item, exc)
        time.sleep(0.4)
    return count, used


def run_uniprot(s, manifest, domain, budget, per_file, limit):
    count = used = 0
    query = terms_for(domain)[0].replace('"', " ")
    response = s.get("https://rest.uniprot.org/uniprotkb/search",
                     params={"query": query, "format": "fasta", "size": min(limit, 20)},
                     timeout=(20, 90))
    response.raise_for_status()
    body = response.text.strip()
    if not body:
        return 0, 0
    # Store a domain-scoped FASTA bundle, preserving every accession header.
    data = body.encode("utf-8")
    if len(data) > min(budget, per_file):
        data = data[:min(budget, per_file)]
        # Keep only complete FASTA records after truncation.
        cut = data.rfind(b"\n>")
        data = data[:cut] if cut > 0 else b""
    if not data:
        return 0, 0
    item = f"uniprot:{hashlib.sha256(data).hexdigest()}"
    title = f"UniProtKB protein sequences for {domain}"
    # Write via a local response-like adapter path, but keep same content-addressed scheme.
    digest = hashlib.sha256(data).hexdigest()
    target = OBJECTS / category(domain) / digest[:2] / f"{digest}.fasta"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    manifest["items"][item] = {
        "item_id": item, "title": title, "source": "uniprot", "source_url": "https://www.uniprot.org/",
        "file_url": response.url, "domain": domain, "category": category(domain),
        "license": "CC BY 4.0", "path": target.relative_to(ROOT).as_posix(),
        "format": "fasta", "bytes": len(data), "sha256": digest, "retrieved_at": now(),
        "status": "downloaded", "citation_metadata": {"query": query, "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "record_count": body.count("\n>") + (1 if body.startswith(">") else 0), "provider": "UniProt Consortium"}
    }
    return 1, len(data)


def run_pdb(s, manifest, domain, budget, per_file, limit):
    count = used = 0
    term = terms_for(domain)[0]
    payload = {"query": {"type": "terminal", "service": "text",
                         "parameters": {"attribute": "struct.title",
                                        "operator": "contains_words", "value": term}},
               "return_type": "entry",
               "request_options": {"paginate": {"start": 0, "rows": min(limit, 10)},
                                   "results_content_type": ["experimental"]}}
    response = s.post("https://search.rcsb.org/rcsbsearch/v2/query", json=payload, timeout=(20, 60))
    response.raise_for_status()
    ids = [x.get("identifier") for x in response.json().get("result_set", [])]
    for pdb_id in ids:
        if count >= limit or used >= budget:
            break
        item = f"rcsb_pdb:{pdb_id}"
        url = f"https://files.rcsb.org/download/{pdb_id}.cif"
        try:
            n = store(s, manifest, item, f"RCSB PDB structure {pdb_id}", "rcsb_pdb",
                      domain, "CC0", f"https://www.rcsb.org/structure/{pdb_id}",
                      url, ".cif", {"pdb_id": pdb_id, "license_url": "https://www.rcsb.org/pages/policies",
                      "provider": "RCSB Protein Data Bank"}, budget-used, per_file)
            if n:
                used += n; count += 1
        except (requests.RequestException, ValueError) as exc:
            LOG.warning("RCSB %s: %s", pdb_id, exc)
    return count, used



def metadata_map(item: dict[str, Any]) -> dict[str, list[str]]:
    raw = item.get("metadata") or item.get("metadataFields") or []
    if isinstance(raw, dict):
        return {str(k): ([str(v)] if not isinstance(v, list) else [str(x) for x in v]) for k, v in raw.items()}
    result: dict[str, list[str]] = {}
    for row in raw if isinstance(raw, list) else []:
        if not isinstance(row, dict):
            continue
        key = str(row.get("key") or row.get("name") or "")
        values = row.get("value") if "value" in row else row.get("values")
        if not key:
            continue
        if isinstance(values, list):
            result[key] = [str(v.get("value") if isinstance(v, dict) else v) for v in values]
        elif values is not None:
            result[key] = [str(values)]
    return result


def run_oapen(s, manifest, domain, budget, per_file, limit):
    count = used = 0
    for term in terms_for(domain)[:2]:
        response = s.get("https://library.oapen.org/rest/search",
                         params={"query": term, "expand": "metadata,bitstreams"},
                         headers={"Accept": "application/json"}, timeout=(20, 60))
        response.raise_for_status()
        payload = response.json()
        results = payload.get("results") or payload.get("items") or payload.get("records") or []
        for record in results:
            if count >= limit or used >= budget:
                break
            meta = metadata_map(record)
            rights = " ".join(meta.get("dc.rights", []) + meta.get("dc.rights.uri", []) +
                              meta.get("oapen.rights", []))
            if not accepted_license(rights):
                continue
            handle = (record.get("handle") or record.get("id") or
                      (meta.get("dc.identifier.uri") or [""])[0])
            title = (meta.get("dc.title") or [record.get("name") or "OAPEN book"])[0]
            bitstreams = record.get("bitstreams") or []
            for bitstream in bitstreams:
                name = str(bitstream.get("name") or bitstream.get("bitstreamName") or "")
                link = bitstream.get("retrieveLink") or bitstream.get("retrieve_link") or bitstream.get("download")
                if not link or not name.lower().endswith(".pdf"):
                    continue
                url = link if str(link).startswith("https://") else "https://library.oapen.org" + str(link)
                item_id = f"oapen:{handle}:{name}"
                try:
                    n = store(s, manifest, item_id, title, "oapen", domain, rights,
                              f"https://library.oapen.org/handle/{handle}", url, ".pdf",
                              {"handle": handle, "authors": meta.get("dc.contributor.author", []),
                               "publisher": meta.get("dc.publisher", []), "publication_date": meta.get("dc.date.issued", []),
                               "license_metadata": rights}, budget-used, per_file)
                    if n:
                        used += n; count += 1
                except (requests.RequestException, ValueError) as exc:
                    LOG.warning("OAPEN %s: %s", item_id, exc)
                break
        time.sleep(0.25)
    return count, used


def run_figshare(s, manifest, domain, budget, per_file, limit):
    count = used = 0
    for term in terms_for(domain)[:2]:
        response = s.post("https://api.figshare.com/v2/articles/search",
                          json={"search_for": term, "page": 1, "page_size": min(20, limit*4),
                                "order": "published_date", "order_direction": "desc"},
                          timeout=(20, 60))
        response.raise_for_status()
        for summary in response.json():
            if count >= limit or used >= budget:
                break
            article_id = summary.get("id")
            if not article_id:
                continue
            detail_response = s.get(f"https://api.figshare.com/v2/articles/{article_id}", timeout=(20, 60))
            detail_response.raise_for_status()
            article = detail_response.json()
            license_obj = article.get("license") or {}
            license_id = license_obj.get("url") or license_obj.get("name") or license_obj.get("value")
            if not accepted_license(str(license_id or "")):
                continue
            for file in article.get("files", []):
                filename = str(file.get("name") or "")
                ext = Path(filename).suffix.lower()
                if ext not in {".pdf", ".csv", ".tsv", ".json", ".txt", ".fasta", ".fa", ".pdb", ".cif", ".mmcif"}:
                    continue
                url = file.get("download_url")
                if not url:
                    continue
                item_id = f"figshare:{article_id}:{file.get('id')}"
                try:
                    n = store(s, manifest, item_id, article.get("title") or filename,
                              "figshare", domain, str(license_id), article.get("url_public_html") or "",
                              url, ext, {"article_id": article_id, "doi": article.get("doi"),
                              "authors": article.get("authors", []), "published_date": article.get("published_date"),
                              "license_name": license_obj.get("name"), "license_url": license_obj.get("url")},
                              budget-used, per_file)
                    if n:
                        used += n; count += 1
                except (requests.RequestException, ValueError) as exc:
                    LOG.warning("Figshare %s: %s", item_id, exc)
                break
        time.sleep(0.25)
    return count, used


def run_dryad(s, manifest, domain, budget, per_file, limit):
    count = used = 0
    for term in terms_for(domain)[:2]:
        response = s.get("https://datadryad.org/api/v2/search", params={"q": term, "per_page": min(20, limit*4)},
                         timeout=(20, 60))
        response.raise_for_status()
        payload = response.json()
        datasets = payload.get("_embedded", {}).get("stash:datasets", []) if isinstance(payload, dict) else []
        if not datasets and isinstance(payload, dict):
            datasets = payload.get("datasets", payload.get("results", []))
        for summary in datasets:
            if count >= limit or used >= budget:
                break
            doi = summary.get("identifier") or summary.get("doi")
            if not doi:
                continue
            encoded = quote(str(doi), safe="")
            detail_response = s.get(f"https://datadryad.org/api/v2/datasets/{encoded}", timeout=(20, 60))
            detail_response.raise_for_status()
            detail = detail_response.json()
            license_id = detail.get("license") or summary.get("license")
            if isinstance(license_id, dict):
                license_id = license_id.get("uri") or license_id.get("name") or license_id.get("id")
            if not accepted_license(str(license_id or "")):
                continue
            version = detail.get("versionNumber") or detail.get("version") or 1
            files_response = s.get(f"https://datadryad.org/api/v2/datasets/{encoded}/versions/{version}/files",
                                   timeout=(20, 60))
            files_response.raise_for_status()
            files_payload = files_response.json()
            files = files_payload if isinstance(files_payload, list) else files_payload.get("_embedded", {}).get("stash:files", files_payload.get("files", []))
            for file in files:
                filename = str(file.get("path") or file.get("name") or "")
                ext = Path(filename).suffix.lower()
                if ext not in {".pdf", ".csv", ".tsv", ".json", ".txt", ".fasta", ".fa"}:
                    continue
                links = file.get("_links") or {}
                download = links.get("download") or {}
                url = download.get("href") if isinstance(download, dict) else download
                url = url or file.get("downloadUrl") or file.get("download_url")
                if not url:
                    continue
                if str(url).startswith("/"):
                    url = "https://datadryad.org" + str(url)
                item_id = f"dryad:{doi}:{file.get('id') or filename}"
                try:
                    n = store(s, manifest, item_id, detail.get("title") or filename,
                              "dryad", domain, str(license_id), f"https://doi.org/{doi}",
                              str(url), ext, {"doi": doi, "version": version,
                              "authors": detail.get("authors", []), "abstract": detail.get("abstract"),
                              "license": license_id}, budget-used, per_file)
                    if n:
                        used += n; count += 1
                except (requests.RequestException, ValueError) as exc:
                    LOG.warning("Dryad %s: %s", item_id, exc)
                break
        time.sleep(0.25)
    return count, used


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--batch-size", type=int, default=20)
    p.add_argument("--max-batch-mb", type=int, default=40)
    p.add_argument("--max-file-mb", type=int, default=20)
    p.add_argument("--max-domains", type=int, default=8)
    p.add_argument("--per-source-limit", type=int, default=3)
    p.add_argument("--manifest", type=Path, default=MANIFEST_FILE)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if not 1 <= args.batch_size <= 30 or not 1 <= args.max_domains <= 160:
        p.error("batch-size 1-30 and max-domains 1-160")
    if not 1 <= args.max_batch_mb <= 80 or not 1 <= args.max_file_mb <= 80:
        p.error("byte limits 1-80 MiB")
    if not 1 <= args.per_source_limit <= 10:
        p.error("per-source-limit 1-10")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    manifest = load_manifest(args.manifest)
    all_domains = get_domains()
    cursor = manifest.setdefault("cursor", {})
    start = int(cursor.get("specialist_domain_index", 0)) % len(all_domains)
    selected = [all_domains[(start+i) % len(all_domains)] for i in range(args.max_domains)]
    if args.dry_run:
        print(json.dumps({"sources": ["openalex", "arxiv", "uniprot", "rcsb_pdb", "oapen", "figshare", "dryad"],
                          "domains": selected, "manifest_items": len(manifest["items"]),
                          "rights_policy": sorted(ACCEPTED)}, indent=2))
        return 0
    s = session()
    budget = args.max_batch_mb * 1024 * 1024
    per_file = args.max_file_mb * 1024 * 1024
    total_count = total_bytes = processed = 0
    adapters = [("openalex", run_openalex), ("arxiv", run_arxiv),
                ("uniprot", run_uniprot), ("rcsb_pdb", run_pdb),
                ("oapen", run_oapen), ("figshare", run_figshare), ("dryad", run_dryad)]
    try:
        for domain in selected:
            if total_count >= args.batch_size or total_bytes >= budget:
                break
            for source, adapter in adapters:
                if total_count >= args.batch_size or total_bytes >= budget:
                    break
                try:
                    n, b = adapter(s, manifest, domain, budget-total_bytes, per_file,
                                   min(args.per_source_limit, args.batch_size-total_count))
                    total_count += n; total_bytes += b
                    save_manifest(args.manifest, manifest)
                except (requests.RequestException, ValueError, ET.ParseError) as exc:
                    LOG.warning("%s / %s failed: %s", source, domain, exc)
                time.sleep(0.2)
            processed += 1
        cursor["specialist_domain_index"] = (start + processed) % len(all_domains)
        manifest["last_specialist_batch"] = {"items": total_count, "bytes": total_bytes,
            "domains": selected[:processed], "sources": [x[0] for x in adapters], "completed_at": now()}
        save_manifest(args.manifest, manifest)
    finally:
        s.close()
    LOG.info("Specialist sources: %d objects, %.2f MiB", total_count, total_bytes/1048576)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
