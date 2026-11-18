# Potential Research Project

**Status: DORMANT — OWNER ACTIVATION REQUIRED**  
**Activation authority:** repository owner only.  
**Effective date:** 2026-11-18.

> This file is an archive and planning register. It is not an executable specification, runtime configuration, feature flag, approval, ethics authorization, clinical authorization, dataset licence, or permission to process patient data. No workflow, CI job, app screen, service, agent, model, script, or contributor may activate any item in this file until the owner gives an explicit written instruction identifying the scope to activate.

## 1. Dormancy contract

1. Everything catalogued here is future research material only.
2. Do not add these plans to app navigation, capability registries, service dispatchers, scheduled jobs, CI release gates, background workers, or production defaults.
3. Do not download, ingest, train on, curate, publish, or process research datasets merely because they are listed here.
4. Do not enable patient-specific interpretation, diagnosis, treatment/dosing recommendations, clinical decision support, or clinical mode through this archive.
5. A future activation requires an explicit owner instruction and a separate scope review covering purpose, methods, datasets, licences, provenance, privacy, security, validation, compute, and applicable institutional/legal/clinical approvals.
6. Keep this archive non-executable. Any future implementation must be separately designed, reviewed, tested, and merged as normal software changes.
7. If a document listed below changes, update this index; do not silently activate its contents.

## 2. Archived research and scientific rule documents

The source documents remain preserved at their existing paths. This index gathers them into one dormant research-project register without moving or deleting source files that the current engineering build may reference.

### Research architecture and boundaries
- `docs/research-platform-implementation.md` — research platform implementation inventory, limitations and outstanding validation.
- `docs/track-i/research-boundaries.md` — molecular descriptors, docking, molecular dynamics, ADMET/PK/PD/PBPK and variant research boundaries.
- `docs/track-u/u5-genomics-pgx-research.md` — genomics/PGx research scope, evidence and implementation limitations.
- `docs/track-u/public-database-retrieval-rulebook.md` — public database retrieval, parsing, canonical records, provenance and engine obligations.
- `docs/research-grade-readiness-audit-2026-11-12.md` — research-readiness audit and open evidence.
- `docs/track-u/completion-audit.md` — Track U implementation/integration status and remaining gaps.

### Ethics, privacy, security and governance references
- `docs/track-p/p5-ethics-protocol-template.md` — future protocol template; not an approval.
- `docs/ethics-committee/engineering-evidence-brief.md` — engineering evidence brief; not committee authorization.
- `docs/track-u/u2-security-privacy.md` — security and privacy engineering requirements.
- `PRIVACY.md` — product privacy commitments and handling boundaries.
- `SECURITY.md` — vulnerability reporting and security policy.
- `governance/threat-model.md` and `docs/security-threat-model.md` — threat and mitigation records.
- `docs/BASELINE_GOVERNANCE.md` — release and change-control governance.

### Machine-readable schemas, catalogues and validation assets
- `api/pgx-curation-record.schema.json`
- `api/pgx-guideline-evidence.schema.json`
- `api/admet-validation.schema.json`
- `data/admet-source-catalog.yaml`
- `api/admet-source-catalog.schema.json`
- `validation/DATASET-INTAKE.md`
- `validation/README.md`
- `validation/RESULT-MANIFEST.md`
- `validation/reproduction_jobs.yaml`
- `tests/test_research_primitives.py`, `tests/test_genomics.py`, `tests/test_pgx.py`, `tests/test_admet_validation.py`

These assets may be used by ordinary software tests where they are already part of the current build. Their presence does not authorize a research study, dataset intake, model training, or clinical use.

## 3. Research themes reserved for future owner activation

- Sequence, genomics, transcriptomics, phylogenetics and variant research.
- Pharmacogenomics and guideline-evidence curation.
- Protein structures, molecular geometry, docking and molecular dynamics.
- Chemistry, molecular descriptors, reaction and property modelling.
- ADMET, pharmacokinetics, pharmacodynamics and PBPK research.
- Public scientific database retrieval, dataset curation and reproducible benchmarking.
- Statistical, physics-based, rule-based and AI/ML methods with explicit method labels.
- Research-grade provenance, uncertainty, applicability-domain and reproducibility frameworks.

## 4. Dataset and evidence intake rules (dormant)

Candidate public sources named in existing research documents are leads only, not approved datasets. Before any future intake, record exact release/version, canonical source URL, licence and redistribution terms, checksum, retrieval date, schema, units, assay/measurement context, exclusions, missingness, provenance, intended use and validation plan. Do not place patient-identifiable or confidential research data in GitHub, CI logs, public issues, or public artifacts.

## 5. Engineering freedom versus research activation

Normal product engineering may continue without activating this research archive. Build, UI, navigation, local storage, packaging, offline behaviour, generic import/export, software quality, performance, accessibility, and non-clinical utility work are not to be held up solely because a future research protocol, dataset, scientific validation programme, or ethics committee review is pending.

The following remain mandatory independent engineering safeguards and are not waived by this separation: secure handling of any data actually processed, consent and access controls where applicable, protection of sensitive/patient data, secret management, dependency/licence compliance, truthful capability claims, and disabling clinical decision functions unless separately authorized. If a proposed engineering change would process real patient data or expose a clinical function, stop that specific change and obtain the required authorization rather than weakening safeguards.

## 6. Activation record

Current state: **DORMANT**  
Owner activation instruction: **NOT RECEIVED**  
Activated scope: **NONE**  
Research datasets approved by this file: **NONE**  
Clinical capabilities enabled by this file: **NONE**

Only the owner may change this state with an explicit instruction. Do not infer activation from a commit, release, test run, issue, or discussion.
