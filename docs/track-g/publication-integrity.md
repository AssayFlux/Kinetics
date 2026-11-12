# Track G — publication and research integrity protocol

**Status:** protocol draft; no manuscript is approved for submission.  
**Publication strategy:** D-003 calls for multiple evidence-scoped papers over time, beginning with a platform/software-methods paper only when its reproducible evidence is sufficient.

## Claim control

Every material manuscript claim must be represented in `paper/claim-evidence-ledger.csv` and linked to:
- exact source commit and, where applicable, release artifact digest;
- implementation path and reproducible command;
- dataset/source accession, version, checksum, license and intended-use basis;
- protocol, metric, measured result, uncertainty and limitations;
- CI run/artifact and independent reviewer record;
- status that distinguishes implemented, software-tested, independently validated and device-verified.

A blank field is not a positive result. Do not infer accuracy, superiority, novelty, clinical utility, broad generalisability, offline completeness or regulatory suitability from implementation or synthetic fixtures.

## Authorship and contribution

Before submission, each author must:
1. approve the final manuscript and the specific version submitted;
2. document substantive contributions using the target journal's required taxonomy;
3. disclose conflicts, funding, institutional affiliations and relevant relationships;
4. accept responsibility for their contribution and identify a corresponding author;
5. confirm permissions for third-party figures, datasets, software, logos and reproduced text.

No author, affiliation, contribution, funding source, conflict declaration or approval may be invented. The repository owner is not automatically the sole author.

## Methods and reproducibility packet

- Research question, scope and protocol version.
- Software version, exact commit, environment/toolchain and command line.
- Input data source, accession, retrieval date, checksum and license.
- Preprocessing, exclusions, parameters, random seeds and missing-data handling.
- Reference baseline, metrics, tolerances, uncertainty and subgroup/coverage analysis.
- Full outputs, failed runs, deviations and limitations.
- Data/code availability statement and durable archive links where legally permitted.

## Literature and novelty review

Maintain a dated, reproducible search strategy with databases, queries, date range, inclusion/exclusion criteria and screened records. Compare against relevant software and methods, not only a narrow hand-picked set. Novelty or priority language requires documented evidence and qualified co-author review.

## Submission gate

The corresponding author must verify current journal instructions, article type, scope, fees, indexing claims, peer-review model, data/software policy and ethics declarations directly from the journal. Predatory-journal screening and venue fit are required. External peer review and editor decisions cannot be pre-claimed.

## Current restrictions

No clinical effectiveness, patient benefit, diagnosis/treatment performance, clinical deployment or regulatory compliance claims. Current synthetic reference comparisons are software checks only. Manuscript skeletons and strategy notes are planning artifacts, not results.
