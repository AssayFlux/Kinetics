#!/usr/bin/env python3
"""Validate the base SQLite schema and all numbered SQL migrations."""
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "database/sqlite/schema.sql"
MIGRATIONS = ROOT / "database/sqlite/migrations"

def main() -> int:
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys=ON")
    try:
        db.executescript(SCHEMA.read_text(encoding="utf-8"))
        for path in sorted(MIGRATIONS.glob("[0-9][0-9][0-9]_*.sql")):
            db.executescript(path.read_text(encoding="utf-8"))
        check = db.execute("PRAGMA integrity_check").fetchone()[0]
        if check != "ok":
            raise RuntimeError(f"integrity_check failed: {check}")
        required = {
            "entities", "identifiers", "sequences", "structures", "compounds",
            "measurements", "relationships", "entity_fts", "record_fts",
            "genetic_variants", "expression_measurements", "omics_samples",
            "interaction_evidence", "pathway_memberships", "ontology_terms",
            "publications", "dataset_files", "import_checkpoints",
            "token_index_metadata",
        }
        actual = {row[0] for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table','view')"
        )}
        missing = sorted(required - actual)
        if missing:
            raise RuntimeError("missing required tables: " + ", ".join(missing))
        version = db.execute("SELECT MAX(version) FROM schema_migrations").fetchone()[0]
        print(f"SQLite schema valid; migration version={version}; tables={len(actual)}; FTS5=available")
        return 0
    except sqlite3.Error as exc:
        print(f"SQLite schema validation failed: {exc}", file=sys.stderr)
        return 1
    finally:
        db.close()

if __name__ == "__main__":
    raise SystemExit(main())
