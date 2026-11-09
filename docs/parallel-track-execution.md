# Historical parallel execution protocol — SUPERSEDED

**ARCHIVED — DO NOT USE FOR CURRENT SEQUENCING**

**Historical owner direction:** 2026-11-08. This document recorded a temporary instruction to execute R/S/I/P concurrently. On 2026-11-09, D-019 explicitly superseded that sequencing permission. The current controlling order is **R → S → I → P → G**, with two steps per track. This file is retained only for decision history; do not use its parallel work lanes or immediate deliverables as current instructions. Refer to `DECISIONS.md` D-019 and the current sequencing gate in `ROADMAP.md`.

## Operating rules

1. The canonical source of truth is `ROADMAP.md`; phase IDs, dependencies, exit gates and status must match it.
2. Parallel means independent tasks can progress at the same time. It does not mean a dependent phase is marked started, implemented, validated or released before its prerequisite is satisfied.
3. Use public, redistributable test/reference data only unless a separate approved data governance gate exists. No real patient data, human-subject research or clinical advice.
4. Separate source implementation, software tests, analytical validation, external replication, device verification and publication readiness in every report.
5. Each scientific output records input hash, tool/version, database release, parameters, random seed, execution environment, warnings, uncertainty, exclusions and limitations.
6. A failed/unsupported/ambiguous result must be representable; never convert absence of evidence into a positive call.
7. Record license provenance for every dependency, model, dataset, reference database, font, renderer and generated asset before bundling or redistributing.
8. Keep the UI a client of typed domain/orchestrator APIs. Scientific logic does not live in Compose or WebView JavaScript.
9. Every phase change is evidence-backed. Update the capability registry only when the implementation path and tests exist; set validation evidence only after independent reference validation.
10. Stop at all roadmap gates. In particular, P0 remains blocked; patient-facing PGx and Clinical Mode remain disabled.

## Parallel work lanes

### R — Research platform (R1–R10)
- R1/R2: finish reproducible Android build/runtime probes, SAF lifecycle, encrypted-store recovery/export and architecture feasibility.
- R3: curate independent kinetics/sequence/protein reference fixtures; quantify agreement, residual behaviour, uncertainty and failure modes.
- R4/R5/R6/R7/R8: expand format correctness and algorithmic reference suites; document unsupported formats and approximations; run bounded-resource benchmarks.
- R9: versioned gene/PGx source ingestion, provenance, schema migration and coverage reports. No claim of comprehensive PGx interpretation.
- R10: transitive SBOM, license review, threat-model verification, accessibility/device/performance evidence and release hardening.

### S — Structure, sequence and genome discovery
- S1: preserve the deterministic viewer payload contract; finish renderer selection only after R1 WebView feasibility and exact license review.
- S2–S5: build fixed reference structures, metrics, variant mapping, approved prediction feasibility and benchmark/export workflow with independent tolerances.
- S6–S9: define typed evidence schemas and versioned reference-pack manifests; build unknown-sequence triage, genome annotation, genetic-code hypotheses and protein-family/structure mapping only as their R4/R5 and data dependencies pass.
- S10: model/data/compute/license/biosafety feasibility and literature/benchmark review only. Candidate generation remains gated until all explicit approvals and validation requirements pass.

### I — In-silico laboratory
- I1: begin with deterministic ligand/SDF validation and physicochemical descriptor baselines that reuse R6 chemistry foundations. Clearly label heuristic descriptors and applicability domains.
- I2: specify docking request/result schemas, node isolation and benchmark design; no docking engine or weights are bundled before license/security review.
- I3: define molecular-dynamics input validation, reproducibility metadata and energy/stability benchmark protocol; engine integration waits for node and license approval.
- I4: create an ADMET/PK/PD/PBPK model inventory and data/license audit; no performance claims before held-out external validation.
- I5: define research-only variant-effect/virtual-cohort simulation schemas and bias/ancestry review. No real cohorts or clinical outputs.

### P — Precision medicine (PGx first)
- P0 remains **blocked** until the intended-use, legal/ethics/regulatory advice, qualified advisers and owner-approved gate packet exist.
- While blocked, only non-patient, public-data preparation is permitted: source inventory, schema/provenance, build/version metadata, test fixtures and coverage methodology.
- P1–P4 implementation that could be mistaken for patient interpretation remains gated by P0 and relevant caller/reference/guideline licenses. Do not infer missing star alleles, diplotypes or phenotypes; indeterminate is a valid result.
- P5–P7 remain blocked pending qualified review, ethics/regulatory approvals and prior phase evidence.

## Research-paper readiness (G5)

Prepare a platform/software-methods paper only after R1–R3 evidence is complete enough to reproduce the methods. Maintain a claim-to-evidence ledger; no planned feature may appear as a completed result.

Required paper package:
- Research question, intended scope, contribution statement and explicit non-clinical intended use.
- Architecture and execution environment, exact hardware/OS/runtime/toolchain versions.
- Versioned methods, algorithms, parameters, seeds, reference dataset accessions/releases/licenses and input checksums.
- Prespecified benchmark protocol, train/validation/test separation where relevant, baselines, metrics, tolerances and statistical analysis plan.
- Independent reference comparisons, positive/negative fixtures, failure analysis, missingness, applicability domain and uncertainty/calibration.
- Resource measurements: runtime, peak memory, storage, energy where measurable, network transfer and device classes.
- Reproduction scripts, environment lockfiles, data acquisition instructions, output hashes and immutable CI run/commit references.
- SBOM and license/attribution inventory for code, dependencies, models, databases and assets.
- Threat/privacy review; confirm no patient data or unsupported clinical claims.
- Figures/tables generated from committed machine-readable results, with scripts and captions.
- Authorship/contributions, affiliations, funding, competing interests, ethics statements, data/code availability and venue requirements reviewed by the owner before submission.

## Publication gates and paper sequence

1. **Paper 1 — Platform/software methods:** candidate only after R1–R3 exit evidence, independent reference validation, reproducible builds, complete relevant license/SBOM review and owner approval.
2. **Domain papers:** one at a time after the relevant R/S/I/P phase has independent external validation and reproducible benchmarks. Do not combine unvalidated domains into a broad performance claim.
3. **No paper submission** based solely on green CI, unit tests, feature checklists or generated screenshots. A passing test proves only the tested software behaviour.

## Historical immediate next deliverables (not current sequencing instructions)

- A claim/evidence ledger and manuscript skeleton under `paper/`.
- A validation protocol and machine-readable result schema under `validation/`.
- I1 descriptor correctness tests and public reference fixtures, reusing existing R6 primitives.
- S6/S7 reference-pack manifest and sequence-evidence schema, without implying full annotation.
- P-track public-data source/license inventory only; P0 remains blocked.
- R1/R2 runtime checklist and R3 independent kinetics reference comparison.

## Status vocabulary

- `planned`: scoped but no implementation evidence.
- `in-progress`: implementation or validation work has started; specify exactly which.
- `implemented`: source path and automated tests exist.
- `validated`: independent reference/benchmark evidence exists and is linked.
- `device-verified`: named physical/emulated device evidence exists.
- `blocked`: a named dependency or formal gate prevents the next action.
- `done`: all roadmap exit criteria and owner approval are recorded.
