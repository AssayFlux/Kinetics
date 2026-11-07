from __future__ import annotations

import importlib.util
import json
import hashlib

import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_domain_catalogue_has_at_least_150_domains():
    fetch = load_script("fetch_corpus")
    domains = fetch.domain_catalogue()
    assert len(domains) == 160
    assert "Quantum computing" in domains
    assert "Computational chemistry" in domains
    assert "Atmospheric science" in domains
    assert len(domains) == len(set(domains))


def test_license_gate_is_conservative():
    fetch = load_script("fetch_corpus")
    assert fetch.license_allowed("https://creativecommons.org/licenses/by/4.0/")
    assert fetch.license_allowed("CC BY-SA 4.0")
    assert fetch.license_allowed("Public Domain")
    assert not fetch.license_allowed("")
    assert not fetch.license_allowed("CC BY-NC 4.0")
    assert not fetch.license_allowed("CC BY-ND 4.0")
    assert not fetch.license_allowed("All Rights Reserved")


def test_manifest_atomic_shape(tmp_path: Path):
    fetch = load_script("fetch_corpus")
    path = tmp_path / "manifest.json"
    manifest = fetch.load_manifest(path)
    manifest["items"]["example"] = {"status": "downloaded", "sha256": "abc"}
    fetch.save_manifest(path, manifest)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["items"]["example"]["sha256"] == "abc"
    assert not path.with_suffix(".json.tmp").exists()


def test_tokenizer_chunks_overlap_and_boundaries():
    tokenizer = load_script("tokenize_corpus")
    text = " ".join(f"token{i}" for i in range(100))
    pieces = list(tokenizer.chunks(text, max_tokens=20, overlap=5))
    assert len(pieces) > 1
    assert all(count <= 20 for _, _, count in pieces)
    assert pieces[0][0] == 0
    assert pieces[-1][1]


def test_safe_category_routing():
    fetch = load_script("fetch_corpus")
    assert fetch.safe_category("Biomedical engineering") == "engineering"
    assert fetch.safe_category("Cardiology") == "medicine"
    assert fetch.safe_category("Genomics") == "biomedical"


def test_reusable_knowledge_store_api(tmp_path: Path):
    tokenizer = load_script("tokenize_corpus")
    database = tmp_path / "knowledge.sqlite3"
    db = tokenizer.connect(database)
    with db:
        db.execute("""INSERT INTO knowledge_documents
            (item_id,title,source,source_url,license,domain,object_path,sha256,
             byte_size,token_count,indexed_at,status)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            ("PMC123", "Cardiac imaging review", "fixture", "https://example.org/paper",
             "CC BY 4.0", "Cardiology", "data/corpus/objects/aa/example.pdf",
             "a" * 64, 100, 5, "2026-01-01T00:00:00+00:00", "indexed"))
        db.execute("INSERT INTO knowledge_chunks VALUES (?,?,?,?,?,?)",
                   ("chunk-1", "PMC123", 0, "cardiac imaging evidence", 5, "b" * 64))
        db.execute("""INSERT INTO knowledge_fts(chunk_id,item_id,title,domain,text)
                      VALUES (?,?,?,?,?)""",
                   ("chunk-1", "PMC123", "Cardiac imaging review",
                    "Cardiology", "cardiac imaging evidence"))
    db.close()

    from kinetics_core.knowledge import KnowledgeStore

    store = KnowledgeStore(database)
    results = store.search("cardiac AND imaging", limit=5)
    assert len(results) == 1
    assert results[0]["item_id"] == "PMC123"
    assert results[0]["source_url"] == "https://example.org/paper"
    assert results[0]["citation_metadata"] == {}
    assert store.get_document("PMC123")["license"] == "CC BY 4.0"
    assert store.get_document("missing") is None


def test_domain_search_terms_include_synonyms():
    fetch = load_script("fetch_corpus")
    terms = fetch.domain_search_terms("Computational chemistry")
    assert "Computational chemistry" in terms
    assert "molecular modelling" in [term.lower() for term in terms]


def test_source_registry_is_valid_and_only_known_adapters_enabled():
    fetch = load_script("fetch_corpus")
    registry = fetch.load_source_registry()
    assert registry["internet_archive"]["enabled"] is True
    assert registry["europe_pmc_oa"]["enabled"] is True
    assert registry["doab"]["enabled"] is False


def test_all_extension_domains_have_scope_definitions():
    extension = json.loads((ROOT / "database/domains/extended_domains.json").read_text())
    scopes = json.loads((ROOT / "database/domains/extended_domain_scopes.json").read_text())
    assert len(extension["domains"]) == 60
    assert set(extension["domains"]) == set(scopes["domains"])


def test_stream_download_resumes_partial_http_range(tmp_path: Path):
    fetch = load_script("fetch_corpus")

    class Response:
        url = "https://example.org/book.pdf"

        def __init__(self, status, headers, chunks, fail=False):
            self.status_code = status
            self.headers = headers
            self.chunks = chunks
            self.fail = fail

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def raise_for_status(self):
            return None

        def iter_content(self, chunk_size):
            for chunk in self.chunks:
                yield chunk
            if self.fail:
                raise requests.exceptions.ChunkedEncodingError("connection interrupted")

    class Session:
        def __init__(self):
            self.calls = []

        def get(self, url, **kwargs):
            self.calls.append(kwargs)
            if len(self.calls) == 1:
                return Response(200, {"Content-Length": "6"}, [b"abc"], fail=True)
            return Response(206, {"Content-Length": "3", "Content-Range": "bytes 3-5/6"}, [b"def"])

    session = Session()
    destination = tmp_path / "book.pdf"
    try:
        fetch.stream_download(session, "https://example.org/book.pdf", destination, 1024, 1024)
        assert False, "first transfer should be interrupted"
    except requests.exceptions.ChunkedEncodingError:
        pass

    part = destination.with_suffix(".pdf.part")
    assert part.read_bytes() == b"abc"
    size, digest = fetch.stream_download(session, "https://example.org/book.pdf", destination, 1024, 1024)
    assert size == 6
    assert destination.read_bytes() == b"abcdef"
    assert digest == hashlib.sha256(b"abcdef").hexdigest()
    assert session.calls[1]["headers"] == {"Range": "bytes=3-"}
