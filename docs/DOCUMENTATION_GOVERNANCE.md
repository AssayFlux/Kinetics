# Documentation and repository consistency audit

> Review date: 2026-11-07. Scope: recursive tracked-file inventory of the 200-file base branch (203 tracked files after this documentation change), root plans, subsystem documentation, directory layout, key implementation/status documents, UI asset notes, and selected source/test cross-checks. This is a repository inspection, not a full local execution of every test or every scientific workflow.

## Source-of-truth hierarchy

1. `KINETICS_MISSION.md` — purpose, principles and non-negotiable boundaries.
2. `VISION.md` — long-term product/scientific ambition.
3. `ROADMAP.md` — 15 long-term programmes and dependency order.
4. `ARCHITECTURE.md` and `ENGINEERING_STACK.md` — system and technology boundaries.
5. `docs/KINETICS_10_STEP_COMPLETION_PROGRAMME.md` — active engineering sequence and acceptance criteria.
6. `docs/IMPLEMENTATION_STATUS.md` — current implementation snapshot.
7. Subsystem specifications — detailed contracts and acceptance tests.
8. `docs/IMPLEMENTATION_HISTORY.md` — historical record only; not a current status authority.

The 100-domain catalogue is a scope register, not an implementation checklist. The 10-step programme is the current engineering sequence; the 15-programme roadmap is the long-range plan. Neither replaces the mission.

## Findings and actions taken in this change

| Finding | Why it mattered | Action |
|---|---|---|
| The root `project_structure.md` described only knowledge ingestion, not the repository | Filename and scope were misleading | Moved the subsystem guide to `docs/KNOWLEDGE_INGESTION_STRUCTURE.md`; added `docs/REPOSITORY_STRUCTURE.md`; removed the misleading root file |
| `IMPLEMENTATION_STATUS.md` repeated Step 6 headings and contained superseded status statements | Readers could not tell which implementation state was current | Preserved the previous detailed register as `IMPLEMENTATION_HISTORY.md`; replaced current status with a dated, capability-by-capability snapshot |
| Roadmap's immediate checklist instructed maintainers to replace the already-established vision and roadmap | Stale instruction contradicted the existing authoritative documents | Replaced it with near-term work aligned to current Step 1–10 blockers |
| Roadmap and contribution notes referenced an unrelated legacy external project by name | Distracted from the actual separate Kinetics Ecosystem boundary | Reworded as a general external-project/API boundary |
| Asset policy said generated GIF/animation assets were not maintained, while the README and asset test require the tracked GIF | Documentation, tests and README disagreed | Clarified the GIF as a legacy presentation asset and the HTML/CSS layouts as prototypes |
| Documentation index omitted the knowledge-ingestion guide and structure maps, and mislabeled the asset policy | Index was incomplete and some descriptions were inaccurate | Rebuilt the index around the authority hierarchy and current files |
| Step 9 documentation described PDB/mmCIF support inconsistently across Python and native C++ components | It could imply mmCIF support in the C++ parser or incorrectly imply no Python mmCIF adapter | Explicitly separate the native C++ PDB parser from Python PDB/mmCIF adapters and the Biopython workbench |
| README documentation links did not expose the full plan/status hierarchy | New contributors could miss the authoritative plan and active completion programme | Updated README links now surface the mission, roadmap, architecture, active completion programme, current status and documentation index |

## Verified implementation boundaries used in the status register

- The repository contains Python scientific modules, data/identity/feature/modeling/validation code, a local workbench, knowledge ingestion, C++ native structure code, Rust infrastructure and AWS Terraform candidates.
- The native C++ molecular parser is PDB-oriented; its XY PPM renderer is a diagnostic projection, not a full interactive 3D renderer.
- Python contains separate PDB and mmCIF coordinate adapters with fixture tests; this does not mean that the C++ parser supports mmCIF.
- The workbench is local-first and loopback-only; it is not a deployed multi-user service.
- Rust/AWS infrastructure is a candidate implementation, not a live production deployment. The worker currently registers only a no-op health-check task.
- The knowledge pipeline is a resumable, source/license-aware full-text acquisition and retrieval foundation. It is not a complete knowledge graph or 10,000+ acquired corpus.
- The CatPred real-data release and actual pinned ESM-2/MMseqs2 execution are not recorded as completed; scientific model validation remains open.
- Responsive HTML/CSS shells are prototypes, not native desktop applications or an Android APK.
- Release-gate software does not provide human release sign-off or clinical authorization.

## Remaining review work

The changes in this branch establish the documentation hierarchy and resolve the identified high-impact contradictions. They do not claim that every one of the 200 tracked files has been line-edited. The following require a separate, evidence-led pass rather than speculative mass edits:

1. Run all repository CI jobs on the final branch commit and resolve any failures.
2. Validate every relative Markdown link and every documented CLI command against the actual source tree.
3. Reconcile the detailed 10-step programme against the new status snapshot, including all dated CI references and any newly merged PRs.
4. Review the full 100-domain catalogue and source registry for duplicate scopes, source terms, stale endpoints and unsupported redistribution assumptions.
5. Review every workflow for permissions, schedules, secrets exposure, release publication and actual recent run evidence.
6. Review the entire source/test tree for dead modules, duplicated APIs, unreferenced assets and unused dependencies before deleting anything.
7. Review privacy, retention, consent and threat-model documents before any personal genomic or clinical data is accepted.
8. Reassess each subsystem's acceptance state after real-data and independent scientific validation.

## Deletion policy

No scientific source, schema, test, fixture, data adapter, historical plan or asset should be deleted merely because it is not currently used by the README. Delete only when references, import paths, workflows, package metadata, tests, historical evidence and user-facing documentation have been checked. Prefer deprecation and a migration window for public interfaces.

## Change boundary

This audit changes documentation organization, wording and a source-code comment only. It does not remove scientific modules, datasets, model code, workflows, assets or historical implementation evidence.
