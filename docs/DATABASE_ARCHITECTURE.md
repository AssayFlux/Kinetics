# Kinetics data and training storage architecture

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
