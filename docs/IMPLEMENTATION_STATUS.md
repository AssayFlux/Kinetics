# Implementation status

> 100-domain scope register: docs/SCIENCE_DOMAIN_CATALOGUE_100.md. This catalogue defines intended breadth; it is not evidence that every domain is implemented or clinically validated.
> **Mission authority:** This document is governed by [KINETICS_MISSION.md](../KINETICS_MISSION.md). Kinetics is a cross-disciplinary biomedical and precision-health research platform—not only an enzyme-kinetics project. All domains, datasets, models and applications must align with the mission, preserve provenance and clinical safety, and follow the foundation-first build order. Small Android devices are a first-class performance target.

This file distinguishes repository contents from execution, verification and scientific evidence. The expanded Kinetics platform is a long-term plan; it is not implemented merely because it appears in the roadmap.

## Existing repository foundation observed

- Protein sequence and substrate SMILES feature extraction using ESM-2 and Morgan fingerprints.
- XGBoost baselines for log10(Km) and log10(kcat), including legacy paired-row preprocessing.
- CSV preprocessing, feature caching, prediction interface and optional ONNX export.
- CatPred-DB public download and CSV inspection scripts.
- Dataset notes for public biochemical/biological resources.

## Research infrastructure present in the codebase

- Canonical one-target-per-row kinetic observation contract.
- Explicit legacy paired-row adapter to canonical observations, requiring source record IDs and preserving independently available Km/kcat values.
- Provenance-aware `kinetics-research import-legacy` CLI, including input/output hashes, source version/license metadata, and protection against raw-input overwrite.
- `kinetics-research persist` and a canonical persistence service that re-audits input, validates target-specific canonical units, and atomically records immutable dataset snapshots, measurement rows, and provenance events in SQLite.
- Idempotent replay for identical dataset snapshots; changed content or source metadata under an existing dataset ID is rejected.
- End-to-end fixture covering legacy import → quality audit → SQLite persistence, including independent Km/kcat rows, original values/units, source IDs, license, and checksums.
- Text-preserving source-record ID ingestion so opaque IDs and leading zeroes survive CSV import.
- Explicit Km-to-M and kcat-to-s^-1 conversion.
- CatPred-DB acquisition with pinned Hugging Face data revision and separately pinned GitHub processing-code revision; downloads include Km/kcat train/validation/test tables and published sequence-cluster test files, each with SHA-256 hashes.
- CatPred source adapter using the target-specific aggregate fields `log10km_mean` (Km geometric mean) and `log10kcat_max` (kcat maximum), exponentiating to linear values and normalizing Km to M.
- Explicit `source_aggregated` measurement semantics; representative row-level `value` and `log10_value` are retained separately from the aggregate target.
- Source clipping policy, source revision, processing-code revision, source-row locator, dataset citation/license metadata, pH/temperature/taxonomy/accession context, and all original source columns recorded in curation manifests.
- Celsius-to-kelvin conversion; required target-specific source units (Km mM, kcat s^-1); explicit warnings for missing BRENDA per-row unit metadata and the upstream SABIO kcat min^-1 conversion.
- Sequence/SMILES identity normalization CLI, stereochemistry-preserving RDKit canonicalization, content hashes, and row-level identity rejection reports.
- Same-source duplicate/conflict review plus non-destructive cross-source duplicate candidates.
- Immutable KDB release and verify-release commands, combined rejection logs, source manifest retention, data cards, SHA-256 artifact verification, and propagation of source-quality warnings.
- Duplicate/conflict audits and metadata completeness summaries.
- Dataset provenance manifests and experiment metadata.
- Grouped holdout, protein-cluster and chemical-scaffold split utilities.
- MMseqs2 wrapper with validated protein sequences, source-qualified record keys, repeated-observation collapse only when sequence identity agrees, complete unique-entity coverage checks, and hashes for the input FASTA, raw cluster output, and mapping.
- RDKit canonical isomeric SMILES, stereo-agnostic Bemis-Murcko scaffold grouping, and row-level scaffold rejection audits.
- Pinned ESM-2 model/tokenizer revisions, residue-only mean pooling, strict sequence validation, no silent truncation, and bounded batch inference.
- Morgan fingerprints (radius 2, 2,048 bits, chirality enabled by default) and stereochemistry-aware molecular graph tensors with atom/bond features and packed offsets.
- Versioned feature NPZ archives with source IDs/labels, normalized sequences, original/canonical SMILES, target values, split-group arrays, molecular graphs, and non-object Unicode arrays safe for `allow_pickle=False`.
- Dependency/configuration-aware atomic feature caches; feature manifests record model/tokenizer revisions, representation parameters, runtime/software versions, source input hashes, source versions/licenses, row-identity hashes and archive SHA-256.
- CLI workflows for `annotate-scaffolds`, `cluster-sequences`, and `build-features`; clustering attaches source-qualified `protein_cluster_id` values back to canonical observations.
- Merged Step 3 representation implementation: [PR #21](https://github.com/AssayFlux/Kinetics/pull/21), with CI matrix [#42182490997](https://github.com/AssayFlux/Kinetics/actions/runs/42182490997) successful on Python 3.10, 3.11 and 3.12 (61 tests per version at that revision).
- Split-conformal interval utilities and held-out coverage reporting.
- Applicability-domain warnings, explicitly not calibrated confidence.
- Assay-context preprocessing designed to avoid cross-validation leakage.
- Classical model-family comparison and held-out reporting utilities.
- Research CLI, metrics, model cards, prediction/reporting and visualization helpers.
- SQLite experiment storage with schema version 1, transactional/idempotent bootstrap, forward-version protection, and consistent backup support.
- Package/CLI metadata and CI verification across Python 3.10–3.12; Ruff checks cover the KDB adapters, curation, identity, release, quality, scripts, and associated tests.
- Domain documentation, publication protocol, paper outline and contribution guidance.
- Dependency-free research-assistant protocol/facade that can later be exposed through documented, permission-scoped interfaces to the separate Kinetics Ecosystem project.

## Current engineering gaps

- Step 2 tooling is implemented, but no real CatPred snapshot has yet been downloaded, curated, or released in this repository. The current Hugging Face dataset is gated; the downloader now accepts a researcher-supplied `HF_TOKEN` read token and scopes it to the Hugging Face dataset host, but an authorized user must first accept the gate in a browser. The upstream kcat unit caveat must be resolved against source-level BRENDA/SABIO records before treating its absolute scale as validated. Direct BRENDA and SABIO adapters remain pending current schema, access, and license verification.

- Connect canonical observation outputs to legacy preprocessing, prediction and ONNX paths.
- Retire or isolate the legacy two-target-per-row assumption without breaking supported workflows.
- Execute real ESM-2 inference and MMseqs2 clustering on a reviewed, licensed dataset; establish hardware-specific repeat-run numerical tolerances and generate a real feature reproducibility report.
- Complete reproducible orchestration from source acquisition through curation, partitioning, features, calibration, model selection and reporting.
- Execute the pinned ESM-2 checkpoint and MMseqs2 on a reviewed real dataset; record repeatability and runtime evidence (Step 3 execution validation).
- Run classical and Kinetics-Multi fusion models on the same reviewed real dataset and frozen cold-start partitions; complete external validation (Step 4 scientific validation).
- Expand shift-stratified diagnostics, uncertainty coverage-versus-width analysis and statistical comparisons.
- Add BRENDA and SABIO-RK adapters only after current schemas, licenses and access terms are verified.
- Integrate report/figure utilities into a single reproducible experiment workflow.
- Complete CLI ergonomics, packaging compatibility, migration and user documentation.
- Define the cross-language contracts before introducing C++ and Rust components.
- Prototype and validate the native 3D/imaging engine; no such engine is claimed as implemented.
- Define secure project/data boundaries and threat model before handling sensitive data.

## Platform roadmap status

The genomics, transcriptomics, proteomics, structural biology, chemistry, pharmacology, molecular simulation, multi-omics, biomedical imaging, desktop workbench, clinical translation and Android capabilities are roadmap programmes unless explicitly listed above as present code. No clinical capability is claimed.

## Step 8 — Research workbench (ENGINEERING FOUNDATION MERGED; ACCEPTANCE IN PROGRESS)

- Added optional `kinetics-workbench` package extra and launcher. It binds to `127.0.0.1` only and uses the existing Python scientific CLI through a versioned HTTP API.
- Added project workspace management, browser-based bounded dataset upload, SQLite schema v2 for projects/jobs/artifacts, fixed allow-listed job dispatch, project-relative/symlink-safe paths, single-worker execution, cancellation, timeouts, durable state/logs, artifact checksums, verified downloads and Markdown report generation.
- Workbench actions cover legacy import, audit, dataset persistence/release/verification, identity/scaffold/sequence processing, feature generation, partitioning, baseline comparison, target-specific and multimodal training, and multimodal inference.
- UI includes dataset registry, job monitor, logs, artifact browser, report creation and keyboard-accessible controls. See `docs/WORKBENCH_GUIDE.md`.
- Integration tests exercise schema-v1 to v2 migration with data preservation, command allow-list/path confinement, dataset upload, cross-site request rejection, actual audit subprocess execution, artifact tampering detection, report and machine-readable reproducibility-manifest downloads. Dedicated CI builds and installs a wheel and verifies the launcher and bundled UI.

**CI evidence:** PR [#42](https://github.com/AssayFlux/Kinetics/pull/42) merged after the full GitHub Actions matrix passed: Python 3.10/3.11/3.12 suites, dedicated workbench integration/lint/wheel-install checks, Linux/macOS/Windows native C++ jobs, and Rust checks. The run was [#42209064389](https://github.com/AssayFlux/Kinetics/actions/runs/42209064389). This is engineering verification, not scientific or researcher acceptance.

**Not yet accepted as complete:** researcher usability and screen-reader testing; built-wheel installation and upgrade/rollback on supported desktop environments; real reviewed-dataset end-to-end workflow; measured ESM-2/MMseqs2 runtime/memory/cancellation/recovery; and validated uncertainty display. The workbench is local single-user software, not a remote multi-tenant service. These are release gates, not implied by code presence.

## Verification status

Step 2 fixture tests cover CatPred aggregate target selection, source-unit declarations, aggregation semantics, source-row locators, identity normalization, duplicate candidates, release manifests, warning propagation and checksums. Step 3 fixture tests cover pinned ESM configuration, cache invalidation, non-pickle feature archives, molecular graph alignment/stereochemistry, scaffold rejection audits, source-qualified MMseqs mapping, repeated target observations, incomplete-cluster rejection, CLI workflows and source/artifact hashes.

GitHub Actions run [#42182250301](https://github.com/AssayFlux/Kinetics/actions/runs/42182250301) passed on Python 3.10, 3.11 and 3.12: **61 tests passed on each version**, source compilation passed, and scoped Ruff checks passed. This verifies software and fixture-driven workflows only. The pinned ESM checkpoint has not been downloaded or executed; MMseqs2 has not been run on a real dataset; no real CatPred snapshot has been imported or released; no real feature archive, model training or benchmark run has been performed. Hardware-specific embedding repeatability tolerances and scientific generalization remain unvalidated.

## Project direction

The authoritative long-term direction is in [VISION.md](../VISION.md), [ROADMAP.md](../ROADMAP.md), [ARCHITECTURE.md](../ARCHITECTURE.md), [ENGINEERING_STACK.md](../ENGINEERING_STACK.md) and [CLINICAL_TRANSLATION.md](../CLINICAL_TRANSLATION.md). Kinetics Ecosystem is a separate project; this repository provides interfaces, not a bundled assistant runtime.


## Kinetics-Multi implementation branch

The feature-fusion MLP training/inference engine was merged in [PR #22](https://github.com/AssayFlux/Kinetics/pull/22); corrective context/provenance hardening was merged in [PR #23](https://github.com/AssayFlux/Kinetics/pull/23). It combines precomputed ESM-2 and Morgan vectors, 24 pooled RDKit graph descriptors and optional raw assay context with fold-local preprocessing. It is not a message-passing GNN. CI run [#42185425243](https://github.com/AssayFlux/Kinetics/actions/runs/42185425243) passed with 69 tests on each of Python 3.10, 3.11 and 3.12. Synthetic tests are not evidence of scientific validity. Real-data execution is blocked by the still-open Step 2 source release and Step 3 checkpoint/MMseqs2 execution requirements. See [KINETICS_MULTI.md](KINETICS_MULTI.md).


## Step 5 benchmarking implementation

- Pre-execution scientific validation protocol added at `docs/STEP5_VALIDATION_PROTOCOL.md`, including frozen protein-cold, scaffold-cold, double-cold and supported external-shift regimes; selection/test isolation; subgroup, ablation, contamination and reproducibility requirements.
- Added deterministic paired-row percentile-bootstrap intervals for held-out log10 MAE/RMSE in `kinetics_core.validation`; baseline benchmark reports now include 95% intervals (2,000 resamples by default).
- Tests cover reproducibility, interval structure and invalid input/configuration. These intervals are descriptive row-sampling uncertainty only; they do not account for cluster dependence or establish calibrated predictive uncertainty.
- Step 5 real-data execution remains blocked by Step 2's reviewed immutable dataset release and Step 3's actual pinned ESM-2/MMseqs2 execution and repeatability evidence. No scientific performance claim is made.


- Step 5 implementation PR [#24](https://github.com/AssayFlux/Kinetics/pull/24) merged as `89146f74174a89b11f0b065fa77b0b1bd7d98163`; its three-Python-version CI matrix passed. It adds the pre-execution protocol and paired-row bootstrap reporting, not empirical scientific validation.
- Step 5 follow-on cluster-aware bootstrap implementation is being added in a separate change. It resamples whole held-out protein/scaffold groups and reports intervals by declared holdout axis; real-data scientific acceptance remains blocked by Step 2/3 execution prerequisites.


## Step 6 — Native molecular visualization and simulation

- In progress on feature branch `kinetics/step6-native-molecular-engine`: initial C++17 molecular structure model, PDB atom/CONECT parser, explicit angstrom coordinates, atom identity preservation, selection/highlight state, JSON scene serialization, and a small reference fixture.
- Not complete: native build/test evidence, mmCIF and broader format support, Python/Rust interoperability, renderer/GPU integration, simulation adapters, and reproducible performance/physics validation remain outstanding.

## Step 7 — Rust infrastructure and security

- Merged Rust foundation: principal scope/tenant checks; bounded job contract and lifecycle/idempotency state machine; durable SQLite job store with tenant-scoped idempotency and bounded retry state; SHA-256 content-addressed artifact store with verified backup/restore; structured audit event validation; redacted runtime secret wrapper; typed versioned request/response contracts; OpenAPI 3.1 specification; negative/unit/contract tests.
- Rust CI now runs `cargo fmt --all -- --check`, `cargo clippy --all-targets -- -D warnings`, and `cargo test --all-targets`. Main-branch workflow run [#42196792717](https://github.com/AssayFlux/Kinetics/actions/runs/42196792717) passed Rust formatting, Clippy, Rust tests, Python 3.10, 3.11 and 3.12 suites, and native C++ builds on Ubuntu, macOS and Windows. The durable SQLite and backup/restore additions are included in that run.
- This is a verified infrastructure foundation, not a deployed production service. External OIDC/JWT verification, managed secret-provider integration, durable distributed queue/leases/retries and enforced container quotas, authenticated network artifact handlers, append-only audit persistence, encrypted backup/restore drills, deployment isolation, and integration security testing remain required before Step 7 can be called fully complete.
- Threat model, API contract and deployment requirements are documented in `docs/STEP7_RUST_INFRASTRUCTURE.md` and `docs/api/openapi-v1.yaml`.


## Step 6 — Native molecular visualization and simulation

The initial C++17/CMake molecular structure and scene-data foundation is implemented and CI-verified. See [Native molecular engine](NATIVE_MOLECULAR_ENGINE.md) and [Step 6 implementation status](STEP6_IMPLEMENTATION_STATUS.md). Do not mark Step 6 complete until reviewed reference structures validate the parser/scene contract, a production 3D renderer is delivered, and real OpenMM/GROMACS adapters produce fully parameterized, traceable execution artifacts with reference-system checks. No simulation execution or performance claim is currently asserted.


## Step 9 — Domain expansion (CONTRACT PROPOSED; IMPLEMENTATION NOT STARTED)

- Selected proteomics and structural biology as the first domain expansion because it reuses existing protein-sequence and structure foundations while keeping domain semantics explicit.
- Added `docs/STEP9_PROTEOMICS_STRUCTURAL_CONTRACT.md` defining sequence, structure, residue-mapping and derived-feature contracts; source/license provenance; evidence classes; bounded parsing; and validation gates.
- No proteomics/structural adapter, real source ingestion, curated structural benchmark or domain acceptance test is claimed yet. Genomics, transcriptomics, multi-omics, imaging and pharmacology remain separate future modules.

## Step 10 — Integration and release readiness (CONTROL SPECIFICATION ADDED; RELEASE NOT SIGNED OFF)

- Added `docs/STEP10_RELEASE_READINESS_GATES.md` with build/compatibility, scientific reproducibility, security/privacy, runtime/recovery and researcher-acceptance gates, a release-candidate manifest, evidence states and GO/CONDITIONAL/NO-GO decision rules.
- Current release decision is NO-GO for scientific performance claims and remote multi-tenant production because real-data validation and production deployment gates remain unverified. No production release or recovery drill is claimed.


## Step 9/10 executable contract increment (2026-11-06)

- Added `kinetics_core.proteomics`: deterministic sequence normalization and SHA-256 identity, provenance-bearing sequence and structure records, explicit experimental/predicted distinction, explicit residue mapping with sequence/structure/chain checks, and derived-feature provenance requirements.
- Added `kinetics_core.release_gate`: required release gate inventory, evidence-state validation, passed-evidence requirement, strict critical-gate non-waivability, complete non-critical waiver metadata, and conservative GO/CONDITIONAL/NO-GO evaluation. The evaluator never claims human sign-off.
- Added focused unit tests and included both modules/tests in the CI lint command.
- These increments are contract/data-integrity foundations only. Structure parsing, source adapters, actual mapping/feature computation, scientific validation, live CI/evidence verification, deployment, backup restore, and human release sign-off remain open.

## Step 7 production reconciliation (2026-11-06)

- PR #46 merged the reconciled Rust OIDC/JWT API, AWS Secrets Manager and S3/KMS adapters, PostgreSQL durable job/audit store, worker lease runtime, migration, container, and encrypted backup/restore scripts.
- PR #47 added the AWS ECS/RDS/S3/KMS Terraform deployment candidate, required API CIDR allowlist, Terraform validation in CI, typed job-limit SQL bindings, retry accounting/maximum-attempt fixes, and PostgreSQL retry/success integration coverage. PR #48 restored the mutable audit-event fixture needed by the tamper-rejection test.
- Production is not deployed. The worker currently registers only `kinetics.noop_healthcheck`; scientific task handlers and per-job CPU/memory sandbox isolation are not yet implemented. Cloud account/VPC/ACM/ECR/OIDC configuration, live cross-tenant security tests, IAM review and database/artifact restore drill remain outstanding.
- The latest main-branch workflow is still running its Rust integration test job; Python 3.10/3.11/3.12, workbench integration, Terraform validation, and native C++ Linux/macOS/Windows jobs have passed. Earlier failed runs are not passing evidence.

## Step 8 research workbench

The local-first FastAPI workbench is merged and has a documented end-to-end fixture integration for upload → audit job → artifact verification/download → report generation. It exposes the curation, feature, partition, compare, fit and inference CLI workflows through a strict allowlist. It binds to loopback only and is not a remote multi-user service. Researcher/screen-reader UAT, the full real-data workflow, ESM-2/MMseqs2 hardware benchmarks, and install/upgrade/rollback evidence remain open; see `docs/WORKBENCH_GUIDE.md`.

## Step 9 scientific expansion

The versioned sequence, structure, residue-mapping and derived-feature contracts are implemented. A fixed-column PDB adapter verifies source SHA-256, preserves model/chain/author residue/insertion/alternate-location metadata, and calculates C-alpha distances only from explicit validated mappings with evidence IDs. Tests use deterministic fixtures. mmCIF, source adapters, automated sequence alignment, independent structural reference checks and real-data benchmarks remain open; no broad scientific validation is claimed.

## Step 10 release readiness

The executable release evaluator validates required gates, source commit, evidence references and non-critical waiver metadata. It always reports `release_signoff: false`; it does not inspect evidence files or replace human approvals. Release manifest, SBOM, security/recovery/UAT evidence, signed reviews and production release remain outstanding.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.


## 100-domain scope and visual asset implementation status

- The 100-domain scope is defined in `docs/SCIENCE_DOMAIN_CATALOGUE_100.md`; catalogue inclusion is not implementation evidence.
- The Wikimedia Commons importer targets 100 categories and restricts accepted licenses to CC0, public domain, CC BY and CC BY-SA.
- The 100 PNG binaries have not yet been downloaded and committed. Until they are present, README avoids embedding missing PNG paths.
- A reproducible pixel-art GIF generator and asset validator are provided. The currently tracked legacy GIF fails structural validation; the README therefore no longer embeds it. Run the generator locally and commit the replacement binary. The validator checks dimensions, frame count and looping metadata.


## Knowledge corpus ingestion foundation

- Added a resumable, bounded acquisition pipeline for explicitly redistributable Internet Archive and Europe PMC/PMC Open Access material.
- The fetcher reads the canonical 100-domain catalogue and extends it with 45 cross-disciplinary computing, engineering, mathematics, physics and natural-science scopes.
- Added a per-item license gate, source/citation provenance, content-addressed storage, SHA-256 verification, source pagination, retry/backoff and per-file/per-batch byte limits.
- Added PDF/EPUB/XML/HTML/TXT extraction, deterministic tokenization, SQLite FTS5 chunk indexing, exploratory analysis, and source-grounded retrieval scripts.
- Added scheduled/manual GitHub Actions automation. The default durable export is a GitHub Release asset batch with bundled attribution metadata; Git LFS remains an optional alternative.
- Added checksum-verified release restoration and focused tests. The full 10,000+ corpus has not been acquired yet; collection is incremental and limited by upstream rights, API availability and storage budgets.
- DOAB, DOAJ and arXiv are registered as future discovery adapters but are not enabled for bulk downloads. Their item-level rights and adapter behaviour require review before activation.
- This is a research knowledge layer, not a clinical decision system. Keyword/entity summaries are exploratory; model-specific embeddings, OCR, domain validation and clinical validation are not claimed.
- GitHub-hosted execution and the new test suite require CI verification. Public Release assets must contain only redistributable material; SQLite and local raw working files are not committed as ordinary Git blobs.
