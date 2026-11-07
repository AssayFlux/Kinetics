# Kinetics: 10-Step Completion Programme

> 160-domain acquisition scope register: docs/SCIENCE_DOMAIN_CATALOGUE_100.md. This catalogue defines intended breadth; it is not evidence that every domain is implemented or clinically validated.
> **Mission authority:** This document is governed by [KINETICS_MISSION.md](../KINETICS_MISSION.md). Kinetics is a cross-disciplinary biomedical and precision-health research platform—not only an enzyme-kinetics project. All domains, datasets, models and applications must align with the mission, preserve provenance and clinical safety, and follow the foundation-first build order. Small Android devices are a first-class performance target.

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

## Step 2 — Kinetics-KDB: scientific data foundation (IN PROGRESS)

**Purpose:** Establish an auditable, versioned source of enzyme kinetic observations.

**Implemented engineering foundation:**
- Canonical one-target-per-row Km/kcat observations, original source fields, source-version and license metadata, row-level rejection audits, and SQLite persistence.
- CatPred-DB downloader pins the Hugging Face dataset revision separately from the GitHub processing-code revision; records hashes for random train/validation/test tables and published sequence-cluster test files.
- CatPred adapter uses the target-specific aggregate columns `log10km_mean` for Km and `log10kcat_max` for kcat, converts these log10 aggregates to linear values, and normalizes Km from mM to M.
- The representative `value` and `log10_value` columns are preserved separately; records are explicitly marked `source_aggregated` with geometric-mean or maximum aggregation semantics.
- Source clipping bounds, source-row locators, processing revisions, dataset citation, license declaration, all upstream columns, pH, temperature, EC, taxonomy and accessions are retained in provenance manifests.
- Sequence and stereochemistry-preserving SMILES identity normalization, deterministic internal content IDs, row-level identity rejection, same-source conflict audit and cross-source duplicate candidates.
- Immutable dataset releases combine rejection audits, retain acquisition/curation/identity manifests, emit data cards and quality reports, hash artifacts, propagate source-quality warnings, and support verification.

**Acceptance:** Every accepted observation traces to a source row and immutable source version; rejected rows have machine-readable reasons; target-specific unit conversions are tested and source values retained; duplicate/conflict candidates remain visible; release manifests and all artifacts verify; license and source-quality caveats are visible before export.

**Evidence:** CatPred schema/adapter tests, aggregate target and clipping semantics tests, source revision and unit-warning assertions, identity CLI tests, duplicate-candidate tests, immutable release/checksum tests, and [CI run #42178564530](https://github.com/AssayFlux/Kinetics/actions/runs/42178564530), with 48 tests passing on each of Python 3.10, 3.11, and 3.12 plus compilation and Ruff checks. See `DATASETS.md`, `docs/WORKFLOW.md`, and `docs/IMPLEMENTATION_STATUS.md`.

**Remaining blockers before Step 2 can be declared complete:**
- No real public CatPred snapshot has yet been downloaded, normalized, and released in this repository; current tests use fixtures.
- CatPred is an aggregate benchmark source, not a collection of individual assay measurements. Its public table does not retain per-row original BRENDA/SABIO record IDs, units, DOI, or assay IDs.
- The upstream processing code carries BRENDA values without per-row unit metadata, and its SABIO kcat `min^-1` conversion multiplies by 60, opposite to the standard conversion to `s^-1`. CatPred kcat absolute scale must be audited against original source records before scientific use.
- Direct BRENDA and SABIO adapters require current schema, access, and license review; these are not claimed as implemented.

Do not treat the CatPred aggregate as individually replicated assay data or claim its kcat scale is independently validated. Step 2 remains open until a real, reviewed source snapshot and release pass the acceptance checks.

### Parallel knowledge-archive track under the shared data foundation

The cross-domain archive is a platform-level deliverable alongside the kinetics-specific Kinetics-KDB work; it does not change the one-observation-per-row semantics or acceptance criteria of the kinetic dataset. Its first scale milestone is **at least 10,000 books and 10,000 research papers**. Each object must pass source-rights review, download integrity checks, extraction/normalization and tokenization before it is counted as processed; it is counted as searchable only after a successful index commit with provenance. Track books and papers separately, preserve immutable originals and manifests, deduplicate without deleting source provenance, and keep raw corpora outside ordinary Git blobs. See [Scientific capability map](SCIENTIFIC_CAPABILITY_MAP.md) and [Knowledge ingestion](KNOWLEDGE_INGESTION.md). The target is not a current-holdings claim and is not complete until verified manifests and index counts demonstrate it.

## Step 3 — Protein and chemical representation (IMPLEMENTED; EXECUTION VALIDATION PENDING)

**Purpose:** Produce reproducible validated representations of enzymes and substrates.

**Implemented engineering scope:**
- ESM-2 model and tokenizer pinned to full immutable Hugging Face commit `8c576d2aba1b27317e9321c8491d72f00d1b110a`; evaluation/inference mode, residue-only mean pooling, explicit 1,022-residue default limit, strict residue validation, and no silent truncation.
- Representation card documenting model identity/license, intended use, limitations, source revision, pooling, reproducibility and non-clinical scope (`docs/ESM2_REPRESENTATION_CARD.md`).
- Morgan radius-2, 2,048-bit fingerprints with chirality enabled by default; RDKit canonical isomeric SMILES; explicit no-salt/no-tautomer-normalization policy.
- Bemis-Murcko scaffold IDs that ignore stereochemistry so stereoisomers stay in the same scaffold split; acyclic compounds use a canonical non-isomeric molecular-graph fallback. Invalid SMILES receive row-level rejection reasons.
- Stereochemistry-aware molecular graph arrays: atom atomic number/degree/charge/hydrogen/aromaticity/CIP/hybridization/isotope/mass; bond type/conjugation/ring/stereo; canonical atom ordering; bidirectional edges and packed per-molecule offsets/cardinalities.
- Feature NPZ schema 2.0 containing ESM+Morgan vectors, graph tensors, target values, source/record identifiers, original and canonical SMILES, normalized sequences and requested grouping arrays. All string arrays use non-object Unicode dtypes and load with `allow_pickle=False`.
- Atomic cache files and deterministic cache keys incorporating model/tokenizer revisions, feature schema, fingerprint/graph settings, runtime dependency versions, device policy, normalized sequence and canonical isomeric SMILES.
- Adjacent JSON feature manifests with row/source hashes, source input file hash, source versions/licenses, model/tokenizer settings, runtime/software versions and archive SHA-256.
- MMseqs2 clustering validates sequences and source/record keys, collapses repeated target observations only when the same source record has the same normalized sequence, rejects conflicting sequence identities, verifies every unique protein entity is assigned exactly once, and records tool version, parameters, FASTA/cluster-output/mapping hashes.
- CLI workflow: `normalize-identities` → `annotate-scaffolds` → `cluster-sequences` (writes `protein_cluster_id` back to observations) → double-cold `partition` → per-partition `build-features`. Source/record IDs remain text through partitioning.

**Acceptance evidence achieved:** Fixture-driven tests cover immutable revision validation, cache reuse/invalidation, chirality policy, graph tensor packing and row alignment, non-pickle archive safety, scaffold rejection audits, source-qualified MMseqs mappings, repeated Km/kcat source rows, incomplete cluster rejection, CLI workflows and provenance hashes. GitHub Actions run [#42182250301](https://github.com/AssayFlux/Kinetics/actions/runs/42182250301) passed: 61 tests on each of Python 3.10, 3.11 and 3.12; compilation and scoped Ruff checks passed. See `docs/WORKFLOW.md` and `docs/IMPLEMENTATION_STATUS.md`.

**Still required before Step 3 can be scientifically closed:**
- The pinned ESM-2 checkpoint has not yet been downloaded or executed; automated tests use a deterministic fixture encoder.
- MMseqs2 has not yet been run on a real reviewed dataset; automated tests use a fake executable to exercise mapping and failure handling.
- No real dataset feature archive has been built. Step 2's real CatPred snapshot/release is still pending.
- Numerical repeat-run tolerances have not been measured on a pinned CPU/GPU environment. The manifest explicitly does not promise bitwise identity across hardware/library builds.
- No graph neural network is claimed; graph tensors are a representation artifact for later model work.

Step 3's representation software is implemented and CI-verified, but execution-level reproducibility and real-data evidence remain outstanding. A first Step 4 feature-fusion engine has been built as a software prototype; do not make scientific model claims until the pinned ESM-2 and MMseqs2 have been exercised on a reviewed dataset and the numerical reproducibility report is retained.


## Step 4 — Kinetics-Multi prediction engine (SOFTWARE IMPLEMENTATION ADDED; SCIENTIFIC VALIDATION PENDING)

**Purpose:** Build the multimodal enzyme–substrate prediction system described in the research blueprint.

**Implemented engineering scope on this branch:**
- Retain the existing target-specific XGBoost fit path and classical model-family comparison as baselines.
- Add `fit-multi` and `predict-multi` CLI commands and a target-specific feature-fusion MLP.
- Fuse ESM-2 sequence vectors, Morgan fingerprints, fixed-width summaries of RDKit atom/bond graph tensors, and optional raw assay context.
- Fit assay-context imputation, scaling and category encoding inside each CV fold; do not prefit context transforms on held-out folds.
- Validate feature schema/metadata, target identity, graph tensor dimensions and packed offsets, train/test group boundaries, and calibration group boundaries.
- Keep Km and kcat as independent training/inference jobs with their own units, artifacts and metrics.
- Support grouped CV, diagnostic-only row-random CV, untouched held-out scoring and optional split-conformal calibration on a separate archive.
- Require adjacent feature provenance manifests with verified archive hashes, source/version/license declarations, and a full immutable code commit SHA.
- Save a trusted-local joblib model bundle, held-out/inference predictions, metrics JSON, model card and experiment manifest. Model metadata records target, feature contract, code revision, data source/version/license and configuration.
- Inference rejects mismatched target, feature dimension/schema, representation metadata, graph layout and assay-context schema.

**Architecture boundary:** This first MLP performs nonlinear fusion of precomputed modalities plus 24 pooled graph descriptors. It is not a message-passing GNN, cross-attention model, residue–atom interaction model or molecular simulation. No such capability is claimed.

**Software acceptance evidence:** Synthetic tests cover graph summary alignment and corruption rejection, grouped split leakage checks, fold-local assay-context preprocessing, source-manifest hash/metadata validation, immutable code revision, calibration, model artifact generation and inference round-trip. CI run [#42185425243](https://github.com/AssayFlux/Kinetics/actions/runs/42185425243) passed on Python 3.10, 3.11 and 3.12: 69 tests passed on each version, compilation and scoped Ruff checks passed. The initial implementation was merged in [PR #22](https://github.com/AssayFlux/Kinetics/pull/22); corrective hardening was merged in [PR #23](https://github.com/AssayFlux/Kinetics/pull/23).

**Still required before Step 4 can be scientifically closed:**
- A reviewed, licensed, immutable real dataset release from Step 2; this is not yet present.
- Actual execution of pinned ESM-2 and MMseqs2 on that dataset, with repeatability/runtime evidence from Step 3.
- Classical and MLP training on the same real frozen partitions; no result can be reported from synthetic tests.
- External source/organism/assay/time validation where available, predeclared subgroup analysis and uncertainty coverage/width analysis.
- Explicit model-selection protocol, independent reproduction and an artifact/installation test on the real workflow.

Step 4 is being implemented as a software engine, not validated as a scientific predictor. Do not claim model superiority, external validity or calibrated uncertainty until the real-data validation gates are passed. Joblib bundles are pickle-based and must only be loaded from trusted sources.


## Step 5 — Scientific validation and benchmarking (IN PROGRESS — PROTOCOL, ROW/CLUSTER BOOTSTRAP REPORTING IMPLEMENTED)

**Purpose:** Test generalization beyond familiar proteins, chemicals, and assay settings.

**Work:** Predeclare benchmark tasks and splits; protein-cold, scaffold-cold, double-cold evaluation; external source/organism/assay/time evaluations where supported; target-appropriate metrics and confidence intervals; subgroup and applicability-domain reports; uncertainty calibration and coverage tests; ablations; overlap/contamination checks; failed-experiment records.

**Acceptance:** Frozen split assignments and dataset versions; test sets never used for selection; versioned evaluation code; uncertainty claims supported by empirical coverage evidence; reports disclose sample sizes, missingness, subgroup limitations, and confidence intervals; independent reproduction of reports.

**Initial software evidence:** Pre-execution protocol in `docs/STEP5_VALIDATION_PROTOCOL.md`; deterministic paired-row and (when group arrays are provided) paired cluster-bootstrap intervals for held-out log10 MAE/RMSE are emitted by the baseline comparison workflow. Tests cover reproducibility and invalid input. These are descriptive intervals and do not establish calibrated predictive uncertainty. Real-data reports, matched model ablations, external evaluations and independent reproduction remain outstanding because the reviewed Step 2 dataset release and Step 3 execution evidence are not yet available.

**Evidence required for completion:** Benchmark cards, frozen split manifests, real evaluation reports, ablations, contamination/leakage audits, cluster-aware or independent uncertainty evidence, and independent reproduction run.

## Step 6 — Native molecular visualization and simulation (FOUNDATION IMPLEMENTED; FULL STEP IN PROGRESS)

**Purpose:** Deliver scientifically faithful structural inspection and native performance where justified.

**Implemented foundation:**
- C++17/CMake native molecular structure and scene-data library with a command-line PDB inspector.
- Deterministic first-model PDB parsing; preservation of atom serial/name, alternate location, residue/chain identity, insertion code, element, occupancy, temperature factor and original Cartesian coordinates in angstrom.
- Explicit CONECT-only bonds; strict failure for truncated records, duplicate atom serials, non-finite coordinates and dangling/self bond references. No guessed bonds, inferred elements, implicit coordinate transforms or silent atom renumbering.
- Versioned JSON molecular-scene contract with validated selection/highlight serial sets, reference atom-distance calculation and a deterministic CPU XY PPM preview renderer with element colors and selection/highlight overlays.
- Narrow Python bridge that invokes the explicitly selected native executable without a shell, validates returned atom/bond references and coordinates, and adds source SHA-256 provenance.
- Parameter-validated OpenMM/GROMACS simulation-plan schema that records engine/version, input hash, force field, water model, integrator, timestep, steps, temperature, pressure, random seed and outputs. Plans are explicitly marked planned-not-executed.
- Native CMake/CTest CI matrix declared for Ubuntu, macOS and Windows; Python interoperability and simulation-plan tests.

**Scope boundaries:** The native C++ parser in this step supports PDB only. A separate Python mmCIF coordinate adapter is tracked under Step 9; it does not extend the C++ parser. The CPU XY preview is not a GPU-accelerated 3D renderer or interactive desktop viewer. Molecular surfaces, biological assembly expansion and molecular dynamics execution are not implemented. No performance claim is made.

**Remaining acceptance work:**
- Pass the native build and test matrix on all declared operating systems.
- Expand fixtures to reviewed reference structures and validate coordinate/identity round trips, altlocs, insertion codes, multi-model behavior and malformed-input handling.
- Add a renderer with camera, picking, visual representations and interaction overlays, selected only after a dependency/platform prototype.
- Implement real engine-specific OpenMM/GROMACS adapters, generated input decks, controlled execution, restart/cancellation and reference-system stability checks with complete execution provenance.
- Add representative parser/renderer benchmarks with reproducible structures, compiler flags, hardware and memory/time measurements; optimize only after profiling.

**Evidence:** native/, tests/test_native_molecule.py, docs/NATIVE_MOLECULAR_ENGINE.md, docs/IMPLEMENTATION_STATUS.md and docs/NATIVE_MOLECULAR_ENGINE.md, CMake/CTest workflow matrix. This is an engineering foundation, not full Step 6 acceptance.

## Step 7 — Rust infrastructure and security

**Purpose:** Provide dependable service and systems boundaries without coupling scientific code to infrastructure internals.

**Work:** Versioned API contracts; authentication and least-privilege authorization; secret management; job orchestration with limits, cancellation, retries, idempotency; secure artifact upload/download; audit events and observability; backup/restore; threat modeling for data access, external tools, and user isolation.

**Acceptance:** Contract tests; negative tests for unauthorized and cross-user access; no secrets in source/logs; explicit job lifecycle and resource limits; tested recovery and artifact integrity; critical security findings resolved or formally risk-accepted.

**Evidence:** Threat model, API specifications, integration tests, audit samples, recovery drill, security review.

**Implementation delivered in merged PR #46, with follow-up hardening in PR #47:**
- RS256 OIDC/JWT verification with issuer/audience/key/expiry/tenant/scope checks; managed AWS Secrets Manager access using workload identity.
- Tenant-bound HTTP artifact and job APIs; S3/KMS content-addressed artifacts; PostgreSQL durable jobs, idempotency, quotas, leases, heartbeats, cancellation and append-only hash-chained audit events.
- AWS ECS/Fargate, RDS, S3 replication, KMS, ALB/TLS and IAM Terraform candidate; encrypted database backup and isolated restore scripts; explicit API CIDR allowlist and Terraform CI validation.
- Follow-up SQL binding/retry accounting fixes and PostgreSQL retry/success integration coverage.

**Acceptance remains blocked:** no cloud deployment or OIDC provider configuration; the worker currently has only a no-op health-check handler, no scientific task handlers; per-job CPU/memory isolation is not enforced by the shared worker; live cross-tenant/security tests, IAM/network review and actual database/artifact restore drills have not been performed. Do not expose the candidate as production-ready. See `docs/STEP7_PRODUCTION_ACCEPTANCE.md`.

## Step 8 — Kinetics research workbench

**Purpose:** Enable complete research workflows through one coherent interface.

**Work:** Researcher workflows and accessibility requirements; dataset discovery and curation; experiment setup, training, inference, reports, provenance and uncertainty display; project/workspace management; job monitoring and artifact browsing; UI separated from scientific computation through stable APIs; usability testing and installation/update procedures.

**Acceptance:** A researcher completes a documented workflow without manual script stitching; every result links to inputs, dataset, model, and manifest; errors/job states are visible and recoverable; primary workflows pass user acceptance tests; accessibility and operations documentation exist.

**Engineering implementation merged; CI verified:**
- Optional local-first FastAPI workbench with a semantic, responsive browser UI; loopback-only launcher; project/workspace creation; bounded dataset uploads with atomic writes and SHA-256 checksums.
- Versioned SQLite schema 2 adds project, durable job-state, and artifact-registry tables through an additive migration from schema 1.
- Fixed allow-list maps researcher actions to the existing `kinetics-research` CLI without a shell. Supports legacy import, quality audit, identity/scaffold/sequence processing, feature building, partitions, classical and multimodal training/inference, dataset persistence/release and release verification.
- Project-relative path validation, symlink-escape checks, no-overwrite output policy, bounded worker concurrency, persisted job states, cancellation, timeouts, logs, output artifact hashing, checksum-verified downloads and provenance-aware Markdown reports.
- Accessible UI primitives: semantic headings/forms/tables, explicit labels, keyboard focus, live status, responsive layout and system color-scheme support. API and UI are separate from scientific computation.
- Added installation/operations/accessibility guide and integration tests for schema migration, path confinement, upload, a real quality-audit subprocess, artifact download/hash integrity and report generation.

**Current acceptance status:** PR #40 delivered the local-first workbench; follow-up PR #42 repaired CI and merged after the full Python 3.10/3.11/3.12, workbench integration/wheel, native C++ Linux/macOS/Windows and Rust checks passed ([run #42209064389](https://github.com/AssayFlux/Kinetics/actions/runs/42209064389)). The local API and UI are not a remote multi-user service; the launcher intentionally binds only to loopback. Engineering CI is green, but Step 8 is not yet fully accepted because real-data end-to-end execution, measured ESM-2/MMseqs2 performance and recovery, desktop upgrade/rollback evidence, uncertainty display verification, and researcher/accessibility sign-off remain outstanding.

**Remaining before Step 8 can be declared complete:** all workbench integration and cross-platform packaging checks pass; execute the complete curation → partitions → features → model comparison/training → inference → report flow on a reviewed licensed dataset; measure representative ESM-2/MMseqs2 runtime, memory, cancellation and recovery; perform keyboard/screen-reader and researcher usability sessions; document installation, upgrade and rollback; verify uncertainty/calibration/applicability displays against real model outputs; retain acceptance evidence.

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

The initial foundation fixes were merged through PR #1. SQLite schema versioning, transactional/idempotent initialization, forward-version protection, and safer backups were merged through PR #3. The explicit legacy paired-row to canonical-observation adapter and scoped Ruff CI check were merged through PR #4. PR #5 verifies preservation of records in a pre-versioned database. PR #6 adds a provenance-aware legacy import CLI; PR #7 preserves opaque source IDs; PR #8 hardens generated-path protection; PR #9 corrects regression assertions. PR #10 adds the canonical audit-to-SQLite persistence path and end-to-end tests; PR #11 fixes the final Ruff finding from that increment.

The latest verification run [#42173358868](https://github.com/AssayFlux/Kinetics/actions/runs/42173358868) passed on Python 3.10, 3.11, and 3.12: 36 tests passed on each version, source compilation passed, and scoped Ruff checks passed. This is meaningful but partial Step 1 progress, not completion of Step 1 or of the platform.

**Next Step 1 work:** establish and test the supported package/CLI compatibility contract; verify clean installation from the built wheel in CI; broaden static checks carefully; then complete the remaining security/dependency review. Do not force canonical independent target observations back into the legacy paired-target trainer, as that would reintroduce scientifically unsafe pairing. No later step is complete based on plans or stubs alone.


## Step 9 and Step 10 implementation status

The first Step 9 increment implements versioned protein-sequence, structure, residue-mapping and derived-feature records, plus provenance-checked Python PDB and mmCIF coordinate adapters that compute evidence-linked C-alpha distances only from explicit mappings. Deterministic fixtures cover both coordinate formats, digest integrity, author residue/chain identity and mapping evidence. External structure-source adapters, automatic mapping generation, independent reference validation and real-data benchmarks remain open. This Python support is separate from the native C++ PDB-only parser. See [Proteomics and structural biology](STEP9_PROTEOMICS_STRUCTURAL_CONTRACT.md).

Step 10 includes an executable release-manifest evaluator that validates required gates, source commit, evidence references and waiver metadata and conservatively emits GO/CONDITIONAL/NO-GO without claiming human sign-off. Actual release evidence, SBOM, vulnerability triage, security/recovery/UAT reports, accountable reviews and production sign-off remain open. See [Release readiness gates](STEP10_RELEASE_READINESS_GATES.md).


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
