# Kinetics knowledge ingestion and retrieval

## Scope

This subsystem turns openly redistributable books and research articles into a source-grounded local knowledge index for Kinetics. It is an acquisition and research-support pipeline, not a clinical decision system. The 100 foundational domains in `docs/SCIENCE_DOMAIN_CATALOGUE_100.md` are combined with 60 extensions in `database/domains/extended_domains.json`, yielding 160 unique acquisition domains. Their extension scope descriptions are maintained in `database/domains/extended_domain_scopes.json`. `database/domains/domain_synonyms.json` expands each domain into source-search terms; this is the single acquisition taxonomy used by the fetcher.

## Components

- `scripts/fetch_corpus.py`: Internet Archive books and Europe PMC Open Access papers, with explicit license gates, bounded streaming, HTTP Range resume, SHA-256, retry/backoff and resumable manifest.
- `scripts/fetch_research_data.py`: Zenodo books, publications and research datasets. It requires explicit CC0, CC BY or CC BY-SA record licenses and records DOI, creators, version, keywords, file identity and source links.
- `scripts/fetch_specialist_sources.py`: OpenAlex and arXiv openly licensed literature, UniProtKB protein FASTA, RCSB PDB macromolecular structures, OAPEN academic books, Figshare research files and Dryad datasets. OpenAlex/arXiv/OAPEN/Figshare/Dryad files require explicit accepted item-level CC rights; UniProtKB data is CC BY 4.0 and RCSB PDB archive data is CC0.
- `scripts/tokenize_corpus.py`: PDF/EPUB/XML/NXML/HTML/TXT extraction, deterministic word/punctuation tokenization, overlapping chunks and SQLite FTS5 indexing.
- `scripts/analyze_corpus.py`: exploratory term/entity counts and domain summaries.
- `scripts/query_knowledge.py`: source-linked local full-text retrieval.
- `scripts/git_sync.py`: manifest commits, GitHub Release assets or optional Git LFS for redistributable PDFs/EPUBs.
- `scripts/restore_corpus_releases.py`: safe, checksum-verified release restore.

## Legal and source policy

A public API or downloadable URL is not a redistribution grant. Internet Archive items are acquired only when item metadata carries a recognized CC0, Public Domain Mark, CC BY or CC BY-SA license. Europe PMC/PMC OA records must expose an accepted license and an OA package. Zenodo records must carry an explicit CC0, CC BY or CC BY-SA license; record-level rights are applied conservatively to the selected file. Unknown, NC, ND and all-rights-reserved records are skipped. Review third-party content notices, attribution and exact item/file terms before redistributing any mirrored corpus.
DOAB and DOAJ remain discovery candidates until their individual adapters and item-level rights checks are implemented. OAPEN, Figshare and Dryad use their public APIs but skip records where a supported item-level license cannot be established. arXiv is implemented conservatively and skips records without an explicit CC license. OpenAlex is likewise restricted to explicit CC licenses.

The repository is public. Never ingest patient records, identifiable health information, credentials, private research, restricted full text or data-use agreement material into it. The SQLite database is local-only by default and its file permissions are restricted to the current POSIX user (0600). This is not encryption; use full-disk encryption and encrypted backups where needed. Raw corpus batches are published as public GitHub Release assets. Use encrypted, access-controlled object storage for confidential or larger collections.

## Install

Python 3.10+ is required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-knowledge.txt
python -m pip install -e . --no-deps
```

The ingestion dependencies are pinned in `requirements-knowledge.txt`. PDF, EPUB, HTML, tabular and JSON parsers are used during indexing. Biopython parses FASTA/GenBank sequences and PDB/mmCIF structures into searchable sequence representations; original source objects remain preserved and checksummed. UniProtKB and RCSB PDB adapters add dedicated, structured molecular data alongside books and papers.

## Run locally

Preview the rotating domains and current manifest without downloading:

```bash
python scripts/fetch_corpus.py --dry-run
```

Fetch one bounded batch (30 files maximum; 80 MiB total by default):

```bash
python scripts/fetch_corpus.py --batch-size 15 --max-batch-mb 40 --max-domains 8 --max-file-mb 40
python scripts/fetch_research_data.py --batch-size 10 --max-batch-mb 25 --max-file-mb 25 --max-domains 8
python scripts/fetch_specialist_sources.py --batch-size 10 --max-batch-mb 25 --max-file-mb 25 --max-domains 8 --per-source-limit 3
```

The source IDs and states are checkpointed in `data/corpus-manifests/metadata_index.json`. Binary objects are stored under `data/corpus/objects/{medicine,biomedical,engineering}/`. Re-running the command resumes from the domain cursor and skips already downloaded IDs. A failed transient item can be retried on a later run. The default batch configuration is deliberately bounded. The per-file cap defaults to 80 MiB (`--max-file-mb`, maximum 80 MiB) and the aggregate byte guard remains mandatory for unattended execution.

To restore the public corpus batches published by Actions, authenticate GitHub CLI and run:

```bash
gh auth login
python scripts/restore_corpus_releases.py
```

The restore utility validates archive paths and verifies every SHA-256 checksum before writing objects.

Extract and index up to 100 downloaded documents per cycle:

```bash
python scripts/tokenize_corpus.py --max-documents 50
python scripts/analyze_corpus.py
python scripts/query_knowledge.py "cardiac AND imaging" --limit 10
kinetics-knowledge "cardiac AND imaging" --limit 10
```

The index is added to the existing `data/kinetics.sqlite3` SQLite database. Other Kinetics modules can use the read-only `kinetics_core.knowledge.KnowledgeStore` API or the installed `kinetics-knowledge` command to retrieve source-linked chunks. FTS5 stores text chunks and source metadata; the original document stays in the content-addressed filesystem store. Chunking is a deterministic baseline tokenizer, not a model-specific tokenizer. A future embedding adapter can add versioned vectors without changing source identity or provenance.

## GitHub automation

1. Push the subsystem to the repository's `main` branch.
2. In **Settings → Actions → General → Workflow permissions**, select **Read and write permissions** so the workflow can publish Release assets and push the compact manifest.
3. No third-party API token is required for the configured public APIs. The workflow uses the short-lived `GITHUB_TOKEN` provided by Actions.
4. Open **Actions → Kinetics knowledge corpus ingestion → Run workflow**.
5. Choose 1–3 cycles, up to 30 records per cycle and at most 80 MiB per cycle. A push to the main branch that changes the ingestion adapters/configuration starts an initial bounded run; the scheduled run executes two bounded cycles per week.
6. The workflow publishes each bounded binary batch as a GitHub Release asset and commits compact manifests. Release assets are separate from Git history and each archive is kept below 80 MiB. Release assets on this public repository are public; only explicitly redistributable documents may be included. Git LFS remains an opt-in alternative because it has separate storage and bandwidth quotas.

Git pushes use an HTTP authorization header scoped to the single git command; the token is never written to the remote URL or manifest. Commit messages include `[skip ci]` to avoid recursively triggering the general CI workflow. The workflow uses a concurrency group and a non-forced push.

## Git LFS

For an explicitly approved public corpus mirror:

```bash
git lfs install
git lfs track "*.pdf" "*.epub"
git add .gitattributes
python scripts/git_sync.py --mode lfs --push
```

Each file is capped by `--max-file-mb` (80 MiB maximum) so the object remains compatible with bounded GitHub Release batches. Git LFS is not unlimited storage; review current account and repository quotas. For a large corpus, prefer an object store (S3-compatible or equivalent) and commit only immutable manifests and checksums to Git. Do not place SQLite database files in Git.

## Recovery, audit and limitations

- Interrupted `.part` downloads are retained and resumed with HTTP Range when the origin supports it; a server that ignores Range safely restarts the transfer. Only complete files are moved into the object store.
- The manifest is atomically replaced after a successful batch and includes source, item ID, URL, license, domain, retrieval time, size and SHA-256.
- The tokenizer re-hashes every object before parsing it.
- Keep the source package, source citation and license snapshot for audits.
- OCR is not performed. Scanned PDFs may yield no text and are marked as such.
- Token counts are tokenizer-specific estimates; current chunking counts Unicode word/punctuation tokens, not LLM model tokens.
- Lightweight entity/keyword counts are exploratory signals, not validated scientific assertions. Every retrieval result should be checked against its cited source and relevant study limitations.
- The 160-domain target is a taxonomy breadth objective, not a claim of corpus coverage. Zenodo expands books and general research-data coverage; BioPython adds sequence and structure-aware indexing. The 10,000+ target is an incremental collection objective, not a promise that one workflow run downloads that many files. Rate limits, rights, source availability and storage budgets govern actual throughput.


### Reuse from Kinetics Python modules

~~~python
from kinetics_core.knowledge import KnowledgeStore

knowledge = KnowledgeStore("data/kinetics.sqlite3")
hits = knowledge.search("cardiac AND imaging", limit=8, domain="Cardiology")
for hit in hits:
    print(hit["title"], hit["source_url"], hit["license"])
    print(hit["citation_metadata"])
    print(hit["text"])
~~~

The API opens the index read-only and returns the original source URL, license,
SHA-256 and citation metadata with each chunk. Consumers must preserve those
fields when presenting derived summaries and should verify the source document
before relying on a claim.
