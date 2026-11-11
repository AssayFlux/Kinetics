# Track P — implementation and verification plan

**Track status:** STARTED 2026-11-11 by project-owner authorization (D-022).  
**Execution model:** two steps — (1) build the documented base; (2) audit, test and fix the base.  
**P0 status:** evidence preparation active; formal gate BLOCKED / NOT APPROVED.  
**Allowed data:** synthetic fixtures and public non-patient metadata/resources only, subject to exact source terms.

## Component ownership and integration boundaries
- **Python:** reference-build metadata, normalization/QC, provenance, scientific comparisons and future research analysis.
- **C++:** performance-critical algorithms only after measured need and reviewed cross-language contract; no independent clinical interpretation logic.
- **Kotlin/Android:** Research Mode workflows, bounded import, local persistence, user-visible provenance and safe failure/abstention states.
- **Rust:** security-sensitive parsing or bounded native components only where an explicit integration contract and tests exist.
- **Shared contracts:** versioned JSON Schema/API contracts; source build, coordinate convention, reference digest, parameters and software versions travel with every result.
- **Data boundary:** no patient records, direct identifiers, human-subject data or individual-level clinical outputs while P0 is not approved.

## Step 1 — build the base

### P0 — governance and safety preparation
1. Draft intended use, excluded use, users, outputs and jurisdiction questions.
2. Create evidence register, data/privacy inventory, threat model, quality lifecycle outline, risk register and stop/incident plan.
3. Identify independent legal, ethics, clinical pharmacology/PGx and scientific determinations required; record evidence owners and status without claiming appointments or approvals.
4. Define independent validation questions, reference truth-set requirements, metrics, subgroup analysis and abstention criteria.
5. Keep every P0 document visibly DRAFT until reviewed and approved by the competent party.

### P1 — public-data and synthetic foundation
1. Maintain metadata-only candidate sources; no source is approved merely because it is public.
2. For future acquired non-patient resources, pin accession/release, exact terms, attribution, retrieval time, intended use and SHA-256; retain provenance and known limitations.
3. Expand synthetic reference-build, contig, coordinate, REF/ALT and normalization fixtures; label every fixture synthetic.
4. Build genotype parsing/QC only against synthetic fixtures until P0 and relevant data-use gates pass. Reject unsupported ploidy, ambiguous build/contig, malformed alleles and uncertain mappings rather than guessing.
5. Keep genotype-to-phenotype interpretation, star-allele calling, diplotype/phenotype assignment and guideline recommendations out of scope until later P gates and qualified review.

### P2–P7 — staged, not started
- **P2:** expandable PGx allele/diplotype/phenotype research after P1 evidence, source/tool licences, adviser review and owner scope decision.
- **P3:** versioned guideline mapping with source licensing and bounded research wording.
- **P4:** evidence assistant with human curator; no autonomous final classification.
- **P5:** adviser review/usability study only after ethics determination and required approvals.
- **P6:** governance, audit, access controls and internal validation; Clinical Mode remains disabled unless separately authorized after all requirements.
- **P7:** jurisdiction-specific regulatory planning and prospective evaluation only under approved protocol and oversight.

## Step 2 — audit, test and fix
- Verify schema contracts and negative cases; malformed, ambiguous, out-of-range and mismatched-reference inputs must fail closed.
- Test deterministic outputs, provenance preservation, coordinate/build conversions and digest tampering with synthetic truth fixtures.
- Review source terms and attribution for every exact acquired release; remove or quarantine unapproved resources.
- Review privacy/security threat controls and confirm no patient-data path is reachable.
- Run exact-head CI after a stable implementation increment; record exact commit, workflow, jobs and skipped/not-run checks.
- Review Research Mode wording; no diagnostic, treatment, dosing or patient-specific recommendations.
- Record defects, risk decisions, evidence links and owner disposition. CI success is not scientific or clinical validation.

## Exit criteria
Each P phase needs documented implementation evidence, exact-source automated tests, applicable independent reference validation, source/licence review, security/privacy review and explicit owner acceptance. P0 additionally requires external determinations and a formal gate decision. Physical-device tests and any human-subject/clinical evaluation are separate evidence classes.

## Current open items
- P0 packet is a draft; all independent review and approval items remain pending.
- Public dataset catalogue has candidate sources only; acquired entries remain empty.
- No patient data, human subjects, individual interpretation, clinical report or Clinical Mode is authorized.
- P1 now includes a bounded aggregate-only synthetic VCF QC module and versioned result schema, with negative tests for malformed alleles, unsupported symbolic alleles, phase separators, missingness, resource limits and unsupported ploidy. Reference/build provenance and left-normalization fixtures remain synthetic-only. Exact-head audit and independent reference concordance are still required.
