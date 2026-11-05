# Implementation status

Status is updated as code is added. This document separates implementation from execution and verification.

## Existing baseline observed during repository inspection

- Protein sequence and substrate SMILES feature extraction using ESM-2 and Morgan fingerprints.
- Separate XGBoost regressors for log10(Km) and log10(kcat), wired through a legacy paired-row preprocessing archive.
- CSV preprocessing, feature caching, prediction interface, and optional ONNX export.
- CatPred-DB public download and CSV inspection scripts.
- Dataset notes describing BRENDA, SABIO-RK, UniProt, PubChem, and Rhea.

## Research infrastructure implemented

- Canonical one-target-per-row kinetic observation contract.
- Explicit Km-to-M and kcat-to-s^-1 conversion, including configurable per-record unit columns.
- Source-table normalization with explicit mappings and row-level rejection audit.
- CatPred-DB adapter that processes Km and kcat tables separately.
- SHA-256 provenance, atomic JSON writing, and experiment manifests.
- Grouped holdout and strict double-cold partition utilities.
- MMseqs2 sequence-clustering wrapper with version/command manifest.
- RDKit canonical SMILES and Bemis-Murcko scaffold utilities.
- Target-specific protein/substrate feature archives with optional grouping arrays.
- Target-specific model-fitting and inference workflows with grouped cross-validation and multi-axis holdout leakage checks.
- Separate log-scale and original-unit metric reporting.
- Split-conformal interval utilities.
- Model-card generation, target-specific prediction interface, experiment report generation, and parity/residual plotting utilities.
- Installable kinetics_core package metadata and CLI entry point.
- Scientific architecture, data model, split design, publication protocol, paper outline, contribution guidance, and citation metadata.

## Integration work still required

- Connect canonical observation outputs to the legacy preprocessing, prediction, and ONNX paths.
- Retire or isolate the legacy two-target-per-row assumption without breaking documented compatibility.
- Add end-to-end sequence-cluster and scaffold generation to the dataset workflow.
- Add assay-context feature engineering and applicability-domain diagnostics.
- Add calibration-data workflow and prediction-time uncertainty outputs to the inference interface.
- Add BRENDA and SABIO-RK adapters after verifying current source schemas and terms.
- Integrate the report/figure utilities into a complete end-to-end experiment orchestrator.
- Complete CLI ergonomics, packaging compatibility, and user documentation.

## Verification status

No model training, test execution, numerical validation, benchmark run, or scientific evaluation has been performed during this implementation-first phase. The newly added workflows are code, not evidence that they have passed verification. No performance, generalization, or publication-readiness claims are made.
