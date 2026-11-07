#!/usr/bin/env python3
"""Search the local Kinetics knowledge index and return source-grounded chunks."""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data/kinetics.sqlite3"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="FTS5 query, e.g. 'cardiac AND imaging'")
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--domain")
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    db = sqlite3.connect(args.database)
    db.row_factory = sqlite3.Row
    try:
        sql = """SELECT f.item_id,f.title,f.domain,f.text,
                        d.source_url,d.license,d.citation_metadata_json,d.sha256,d.object_path,
                        bm25(knowledge_fts) AS score
                 FROM knowledge_fts f
                 JOIN knowledge_documents d ON d.item_id=f.item_id
                 WHERE knowledge_fts MATCH ?"""
        params: list[object] = [args.query]
        if args.domain:
            sql += " AND f.domain = ?"
            params.append(args.domain)
        sql += " ORDER BY score LIMIT ?"
        params.append(args.limit)
        rows = [dict(row) for row in db.execute(sql, params).fetchall()]
        for row in rows:
            row["citation_metadata"] = json.loads(row.pop("citation_metadata_json") or "{}")
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
