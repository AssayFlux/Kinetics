"""Fast, reproducible SQLite metadata store for Kinetics.

SQLite is deliberately not used as a tensor-training store. Keep large arrays,
embeddings, structures, and model checkpoints in versioned files (for example
Parquet/Arrow, NumPy, HDF5/Zarr, or safetensors) and store their paths, hashes,
schemas, and provenance here.

WAL permits concurrent readers while a writer is active; SQLite still serializes
writes. Use short transactions and executemany() batches for ingestion.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

SCHEMA_VERSION = 1

_SCHEMA = """
CREATE TABLE IF NOT EXISTS datasets (
    dataset_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    source TEXT,
    version TEXT,
    license TEXT,
    citation TEXT,
    checksum_sha256 TEXT,
    local_path TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS biological_entities (
    entity_id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL CHECK(entity_type IN
        ('protein','gene','transcript','organism','structure','other')),
    accession TEXT,
    sequence TEXT,
    sequence_sha256 TEXT,
    organism TEXT,
    source_dataset_id TEXT REFERENCES datasets(dataset_id),
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_entities_accession ON biological_entities(accession);
CREATE INDEX IF NOT EXISTS idx_entities_sequence_hash ON biological_entities(sequence_sha256);
CREATE TABLE IF NOT EXISTS compounds (
    compound_id TEXT PRIMARY KEY,
    canonical_smiles TEXT,
    inchikey TEXT,
    source_dataset_id TEXT REFERENCES datasets(dataset_id),
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_compounds_inchikey ON compounds(inchikey);
CREATE TABLE IF NOT EXISTS assays (
    assay_id TEXT PRIMARY KEY,
    dataset_id TEXT REFERENCES datasets(dataset_id),
    assay_type TEXT NOT NULL,
    description TEXT,
    conditions_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS measurements (
    measurement_id TEXT PRIMARY KEY,
    assay_id TEXT REFERENCES assays(assay_id),
    entity_id TEXT REFERENCES biological_entities(entity_id),
    compound_id TEXT REFERENCES compounds(compound_id),
    measurement_type TEXT NOT NULL,
    value REAL,
    unit TEXT,
    relation TEXT,
    replicate_group TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    CHECK(value IS NULL OR value = value)
);
CREATE INDEX IF NOT EXISTS idx_measurements_assay ON measurements(assay_id);
CREATE INDEX IF NOT EXISTS idx_measurements_entity ON measurements(entity_id);
CREATE INDEX IF NOT EXISTS idx_measurements_compound ON measurements(compound_id);
CREATE INDEX IF NOT EXISTS idx_measurements_type ON measurements(measurement_type);
CREATE TABLE IF NOT EXISTS artifacts (
    artifact_id TEXT PRIMARY KEY,
    artifact_type TEXT NOT NULL,
    uri TEXT NOT NULL,
    checksum_sha256 TEXT,
    format TEXT,
    byte_size INTEGER,
    schema_json TEXT NOT NULL DEFAULT '{}',
    provenance_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_artifacts_type ON artifacts(artifact_type);
CREATE TABLE IF NOT EXISTS feature_sets (
    feature_set_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    artifact_id TEXT REFERENCES artifacts(artifact_id),
    feature_schema_json TEXT NOT NULL DEFAULT '{}',
    dataset_id TEXT REFERENCES datasets(dataset_id),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS training_runs (
    run_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT,
    status TEXT NOT NULL DEFAULT 'created',
    dataset_id TEXT REFERENCES datasets(dataset_id),
    feature_set_id TEXT REFERENCES feature_sets(feature_set_id),
    config_json TEXT NOT NULL DEFAULT '{}',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    random_seed INTEGER,
    code_revision TEXT,
    started_at TEXT,
    finished_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_training_runs_model ON training_runs(model_name, created_at);
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id TEXT PRIMARY KEY,
    run_id TEXT REFERENCES training_runs(run_id),
    entity_id TEXT REFERENCES biological_entities(entity_id),
    compound_id TEXT REFERENCES compounds(compound_id),
    task TEXT NOT NULL,
    predicted_value REAL,
    unit TEXT,
    uncertainty REAL,
    confidence REAL,
    artifact_id TEXT REFERENCES artifacts(artifact_id),
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_predictions_run ON predictions(run_id);
CREATE INDEX IF NOT EXISTS idx_predictions_task ON predictions(task);
CREATE TABLE IF NOT EXISTS provenance_events (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    subject_id TEXT,
    source TEXT,
    details_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_provenance_subject ON provenance_events(subject_id);
"""

class KineticsSQLite:
    """SQLite repository for Kinetics metadata and experiment bookkeeping."""

    def __init__(self, path: str | Path = "data/kinetics.sqlite3", *,
                 timeout_seconds: float = 30.0, cache_size_mb: int = 64,
                 mmap_size_mb: int = 256) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.timeout_seconds = timeout_seconds
        self.cache_size_mb = max(8, cache_size_mb)
        self.mmap_size_mb = max(0, mmap_size_mb)

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.path,
            timeout=self.timeout_seconds,
            isolation_level=None,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute(f"PRAGMA busy_timeout={int(self.timeout_seconds * 1000)}")
        connection.execute("PRAGMA synchronous=NORMAL")
        connection.execute(f"PRAGMA cache_size=-{self.cache_size_mb * 1024}")
        connection.execute("PRAGMA temp_store=MEMORY")
        connection.execute(f"PRAGMA mmap_size={self.mmap_size_mb * 1024 * 1024}")
        return connection

    @contextmanager
    def session(self) -> Iterator[sqlite3.Connection]:
        """Yield a configured connection and always close it on exit."""
        connection = self.connect()
        try:
            yield connection
        finally:
            connection.close()

    def initialize(self) -> None:
        """Create or upgrade the metadata schema to the current version.

        Databases created before schema versioning have user_version=0. The
        initial migration is additive and idempotent, preserving their data.
        Future schema changes must add an explicit migration before bumping
        SCHEMA_VERSION.
        """
        with self.session() as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            current_version = int(connection.execute("PRAGMA user_version").fetchone()[0])
            if current_version > SCHEMA_VERSION:
                raise RuntimeError(
                    f"Database schema version {current_version} is newer than "
                    f"this Kinetics version supports ({SCHEMA_VERSION})."
                )
            try:
                connection.executescript(
                    "BEGIN IMMEDIATE;\n"
                    + _SCHEMA
                    + f"\nPRAGMA user_version = {SCHEMA_VERSION};\nCOMMIT;"
                )
            except Exception:
                if connection.in_transaction:
                    connection.rollback()
                raise

    @contextmanager
    def transaction(self, *, immediate: bool = True) -> Iterator[sqlite3.Connection]:
        """Open a short atomic transaction; always commit or roll back."""
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE" if immediate else "BEGIN")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def execute_many(self, sql: str, rows: Sequence[Sequence[Any]]) -> int:
        """Insert/update rows efficiently in one transaction."""
        if not rows:
            return 0
        with self.transaction() as connection:
            connection.executemany(sql, rows)
            return connection.total_changes

    def fetch_all(self, sql: str, parameters: Sequence[Any] = ()) -> list[dict[str, Any]]:
        with self.session() as connection:
            return [dict(row) for row in connection.execute(sql, parameters).fetchall()]

    @staticmethod
    def json_dumps(value: Mapping[str, Any] | None) -> str:
        return json.dumps(value or {}, sort_keys=True, separators=(",", ":"), default=str)

    @staticmethod
    def sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
        digest = hashlib.sha256()
        with Path(path).open("rb") as stream:
            for chunk in iter(lambda: stream.read(chunk_size), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def checkpoint(self, *, truncate: bool = False) -> None:
        """Checkpoint the WAL, e.g. after a large import or before archival."""
        mode = "TRUNCATE" if truncate else "PASSIVE"
        with self.session() as connection:
            connection.execute(f"PRAGMA wal_checkpoint({mode})")

    def optimize(self) -> None:
        """Refresh planner statistics after bulk loading."""
        with self.session() as connection:
            connection.execute("PRAGMA optimize")

    def backup(self, destination: str | Path) -> None:
        """Create a consistent SQLite backup while the database is in use."""
        destination_path = Path(destination)
        if destination_path.resolve() == self.path.resolve():
            raise ValueError("Backup destination must differ from the source database.")
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        target = sqlite3.connect(str(destination_path))
        try:
            with self.session() as source:
                source.backup(target)
        finally:
            target.close()
