# Implementation status

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

The initial C++17/CMake molecular structure and scene-data foundation is under implementation. See [Native molecular engine](NATIVE_MOLECULAR_ENGINE.md) and [Step 6 implementation status](STEP6_IMPLEMENTATION_STATUS.md). Do not mark Step 6 complete until the declared cross-platform native CI passes, reviewed reference structures validate the parser/scene contract, a renderer is delivered, and real OpenMM/GROMACS adapters produce fully parameterized, traceable execution artifacts with reference-system checks. No simulation execution or performance claim is currently asserted.
