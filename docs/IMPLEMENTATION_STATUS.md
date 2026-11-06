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
- SQLite experiment storage and package/CLI metadata.
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

No model training, test execution, numerical validation, benchmark run or scientific evaluation is claimed by this status document. Code presence is not proof that a workflow executes correctly or generalizes. Record actual commands, environments, outputs and commit identifiers when verification is performed.

## Project direction

The authoritative long-term direction is in [VISION.md](../VISION.md), [ROADMAP.md](../ROADMAP.md), [ARCHITECTURE.md](../ARCHITECTURE.md), [ENGINEERING_STACK.md](../ENGINEERING_STACK.md) and [CLINICAL_TRANSLATION.md](../CLINICAL_TRANSLATION.md). Kinetics Ecosystem is a separate project; this repository provides interfaces, not a bundled assistant runtime.
