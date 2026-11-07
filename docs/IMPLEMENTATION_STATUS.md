# Implementation status

> **Snapshot date:** 2026-11-07. This is the current repository status register. Detailed dated implementation notes are preserved in [IMPLEMENTATION_HISTORY.md](IMPLEMENTATION_HISTORY.md). The mission and roadmap describe intended scope, not implemented capability.

## How to read this register

- **Present in repository** means source, schema, documentation or configuration exists on the inspected branch.
- **CI-verified** means a named workflow run passed for a specific commit; it does not imply scientific validation.
- **Real-data validated** requires a reviewed, licensed real dataset and a reproducible scientific evaluation.
- **Production deployed** requires a live environment and operational evidence.
- **Clinically validated** requires a defined intended use, appropriate ethics and clinical evidence, qualified oversight and applicable authorization.

A design, fixture, passing unit test, workflow configuration or deployment candidate must never be described as a completed scientific or operational capability.

## Current platform snapshot

| Workstream | Present foundation | Current limitation / next evidence |
|---|---|---|
| Core Python research package | Scientific curation, identity, feature, modeling, validation, reporting, persistence and CLI modules | Complete compatibility, migration, security and end-to-end acceptance |
| Kinetics-KDB | Canonical one-target-per-row records, provenance, SQLite persistence, curation and release tooling | No reviewed immutable CatPred real-data release is recorded; gated access and upstream unit caveats remain |
| Protein/chemical representations | ESM-2 configuration, feature caching, Morgan fingerprints, graph descriptors, MMseqs2 wrapper and split utilities | Pinned ESM-2 checkpoint and MMseqs2 have not been executed on a reviewed real dataset |
| Kinetics-Multi | Feature-fusion MLP training/inference software and provenance-aware artifacts | Not a message-passing GNN; no real-data scientific validation or external generalization evidence |
| Scientific validation | Leakage-aware protocols, row/cluster bootstrap reporting, uncertainty and applicability utilities | Real benchmark, calibration evidence, external validation and independent reproduction remain open |
| Structural biology | Versioned protein/structure/mapping/feature contracts; Python PDB and mmCIF coordinate adapters; evidence-linked C-alpha distance utility; Biopython workbench analyses | Fixture tests are not biological validation; broader source adapters, mapping review, independent reference checks and real-data benchmarks remain |
| Native C++ molecular engine | C++17 PDB parser, scene contract, explicit CONECT bonds, CPU XY preview and Python bridge | Native parser is PDB-only; preview is not an interactive 3D renderer; no executed MD adapters or performance claims |
| Research workbench | Local-first FastAPI/browser workbench, bounded workflows, project/job/artifact handling and report generation | Loopback/single-user only; researcher/accessibility UAT, real-data workflow and install/upgrade/recovery acceptance remain |
| Rust infrastructure | Auth/job/artifact/audit foundations, PostgreSQL and AWS adapters, Terraform candidate and recovery scripts | Not deployed; worker has only the no-op health-check handler; per-job sandboxing, live tenant/security tests and restore drills remain |
| Knowledge ingestion | Resumable license-aware acquisition, extraction, tokenization, SQLite FTS5 indexing, source-linked retrieval API/CLI and scheduled workflow | The 10,000-book + 10,000-paper minimum is a plan, not achieved; no verified corpus at that scale is recorded. No complete knowledge graph or clinical knowledge system is implied |
| Desktop/mobile UI | Four responsive HTML/CSS shell layouts for Windows, macOS, Linux and Android; local workbench UI | These are web layout prototypes, not native desktop installers or an Android APK |
| Release readiness | Executable release-gate evaluator and documented evidence requirements | No production release or human sign-off; SBOM, security/recovery/UAT evidence and signed reviews remain outstanding |
| Precision-health research | Mission, architecture, governance and clinical-translation requirements documented | Long-term research programme only; no autonomous diagnosis, prescribing or treatment recommendation capability |

## Important implementation distinctions

### Structural parsers are separate components

- The **native C++ scene parser** currently reads PDB and emits a diagnostic XY projection.
- The **Python structural adapters** include provenance-checked PDB and mmCIF coordinate parsing.
- The **Biopython workbench** has separate PDB/mmCIF analysis and browser-viewer workflows.
- These capabilities do not imply a GPU renderer, full structural biology suite, molecular dynamics execution or biological validation.

### Research software versus scientific evidence

The CatPred adapter and feature/model software are present, but no reviewed real-data model result is claimed. The Hugging Face access gate must be accepted by an authorized researcher. The upstream kcat unit-conversion caveat must be resolved against source-level records before absolute kcat values are treated as independently validated.

### Knowledge retrieval versus knowledge integration

The current corpus pipeline creates a local full-text index and source-grounded retrieval results. It is not yet a normalized cross-domain knowledge graph linking genes, variants, proteins, compounds, pathways, diseases, assays, cohorts and clinical evidence.

### Local workbench versus production service

The Python workbench is intentionally loopback-only and single-user. The Rust/AWS infrastructure is a deployment candidate, not a live production service. The worker's registered task handler is currently a no-op health check; scientific job execution and enforced per-job isolation remain open.

## Immediate execution priorities

1. Close Step 1 package, API, dependency, security and migration acceptance.
2. Obtain and review an authorized, licensed real Kinetics-KDB snapshot; audit source semantics and release it immutably.
3. Execute pinned ESM-2 and MMseqs2 on that reviewed dataset and retain repeatability/resource evidence.
4. Run the predeclared matched model and cold-start evaluation protocol; obtain independent review.
5. Complete the structural adapters' reference checks and real-data validation without conflating Python and native C++ capabilities.
6. Complete researcher, accessibility, desktop installation/upgrade and workbench recovery acceptance.
7. Keep production deployment blocked until scientific workers, per-job sandboxing, tenant isolation, security review and restore drills pass.
8. Continue multidisciplinary expansion through explicit domain contracts, source/license review and validation gates.
9. Build polished desktop and Android applications only against stable scientific APIs and measured device requirements.
10. Keep clinical translation a separate, evidence-gated programme.

## Governing documents

- [Scientific capability map](SCIENTIFIC_CAPABILITY_MAP.md)

- [Foundational mission](../KINETICS_MISSION.md)
- [Vision](../VISION.md)
- [Master roadmap](../ROADMAP.md)
- [System architecture](../ARCHITECTURE.md)
- [Engineering stack](../ENGINEERING_STACK.md)
- [10-step completion programme](KINETICS_10_STEP_COMPLETION_PROGRAMME.md)
- [Clinical translation boundary](../CLINICAL_TRANSLATION.md)
- [Documentation index](DOCUMENTATION_INDEX.md)
- [Implementation history](IMPLEMENTATION_HISTORY.md)

## Status integrity

This register is a repository review snapshot, not a live CI dashboard. Recheck the exact commit and workflow run before citing CI status. Update this file only when the relevant code, test output, real-data evidence, deployment evidence or independent review can be linked. Never promote a capability's status based solely on a plan or prototype.
