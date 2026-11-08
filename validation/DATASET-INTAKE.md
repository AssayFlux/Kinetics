# Public reference-data intake policy

This policy applies to R, S, I and permitted P-track preparation. It does not authorize patient data, human-subject research, clinical interpretation or redistribution of third-party datasets.

## Admission checklist

A dataset or reference pack may enter a reproducible validation job only when every field below is recorded:

- Stable source name, accession/record identifier, version or release date, retrieval date and canonical source URL.
- Explicit data licence/terms and redistribution status; retain the licence text or a durable link. Unknown or incompatible terms mean **do not bundle**.
- Exact input bytes and SHA-256; preserve the original source file and never silently rewrite it.
- Intended scientific role: positive control, negative control, calibration, reference answer, or exploratory example.
- Organism/taxon, molecule type, assembly/reference build, coordinate convention, strand and genetic-code table where applicable.
- Inclusion/exclusion criteria, known caveats, source publication and citation.
- Expected outputs, metric definitions, tolerances, uncertainty method and adjudication procedure.
- Independent reviewer and review date for any result used to support a manuscript claim.

## Separation of data roles

1. **Development fixtures** may guide implementation and must not be presented as independent evaluation.
2. **Validation fixtures** must be frozen before the evaluated implementation/version is assessed.
3. **Exploratory data** may generate hypotheses but cannot establish accuracy or novelty.
4. **Patient/clinical data** are out of scope until P0 has explicit legal, ethics, privacy, security and qualified-adviser approval.

## Scientific safeguards

- A no-hit result is not proof of novelty, absence or non-function.
- Predictions and in-silico rankings are hypotheses, not experimental findings.
- Record reference-build and coordinate mismatches as failures, not silent corrections.
- Report missingness, exclusions, class balance, confidence intervals and failure cases.
- Never tune thresholds on the held-out evaluation set.
- Keep all input data, scripts, environment lockfiles, commands and output manifests immutable by commit/hash.

## Release rule

No dataset is described as validated until its licence is checked, inputs are pinned, a reproducible job is committed, tolerances are justified, tests pass, and an independent review is recorded. This document is a process control, not evidence that any dataset has been evaluated.
