# P0 — Governance and safety evidence packet

**Status: DRAFT — PREPARATION IN PROGRESS — NOT APPROVED.**  
**Owner authorization:** D-022; Track P preparation authorized 2026-11-11.  
**Formal P0 gate:** BLOCKED / NOT APPROVED.  
**Scope:** engineering-side preparation only; not legal advice, ethics determination, clinical endorsement, regulatory clearance or quality-system certification.

## 1. Draft intended use (owner/adviser review required)
Kinetics is being developed as an offline-first computational biology and in-silico research workbench. Current permitted work is software development, synthetic fixtures and appropriately licensed public non-patient research resources. Outputs are exploratory research artifacts with provenance, limitations and uncertainty; they are not patient-specific medical advice or a substitute for professional judgment.

The eventual PGx research scope is a future objective, not a current authorization. Intended use, users, outputs, deployment model and jurisdictions must be specified and reviewed before patient-related work.

## 2. Prohibited while P0 is not approved
- Patient/clinical record ingestion, storage, transfer or analysis.
- Human-subject recruitment, consent collection, intervention or prospective evaluation.
- Individual genotype-to-phenotype interpretation or patient-specific risk scores.
- Diagnosis, treatment/medication selection or dosing recommendations.
- Clinical decision support, patient-facing reports, Clinical Mode or claims of clinical validity/utility.
- Clinical-system connections or use of data whose non-patient status and permitted use are unclear.

## 3. Evidence register

| ID | Required evidence | Current status | Evidence owner |
|---|---|---|---|
| P0-E01 | Intended-use statement, users, outputs, exclusions and deployment boundaries | Draft here; review pending | Project owner + qualified advisers |
| P0-E02 | Jurisdiction and product classification assessment, including privacy, health-data and medical-device rules | Pending; qualified external advice required | Legal/regulatory adviser |
| P0-E03 | Research ethics / IRB / IEC determination and approval or documented non-applicability, as applicable | Pending; competent ethics determination required | Research lead + ethics body |
| P0-E04 | Qualified clinical pharmacology / PGx and scientific adviser review, conflicts and scope | Pending; no adviser review claimed | Project owner |
| P0-E05 | Data inventory, lawful basis/authority, privacy impact assessment, minimisation, retention/deletion and data-subject handling | To be drafted; no patient intake | Privacy lead / legal adviser |
| P0-E06 | Threat model, security architecture, access control, encryption/key lifecycle, logging, incident response and recovery | Existing security docs need P-specific review | Security owner |
| P0-E07 | Software quality lifecycle: requirements, risk controls, traceability, verification, change control, defect/CAPA and release records | Outline pending; no QMS certification claimed | Engineering + owner |
| P0-E08 | Dataset/source terms, attribution, redistribution and intended-use review for each exact release | Candidate catalogue only; no acquired entries approved | Data curator + legal reviewer |
| P0-E09 | Independent scientific validation strategy, truth sets, metrics, subgroup/bias analysis and abstention | Plan pending; no clinical validation claimed | Independent scientific reviewers |
| P0-E10 | Incident, stop-work, withdrawal, breach escalation and safe disablement procedure | Draft pending | Owner + security/privacy leads |
| P0-E11 | Consolidated risk register with mitigations, residual-risk acceptance and owners | Initial draft below; review pending | Engineering + owner + advisers |
| P0-E12 | Final evidence review and explicit owner P0 gate decision recorded in DECISIONS.md | Not eligible until prerequisites evidenced | Project owner |

## 4. Work products to prepare
- Intended-use and claims register: users, environment, inputs/outputs, foreseeable misuse, exclusions and jurisdiction assumptions.
- Data protection assessment: data-flow inventory, classification, lawful authority, minimisation, purpose limitation, retention/deletion, access, data-subject requests, cross-border transfer and breach response.
- Threat model: assets, trust boundaries, attacker capabilities, abuse cases, controls, residual risks and verification evidence. Do not introduce sensitive data to test this draft.
- Software quality plan: requirements/traceability, architecture review, risk management, code review, reproducible builds, verification, defect handling, change control, release approval and monitoring.
- Scientific validation plan: independent reference sets, inclusion/exclusion criteria, pre-specified metrics, build/coordinate handling, error analysis, calibration, subgroup coverage, uncertainty and abstention.
- Dataset approval record: exact accession/release, source URL, terms, retrieval date, SHA-256, attribution, intended use, known bias, redistribution status and reviewer evidence.
- Stop/withdrawal plan: triggers, responsible decision-maker, disabling affected capabilities, preserving audit evidence and reopening only after documented review.

## 5. Initial risk register (engineering draft)

| Risk | Initial control | Residual status |
|---|---|---|
| Exploratory output mistaken for patient advice | Research-only UX, explicit limitations, no patient workflows or clinical claims | Open; misuse/wording review required |
| Incorrect reference build/coordinate interpretation | Explicit assembly/accession/contig/coordinate contract, digest verification, abstention | Open; independent truth-set concordance required |
| Unlicensed or misused public resource | Candidate-only catalogue; exact-release terms review before intake | Open; human review per source |
| Sensitive data enters an unapproved workflow | Reject patient data at boundaries; no intake path; synthetic fixtures only | Open; threat-model negative tests required |
| Software defect creates misleading output | Bounded schemas, provenance, regression tests, review and traceability | Open; QMS and independent verification plan required |
| Population bias / poor generalisability | Record cohort/source and coverage; subgroup analysis and abstention plan | Open; governed references and adviser review required |
| Security compromise or data exposure | Minimise data, local-first design, threat model, access/key controls, incident plan | Open; security review and verification required |

This is not a completed risk analysis. Severity, likelihood, detectability, acceptability criteria, control verification and residual-risk sign-off require qualified review.

## 6. External determinations and reviews
Repository changes cannot manufacture:
- Jurisdiction-specific legal and regulatory advice for each intended deployment.
- Ethics committee / IRB / IEC determination and approval or documented exemption/non-applicability where appropriate.
- Qualified clinical pharmacology, pharmacogenomics and scientific review.
- Privacy/legal determination of lawful basis, controller/processor roles, consent/data-use terms and cross-border obligations.
- Independent scientific validation and, if required by intended use, prospective clinical evaluation.

The project owner authorizes preparation and may approve internal project decisions. Owner authorization does not replace independent determinations.

## 7. P0 exit checklist
- [ ] Intended use, user groups, outputs, exclusions and jurisdictions are specific and reviewed.
- [ ] Applicable legal/privacy/regulatory requirements have written qualified advice.
- [ ] Ethics/IRB/IEC applicability is determined by the competent body; required approval is obtained.
- [ ] Qualified clinical/scientific advisers have reviewed scope and evidence plan.
- [ ] Privacy impact assessment and data governance are complete.
- [ ] Threat model and security controls are reviewed and tested.
- [ ] Quality lifecycle, traceability, verification and change controls are approved for intended scope.
- [ ] Exact dataset/source terms and data-use rights are reviewed.
- [ ] Independent validation plan and acceptance criteria are approved.
- [ ] Risk register, stop/withdrawal and incident plans are reviewed; residual risks dispositioned.
- [ ] Project owner reviews the complete evidence packet and records the formal P0 decision.

**Until every applicable item is evidenced and the owner records the formal decision, P0 remains NOT APPROVED and all patient/clinical functionality remains disabled.**
