# Kinetics: 10-Step Completion Programme

**Status:** Active programme. Step 1 is in progress; no step is complete merely because it is planned or has a prototype.
**Governing direction:** `VISION.md`, `RESEARCH_BLUEPRINT.md`, `ROADMAP.md`, `ARCHITECTURE.md`, `ENGINEERING_STACK.md`, and `CLINICAL_TRANSLATION.md`.

## Definition of completion

A step is complete only when its acceptance criteria are met, changes are merged to the default branch, automated checks pass, documentation is current, and evidence is recorded. A design document, stub, open pull request, or passing unit tests alone do not constitute completion.

Every scientific result must be traceable to versioned inputs, code, configuration, model artifacts, and evaluation procedures. Research outputs are not clinical claims. Clinical or translational use requires separate validation, governance, and regulatory review.

## Programme-wide rules

1. Preserve existing working functionality; migrate incrementally with compatibility tests rather than broad rewrites.
2. Keep Kinetics Ecosystem independent; integrate through documented, versioned interfaces.
3. Use Python for scientific/data/model workflows, C++ for justified native visualization or performance-sensitive computation, and Rust for secure services and systems boundaries.
4. Deliver small reviewable changes with tests, docs, migration notes, and rollback considerations.
5. Never silently infer missing identifiers, assay conditions, units, licenses, or provenance.
6. Prevent leakage across protein, chemical scaffold, assay, source, and time boundaries as appropriate to each research question.
7. Record external model, tokenizer, dataset, and tool versions; feature-cache keys include all relevant representation settings.
8. Make no performance, reproducibility, security, or clinical-readiness claim without evidence.

## Step 1 — Core foundation and infrastructure (IN PROGRESS)

**Purpose:** Make the current repository dependable to install, test, operate, and extend.

**Work:** Reconcile legacy paired-target workflows with canonical one-observation-per-row records; define package/module boundaries and stable interfaces; typed configuration, structured logging, and actionable errors; database schema and migration strategy; CI across supported Python versions; lint/type checks; dependency and environment policy; security review of file handling, serialization, subprocesses, secrets, and artifact integrity; architecture decision records.

**Acceptance:** Clean installation on supported environments; full CI and static checks pass; migrations work from clean and previous supported schemas; public interfaces/configuration are documented; legacy paths have compatibility tests or a migration/deprecation path; dependency and security boundaries are documented.

**Evidence:** CI runs, migration tests, installation guide, architecture decisions, dependency inventory, security checklist.

## Step 2 — Kinetics-KDB: scientific data foundation

**Purpose:** Establish an auditable, versioned source of enzyme kinetic observations.

**Work:** Canonical Km/kcat records; units and original values; enzyme/protein and substrate identities; organism and assay context; source record, citation, license, and provenance; source-specific public dataset adapters with explicit mappings; unit validation; row-level rejection audit; duplicate and conflict review; sequence/chemical identity normalization; immutable dataset releases with manifests and checksums.

**Acceptance:** Every accepted observation traces to a source record and version; rejected rows have machine-readable reasons; conversions are dimensionally tested and raw values retained; dataset releases can be verified from documented snapshots; licensing is visible before export; conflicting observations are never silently overwritten or averaged.

**Evidence:** Adapter tests, source manifests, curation reports, checksum verification, data cards, release procedure.

## Step 3 — Protein and chemical representation

**Purpose:** Produce reproducible validated representations of enzymes and substrates.

**Work:** Sequence validation and clustering; versioned ESM-family embeddings with pinned model/tokenizer revisions and inference settings; chemical parsing, sanitization, stereochemistry policy, canonicalization, fingerprints and molecular graphs; feature archive schema and provenance; deterministic cache keys; bounded batch processing and invalid-input handling.

**Acceptance:** Every feature artifact records source IDs, representation code, model revision, parameters, and environment; repeat runs meet documented determinism tolerances; invalid inputs are auditable; transforms do not leak across partitions; cache invalidation follows all relevant dependency changes.

**Evidence:** Feature schema, model cards, cache tests, edge-case tests, reproducibility report.

## Step 4 — Kinetics-Multi prediction engine

**Purpose:** Build the multimodal enzyme–substrate prediction system described in the research blueprint.

**Work:** Establish leakage-aware baselines; protein and molecular encoders; interaction/fusion architecture; assay-context conditioning; distinct Km and kcat target handling; reproducible training configuration and checkpoints; experiment manifests; inference validation, batch prediction, and model packaging.

**Acceptance:** End-to-end training and inference run from a versioned dataset; artifacts identify code revision, dataset release, feature configuration, dependencies, target, and training settings; baseline and advanced models use identical declared splits; incompatible metadata and malformed inputs are rejected; no superiority claim without held-out and external evidence.

**Evidence:** Training recipes, model artifacts, model cards, inference tests, experiment manifests.

## Step 5 — Scientific validation and benchmarking

**Purpose:** Test generalization beyond familiar proteins, chemicals, and assay settings.

**Work:** Predeclare benchmark tasks and splits; protein-cold, scaffold-cold, double-cold evaluation; external source/organism/assay/time evaluations where supported; target-appropriate metrics and confidence intervals; subgroup and applicability-domain reports; uncertainty calibration and coverage tests; ablations; overlap/contamination checks; failed-experiment records.

**Acceptance:** Frozen split assignments and dataset versions; test sets never used for selection; versioned evaluation code; uncertainty claims supported by empirical coverage evidence; reports disclose sample sizes, missingness, subgroup limitations, and confidence intervals; independent reproduction of reports.

**Evidence:** Benchmark cards, split manifests, evaluation reports, ablations, reproduction run.

## Step 6 — Native molecular visualization and simulation

**Purpose:** Deliver scientifically faithful structural inspection and native performance where justified.

**Work:** Define C++ engine scope/build/platform support and Python/Rust interoperability; validated structure loading with provenance; rendering, selection, highlighting, interaction overlays; reference-tested measurements; explicit simulation adapters; record software, force fields, parameters, seeds, and structures; profile before optimizing.

**Acceptance:** Reproducible builds and native tests on declared platforms; reference structures preserve atom/bond identity and coordinate handling; interoperability preserves required metadata; simulation workflows are fully parameterized and traceable; performance claims include reproducible workloads and hardware.

**Evidence:** Build matrix, reference fixtures, interoperability tests, benchmarks, API docs.

## Step 7 — Rust infrastructure and security

**Purpose:** Provide dependable service and systems boundaries without coupling scientific code to infrastructure internals.

**Work:** Versioned API contracts; authentication and least-privilege authorization; secret management; job orchestration with limits, cancellation, retries, idempotency; secure artifact upload/download; audit events and observability; backup/restore; threat modeling for data access, external tools, and user isolation.

**Acceptance:** Contract tests; negative tests for unauthorized and cross-user access; no secrets in source/logs; explicit job lifecycle and resource limits; tested recovery and artifact integrity; critical security findings resolved or formally risk-accepted.

**Evidence:** Threat model, API specifications, integration tests, audit samples, recovery drill, security review.

## Step 8 — Kinetics research workbench

**Purpose:** Enable complete research workflows through one coherent interface.

**Work:** Researcher workflows and accessibility requirements; dataset discovery and curation; experiment setup, training, inference, reports, provenance and uncertainty display; project/workspace management; job monitoring and artifact browsing; UI separated from scientific computation through stable APIs; usability testing and installation/update procedures.

**Acceptance:** A researcher completes a documented workflow without manual script stitching; every result links to inputs, dataset, model, and manifest; errors/job states are visible and recoverable; primary workflows pass user acceptance tests; accessibility and operations documentation exist.

**Evidence:** Workflow tests, usability findings, user guide, release candidate.

## Step 9 — Multidisciplinary scientific expansion

**Purpose:** Expand beyond enzyme kinetics without weakening scientific quality.

**Work:** Add genomics, proteomics, multi-omics, biological networks, chemical discovery, and simulation only when each has a defined question, data model, source/license strategy, and validation plan; reuse shared provenance/workflow infrastructure while preserving domain-specific semantics; define identifier mapping and uncertainty propagation.

**Acceptance:** Every domain has reviewed specifications, data contracts, source/license inventory, tests, and benchmarks; cross-domain mappings preserve source identity and mapping confidence; modules are independently testable/releasable where practical; claims do not exceed validation.

**Evidence:** Domain specifications, adapters, tests, validation reports, release notes.

## Step 10 — Integration, release, and operational readiness

**Purpose:** Deliver a maintainable platform with a controlled release process.

**Work:** End-to-end, compatibility, load, security, and recovery testing; packaging, versioned artifacts, install/upgrade/rollback; deployment and hardware documentation; backup/restore and disaster recovery; vulnerability response and release policy; scientific/software review; Android companion only against stable APIs and real workflows.

**Acceptance:** Clean installation and upgrade demonstrated; full source-to-report workflow passes; security/performance/recovery gates signed off; release artifacts, dependency inventory, docs, and limitations published; no unresolved critical security or data-integrity issues; research and clinical claims accurately bounded.

**Evidence:** Release checklist, test reports, deployment guide, recovery evidence, sign-offs, release notes.

## Cross-step release gates

Every step must pass all applicable gates:

- **Scientific integrity:** units, identities, split design, provenance, uncertainty, and limitations are correct.
- **Software quality:** automated tests, static checks, documented interfaces, and supported-environment verification pass.
- **Data governance:** source terms, licenses, privacy, retention, and export restrictions are respected.
- **Reproducibility:** inputs, code revision, configuration, environment, and outputs are recorded.
- **Operations:** errors, logs, resource limits, recovery, and rollback are suitable for the component.
- **Review:** changes are reviewed and merged; draft PRs and prototypes are not completion.

## Current execution baseline

The initial foundation fixes were merged through PR #1. SQLite schema versioning, transactional/idempotent initialization, forward-version protection, and safer backups were merged through PR #3. The explicit legacy paired-row to canonical-observation adapter and scoped Ruff CI check were merged through PR #4. PR #5 verifies preservation of records in a pre-versioned database. PR #6 adds a provenance-aware legacy import CLI; PR #7 preserves opaque source IDs; PR #8 hardens generated-path protection; PR #9 corrects regression assertions exposed by the expanded tests.

The latest verification run [#42172305487](https://github.com/AssayFlux/Kinetics/actions/runs/42172305487) passed on Python 3.10, 3.11, and 3.12: 34 tests passed on each version, source compilation passed, and scoped Ruff checks passed. This is meaningful but partial Step 1 progress, not completion of Step 1 or of the platform.

**Next Step 1 work:** establish and test the supported package/CLI compatibility contract; add a full fixture from legacy import through canonical audit and persistence; then broaden static checks carefully. Do not force canonical independent target observations back into the legacy paired-target trainer, as that would reintroduce scientifically unsafe pairing. No later step is complete based on plans or stubs alone.
