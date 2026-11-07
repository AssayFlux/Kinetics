# Kinetics repository audit

**Audit date:** 2026-11-07  
**Repository:** https://github.com/AssayFlux/Kinetics  
**Audited ref:** `main` at `6a66bfc6044e0f066c35512fc9b90bf24bc3d34c`  
**Scope:** GitHub-tracked remote tree. This is not a local working-tree audit.

## Executive summary

Kinetics is currently a mixed scientific Python/workbench, Rust infrastructure, C++ molecular-structure and corpus-ingestion repository. It is not yet the Android-first Kotlin/Compose application described by the supplied master plan. The intended direction is a scientific toolbox: tools, computational engines, curated data packs and a protected domain catalogue. Bulk books, papers, scraped text and literature corpora are out of scope.

No files have been deleted or moved in this audit. The 160-domain catalogue and existing scientific source are protected. The LICENSE has not been modified.

## Repository inventory

The previously inspected tracked tree contains 211 files in 37 directories. Approximate top-level tracked sizes:

| Area | Files | Approx. size | Initial classification |
|---|---:|---:|---|
| .github | 5 | 15 KB | KEEP/MIGRATE workflows after trigger review |
| root | 16 | 129 KB | KEEP selectively; consolidate plans |
| Assets | 9 | 4.81 MB | KEEP brand/UI assets; inspect large assets |
| data | 2 | <1 KB | KEEP manifests/placeholders |
| database | 8 | 72 KB | KEEP domain catalogue; migrate data-pack metadata |
| deploy | 3 | 18 KB | REVIEW; remote-node relevance |
| docs | 42 | 335 KB | MIGRATE essential architecture; ARCHIVE historical plans |
| models | 1 | placeholder | REVIEW |
| native | 8 | 23 KB | KEEP/MIGRATE C++ |
| rust | 21 | 83 KB | KEEP/MIGRATE Rust infrastructure |
| scripts | 16 | 133 KB | KEEP useful tooling; corpus scripts DELETE candidates |
| src | 52 | 442 KB | KEEP/MIGRATE Python scientific code |
| tests | 28 | 121 KB | KEEP/MIGRATE tests |

Tracked files over 1 MB:
- `Assets/Kinetics.gif`: approximately 2.72 MB; review whether still required.
- `Assets/Brand Logo.svg`: approximately 2.07 MB; preserve the original brand asset; optimize only without changing identity and with owner approval.

No tracked PDF, EPUB, DOC, DOCX, PPTX or RTF corpus was found. This does not establish whether ignored, untracked or locally stored corpora exist. The repository ignore rules exclude some local corpus/data paths.

## Domain catalogue

The catalogue is represented in:
- `docs/SCIENCE_DOMAIN_CATALOGUE_100.md`: 100 foundational domains.
- `database/domains/extended_domains.json`: 60 extension domains.
- `database/domains/extended_domain_scopes.json`: scope descriptions for the 60 extensions.
- `database/domains/domain_synonyms.json`: aliases for a subset.

**Catalogue count: 160 (100 + 60).** The extension set includes computing, engineering, physical sciences, Earth systems, education and technical communication, so the full set should not be described as 160 exclusively biological domains without an owner-approved scope decision. Earlier normalization checks found 160 unique canonical names and no exact duplicate names. Near-duplicate and coverage mapping still require a deterministic semantic review. There are not yet 160 individual `domains/<id>.yaml` records.

All 160 entries are protected KEEP/MIGRATE. Convert them to small YAML records only after stable IDs, categories and mapping rules are established. Do not drop any domain.

## Scientific implementation

Existing Python work includes sequence/Biopython-related functionality, protein records and properties, PDB/mmCIF adapters, chemistry/SMILES handling, proteomics, curation, provenance, validation, metrics, uncertainty, quality checks, SQLite persistence and a browser workbench.

Rust currently contains the `rust/kinetics-infra` infrastructure project (jobs/artifacts/authentication); it is not yet the planned `kinetics_core` scientific compute + FFI workspace. Existing worker functionality is documented as incomplete/no-op in implementation-status material.

C++ under `native/` includes a small PDB parser and molecular-scene data/fixtures/tests.

Enzyme kinetics: existing code includes Km/kcat prediction, curation or modelling foundations. The audit did not verify working experimental rate-curve fitting for Michaelis–Menten, Lineweaver–Burk, Eadie–Hofstee, Hanes–Woolf, nonlinear regression or the four inhibition models. These are Phase 3 implementation/validation requirements, not claims about current functionality. Preserve the existing foundation.

## Android gap

There is an Android-oriented static HTML prototype at `Assets/kinetics-android.html`, but no native Android Gradle/Kotlin/Jetpack Compose application or Android manifest was found in the tracked tree. No Chaquopy configuration, Rust Android FFI bridge, or NDK/CMake JNI application integration was found. Android feasibility remains untested.

## Corpus and literature infrastructure

The following tracked components conflict with the no-literature-archive mission and are DELETE candidates, subject to final path-by-path review before execution:
- `.github/workflows/bulk_downloader.yml`
- `scripts/fetch_corpus.py`
- `scripts/fetch_research_data.py`
- `scripts/fetch_specialist_sources.py`
- `scripts/tokenize_corpus.py`
- `scripts/analyze_corpus.py`
- `scripts/restore_corpus_releases.py`
- `scripts/update_corpus_dashboard.py`
- `scripts/query_knowledge.py`
- literature-oriented portions of `src/kinetics_core/knowledge/`
- associated corpus-specific tests and long-form acquisition/indexing documentation.

Do not remove useful scientific data-pack manifests, domain definitions, reference datasets, provenance, parsers or source-license metadata merely because they relate to data. Review `.github/workflows/acquire-starter-data.yml` and its sources individually: curated scientific reference packs may be retained if license-checked and not bulk literature.

No 10,000-document corpus is present in the tracked Git tree inspected. Local or ignored files remain unknown.

## Proposed classification and migration

| Existing path/area | Proposal | Destination/reason |
|---|---|---|
| `src/kinetics_core/` scientific modules | KEEP/MIGRATE | `python/kinetics/`; preserve tests and provenance |
| `native/` | KEEP/MIGRATE | `cpp/`; retain C++ parser/scene work |
| `rust/kinetics-infra/` | KEEP pending decision | Review remote-node/job-service fit; do not discard |
| `database/domains/*` | KEEP/MIGRATE | `domains/*.yaml` plus generated registry |
| `docs/SCIENCE_DOMAIN_CATALOGUE_100.md` | KEEP/MIGRATE | Extract structured records; preserve source until approved |
| `Assets/Brand Logo.svg` | KEEP | Preserve brand identity |
| `Assets/kinetics-android.html`, layout assets | KEEP as design reference | Use to inform Compose shell, not as native app |
| corpus download/tokenization/search subsystem | DELETE candidates | Outside product mission; remove only after gate |
| duplicate historical roadmaps/long-form plans | ARCHIVE candidates | Preserve only on archive ref after unique requirements extracted |
| `deploy/aws/` | REVIEW/MIGRATE | Determine whether useful for optional remote node |
| `LICENSE` | KEEP unchanged | Owner decision required for any change |

Root documents that overlap include `VISION.md`, `KINETICS_MISSION.md`, `ROADMAP.md`, `RESEARCH_BLUEPRINT.md`, `ENGINEERING_STACK.md` and `ARCHITECTURE.md`. Do not mass-delete them: extract unique requirements into the supplied master plan, then propose archival of redundant history.

## Build and test evidence

A GitHub Actions run associated with the audited main revision previously passed Python 3.10–3.12, Rust, C++, browser acceptance, workbench integration and Terraform validation. This is CI evidence only; it is not a local rebuild and does not verify Android/device execution. The tracked test tree has 28 files. No local tests were run in this remote audit.

SciPy was not found in the declared dependency setup during prior inspection. Root Cargo workspace, maturin/PyO3 setup, Android Gradle project, and planned engines/datapacks/domain YAML registry are absent.

## Security and secrets

Limited public-code pattern searches did not surface an obvious committed credential. This is not a complete secret scan. A full scan requires repository history and the local checkout; never print secret values. Rotate any credential found and review Git history only with explicit authorization.

## Branch audit

At the time of inspection, 12 remote branches existed:
- `cleanup/documentation-consolidation-2026-11`: 0 commits ahead, 1 behind main.
- `design/blank-cross-platform-layouts`: 0 ahead, 259 behind.
- `docs/live-corpus-growth-dashboard`: 0 ahead, 66 behind.
- `docs/reconcile-project-documentation-2026-11`: 0 ahead, 152 behind.
- `expand-open-research-sources-today`: 3 ahead, 78 behind; unique commits modify corpus workflow/research-ingestion files.
- `feat/workbench-platform-shell-ingestion-resilience`: 0 ahead, 54 behind.
- `fix/repair-corpus-sync-and-workflow`: 0 ahead, 63 behind.
- `main`: baseline.
- `rebuild/canonical-documentation-2026-11`: 6 ahead, 0 behind; unique README/docs changes.
- `research-corpus-expansion-biopython`: 3 ahead, 102 behind; unique corpus workflow change.
- `scale-same-day-corpus-ingestion`: 0 ahead, 73 behind.
- `upgrade/knowledge-ingestion-160-domains`: 0 ahead, 116 behind.

Eight branches have no unique commits relative to main and are candidates for deletion after confirming no open PRs or external dependencies. The four branches with unique commits (including the six-commit documentation branch) must be reviewed/preserved before any deletion. The branch tool does not expose deletion in this environment; no branch has been deleted.

## Safety operations and limitations

- The audited main commit is `6a66bfc6044e0f066c35512fc9b90bf24bc3d34c`.
- Remote snapshot branches `backup/pre-restructure` and `restructure/android-v1` were created at that exact commit.
- A local `git status` and uncommitted-work backup commit cannot be performed through GitHub remote access.
- The archive tag `pre-restructure-archive` could not be created with the available GitHub actions.
- No deletion, file move, LICENSE edit, history rewrite or branch deletion was performed.
- No local files, ignored files or untracked work were inspected.

## Approval gate (Part 3.4)

Before Phase 0 restructuring, owner approval is required for:
1. The listed corpus/literature DELETE candidates and the exact path list.
2. Historical-document ARCHIVE candidates.
3. The migration map and handling of Rust infrastructure and AWS deployment.
4. Any deletion that could be considered original user-authored work.
5. Any history rewrite (not currently proposed).
6. Any LICENSE or scientific-claim wording changes.

**Recommended next step:** approve the corpus subsystem removal list and migration map. Keep all 160 domain definitions, scientific source, tests, brand assets and LICENSE. Then execute the approved changes on `restructure/android-v1`, not on `main`, and validate CI before proposing a merge.
