"""Reusable, source-grounded retrieval API for the Kinetics knowledge corpus."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any


class KnowledgeStore:
    """Read-only retrieval facade over the Kinetics SQLite FTS5 knowledge index."""

    def __init__(self, database: str | Path = "data/kinetics.sqlite3") -> None:
        self.database = Path(database)

    def _connect(self) -> sqlite3.Connection:
        if not self.database.is_file():
            raise FileNotFoundError(f"Knowledge database not found: {self.database}")
        connection = sqlite3.connect(f"{self.database.resolve().as_uri()}?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        return connection

    def search(self, query: str, *, limit: int = 10,
               domain: str | None = None) -> list[dict[str, Any]]:
        """Return ranked text chunks with title, source, license and checksum."""
        if not query.strip():
            raise ValueError("query must not be empty")
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        sql = """SELECT f.item_id,f.title,f.domain,f.text,
                        d.source,d.source_url,d.license,d.citation_metadata_json,d.sha256,d.object_path,
                        c.chunk_index,c.token_count,bm25(knowledge_fts) AS score
                 FROM knowledge_fts f
                 JOIN knowledge_documents d ON d.item_id=f.item_id
                 JOIN knowledge_chunks c ON c.chunk_id=f.chunk_id
                 WHERE knowledge_fts MATCH ?"""
        parameters: list[Any] = [query]
        if domain:
            sql += " AND f.domain = ?"
            parameters.append(domain)
        sql += " ORDER BY score LIMIT ?"
        parameters.append(limit)
        try:
            with closing(self._connect()) as connection:
                results = [dict(row) for row in connection.execute(sql, parameters).fetchall()]
                for result in results:
                    result["citation_metadata"] = json.loads(result.pop("citation_metadata_json") or "{}")
                return results
        except sqlite3.OperationalError as exc:
            if "fts5" in str(exc).lower() or "no such table" in str(exc).lower():
                raise RuntimeError("Knowledge index is not initialized; run scripts/tokenize_corpus.py") from exc
            raise

    def get_document(self, item_id: str) -> dict[str, Any] | None:
        """Return document provenance without loading its binary payload."""
        with self._connect() as connection:
            row = connection.execute(
                """SELECT item_id,title,source,source_url,license,citation_metadata_json,domain,object_path,
                          sha256,byte_size,token_count,indexed_at,status
                   FROM knowledge_documents WHERE item_id=?""",
                (item_id,),
            ).fetchone()
            if not row:
                return None
            record = dict(row)
            record["citation_metadata"] = json.loads(record.pop("citation_metadata_json") or "{}")
            return record

    def verify_document(self, item_id: str, *, root: str | Path | None = None) -> bool:
        """Verify a local content object against the database's recorded SHA-256."""
        record = self.get_document(item_id)
        if not record:
            return False
        base = Path(root) if root is not None else Path.cwd()
        path = (base / record["object_path"]).resolve()
        if base.resolve() not in path.parents or not path.is_file():
            return False
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest() == record["sha256"]


__all__ = ["KnowledgeStore"]
