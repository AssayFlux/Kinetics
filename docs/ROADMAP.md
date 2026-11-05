# Kinetics implementation roadmap

The agreed sequence is to finish assembling the software before executing training, testing, benchmarking, and scientific validation. These verification activities remain mandatory before release.

## Stage 0 — Scientific foundation
- [x] Inspect the existing enzyme Km/kcat prediction baseline.
- [x] Establish the scientific scope and architecture.
- [x] Define the canonical one-target-per-row observation contract.
- [x] Define publication, provenance, and data-governance standards.
- [x] Keep Astronaut integration explicitly deferred.\n- [x] Add a dependency-free, offline-first assistant adapter contract in Kinetics.\n- [x] Document the future Astronaut adapter boundary and security requirements.

## Stage 1 — Data and provenance
- [x] Canonical kinetic observation schema and explicit unit conversion.
- [x] Source-table normalization with configurable column mapping.
- [x] Row-level rejected-record audit.
- [x] SHA-256 source file provenance and curation manifests.
- [x] CatPred-DB target-specific normalization adapter.
- [x] Grouped and double-cold partition utilities.
- [x] MMseqs2 sequence-clustering wrapper with versioned mapping manifest.
- [x] RDKit canonical SMILES and Bemis-Murcko scaffold assignment utilities.
- [ ] BRENDA and SABIO-RK adapters after source schema/license verification.

## Stage 2 — Feature and model architecture
- [x] Target-independent protein/substrate feature generation.
- [x] Feature cache keyed by encoder and fingerprint configuration.
- [x] Target-specific prediction interface.
- [x] Preserve source IDs and grouping metadata in feature archives.
- [x] Target-specific model fitting workflow definition.
- [x] Assay-context feature encoder with train-only fitting and missingness handling.\n- [ ] Connect assay-context features to the experiment/model orchestration workflow.
- [ ] Additional model families and baseline comparison interfaces.
- [ ] Applicability-domain and out-of-distribution diagnostics.
- [ ] Prediction-time uncertainty interface.

## Stage 3 — Scientific analysis
- [x] Target-specific log-scale and original-scale metrics.
- [x] Split-conformal interval utilities.
- [ ] Calibration data workflow and empirical coverage reporting.
- [ ] Residual and subgroup diagnostics.
- [ ] Sensitivity and ablation analysis orchestration.
- [ ] Model comparison and statistical reporting.

## Stage 4 — Research workflow and outputs
- [x] Experiment manifest and environment metadata utilities.
- [x] Model-card generation.
- [x] Preliminary software citation metadata.
- [x] Publication protocol and manuscript outline.
- [ ] End-to-end experiment runner and artifact store.
- [ ] Reproducible figure/table/report generation.
- [ ] Stable user-facing CLI and Python API.
- [ ] Tutorials and complete example project.

## Stage 5 — Integration and implementation completion
- [ ] Connect canonical data, feature, model, prediction, and report workflows.
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
- Astronaut integration or changes to the Astronaut repository.
- Hosted AI dependencies.
- Claims of completed training, testing, validation, or publication readiness before Stage 6.
