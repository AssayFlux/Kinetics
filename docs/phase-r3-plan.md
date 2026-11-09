# R3 — v0.1 research alpha

**Roadmap item:** Track R / R3  
**Status:** IMPLEMENTATION IN PROGRESS — initial research-core primitives committed; independent validation and alpha exit remain gated  
**Owner:** Engineering + Validation  
**Depends on:** R2 infrastructure integration; R2 exit evidence and explicit approval remain required before v0.1 release  
**Exit gate:** Reproducible offline alpha with independent-reference validation and owner approval

## Objective

Deliver a narrow but real v0.1 research alpha that demonstrates end-to-end scientific workflows on the approved Android architecture. v0.1 is not a broad tool catalogue, clinical product or claim that all planned domains are implemented.

## Initial scientific scope

1. **Sequence tools**
   - FASTA import and strict parser diagnostics.
   - Sequence statistics (length, GC fraction, ambiguity counts).
   - Reverse complement and transcription where biologically defined.
   - Pairwise alignment only through a pinned, license-approved engine with explicit scoring parameters and reproducible output.
   - Reject malformed records and preserve input provenance.
2. **Protein properties**
   - Protein sequence validation and amino-acid composition.
   - Molecular weight, theoretical pI and documented physicochemical descriptors using a pinned, independently checked implementation.
   - Explicit handling of ambiguous/rare residues and terminal modifications; unsupported chemistry must not be silently guessed.
3. **Enzyme kinetics — first validation flagship**
   - Michaelis–Menten model and nonlinear parameter estimation.
   - Lineweaver–Burk, Eadie–Hofstee and Hanes–Woolf transforms as exploratory linearized views, with their statistical limitations disclosed.
   - Km, Vmax and kcat only when required inputs and units are available.
   - Competitive, noncompetitive, uncompetitive and mixed inhibition models only with explicit model definitions and identifiable parameters.
   - Confidence intervals/uncertainty, residual diagnostics, goodness-of-fit and AIC/BIC where assumptions permit.
   - Clearly distinguish fitted estimates from mechanistic interpretation.
4. **Result and provenance presentation**
   - Input and output summary, algorithm/version, parameters, units, warnings, uncertainty and limitations.
   - Export reproducible machine-readable results and a human-readable report.
   - Offline operation; no remote dependency for the alpha's core workflows.

## Validation design

- Unit tests for parser edge cases, sequence calculations, alignment parameter handling, protein descriptors, unit conversions and numerical stability.
- Independent reference implementations or published/reference datasets selected before tuning against them.
- Enzyme-kinetics synthetic datasets with known parameters, noise levels, identifiability limits, model misspecification and outlier cases.
- Compare parameter recovery, residuals, confidence intervals and model selection against independent implementations; predefine tolerances and document failures.
- Include adversarial/invalid inputs, zero/negative concentrations where disallowed, unit mismatches, singular fits and insufficient observations.
- Benchmark runtime and peak memory on the target device tiers; report medians/distributions, not a single favorable run.
- Record validation datasets, provenance, licenses, hashes, exact versions, commands, outputs and tolerances under `validation/` and `benchmarks/`.
- Register every capability separately. Only mark validated when a validation record and reproducible test exist; device_verified requires a device log.

## UX and scientific guardrails

- Research Mode only; visible research-use notice.
- No diagnosis, prescribing, dosing or treatment recommendation.
- No patient data or clinical workflows; P0 remains blocked.
- Display uncertainty, fit warnings, assumptions, applicability limits and provenance.
- Do not imply that a model fit establishes biological mechanism or experimental truth.
- A viewer, demo or successful build is not scientific validation.

## Exit criteria

R3 is complete only when the three workflow families are implemented and registered at the correct status; reference-based validation records and reproducible tests exist; offline workflows operate end-to-end through R2 infrastructure; provenance and export are inspectable; performance and device limitations are documented; all third-party licenses are reviewed; the alpha is installable on an owner-tested target device; and the owner explicitly approves the v0.1 gate.

**Owner instruction (2026-11-08):** implement R1–R10 as one integrated delivery; do not stop implementation at R2. Preserve the R2 evidence/approval gate before v0.1 release.


## Regression-test baseline — 2026-11-08

Added host regression coverage for FASTA/FASTQ, IUPAC reverse complement/transcription, sequence statistics/k-mers, Needleman–Wunsch alignment output, peptide mass/pI and unsupported residues, Michaelis–Menten/inhibition equations, and a synthetic Michaelis–Menten parameter-recovery case. Host CI run 1594 passed all 28 tests. These tests establish current code behavior only; they are not independent scientific validation. Independent experimental/reference datasets, reference-calibrated uncertainty, scientific unit validation, validated fit-identifiability thresholds, external concordance beyond the bounded SciPy synthetic comparison, Android runtime and device benchmarks remain outstanding. Residual diagnostics (standardized residuals, leverage, Cook's distance, Durbin–Watson and sign runs) and Gaussian-iid AIC/BIC are now implemented and regression-tested; they remain descriptive and assumption-dependent, not independently validated. The base log-grid estimator returns no intervals; a separate paired-bootstrap helper now provides exploratory percentile intervals.


### R3 continued source increment — paired bootstrap intervals

Added a deterministic, seeded paired nonparametric bootstrap percentile-interval helper for the exploratory Michaelis–Menten grid fit. It fixes the parameter search bounds across replicates, reports successful/requested replicate counts, and emits explicit IID, grid-resolution, identifiability and model-misspecification caveats. It is not a replacement for independent reference validation or a validated uncertainty model. Regression tests are now included in the exact-source Python CI suite; see the 2026-11-09 CI #2101 audit record below.


### Independent-reference harness

Added a reproducible host-side comparison script using SciPy's bounded trust-region reflective curve_fit as an independent numerical reference for noise-free and seeded Gaussian-noise synthetic Michaelis–Menten datasets. It records versions, parameters, covariance diagonals, tolerances and local residual/identifiability diagnostics. The pinned host scientific-reference CI job now executes the Michaelis–Menten/SciPy comparison step successfully (CI #2101). This is a bounded synthetic software-reference comparison; no external experimental dataset or independent wet-lab validation is claimed.


### Exact-source automated audit — 2026-11-09 (CI #2101)
- Source commit: `8c4128d5e448db51f2b48fec6c38ce6022fdb053`; [workflow #2101](https://github.com/AssayFlux/Kinetics/actions/runs/42554027490) completed successfully across all five jobs.
- Python CI collected 233 tests: 229 passed, 4 skipped (3 optional RDKit adapter tests because RDKit is not installed in the base Python test environment; 1 optional pysam test because pysam is not installed). The separate pinned RDKit descriptor sanity job passed.
- The suite executed the R3/R4 sequence and research primitive tests, R5 structure/structure-view tests, R6 core chemistry tests, R7 phylogenetics tests, R8 omics tests, R9 catalogue/variant-reference tests and R10 registry/SBOM/configuration checks.
- The pinned host scientific-reference job passed its Michaelis–Menten/SciPy comparison and genetic-code/Biopython comparison steps. These are bounded synthetic/software-reference checks, not independent experimental validation.
- Android ARM64 debug APK/AAB packaging, static package/ELF alignment checks and `:app:testDebugUnitTest` passed. APK: 69,875,151 bytes, SHA-256 `059abb9e3a299b5295b8f08772b976195d7be1cd7db46dce34faa7bcf486d2d9`; AAB: 39,952,539 bytes, SHA-256 `9c8e2ca3a81c4ef2b1fb041aefee99ace5cbfb3292574b815c6a87549210044e`.
- Boundaries: no emulator or physical-device installation/runtime evidence; no Android migration/WorkManager/SAF instrumentation; no end-to-end on-device Chaquopy run; no R5 independent structure concordance, R6 approved-engine chemistry concordance, R7 published tree concordance, R8 null/power/FDR calibration, or R9 authoritative licensed PGx content. R10 security/licence/release gates remain open.


### R3 implementation inventory correction — 2026-11-09

A source/test audit confirms that the current Michaelis–Menten fit returns Gaussian-iid AIC/BIC, residual mean/sample SD, standardized residuals, leverage, Cook's distance, Durbin–Watson, residual sign runs, local Jacobian covariance/standard errors and a Jacobian condition-number diagnostic. These are implemented and regression-tested. The separate seeded paired-bootstrap helper provides exploratory percentile intervals. None of these diagnostics establishes model adequacy or calibrated uncertainty; independent experimental/reference datasets, units, predeclared identifiability criteria, uncertainty coverage simulations and device/runtime evidence remain open.
