# Implementation status

Status is updated as code is added. This document intentionally separates implementation from verification.

## Existing baseline observed during repository inspection

- Protein sequence and substrate SMILES feature extraction using ESM-2 and Morgan fingerprints.
- Separate XGBoost regressors for log10(Km) and log10(kcat).
- A CSV preprocessing script, feature cache, prediction interface, and optional ONNX export.
- CatPred-DB public download and CSV inspection scripts.
- Dataset notes describing BRENDA, SABIO-RK, UniProt, PubChem, and Rhea.

## New research infrastructure added

- Canonical one-target-per-row kinetic observation dataclass.
- Explicit unit conversion for Km and kcat.
- Table normalization with caller-supplied column mappings and rejection audit.
- SHA-256 file provenance and atomic JSON writing.
- Experiment manifest builder with environment and package metadata.
- Grouped holdout and strict double-cold partition helpers.
- Target-specific log-scale and original-scale metric reporting.
- CatPred-DB normalization adapter that keeps Km and kcat tables separate.
- Scientific architecture, data model, and publication evidence protocol.

## Known integration work still required

- Connect the new canonical observation schema to the existing preprocessing/feature/training/prediction pipeline.
- Resolve the current two-target-per-row assumption in the baseline so target-specific public tables can be used without fabricated pairing.
- Add sequence-cluster, scaffold, and double-cold evaluation workflows to the model pipeline.
- Add assay-context features and explicit applicability-domain/uncertainty reporting.
- Add versioned model metadata, prediction provenance, and publication report generation.
- Finalize packaging and user-facing CLI consistency.

## Verification status

The dedicated training, test execution, numerical validation, benchmarking, and scientific evaluation stages have not been run as part of this implementation-first phase. No performance or validation claims are made.
