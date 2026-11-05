# Kinetics implementation roadmap

The agreed sequence is to finish assembling the software before executing training, testing, benchmarking, and scientific validation. These verification activities remain mandatory before release.

## Stage 0 — Scientific foundation
- [x] Inspect the existing enzyme Km/kcat prediction baseline.
- [x] Establish the scientific scope and architecture.
- [x] Define the canonical one-target-per-row observation contract.
- [x] Define publication, provenance, and data-governance standards.
- [x] Keep Astronaut integration explicitly deferred.
- [x] Add a dependency-free, offline-first assistant adapter contract in Kinetics.
- [x] Document the future Astronaut adapter boundary and security requirements.

## Stage 1 — Data and provenance
- [x] Canonical kinetic observation schema and explicit unit conversion.
- [x] Source-table normalization with configurable column mapping.
- [x] Row-level rejected-record audit.
- [x] Non-destructive duplicate/conflict and metadata-completeness audit.
- [x] SHA-256 source file provenance and curation manifests.
- [x] CatPred-DB target-specific normalization adapter.
- [x] Grouped and double-cold partition utilities.
- [x] Nested protein/scaffold double-cold train/calibration/test partition workflow with excluded cross-quadrant audit.
- [x] MMseqs2 sequence-clustering wrapper with versioned mapping manifest.
- [x] RDKit canonical SMILES and Bemis-Murcko scaffold assignment utilities.
- [ ] BRENDA and SABIO-RK adapters after source schema/license verification.

## Stage 2 — Feature and model architecture
- [x] Target-independent protein/substrate feature generation.
- [x] Feature cache keyed by encoder and fingerprint configuration.
- [x] Target-specific prediction interface.
- [x] Preserve source IDs and grouping metadata in feature archives.
- [x] Target-specific model fitting workflow definition.
- [x] Assay-context feature encoder with train-only fitting and missingness handling.
- [x] Connect assay-context features to target-specific modeling and inference artifacts.
- [x] Fixed classical baseline comparison interface with training-only CV selection.
- [x] Training-reference applicability-domain warning with explicit non-probabilistic interpretation.
- [x] Prediction-time conformal interval and applicability warning interface.

## Stage 3 — Scientific analysis
- [x] Target-specific log-scale and original-scale metrics.
- [x] Split-conformal interval utilities.
- [x] Independent calibration archive workflow and held-out empirical coverage reporting.
- [x] Residual tables and per-group error/interval-coverage diagnostics with small-sample warnings.
- [ ] Sensitivity and ablation analysis orchestration.
- [ ] Model comparison and statistical reporting.

## Stage 4 — Research workflow and outputs
- [x] Experiment manifest and environment metadata utilities.
- [x] Model-card generation.
- [x] Preliminary software citation metadata.
- [x] Publication protocol and manuscript outline.
- [ ] Unified multi-stage experiment runner and artifact store.
- [ ] Reproducible figure/table/report generation.
- [x] Stable command-line entry point for model comparison and target-specific fitting.
- [ ] Complete unified Python API and tutorial examples.
- [ ] Tutorials and complete example project.

## Stage 5 — Integration and implementation completion
- [ ] Complete unified end-to-end orchestration across curation, splits, features, modeling, prediction, and reports.
- [ ] Resolve legacy paired-target assumptions without breaking documented compatibility.
- [ ] Complete packaging and installation experience.
- [ ] Complete user and developer documentation.
- [ ] Freeze implementation scope before verification.

## Stage 6 — Final verification (only after implementation is assembled)
- [ ] Unit and integration test suite.
- [ ] Analytic/reference numerical validation.
- [ ] Data provenance and transformation reproducibility checks.
- [ ] Parameter recovery and uncertainty coverage studies.
- [ ] Leakage audit and protein/scaffold/double-cold benchmark runs.
- [ ] Performance, memory, and scalability benchmarks.
- [ ] Dependency, security, and clean-install checks.
- [ ] Document failures, limitations, and known issues.

## Stage 7 — Publication and release
- [ ] Reproducible clean-environment release candidate.
- [ ] Regenerate every reported figure and table.
- [ ] Versioned software release and final citation metadata.
- [ ] Methods/results manuscript material supported by completed evidence.

## Explicit exclusions until authorized
- Connecting the Astronaut runtime or changing its repository before the project owner confirms it is ready.
- Hosted AI dependencies.
- Claims of completed training, testing, validation, or publication readiness before Stage 6.
