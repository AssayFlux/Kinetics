# Kinetics data and training storage architecture

> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

## Decision

Use the Python standard-library `sqlite3` engine as the local transactional
metadata and experiment database. Default location: `data/kinetics.sqlite3`.
No additional SQLite package is required.

SQLite will catalog datasets, accessions, protein/gene records, compounds,
assays, measurements, feature-set definitions, training runs, model metadata,
predictions, provenance, and artifact locations. The initial schema and
connection manager live in `kinetics_core.storage.sqlite_store`.

## Important performance boundary

SQLite is not the tensor store and must not be the only storage layer for all
training data. It is excellent for indexed metadata, moderate-sized tabular
records, workflow state, and reproducible experiment tracking. It is not a
high-throughput concurrent training-data lake, vector database, or GPU tensor
loader. SQLite has one writer at a time; WAL allows readers alongside a writer
but does not provide unlimited parallel writes.

Use a hybrid layout:

- **SQLite:** identifiers, labels/assay metadata, dataset manifests, split
  assignments, provenance, run configurations, metrics, prediction summaries,
  and paths/checksums for artifacts.
- **Parquet/Arrow:** large tabular assay and feature datasets with columnar,
  predicate-pushdown reads.
- **NumPy / memory-mapped arrays:** dense numeric feature matrices when suitable.
- **HDF5 or Zarr:** large chunked multidimensional arrays and embeddings.
- **Safetensors / framework-native checkpoints:** model weights.
- **PDB/mmCIF and compressed sequence files:** canonical biological source files.
- **Optional vector index:** add only when semantic embedding retrieval is
  actually required; do not overload SQLite tables with high-dimensional blobs.

## Schema versioning and upgrades

The database uses SQLite's `PRAGMA user_version` as its schema version.
Version 1 is the initial schema bootstrap and is safe to re-run against
databases created by the pre-versioned implementation: tables and indexes are
created with `IF NOT EXISTS`, existing records are retained, and the version
is written in the same schema transaction. Opening a database whose schema
version is newer than the installed Kinetics code supports fails explicitly;
it must not be silently downgraded.

Every future schema change must add a numbered, ordered migration, increment
`SCHEMA_VERSION`, and include tests for both a fresh database and an upgrade
from the previous supported version. Back up production/user databases before
upgrades. Schema migrations must never discard scientific observations or
provenance without an explicit reviewed migration plan.

## SQLite performance defaults

- Write-Ahead Logging (WAL), `synchronous=NORMAL`, foreign keys enabled.
- Busy timeout, bounded page cache, memory temp store, and memory mapping.
- Parameterized SQL and `executemany` in bounded batches.
- Short transactions; avoid holding a write transaction during model training.
- Add indexes for real query patterns, not every column.
- Run `PRAGMA optimize` after bulk imports; checkpoint WAL after large loads.
- Use SQLite's backup API for consistent backups.
- One controlled writer/ingestion queue; multiple independent read connections.
- Keep database files on a local filesystem, not an unreliable network share.
- Record schema version/migrations before public release; test recovery and backups.

## Usage

```python
from kinetics_core.storage import KineticsSQLite

store = KineticsSQLite("data/kinetics.sqlite3")
store.initialize()

# Batch writes use one short transaction.
store.execute_many(
    "INSERT INTO datasets(dataset_id, name, source) VALUES (?, ?, ?)",
    [("uniprot-reviewed", "UniProt reviewed", "UniProt")],
)
```

The database is initialized on first use, not committed as a pre-populated
binary file. Dataset payloads are downloaded/imported only by explicit,
documented ingestion workflows.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
