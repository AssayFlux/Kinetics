# Proposed research paper outline

This outline is a planning document. It does not assert novelty or results before the corresponding work is completed.

## Working title

Kinetics: a reproducible open-source framework for enzyme kinetic parameter prediction from protein and substrate representations

## 1. Abstract
State the research gap, software contribution, datasets, evaluation design, principal measured findings, and limitations. Complete only after external evaluation.

## 2. Introduction
- Why Km and kcat estimation is challenging.
- Dependence on enzyme sequence, substrate chemistry, construct, and assay context.
- Limitations of random-split-only evaluation.
- Need for transparent curation, reproducible computation, and cold-start benchmarks.
- Clearly state the actual contribution after literature review.

## 3. Software and methods
- Software architecture and API.
- Public dataset sources, licenses, and provenance.
- Target-specific observation model and unit normalization.
- Duplicate/conflict handling and assay-context curation.
- Protein and substrate feature representations.
- Baseline and candidate model families.
- Hyperparameter selection and compute environment.
- Experiment manifests and artifact traceability.

## 4. Evaluation design
- Random split as a diagnostic baseline.
- Protein sequence-cluster holdout.
- Chemical scaffold holdout.
- Double-cold protein/substrate evaluation.
- Temporal or external-source evaluation where available.
- Leakage audits and data overlap checks.

## 5. Results
- Dataset composition and curation attrition.
- Target-specific performance with uncertainty.
- Subgroup and applicability-domain analysis.
- Ablations of protein, chemical, and assay-context features.
- Comparisons against appropriate published baselines.
- Computational cost and reproducibility results.

## 6. Discussion
- Generalization boundaries.
- Assay heterogeneity and missing context.
- Parameter identifiability and uncertainty.
- Failure cases and possible dataset bias.
- Implications for experimental prioritization, without claiming replacement of experiments.

## 7. Software availability
- Repository URL, versioned release, license, citation, installation.
- Reproducibility instructions and data availability statement.
- Hardware and dependency requirements.

## 8. Limitations and conclusion
Report what was not evaluated and avoid causal/mechanistic claims unsupported by the design.
