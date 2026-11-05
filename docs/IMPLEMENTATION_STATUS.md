# Implementation status

Status is updated as code is added. This document intentionally separates implementation from execution and verification.

## Existing baseline observed during repository inspection

- Protein sequence and substrate SMILES feature extraction using ESM-2 and Morgan fingerprints.
- Separate XGBoost regressors for log10(Km) and log10(kcat), currently wired through a legacy paired-row preprocessing archive.
- A CSV preprocessing script, feature cache, prediction interface, and optional ONNX export.
- CatPred-DB public download and CSV inspection scripts.
- Dataset notes describing BRENDA, SABIO-RK, UniProt, PubChem, and Rhea.

## Research infrastructure implemented

- Canonical one-target-per-row kinetic observation contract.
- Explicit conversion of Km to M and kcat to s^-1 while retaining raw values/units.
- Configurable source-table normalization with row-level rejection reasons.
- CatPred-DB target-specific normalization adapter; Km and kcat are not implicitly paired.
- SHA-256 source/artifact provenance and atomic JSON serialization.
- Experiment manifest builder with runtime and package metadata.
- Grouped holdout and strict double-cold partition utilities.
- Target-specific feature archives preserving source record IDs and optional grouping labels.
- Target-specific model-fitting workflow with grouped CV support.
- Separate log-scale and original-unit metric reporting.
- Split-conformal interval utilities for calibrated regression intervals.
- Model-card generation and publication-oriented research documentation.
- Installable package metadata for the new kinetics_core research package.

## Integration work still required

- Connect canonical observation outputs to all legacy preprocessing, prediction, and export paths.
- Retire or clearly isolate the legacy two-target-per-row assumption.
- Add automated protein sequence clustering and chemical scaffold assignment workflows with versioned outputs.
- Add assay-context feature engineering and explicit applicability-domain diagnostics.
- Add calibration workflow and prediction-time uncertainty outputs to the inference API.
- Add dataset-specific BRENDA and SABIO-RK adapters after confirming current schemas and terms.
- Add complete report generation for figures, tables, and manuscript methods.
- Finalize CLI ergonomics, packaging compatibility, and user documentation.

## Verification status

No model training, test execution, numerical validation, benchmark run, or scientific evaluation has been performed during this implementation-first phase. The newly added workflows are code, not evidence that the workflows have passed verification. No performance, generalization, or publication-readiness claims are made.
