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

Added host regression coverage for FASTA/FASTQ, IUPAC reverse complement/transcription, sequence statistics/k-mers, Needleman–Wunsch alignment output, peptide mass/pI and unsupported residues, Michaelis–Menten/inhibition equations, and a synthetic Michaelis–Menten parameter-recovery case. Host CI run 1594 passed all 28 tests. These tests establish current code behavior only; they are not independent scientific validation. Independent references/datasets, confidence intervals, residual diagnostics, AIC/BIC, unit handling, fit identifiability, external concordance, Android runtime and device benchmarks remain outstanding. The current log-grid estimator explicitly returns no confidence intervals.
