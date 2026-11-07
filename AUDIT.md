# Repository audit — 2026-11-07

## Scope and method
Read-only inspection of the public GitHub repository AssayFlux/Kinetics at 6a66bfc6044e0f066c35512fc9b90bf24bc3d34c. The recursive Git tree was complete (not truncated). This is a remote repository audit: a local working-tree git status could not be run, and no claim is made about unpushed or uncommitted local changes.

## Repository identity and baseline
- Default branch: main; HEAD at audit: 6a66bfc6044e0f066c35512fc9b90bf24bc3d34c.
- GitHub-reported repository size: approximately 79,177 KiB.
- Recursive tree: 248 entries, 211 blobs, 37 tree entries.
- Existing foundations: Python 3.10+ / setuptools / pyproject; Rust Cargo at rust/kinetics-infra; C++17 / CMake at native; FastAPI/browser workbench; SQLite/PostgreSQL; Terraform.
- No Android/Gradle/Compose project was present in the audited tree.
- No root KINETICS_MASTER_PROMPT.md was present at audit time.
- Python entry points: kinetics-research, kinetics-workbench, kinetics-knowledge, kinetics-curate-catpred.
- Python package: src/kinetics_core; tests: tests; CI: .github/workflows/ci.yml.

## Build and test evidence
The latest completed push CI for this exact main HEAD passed: https://github.com/AssayFlux/Kinetics/actions/runs/42367898956. CI covers Python 3.10–3.12, Rust format/clippy/tests, C++ builds/reference tests on Linux/macOS/Windows, Terraform, workbench integration and browser acceptance. This is software-test evidence only, not scientific validation or Android/device verification.

## Domain inventory
- 100 foundational domains: docs/SCIENCE_DOMAIN_CATALOGUE_100.md.
- 60 extension domains: database/domains/extended_domains.json.
- Extension scope descriptions: database/domains/extended_domain_scopes.json.
- Total: 160 names; 160 unique normalized names; no exact duplicate names detected.
- Existing format: Markdown table for the first 100 and JSON array/scope map for the 60 extensions. These are scope definitions, not implementation records.
- No existing domain YAML registry found.
- Catalogue membership does not imply implementation. The catalogue includes human-health/clinical and cross-disciplinary engineering domains beyond the initial Android tool inventory; preserve all definitions without implying they are shipped tools.

## Scientific foundation
The repository contains scientific/data-engineering code in src/kinetics_core (Biopython adapters, protein features, curation, chemistry, structure adapters, persistence, provenance, model evaluation and workbench), native (C++ molecular-structure support), and rust/kinetics-infra (infrastructure/job services). Preserve these pending code-by-code migration.
Existing capability evidence supports enzyme data curation/model research, protein/sequence/structure/chemistry utilities and provenance. Targeted source searches did not establish a complete classical enzyme-kinetics fitting suite (Michaelis–Menten, Lineweaver–Burk, Eadie–Hofstee, Hanes–Woolf, nonlinear inhibition fits). Keep those capabilities planned until source and benchmark tests demonstrate them.

## Large files and assets
Largest tracked files include:
- Assets/Kinetics.gif — 2,719,629 bytes.
- Assets/Brand Logo.svg — 2,071,266 bytes.
- src/kinetics_core/workbench/app.py — 46,198 bytes.
- database/sources/catalog.json — 36,447 bytes.
- src/kinetics_core/multimodal.py — 32,962 bytes.
- RESEARCH_BLUEPRINT.md — 32,866 bytes.
No PDF, notebook, model-weight, or bulk dataset extension was found in the recursive tree scan. This does not inspect git history or externally downloaded runtime data.

## Contradictory literature/corpus subsystem — removal candidates
Remove after an archival tag exists:
- scripts/fetch_corpus.py (25,702 B)
- scripts/fetch_research_data.py (14,981 B; mixed-purpose; separate structured-data adapters first)
- scripts/fetch_specialist_sources.py (30,880 B; mixed-purpose; separate structured biological data first)
- scripts/tokenize_corpus.py (9,158 B)
- scripts/query_knowledge.py (1,763 B)
- scripts/analyze_corpus.py (3,688 B)
- scripts/restore_corpus_releases.py (4,224 B)
- scripts/update_corpus_dashboard.py (10,263 B)
- scripts/git_sync.py (11,113 B; inspect for non-corpus use)
- src/kinetics_core/knowledge/__init__.py (3,948 B)
- src/kinetics_core/knowledge/cli.py (791 B)
- tests/test_knowledge_ingestion.py (6,663 B)
- tests/test_biopython_corpus_indexing.py (379 B)
- requirements-knowledge.txt (182 B)
- .github/workflows/bulk_downloader.yml (4,647 B)
- docs/KNOWLEDGE_INGESTION.md (12,525 B)
- docs/KNOWLEDGE_INGESTION_STRUCTURE.md (3,624 B)
- database/sources/knowledge_sources.json (5,519 B; review for structured-source records first)
- Assets/corpus-growth.svg (2,174 B; remove if unused)
Historical roadmaps and architecture documents require individual review; do not automatically delete documents containing useful engineering decisions.

## Secrets and credentials
Targeted GitHub code searches for common private-key and cloud/API-token markers did not return a confirmed secret. This is not a complete secret scan and does not establish that git history is clean. No secret values were printed.

## Classification and migration proposal
- KEEP: all 160 domain definitions; scientific source modules; tests; native reference implementations; provenance/reproducibility logic.
- MIGRATE: src/kinetics_core → python/kinetics; native → cpp; domain source files → domains/*.yaml; useful source manifests → datapacks/*/pack.yaml; tests → unit/integration/validation/device subtrees after path updates.
- EVALUATE: Rust infrastructure → optional remote-node versus shared Rust workspace. Do not move until contracts are reviewed.
- ARCHIVE: historical plans and superseded architecture docs only after preserving current HEAD in an archive tag.
- DELETE: confirmed corpus ingestion, tokenization, literature retrieval, generated corpus dashboard and their exclusive workflow/dependencies after structured-data functionality is separated.

## Safety and unresolved constraints
- LICENSE was not changed.
- main is unprotected according to GitHub branch metadata.
- Remote GitHub inspection cannot establish local git status, stash, or unpushed work.
- Available GitHub connector tools do not expose tag creation. The required pre-restructure-archive tag therefore could not be created. Destructive removals are deferred rather than destroying the only reachable copy.
- No branch was created; work is being staged directly on main.
- Android, device execution, 16 KB page alignment, Play-policy compliance, APK/AAB size, memory and cold-start have not been verified.
