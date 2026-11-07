#!/usr/bin/env python3
"""Extract, normalize and chunk downloaded corpus documents into the Kinetics index."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/corpus-manifests/metadata_index.json"
DATABASE = ROOT / "data/kinetics.sqlite3"
TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        import fitz
        with fitz.open(path) as document:
            return "\n".join(page.get_text("text", sort=True) for page in document)
    if suffix == ".epub":
        from ebooklib import ITEM_DOCUMENT, epub
        from bs4 import BeautifulSoup
        book = epub.read_epub(str(path), options={"ignore_ncx": True})
        parts = []
        for item in book.get_items_of_type(ITEM_DOCUMENT):
            parts.append(BeautifulSoup(item.get_content(), "html.parser").get_text(" ", strip=True))
        return "\n".join(parts)
    if suffix in (".xml", ".nxml", ".html", ".htm"):
        from bs4 import BeautifulSoup
        return BeautifulSoup(path.read_bytes(), "xml" if suffix in (".xml", ".nxml") else "html.parser").get_text(" ", strip=True)
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="replace")
    return ""


def chunks(text: str, max_tokens: int = 700, overlap: int = 80) -> Iterator[tuple[int, str, int]]:
    tokens = TOKEN_RE.findall(text)
    if not tokens:
        return
    start = 0
    index = 0
    while start < len(tokens):
        end = min(len(tokens), start + max_tokens)
        content = " ".join(tokens[start:end])
        yield index, content, len(tokens[start:end])
        index += 1
        if end == len(tokens):
            break
        start = max(start + 1, end - overlap)


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    if os.name == "posix" and path.exists():
        os.chmod(path, 0o600)
    db.executescript("""
    CREATE TABLE IF NOT EXISTS knowledge_documents (
      item_id TEXT PRIMARY KEY, title TEXT NOT NULL, source TEXT NOT NULL,
      source_url TEXT, license TEXT, citation_metadata_json TEXT NOT NULL DEFAULT '{}',
      domain TEXT, object_path TEXT NOT NULL,
      sha256 TEXT NOT NULL, byte_size INTEGER NOT NULL, token_count INTEGER NOT NULL DEFAULT 0,
      indexed_at TEXT, status TEXT NOT NULL DEFAULT 'downloaded'
    );
    CREATE TABLE IF NOT EXISTS knowledge_chunks (
      chunk_id TEXT PRIMARY KEY, item_id TEXT NOT NULL REFERENCES knowledge_documents(item_id),
      chunk_index INTEGER NOT NULL, text TEXT NOT NULL, token_count INTEGER NOT NULL,
      text_sha256 TEXT NOT NULL, UNIQUE(item_id, chunk_index)
    );
    CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts USING fts5(
      chunk_id UNINDEXED, item_id UNINDEXED, title, domain, text,
      tokenize='unicode61 remove_diacritics 2'
    );
    CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_item ON knowledge_chunks(item_id, chunk_index);
    """)
    columns = {row[1] for row in db.execute("PRAGMA table_info(knowledge_documents)")}
    if "citation_metadata_json" not in columns:
        db.execute("ALTER TABLE knowledge_documents ADD COLUMN citation_metadata_json TEXT NOT NULL DEFAULT '{}'")
    return db


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--database", type=Path, default=DATABASE)
    parser.add_argument("--max-documents", type=int, default=50)
    parser.add_argument("--max-tokens", type=int, default=700)
    parser.add_argument("--overlap", type=int, default=80)
    args = parser.parse_args()
    if args.max_documents < 1 or not 0 <= args.overlap < args.max_tokens:
        parser.error("Invalid document/token/overlap limits")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    db = connect(args.database)
    indexed = 0
    try:
        for item_id, record in manifest.get("items", {}).items():
            if indexed >= args.max_documents:
                break
            if record.get("status") != "downloaded":
                continue
            path = (ROOT / record["path"]).resolve()
            if ROOT not in path.parents or not path.is_file():
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != record.get("sha256"):
                raise RuntimeError(f"SHA-256 mismatch for {item_id}; refusing to index")
            existing = db.execute(
                "SELECT sha256 FROM knowledge_documents WHERE item_id=?", (item_id,)
            ).fetchone()
            if existing and existing[0] == digest:
                continue
            text = extract_text(path)
            pieces = list(chunks(text, args.max_tokens, args.overlap))
            if not pieces:
                record["index_status"] = "no_extractable_text"
                continue
            token_count = sum(piece[2] for piece in pieces)
            with db:
                db.execute("""INSERT OR REPLACE INTO knowledge_documents
                    (item_id,title,source,source_url,license,citation_metadata_json,domain,
                     object_path,sha256,byte_size,token_count,indexed_at,status)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (item_id, record.get("title", item_id), record.get("source", ""),
                     record.get("source_url"), record.get("license"),
                     json.dumps(record.get("citation_metadata", {}), sort_keys=True),
                     record.get("domain"), record["path"], digest, path.stat().st_size,
                     token_count, datetime.now(timezone.utc).isoformat(), "indexed"))
                db.execute("DELETE FROM knowledge_fts WHERE item_id=?", (item_id,))
                db.execute("DELETE FROM knowledge_chunks WHERE item_id=?", (item_id,))
                for index, content, count in pieces:
                    chunk_id = hashlib.sha256(f"{item_id}:{index}:{digest}".encode()).hexdigest()
                    text_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
                    db.execute("INSERT INTO knowledge_chunks VALUES (?,?,?,?,?,?)",
                               (chunk_id, item_id, index, content, count, text_hash))
                    db.execute("INSERT INTO knowledge_fts(chunk_id,item_id,title,domain,text) VALUES (?,?,?,?,?)",
                               (chunk_id, item_id, record.get("title", item_id),
                                record.get("domain", ""), content))
            record["indexed_at"] = datetime.now(timezone.utc).isoformat()
            record["token_count"] = token_count
            indexed += 1
        tmp = args.manifest.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        tmp.replace(args.manifest)
    finally:
        db.close()
        if os.name == "posix" and args.database.exists():
            os.chmod(args.database, 0o600)
    print(f"Indexed {indexed} documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
