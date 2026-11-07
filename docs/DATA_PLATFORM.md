# Kinetics universal scientific data platform

SQLite is the primary local database. The repository versions schemas, code, source manifests, checksums, acquisition scripts and only small openly redistributable seed datasets. Do not put huge raw datasets or generated indexes in Git history.

## Layers
1. Immutable raw source records with provider IDs, release, retrieval time, license snapshot and SHA-256.
2. Normalized SQLite entities: genes, transcripts, proteins, structures, variants, organisms, compounds, reactions, pathways, cells, tissues, diseases, assays and publications.
3. FTS5 search indexes over metadata, names, synonyms and curated abstracts—not raw coordinates or every sequence residue.
4. Content-addressed artifact files outside SQLite; database stores paths, sizes, checksums and licenses.
5. Derived embeddings/fingerprints with model and preprocessing versions.

## Mobile tokenization
Use FTS5 unicode61 with diacritic folding for searchable labels and descriptive text. Exact accessions use the identifiers table. Protein/DNA/RNA sequence search should use optional alphabet-aware k-mer/minimizer indexes, not one text token per residue. Chemical search uses canonical identifiers, InChIKey and optional fingerprints. Keep structure coordinates compressed as artifacts and parse on demand.

## Android profile
Use bounded batches, streaming parsers, resumable cursors, content hashes, lazy loading and incremental transactions. Keep model weights, matrices and large coordinate corpora outside SQLite. Use WAL with one writer and short transactions. Start with conservative cache/mmap settings in the schema, then benchmark on low-memory devices. Bundle small read-only reference snapshots separately from each user's writable workspace.

## Acquisition and licensing
The source registry is database/sources/catalog.json. Verify exact release terms, attribution, third-party exceptions and redistribution rights before enabling a bulk mirror. API access is not a redistribution license. Record the license with each release and artifact.

## Dataset tiers
- Tier 0: small, redistributable ontology/reference packs.
- Tier 1: user-selected resumable local packs.
- Tier 2: federated queries against large upstream databases, caching requested records.
- Tier 3: optional bulk archive on external disk/object storage, indexed by SQLite.

## Layout
database/sqlite/schema.sql — initial schema
 database/sources/catalog.json — source and license registry
data/raw, data/processed, data/cache — local-only datasets (gitignored)
scripts/data — download, verify and import tools

Schema migration 1 creates the initial cross-domain model. Test migrations against empty and populated databases before application integration.
