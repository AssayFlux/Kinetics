# Kinetics knowledge ingestion and retrieval

## Scope

This subsystem turns openly redistributable books and research articles into a source-grounded local knowledge index for Kinetics. It is an acquisition and research-support pipeline, not a clinical decision system. The existing `docs/SCIENCE_DOMAIN_CATALOGUE_100.md` remains the canonical domain taxonomy; the fetcher rotates through its entries instead of maintaining a duplicate list.

## Components

- `scripts/fetch_corpus.py`: source discovery, explicit license gate, bounded streaming downloads, SHA-256, atomic files, retry/backoff and resumable manifest.
- `scripts/tokenize_corpus.py`: PDF/EPUB/XML/NXML/HTML/TXT extraction, deterministic word/punctuation tokenization, overlapping chunks and SQLite FTS5 indexing.
- `scripts/analyze_corpus.py`: exploratory term/entity counts and domain summaries.
- `scripts/query_knowledge.py`: source-linked local full-text retrieval.
- `scripts/git_sync.py`: manifest commits, GitHub Release assets or optional Git LFS for redistributable PDFs/EPUBs.
- `scripts/restore_corpus_releases.py`: safe, checksum-verified release restore.

## Legal and source policy

A public API or downloadable URL is not a redistribution grant. The initial fetcher enables Internet Archive items only when item metadata carries a recognized CC0, Public Domain Mark, CC BY or CC BY-SA license. It enables Europe PMC/PMC OA records only when the record exposes an accepted license and the OA service supplies a package. Unknown, NC, ND and all-rights-reserved records are skipped. Review every source's terms, third-party content notices, attribution and exact item/release license before using a mirrored corpus.
Source adapters are deliberately conservative; DOAB, DOAJ and arXiv are registered as discovery candidates but are not silently bulk-downloaded.

The repository is public. Never ingest patient records, identifiable health information, credentials, private research, restricted full text or data-use agreement material into it. The SQLite database is local-only by default and its file permissions are restricted to the current POSIX user (0600). This is not encryption; use full-disk encryption and encrypted backups where needed. Raw corpus batches are published as public GitHub Release assets. Use encrypted, access-controlled object storage for confidential or larger collections.

## Install

Python 3.10+ is required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-knowledge.txt
```

The lightweight ingestion dependencies are pinned in `requirements-knowledge.txt`; the existing root `requirements.txt` also includes them for full Kinetics environments. PDF, EPUB and HTML parsing libraries are used only by the tokenization step.

## Run locally

Preview the rotating domains and current manifest without downloading:

```bash
python scripts/fetch_corpus.py --dry-run
```

Fetch one bounded batch (30 files maximum; 80 MiB total by default):

```bash
python scripts/fetch_corpus.py --batch-size 30 --max-batch-mb 80
```

The source IDs and states are checkpointed in `data/corpus-manifests/metadata_index.json`. Binary objects are stored under `data/corpus/objects/{medicine,biomedical,engineering}/`. Re-running the command resumes from the domain cursor and skips already downloaded IDs. A failed transient item can be retried on a later run. The default batch configuration is deliberately bounded; do not remove the per-file or aggregate byte guards for unattended execution.

To restore the public corpus batches published by Actions, authenticate GitHub CLI and run:

```bash
gh auth login
python scripts/restore_corpus_releases.py
```

The restore utility validates archive paths and verifies every SHA-256 checksum before writing objects.

Extract and index up to 50 downloaded documents:

```bash
python scripts/tokenize_corpus.py --max-documents 50
python scripts/analyze_corpus.py
python scripts/query_knowledge.py "cardiac AND imaging" --limit 10
```

The index is added to the existing `data/kinetics.sqlite3` SQLite database. FTS5 stores text chunks and source metadata; the original document stays in the content-addressed filesystem store. Chunking is a deterministic baseline tokenizer, not a model-specific tokenizer. A future embedding adapter can add versioned vectors without changing source identity or provenance.

## GitHub automation

1. Push the subsystem to the repository's `main` branch.
2. In **Settings → Actions → General → Workflow permissions**, select **Read and write permissions** so the workflow can publish Release assets and push the compact manifest.
3. No third-party API token is required for the configured public APIs. The workflow uses the short-lived `GITHUB_TOKEN` provided by Actions.
4. Open **Actions → Kinetics knowledge corpus ingestion → Run workflow**.
5. Choose 1–3 cycles, up to 30 records per cycle and at most 80 MiB per cycle. The scheduled run executes two bounded cycles per week.
6. The workflow publishes each bounded binary batch as a GitHub Release asset and commits compact manifests. Release assets are separate from Git history and each archive is kept below 100 MiB. Release assets on this public repository are public; only explicitly redistributable documents may be included. Git LFS remains an opt-in alternative because it has separate storage and bandwidth quotas.

Git pushes use an HTTP authorization header scoped to the single git command; the token is never written to the remote URL or manifest. Commit messages include `[skip ci]` to avoid recursively triggering the general CI workflow. The workflow uses a concurrency group and a non-forced push.

## Git LFS

For an explicitly approved public corpus mirror:

```bash
git lfs install
git lfs track "*.pdf" "*.epub"
git add .gitattributes
python scripts/git_sync.py --mode lfs --push
```

Each file is capped below 20 MiB by the fetcher. Git LFS is not unlimited storage; review current account and repository quotas. For a large corpus, prefer an object store (S3-compatible or equivalent) and commit only immutable manifests and checksums to Git. Do not place SQLite database files in Git.

## Recovery, audit and limitations

- A `.part` download is deleted after failure; only complete files are moved into the object store.
- The manifest is atomically replaced after a successful batch and includes source, item ID, URL, license, domain, retrieval time, size and SHA-256.
- The tokenizer re-hashes every object before parsing it.
- Keep the source package, source citation and license snapshot for audits.
- OCR is not performed. Scanned PDFs may yield no text and are marked as such.
- Token counts are tokenizer-specific estimates; current chunking counts Unicode word/punctuation tokens, not LLM model tokens.
- Lightweight entity/keyword counts are exploratory signals, not validated scientific assertions. Every retrieval result should be checked against its cited source and relevant study limitations.
- The 10,000+ target is an incremental collection objective, not a promise that one workflow run downloads that many files. Rate limits, rights, source availability and storage budgets govern actual throughput.
