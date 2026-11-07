# Kinetics Archive-First Offline Data Architecture

> **Platform context:** This document describes a focused component of Kinetics. The complete cross-disciplinary scope is catalogued in `docs/SCIENCE_DOMAIN_CATALOGUE_100.md`; catalogue inclusion is not implementation or clinical-validation evidence.


> **Mission authority:** This plan implements the archive and offline-data requirements of [KINETICS_MISSION.md](../KINETICS_MISSION.md). It is a proposed design, not a claim that petabyte-scale processing is already implemented.

## 1. Feasibility and physical limits

Kinetics can inspect archive metadata, stream selected members, decompress bounded portions and query prebuilt indexes without extracting complete archives to a directory. It cannot make arbitrary petabytes fit into a tiny local file: compression ratios depend on the data, and offline access requires the needed compressed bytes and indexes to exist on the device or attached storage.

The realistic product promise is: **no full extraction required; bounded-memory, indexed, selective access; offline operation for data actually present locally.** Do not promise arbitrary petabyte-scale offline analysis on a small phone.

## 2. Three-layer architecture

1. **Archive layer:** immutable compressed source objects and manifests. Preserve original files byte-for-byte where licensing permits.
2. **Catalogue/index layer:** SQLite stores archive/member metadata, source provenance, checksums, schema/format, chunk indexes, scientific identifiers and compact search indexes. SQLite is not the raw storage engine for every byte of every large dataset.
3. **Analysis layer:** domain parsers read only selected archive members or chunks, process bounded batches and return typed results. Full extraction is never the default.

Keep large sequence blocks, structure coordinates, images, books and model weights in separate content-addressed object/chunk files. Store references and metadata in SQLite. Local archives may live on internal storage, SD card or attached disk. Remote references are not offline data.

## 3. Archive formats and access strategy

### Ordinary ZIP / ZIP64
- Support ZIP and ZIP64 as import and compatibility formats.
- Read the central directory first; validate member names, sizes, compression methods, encryption status and checksums.
- Open selected members as streams; never use extract-all as the default.
- ZIP64 supports large archive/member addressing; it does not create compression beyond the physical information content.
- Deflated ZIP members are not a reliable random-access substrate for arbitrary byte offsets inside a member. Seeking may require decompression from an earlier point. Treat ZIP as a package of independently addressable members, not a universal indexed scientific database.

### Kinetics Archive Container (KAC)
Build a versioned Kinetics-native chunk container for efficient random access:
- Manifest: archive UUID, format version, source/release, license/attribution, data schema, chunk table, sizes and checksums.
- Chunk table: dataset/member, chunk ID, logical record or row range, compressed offset/length, uncompressed length, codec, checksum and optional domain-specific key range.
- Compress chunks independently with Zstandard and maintain a seek table/index so only relevant chunks need decompression.
- Benchmark chunk sizes; begin experiments around 1–16 MiB but do not hard-code one size for all modalities.
- Optional content-addressed deduplication across packs, using collision-safe hashes and reference counts.
- Keep chunks immutable; updates create a new manifest/version and reuse unchanged chunks.

Ordinary Zstandard frames are streamable but do not themselves provide arbitrary random access. Use seekable framing or KAC's explicit chunk table; a .zst file extension alone does not imply seekability.

### Domain-specific indexed formats
Use established scientific formats when they outperform a generic container:
- Genomics: BGZF-compressed FASTA/FASTQ where appropriate; indexed BAM/CRAM and tabix-indexed VCF/GFF/interval records. Track reference assembly/version and genomic interval indexes.
- Protein sequences: record-level FASTA indexing, compact sequence blocks, k-mer/minimizer indexes.
- Protein structures: preserve mmCIF/PDB sources; index structures, chains and residues; store coordinate records in independently compressed chunks and load only selected regions where feasible.
- Chemistry: SDF/MOL records chunked by compound; index stable identifiers/InChIKey, descriptors and fingerprints.
- Omics matrices: chunked/tiled arrays or columnar formats such as Zarr, Parquet or Arrow where suitable; keep sample/feature metadata in SQLite.
- Books and papers: preserve licensed PDF/EPUB/HTML; derive page/section text chunks and local full-text indexes with page/paragraph locators and citations. OCR is a separate derived artifact with quality metadata.
- Images and microscopy: tiled or pyramidal multi-resolution representations; fetch only needed tiles.
- Models: independently stored weight shards and validated quantized device-specific variants.

## 4. SQLite's role

SQLite is the local catalogue and coordination database:
- archive, pack, member and chunk metadata;
- source, release, license, attribution and checksum provenance;
- scientific identifiers and cross-domain relationships;
- import jobs, checkpoints and validation outcomes;
- compact FTS indexes for books, papers and descriptive metadata;
- pointers into external chunk/object files.

Do not put all petabytes into one SQLite file. Keep large raw objects separate. Use WAL where appropriate, bounded transactions and a single controlled writer. Coordinate database backups with archive manifests.

## 5. Query flow without full extraction

1. User adds an archive or pack.
2. Kinetics reads its directory/manifest without extracting members.
3. Validate paths, sizes, codecs, hashes and license metadata.
4. Register archive, members and indexes in SQLite.
5. Map a scientific question to identifiers, intervals, pages, structures or chunks.
6. Read only matching members/chunks, decompress into bounded buffers, parse incrementally and release buffers promptly.
7. Cache only useful decoded chunks under a configurable quota.
8. Return results with source accession, release, member, record/page/coordinate locator, checksum and transformation lineage.
9. If data are not locally present, report that the task is unavailable offline rather than silently using the network.

## 6. Small Android mode

- Strict memory budget, streaming parsers and back-pressure.
- Configurable maximum decompressed chunk size and cache quota.
- Background indexing with pause/resume and battery/network constraints.
- Low-priority prefetch only when charging or on an allowed network.
- Query planner prefers local indexes; limit concurrent decompression workers.
- User controls for local packs, free space, cache, pinned offline collections and removable storage.
- Heavy training, whole-cohort analysis and large simulations use suitable compute; phones query selected local data and precomputed results.

## 7. Security and data governance

Treat every archive as untrusted:
- Defend against ZIP bombs with limits on member count, nesting, compression ratio, declared and actual expanded bytes, CPU time and total processing budget.
- Reject path traversal, absolute paths, unsafe symlinks, duplicate/confusable names and unsupported encrypted entries unless explicitly supported.
- Verify archive and chunk integrity with CRC where available and cryptographic hashes.
- Never execute archive content. Sandbox parsers and keep dependencies patched.
- Preserve license, attribution, consent, data-use agreements and geographic restrictions at dataset/record level. An accessible URL does not imply redistribution permission.
- Encrypt private/patient data at rest; separate private data from public reference packs; enforce access controls and audit access.
- Do not commit private, restricted or very large archives into public Git history.

## 8. Staged implementation plan

### Phase A — Safe archive inspection
Implement ZIP/ZIP64 directory inspection, safe member listing, stream-only member reading, metadata limits, checksums, resumable jobs and SQLite archive/member registry. No bulk extraction API in the default workflow.

### Phase B — Indexed chunk format
Specify and implement KAC manifests, independently compressed chunks, seek tables, checksums, immutable versioning, optional deduplication and a bounded chunk cache. Benchmark against Zstandard seekable framing and domain formats.

### Phase C — Scientific adapters
Add adapters for FASTA/FASTQ, VCF, GFF3, BAM/CRAM indexes, PDB/mmCIF, SDF, CSV/TSV/JSON, Parquet/Arrow/Zarr, PDF/EPUB/HTML and image pyramids. Each adapter supports metadata inspection, record iteration, indexed selection and provenance.

### Phase D — Offline scientific library
Build lawful, versioned local packs for ontologies, reference sequences, structures, compounds, pathways, books and literature. Keep bibliographic/page locators and cross-links. Offer curated bundles by domain or research task with transparent storage estimates and update manifests.

### Phase E — Android resource manager
Implement memory/storage quotas, removable storage, selective pack pinning, background indexing, cache eviction, battery-aware scheduling and offline query planning. Profile on low-end physical devices.

### Phase F — Scientific and adversarial validation
Test random-access correctness, decompression integrity, corruption recovery, interrupted imports, duplicate members, huge directories, ZIP bombs, malicious paths, license gates, lineage, airplane-mode operation, low-memory behaviour, battery/thermal impact and cross-platform reproducibility. Publish measured compression ratios, query latency, RAM, CPU, storage and index overhead on representative real datasets.

## 9. Acceptance gates

- Catalogue a ZIP/ZIP64 archive without extracting all members.
- Query a selected member through a bounded-memory stream and prove unrelated members were not decompressed.
- Retrieve a KAC chunk by index without decompressing unrelated chunks.
- Resume interrupted imports without duplicating records.
- Detect corruption and unsafe archives before ingestion.
- Produce reproducible results with source, release, checksum and exact record locator.
- Demonstrate airplane-mode analysis using only pinned local data.
- Pass memory, storage, CPU, battery and thermal budgets on representative low-end Android hardware.
- Never describe remote references as locally available or a compressed archive as petabytes of physical offline data.

## 10. Recommendation

Build ZIP/ZIP64 as an ingestion/compatibility layer, not the core random-access data format. Build KAC as a versioned chunked container while adopting BGZF/tabix and other established indexed scientific formats where appropriate. SQLite remains the local catalogue and index coordinator; compressed scientific chunks and original source files remain separate objects.

This provides the intended experience: add a large archive, inspect it without full extraction, query only what is needed and use pinned collections offline—without impossible claims about petabyte compression or phone storage.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
