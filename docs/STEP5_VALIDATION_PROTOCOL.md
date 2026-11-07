# Step 5 — Scientific validation and benchmarking protocol

> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

## Status and scope

This is the pre-execution protocol for Step 5. It defines analysis before any
real held-out results are inspected. No benchmark result, model superiority,
external validity, or calibrated uncertainty is claimed by this document.

Km and kcat are separate endpoints and must be evaluated in separate runs,
with canonical units M and s^-1 respectively and log10 targets recorded.

## Benchmark regimes

1. **Protein-cold:** protein sequence clusters in test are absent from train.
2. **Scaffold-cold:** chemical scaffold groups in test are absent from train.
3. **Double-cold:** both protein cluster and substrate scaffold are held out.
   Cross-quadrant rows are excluded and counted, never reassigned silently.
4. **External shift:** source, organism, assay, or time-held-out evaluation only
   where the reviewed source provides reliable identifiers and sufficient rows.

Freeze the exact row IDs, group mappings, split seed, software versions, source
release hash, feature archive hashes, and partition manifest before fitting.
Any change to grouping thresholds, standardization, or source snapshot creates
a new benchmark version.

## Selection and scoring

- Candidate/model selection uses training data only, with grouped CV matching
  the intended cold-start axis. Row-random CV is diagnostic only.
- The final held-out archive is scored once after selection. It must not guide
  model, hyperparameter, feature, or threshold selection.
- Compare the classical baseline and Kinetics-Multi on identical rows,
  feature availability, target definition, and frozen partitions.
- Report n, missingness, exclusions, log10 MAE/RMSE/R², original-unit MAE/RMSE,
  median absolute relative error, and median fold error.
- Report predeclared subgroup metrics and sample sizes; retain small groups as
  visible but underpowered rather than suppressing them.
- Report ablations only when the data and feature pipeline support fair,
  matched comparisons (sequence, chemistry, graph summaries, assay context).

## Uncertainty and statistical interpretation

The benchmark implementation reports deterministic paired-row percentile
bootstrap intervals for held-out log10 MAE/RMSE and, when group arrays are
provided, separate paired cluster-bootstrap intervals for each declared held-out
axis. Cluster bootstrap resamples unique groups and retains all rows within each
sampled group. These intervals are still limited by the number and representativeness
of held-out groups and do not address dataset shift or model-selection bias.

Conformal intervals must use a separate calibration partition, report empirical
coverage and width, and never use the final test partition for calibration.
Applicability-domain scores are diagnostics, not probabilities or calibrated
confidence.

## Contamination and integrity checks

Before scoring, verify:
- no source-record or canonical observation ID overlap across partitions;
- no overlap on every declared cold-start group axis;
- no test-set access during feature/model selection;
- source, license, unit, identity and aggregation semantics are reviewed;
- feature sidecar hashes, row counts, target, and representation revisions match;
- all failed runs, exclusions, and protocol deviations are retained.

## Required report artifacts

Each benchmark run must retain:
- benchmark card and protocol version;
- immutable dataset/release and feature archive manifests;
- split/group manifest and leakage audit;
- configuration, random seeds, software/model revisions;
- per-fold selection results and untouched held-out predictions;
- metrics, confidence intervals, subgroup and applicability diagnostics;
- model card, experiment manifest, and independent reproduction record.

## Current blockers

Scientific execution is blocked until Step 2 supplies a reviewed immutable real-data
release and Step 3 supplies actual pinned ESM-2/MMseqs2 execution plus numerical
repeatability evidence. The software can be exercised on synthetic fixtures, but
those fixtures cannot satisfy scientific acceptance. Synthetic fixtures may test software behavior but are
not scientific validation data.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
