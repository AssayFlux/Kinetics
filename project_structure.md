# Kinetics Knowledge Ingestion — Project Structure

This subsystem extends the canonical 100-domain register in
`docs/SCIENCE_DOMAIN_CATALOGUE_100.md` and the existing SQLite/data-platform
architecture. It does not create a second domain catalogue or replace the
existing scientific data model.

```text
Kinetics/
├── .github/
│   └── workflows/
│       └── bulk_downloader.yml
├── database/
│   ├── domains/
│   │   └── extended_domains.json  # additional cross-disciplinary scopes
│   └── sources/
│       └── knowledge_sources.json
├── data/
│   ├── corpus-manifests/          # small, versioned metadata and summaries
│   │   ├── metadata_index.json
│   │   └── analysis_summary.json
│   ├── corpus/                    # local object store; gitignored by default
│   │   └── objects/
│   │       ├── medicine/
│   │       ├── biomedical/
│   │       └── engineering/
│   └── kinetics.sqlite3           # existing local database; gitignored
├── docs/
│   └── KNOWLEDGE_INGESTION.md
├── src/
│   └── kinetics_core/
│       └── knowledge/
│           ├── __init__.py          # reusable KnowledgeStore retrieval API
│           └── cli.py               # installed knowledge search command
├── scripts/
│   ├── fetch_corpus.py             # discovery, licensing, download, resume
│   ├── tokenize_corpus.py          # extraction, tokenization, FTS indexing
│   ├── analyze_corpus.py           # deterministic summaries and entities
│   ├── query_knowledge.py          # local evidence retrieval
│   ├── restore_corpus_releases.py  # verified release restore
│   └── git_sync.py                # manifest/LFS synchronization
├── tests/
│   └── test_knowledge_ingestion.py
├── requirements.txt               # existing requirements + pinned ingestion extras
├── requirements-knowledge.txt     # lightweight pinned ingestion environment
└── README.md
```

## Data flow

1. Discover records from source adapters, rotating through the existing domain catalogue.
2. Require an explicit redistribution-compatible license before downloading.
3. Stream each object to a temporary file, enforce per-file and per-batch byte caps,
   calculate SHA-256, and atomically move it into content storage.
4. Save resumable source IDs and provenance in `metadata_index.json`.
5. Extract supported formats and create bounded overlapping text chunks.
6. Index chunks and source metadata in the existing `data/kinetics.sqlite3` file.
7. Run deterministic analysis and expose source-linked retrieval results.

## Storage policy

- Git versions code, schemas, source registry, manifests and compact summaries.
- Standalone fetch runs keep raw PDFs/EPUBs local. The scheduled GitHub workflow
  publishes newly acquired, explicitly redistributable batches as public Release
  assets; use the restore utility to populate a local object store. Git LFS is an
  optional alternative with separate storage/bandwidth quotas.
- Never put patient data, credentials, private datasets or restricted documents
  in this public repository.
- Use encrypted, access-controlled object storage for private or large corpora.
