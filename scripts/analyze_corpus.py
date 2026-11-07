#!/usr/bin/env python3
"""Produce deterministic domain summaries and lightweight corpus analytics."""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "data/kinetics.sqlite3"
OUTPUT = ROOT / "data/corpus-manifests/analysis_summary.json"
ENTITY_PATTERNS = {
    "doi": re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.I),
    "pmcid": re.compile(r"\bPMC\d+\b", re.I),
    "pmid": re.compile(r"\bPMID\s*:?\s*\d+\b", re.I),
    "gene_like": re.compile(r"\b[A-Z][A-Z0-9]{1,7}\b"),
}
STOP = set("the and for with from that this were have has into about using based between within".split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DATABASE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if not args.database.exists():
        raise FileNotFoundError(f"Knowledge database not found: {args.database}")
    db = sqlite3.connect(args.database)
    db.row_factory = sqlite3.Row
    summary = {"generated_at": datetime.now(timezone.utc).isoformat(),
               "engine": "kinetics-lightweight-analysis-v1", "domains": {},
               "entities": {}, "limitations": [
                   "Keyword/entity counts are exploratory, not validated scientific findings.",
                   "No patient-level inference or clinical recommendation is produced."
               ]}
    try:
        rows = db.execute("""SELECT d.item_id,d.title,d.domain,d.source,d.license,
                             d.token_count, c.text
                             FROM knowledge_documents d
                             LEFT JOIN knowledge_chunks c ON c.item_id=d.item_id""").fetchall()
        terms: dict[str, Counter] = {}
        entities: dict[str, set[str]] = {key: set() for key in ENTITY_PATTERNS}
        docs: dict[str, set[str]] = {}
        for row in rows:
            domain = row["domain"] or "unclassified"
            docs.setdefault(domain, set()).add(row["item_id"])
            terms.setdefault(domain, Counter())
            text = row["text"] or ""
            words = re.findall(r"[A-Za-z][A-Za-z0-9-]{2,}", text.lower())
            terms[domain].update(word for word in words if word not in STOP)
            for kind, pattern in ENTITY_PATTERNS.items():
                entities[kind].update(match.group(0)[:120] for match in pattern.finditer(text))
        for domain, counts in terms.items():
            summary["domains"][domain] = {
                "document_count": len(docs.get(domain, set())),
                "top_terms": [{"term": term, "count": count} for term, count in counts.most_common(40)],
            }
        summary["entities"] = {key: sorted(values)[:10000] for key, values in entities.items()}
        summary["document_count"] = db.execute("SELECT COUNT(*) FROM knowledge_documents").fetchone()[0]
        summary["chunk_count"] = db.execute("SELECT COUNT(*) FROM knowledge_chunks").fetchone()[0]
        summary["source_counts"] = {row[0]: row[1] for row in db.execute(
            "SELECT source,COUNT(*) FROM knowledge_documents GROUP BY source")}
    finally:
        db.close()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temp = args.output.with_suffix(".json.tmp")
    temp.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(args.output)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
