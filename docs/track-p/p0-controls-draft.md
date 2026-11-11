# P0 — Internal control and validation drafts

**Status: DRAFT — FOR OWNER / QUALIFIED REVIEW — NOT APPROVED.**  
**Applies to:** current public-non-patient metadata and synthetic-fixture engineering only.  
**Does not authorize:** patient data, human-subject research, clinical interpretation, clinical decision support, prospective evaluation or regulated deployment.

This document turns the P0 evidence register into concrete engineering drafts. It does not establish a lawful basis, classify the product in any jurisdiction, constitute a privacy impact assessment approved by a competent party, prove security controls, certify a QMS or validate clinical performance.

## 1. Intended-use and claims register (draft)

| Field | Draft position | Review status |
|---|---|---|
| Current product purpose | Offline-first computational biology / in-silico research workbench | Owner and qualified reviewer confirmation pending |
| Current permitted inputs | Generated synthetic fixtures; public non-patient source metadata; exact public resources only after source-specific terms review | Enforced engineering boundary is partial; independent security review pending |
| Current outputs | Exploratory computational summaries with input digest, reference/build provenance, method/version and limitations where implemented | Per-capability verification and wording review pending |
| Proposed users | Bioinformatics / computational-biology researchers and software engineers; final user population not approved | Owner/adviser review pending |
| Deployment | Android application and research software; public deployment and supported device claims not approved | Device and release evidence pending |
| Excluded uses | Patient-specific diagnosis, risk scoring, treatment/medication selection, dosing, prescribing, clinical decision support and patient-facing reports | Must remain disabled |
| Human-subject use | No recruitment, consent, intervention or prospective evaluation | Ethics determination required before any such activity |
| Jurisdictions | Not yet enumerated for any clinical or patient-data use | Qualified local legal/regulatory review required |
| Claims | No clinical validity, clinical utility, regulatory compliance or diagnostic accuracy claims | Claims review required before publication/release |

The eventual PGx objective is a research direction only. A capability name, parser, catalogue entry or synthetic fixture is not evidence of an allele caller, phenotype predictor, clinical recommendation or validated medical product.

## 2. Data inventory and governance boundary (draft)

### 2.1 Data classes

| Class | Current disposition | Intake rule |
|---|---|---|
| Generated synthetic fixtures | Allowed for software tests | Label as synthetic; deterministic provenance where practical; never represent as biological cohort evidence |
| Public source metadata | Allowed for catalogue discovery | Metadata only; source terms and attribution still require review |
| Public non-patient payloads | Not yet approved by default | Exact accession/release, terms, attribution, intended use and digest must be reviewed before retrieval/retention |
| Patient / clinical records | Prohibited | No import, storage, transfer, processing or testing |
| Human-subject / identifiable data | Prohibited | No recruitment, consent collection, intervention or analysis |
| Unknown-provenance data | Prohibited | Quarantine outside the application; do not infer non-patient status |

### 2.2 Data minimisation and lifecycle

- Collect no direct identifiers, patient records, sample identifiers or individual-level clinical data in Track P before formal P0 approval.
- Keep the committed public dataset catalogue metadata-only. An empty entries array means no payload is approved or acquired.
- For any future public non-patient payload, record exact accession/version, source and licence URLs, terms, attribution, retrieval timestamp, intended use, SHA-256, storage location, retention owner and known limitations before intake.
- Do not treat a URL, public availability, repository licence or owner authorization as permission to redistribute a third-party resource.
- Do not place secrets, credentials, private keys or sensitive records in source control, CI logs, fixtures or issue reports.
- Retention/deletion periods, controller/processor roles, lawful basis, data-subject handling, cross-border transfer and breach notification obligations remain undetermined pending qualified jurisdiction-specific advice.

### 2.3 Data-flow boundary

Current intended flow is: synthetic fixture / reviewed public non-patient source → bounded parser → validated schema → provenance-bearing exploratory result. The flow must fail closed on malformed input, unverified source terms, unsupported variant representations or mismatched reference metadata. No clinical system, patient repository or external clinical service is connected or authorized.

## 3. P-specific threat-model draft

| Asset / boundary | Threat | Proposed control | Evidence status |
|---|---|---|---|
| Input file → parser | Oversized, malformed or adversarial VCF causes resource exhaustion or parser confusion | Byte, variant and sample limits; strict field/allele validation; reject unsupported ploidy and symbolic alleles | Synthetic tests and CI cover selected cases; fuzzing and independent security review pending |
| Source metadata → catalogue | Malicious URL, false licence claim or changed upstream release | HTTPS metadata schema; exact accession/version; terms review; content digest | Catalogue schema/checker tests exist; human terms review and retrieval verification pending |
| Reference sequence → normalizer | Wrong assembly/contig, tampered sequence or coordinate convention | Explicit assembly/accession/release/contig; 1-based coordinates; sequence SHA-256; REF match; abstain on mismatch | Synthetic reference tests exist; authoritative reference concordance pending |
| Parser → result schema | Extra fields or accidental sample/genotype disclosure | Aggregate-only result schema; additional properties rejected; no sample IDs in output | Schema and synthetic tests exist; broader privacy review pending |
| Source tree / build → artifact | Dependency compromise or unreviewed licence | Pinned build inputs where configured; direct dependency SPDX inventory; review exact transitive binaries/data | Direct source inventory CI exists; full transitive and data/model licence review pending |
| Local device / storage | Loss, theft, backup leakage or insecure export | Minimise retained data; platform storage controls; documented export and deletion behaviour | Existing platform controls require P-specific review and device testing |
| CI / logs / artifacts | Sensitive content or secrets exposed | Synthetic-only CI fixtures; secret scanning and least-privilege workflow permissions | Workflow permissions and synthetic tests exist; full security assessment pending |

### Abuse cases to verify

1. A user labels a patient file as synthetic. The data_classification argument is a caller assertion, not a detector; it must never be described as a privacy filter. Before any real-data workflow, a separately governed intake boundary and qualified privacy/security review are required.
2. An attacker supplies a huge or malformed VCF. Limits and parser errors must prevent unbounded processing and fail closed.
3. A reference digest or build label is altered. Validation must reject mismatches rather than silently normalize against the wrong sequence.
4. A candidate dataset is presented as licensed because its website is public. The catalogue must keep it verify_before_intake until exact terms are reviewed.
5. An exploratory result is presented as a clinical recommendation. UI, API, documentation and publication language must prohibit that interpretation.

No security control is considered verified solely because it is listed here. Add test IDs, reviewer, date and evidence link before closing each threat.

## 4. Software quality lifecycle draft

| Control | Minimum project practice | Evidence / state |
|---|---|---|
| Requirements | Stable requirement ID, intended use, acceptance criteria and risk link for each capability | Track-specific requirements and roadmap exist; full P traceability matrix pending |
| Architecture | Record component owner, caller/callee, data classification, contract version and failure behaviour | Engineering integration standard and JSON Schemas exist; P-specific review pending |
| Implementation | Peer review; bounded parsing; explicit error/abstention; no hidden coercion | Repository review and regression tests; independent review pending |
| Verification | Unit, negative, schema, integration and exact-head CI tests; preserve logs and commit SHA | CI workflow exists; P1 exact-head run in progress at time of draft |
| Scientific validation | Separate software tests from independent truth-set/reference concordance | Synthetic tests exist; independent P validation not performed |
| Defect handling | Record severity, affected versions, reproduction, root cause, corrective action and retest | Repository issues/session log available; formal CAPA procedure pending |
| Change control | Atomic commits, reviewable diffs, exact-head verification, decision/roadmap/session updates | Existing practice; owner approval and audit sampling pending |
| Release | Build provenance, artifact hashes, SBOM/licence review, security/privacy review and owner release decision | CI artifacts available; no P-track production release authorized |
| Monitoring / withdrawal | Incident triggers, disablement, user notice and retained audit trail | Draft in Section 6; operational exercise pending |

This is a proposed lightweight software quality process, not an ISO 13485, IEC 62304 or other QMS certification or compliance claim. Applicability and required controls must be determined by qualified advisers for the intended use and jurisdictions.

## 5. Staged independent validation plan (draft)

| Phase | Test material | Metrics / acceptance questions | Current state |
|---|---|---|---|
| P1 synthetic reference handling | Deterministic synthetic contigs and known small variants | Exact assembly/contig/digest binding; 1-based coordinate correctness; REF match; normalized representation; explicit abstention | Software tests exist; independent reference comparison pending |
| P1 synthetic genotype QC | Generated diploid VCF fixtures with known missingness, phase and ALT counts | Call rate, missingness, heterozygosity, alternate-allele counts, malformed input rejection, resource bounds, no sample-level output | Software tests exist; CI verification for latest change pending |
| P1 source metadata | Candidate source records and synthetic catalogue entries | Schema correctness, HTTPS URLs, canonical IDs, required licence URL, evidence before approval | Metadata gate exists; exact-source legal review pending |
| P2 allele definition research | Licensed, version-pinned allele-definition sets and independently prepared synthetic calls | Exact-tool/reference concordance; ambiguous/no-call rates; unsupported structural/CNV/phase cases abstain | Not started; depends on P1, source terms and qualified review |
| P3 guideline mapping | Versioned, permitted guideline sources and curated test cases | Correct source/version mapping, traceability, no extrapolation, explicit evidence limitations | Not started; licensing and adviser review required |
| P4 evidence assistant | Curated evidence records with adjudicated positive/negative/uncertain examples | Provenance completeness, reviewer agreement, abstention and correction traceability | Not started; human curator and source permissions required |
| P5 usability / human study | Approved protocol and recruited participants, if applicable | Pre-registered endpoints, ethics oversight, usability/safety outcomes | Not started; competent ethics determination and approval required |
| P6 internal validation | Approved intended-use requirements, risk controls and audit logs | Requirements coverage, security controls, residual risk and independent verification | Not started; P0 and P1–P5 gates required |
| P7 prospective evaluation / regulatory planning | Only under approved protocol and jurisdiction-specific advice | Protocol-defined outcomes and oversight; regulatory evidence as applicable | Not started; no prospective activity authorized |

No clinical threshold, sensitivity/specificity, ancestry fairness, clinical utility or prospective performance claim is established by synthetic tests. Acceptance criteria for any future real-world use must be pre-specified and approved by independent reviewers before evaluation.

## 6. Stop-work, incident and withdrawal draft

### Immediate stop triggers
- Any patient, clinical, identifiable or human-subject data enters an unapproved workflow.
- A source's non-patient status, licence or permitted use becomes unclear or is challenged.
- A reference/build mismatch, parser defect, data leak, security compromise or unexplained output discrepancy is detected.
- A user-facing screen, API, report or publication could reasonably be read as diagnosis, treatment, dosing or patient-specific advice.
- A required legal, ethics, privacy, security or scientific gate is missing, expired or withdrawn.

### Response sequence
1. Stop the affected intake, processing, export or capability; do not continue with a guessed workaround.
2. Preserve the minimum necessary audit evidence (commit, build, error, source digest and timestamps) without copying sensitive payloads into logs or tickets.
3. Notify the project owner and the designated security/privacy lead; escalate to qualified legal/ethics/clinical contacts where the incident requires it.
4. Quarantine the affected source/result and revoke or disable the affected capability or release if safe to do so.
5. Assess scope, exposure, affected versions and applicable notification obligations with qualified advisers; do not make unsupported legal conclusions.
6. Record root cause, corrective/preventive actions, verification and residual risk.
7. Reopen only after documented review, required external determinations and a separate owner decision.

### Roles and unresolved operations
The project owner is accountable for internal stop-work and release decisions. Named security, privacy, clinical/scientific and legal leads have not yet been appointed in this packet. Contact paths, notification deadlines, backup/recovery and operational exercises remain open and must be completed before any gated activity.

## 7. Required review and sign-off record

For each section, record: reviewer name/role, competence and conflicts, organization, jurisdiction/scope, review date, comments, evidence link, unresolved findings, disposition and signature/approval method. Do not populate reviewer identity or approval status until an actual review occurs.

**Current disposition:** all sections above are engineering drafts only. P0 remains **BLOCKED / NOT APPROVED**. No patient/human-subject activity, individual PGx interpretation, clinical recommendation or Clinical Mode is enabled.
