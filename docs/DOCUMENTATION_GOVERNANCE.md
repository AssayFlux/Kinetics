# Documentation and repository governance audit

**Audit date:** 2026-11-07  
**Branch:** `cleanup/documentation-consolidation-2026-11`  
**Scope:** recursive tracked-tree inventory; all Markdown documents; source-of-truth hierarchy; duplicate-document review; link/reference checks for retired documents; and selective source, test, workflow, asset and package-metadata cross-checks.

## Single source-of-truth hierarchy

1. `KINETICS_MISSION.md` — purpose, principles, boundaries and decision filter.
2. `VISION.md` — long-term scientific and product ambition.
3. `ROADMAP.md` — long-range programmes, dependencies and gates.
4. `docs/SCIENTIFIC_CAPABILITY_MAP.md` — functional capability catalogue, maturity labels and dependency-aware scientific build sequence.
5. `ARCHITECTURE.md` and `ENGINEERING_STACK.md` — system boundaries and technology ownership.
6. `docs/KINETICS_10_STEP_COMPLETION_PROGRAMME.md` — active engineering completion sequence.
7. `docs/IMPLEMENTATION_STATUS.md` — current repository evidence snapshot and blockers.
8. Subsystem specifications — detailed data, scientific, security, workflow and acceptance contracts.
9. `docs/IMPLEMENTATION_HISTORY.md` — historical audit trail only; never use it as current status authority.

The 160-domain register is an acquisition/source-discovery taxonomy (100 foundational domains plus 60 extensions). It is not the functional capability map and is not an implementation checklist. The 15-programme roadmap is long-range direction; the 10-step programme is the active engineering sequence. The 10,000-book plus 10,000-paper target is a minimum archive milestone, not a current-holdings claim.

## Consolidation decisions

| Retired document | Information retained in |
|---|---|
| `docs/STEP6_IMPLEMENTATION_STATUS.md` | Current summary in `docs/IMPLEMENTATION_STATUS.md`; technical contract and limitations in `docs/NATIVE_MOLECULAR_ENGINE.md`; step acceptance in the 10-step programme |
| `docs/SCIENTIFIC_ARCHITECTURE.md` | Kinetic observation semantics in `docs/DATA_MODEL.md`; model/evaluation details in `RESEARCH_BLUEPRINT.md`, `docs/MODELING_AND_UNCERTAINTY.md` and `docs/STEP5_VALIDATION_PROTOCOL.md` |
| `docs/RESEARCH_PAPER_OUTLINE.md` | Manuscript structure, figures and tables in Section 8 of `RESEARCH_BLUEPRINT.md` |

No scientific source code, schema, test, fixture, workflow, data adapter, brand asset or UI prototype was removed. The reviewed non-document files have identifiable roles or lack sufficient evidence to classify them as dead. In particular, the four platform HTML/CSS layouts and original brand assets are retained.

## Repository inventory

The base tree inspected for this cleanup contained 213 tracked files, including 54 Markdown documents. The verified cleanup branch contains **211 tracked files and 52 Markdown documents**: one new capability map and three retired duplicate documents. The recursive Git tree contains 248 entries including directories.

## Verified direction and implementation boundaries

- Kinetics is a cross-disciplinary biomedical/scientific research platform, not only an enzyme-kinetics predictor.
- Scientific scope is organized into 18 functional capability areas in the capability map; the 160-domain taxonomy guides acquisition discovery.
- The first archive scale milestone is at least 10,000 books and 10,000 research papers. Counts must be manifest-backed and separated by resource type and processing stage.
- The knowledge pipeline is an acquisition/extraction/tokenization/SQLite FTS retrieval foundation, not a completed 20,000-resource corpus or a complete knowledge graph.
- Kinetic model and feature code, sequence/chemistry utilities, selected Python PDB/mmCIF adapters, Biopython analyses and a local workbench exist; real-data scientific validation remains open.
- The native C++ molecular parser is PDB-only and its XY preview is not a full interactive 3D renderer.
- Rust/AWS infrastructure is a deployment candidate, not a verified live production service; the worker's scientific task execution and per-job isolation remain acceptance blockers.
- The four platform HTML/CSS shells are responsive layout prototypes, not native desktop applications or an Android APK.
- Research, production and clinical status must be reported separately; a plan, fixture test or CI pass cannot substitute for scientific or clinical validation.

## Verification completed in this cleanup

- Inventoried the recursive tracked tree and all 54 Markdown files present at the start of this cleanup.
- Reviewed the project mission, vision, roadmap, research blueprint, active completion programme, current status, documentation index, subsystem specifications, UI documentation and historical notes.
- Checked GitHub code-search references for the three retired document names before deletion; references in the index and active Step 6 programme were updated or confirmed absent.
- Kept the 100+60 taxonomy filename stable to avoid breaking existing links; corrected its title and purpose so the 160-domain scope is unambiguous.
- Updated the README, vision, mission, roadmap and active completion programme so the capability map and 10k+10k archive milestone are part of the project direction.

This was a remote repository/documentation audit. It does not claim that every source file was line-by-line reviewed, that all CI jobs were executed locally, or that every scientific workflow was run.

## Maintenance rules

1. Keep one authority for each concern; do not create another competing roadmap, status register or capability catalogue.
2. Add a capability only with a defined research question, domain contract, authoritative source/license review, validation plan, compute budget and acceptance criteria.
3. Update `IMPLEMENTATION_STATUS.md` only when code and relevant test/evidence links support the change.
4. Keep historical records only when they preserve useful decisions or evidence; label them historical and never let them override current status.
5. Delete a file only after checking references, imports, package metadata, workflows, tests, assets and historical evidence. If uncertain, retain and document the reason.
6. Do not repeat generic mission paragraphs in every technical document; link to the authoritative mission instead.
7. Update the documentation index and repository map whenever maintained documents or major directory ownership changes.
8. Distinguish intended scope, implemented software, fixture/CI evidence, real-data execution, independent scientific validation, production deployment and clinical authorization.
