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
- Source-table normalization and row-level rejection audits.
- Duplicate/conflict audits and metadata completeness summaries.
- Dataset provenance manifests and experiment metadata.
- Grouped holdout, protein-cluster and chemical-scaffold split utilities.
- MMseqs2 sequence-clustering wrapper.
- RDKit canonical SMILES and Bemis-Murcko scaffold utilities.
- Target-specific feature archives and model workflows.
- Split-conformal interval utilities and held-out coverage reporting.
- Applicability-domain warnings, explicitly not calibrated confidence.
- Assay-context preprocessing designed to avoid cross-validation leakage.
- Classical model-family comparison and held-out reporting utilities.
- Research CLI, metrics, model cards, prediction/reporting and visualization helpers.
- SQLite experiment storage with schema version 1, transactional/idempotent bootstrap, forward-version protection, and consistent backup support.
- Package/CLI metadata and CI verification across Python 3.10–3.12; Ruff lint is currently scoped to the new legacy adapter.
- Domain documentation, publication protocol, paper outline and contribution guidance.
- Dependency-free research-assistant protocol/facade that can later be exposed through documented, permission-scoped interfaces to the separate Kinetics Ecosystem project.

## Current engineering gaps

- Connect canonical observation outputs to legacy preprocessing, prediction and ONNX paths.
- Retire or isolate the legacy two-target-per-row assumption without breaking supported workflows.
- Add end-to-end sequence-cluster/scaffold generation to dataset workflows.
- Complete reproducible orchestration from source acquisition through curation, partitioning, features, calibration, model selection and reporting.
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

GitHub Actions run [#42173358868](https://github.com/AssayFlux/Kinetics/actions/runs/42173358868) passed on Python 3.10, 3.11, and 3.12: 36 tests passed on each version, source compilation passed, and Ruff checks passed for the legacy adapter, CLI, package metadata, persistence service, and relevant tests. This is software verification only: no model training, numerical validation, benchmark run, or scientific generalization claim is made here. Code presence and passing software tests do not establish predictive validity.

## Project direction

The authoritative long-term direction is in [VISION.md](../VISION.md), [ROADMAP.md](../ROADMAP.md), [ARCHITECTURE.md](../ARCHITECTURE.md), [ENGINEERING_STACK.md](../ENGINEERING_STACK.md) and [CLINICAL_TRANSLATION.md](../CLINICAL_TRANSLATION.md). Kinetics Ecosystem is a separate project; this repository provides interfaces, not a bundled assistant runtime.
