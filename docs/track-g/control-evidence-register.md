# Track G0 — governance control and evidence register

**Baseline date:** 2026-11-12  
**Status:** initial inventory drafted; owner acceptance and named accountable people pending.  
**Scope:** research-only software governance. This register is not an approval, certification, legal opinion, ethics determination or independent review.

## Status vocabulary

- **IMPLEMENTED:** repository artifact or code exists.
- **AUTOMATED-CHECK:** an automated check exists; its exact-head result must be cited separately.
- **OPEN:** evidence, implementation, review or decision is missing.
- **NOT-APPLICABLE (JUSTIFIED):** a documented rationale and accountable reviewer are recorded.
- **ACCEPTED:** the named authority has made and recorded the decision. Never infer acceptance from a draft, schema or green CI.

An item remains OPEN when evidence is absent, stale, unreviewed, ambiguous or not linked to the exact release/commit.

## Control register

| ID | Control / required outcome | Current repository evidence | Status | Accountable role | Next action / acceptance evidence |
|---|---|---|---|---|---|
| G0-01 | Single governance index with stable IDs, status vocabulary and evidence links | This register; docs/track-g/implementation-plan.md | IMPLEMENTED — draft | Project owner | Owner reviews register; name control owners and review cadence |
| G0-02 | Track/phase status reflects evidence, not aspiration | ROADMAP.md, docs/README.md, per-track plans | OPEN | Project owner + engineering lead | Reconcile stale status statements; exact-head links and explicit carry-forward register |
| G0-03 | Every capability claim maps to implementation, tests, validation, device evidence and limits | capabilities/registry.yaml; validation/README.md | OPEN | Scientific methods lead + engineering lead | Build capability evidence index; do not promote evidence_level none without independent records |
| G0-04 | Decision authority, approval and supersession are recorded | DECISIONS.md | IMPLEMENTED — partial | Project owner | Add missing decision references for G policy adoption and record actual decisions only |
| G0-05 | Requirements and risks map to controls, verification and residual-risk disposition | P0 evidence packet; P-track risk schema; release checklist | OPEN | Risk owner + engineering lead | Create requirement/control/test traceability; qualified reviewer and owner disposition where required |
| G0-06 | Change history and evidence remain auditable | SESSION_LOG.md, CHANGELOG.md, CI artifacts | IMPLEMENTED — partial | Engineering lead | Link each substantial change to PR/commit, exact-head CI and evidence artifact |
| G1-01 | Threat model covers app, imports, storage, native/runtime, WebView, supply chain and optional remote boundary | docs/security-threat-model.md; governance/threat-model.md | OPEN — duplicate scope documents | Security owner | Reconcile into one canonical model and a scoped UI appendix; map each threat to tests and residuals |
| G1-02 | Abuse cases and parser/resource boundaries are tested | Python/Android tests; P parser limits; threat model | OPEN | Security owner + engineering lead | Fuzz parsers, URI lifecycle, process death, storage exhaustion, bridge/origin policy and concurrency |
| G1-03 | Vulnerability reporting and incident handling are operational | SECURITY.md | OPEN | Security owner | Verify private reporting channel; define severity, triage SLA, disclosure, containment and recovery |
| G1-04 | Independent security review and remediation evidence exist | No independent assessment recorded | OPEN — external | Independent security assessor | Commission review, track findings, retest and owner residual-risk decision |
| G2-01 | Direct and transitive build/runtime dependencies are enumerated with exact versions and hashes | scripts/generate_source_sbom.py; sbom/; docs/third-party.md | OPEN — source-only inventory | Supply-chain owner | Generate resolved Gradle/Cargo/Python/build-tool inventories; bind to APK/AAB hashes |
| G2-02 | Every distributed component has license, notices and redistribution decision | LICENSE; docs/third-party.md | OPEN — candidate-only | Legal/licensing reviewer | Exact-artifact/file-level audit, notices, source obligations and explicit bundle approval |
| G2-03 | Datasets, models, reference packs and guideline content have source-specific rights/provenance | data/, datapacks/, docs/third-party.md, P source gates | OPEN | Data steward + legal reviewer | Per-release accession, checksum, terms, intended use, attribution, redistribution and reviewer evidence |
| G2-04 | Build provenance and artifact integrity are reproducible | CI build workflow and artifact hashes | OPEN — partial | Release engineer | Archive exact source, toolchain, resolved graph, artifact digests, provenance attestation and signing evidence |
| G3-01 | Requirements trace to design, code, tests and release claims | Roadmap, registry, tests, release checklist | OPEN | Quality owner | Create stable requirement IDs and traceability matrix |
| G3-02 | Code/design review and change control are recorded | Git history and contribution guidance | OPEN — partial | Engineering lead | Define review evidence and protected-branch/approval expectations; retain PR references |
| G3-03 | Defect, nonconformance and corrective-action process exists | No maintained CAPA register identified | OPEN | Quality owner | Add defect/nonconformance record template, severity, containment, root cause, correction and effectiveness check |
| G3-04 | Release criteria and artifact approvals are enforced | docs/release-checklist.md; docs/release-hardening.md | OPEN — checklist only | Release owner + project owner | Tie release authorization to exact artifact hashes and completed checks |
| G4-01 | Data flows, assets, trust boundaries and storage destinations are inventoried | PRIVACY.md; docs/security-threat-model.md; Android manifest | OPEN — partial | Privacy owner + Android lead | Complete component/permission/URI/storage/log/backup/export/remote-path inventory |
| G4-02 | Data minimisation, retention, deletion, backup and export behavior are tested | Privacy policy and release checklist | OPEN | Privacy owner + Android lead | Add behavior matrix and device/provider tests; document deletion limits and user choices |
| G4-03 | Lawful basis, roles, notices and jurisdiction obligations are determined | No qualified determination recorded | OPEN — external | Qualified privacy/legal adviser | Written jurisdiction-specific advice; DPIA if applicable; owner accepts operational policy |
| G5-01 | Scientific claims are scoped to evidence level and abstention behavior | Capability registry; validation evidence index | OPEN — partial | Scientific methods lead | Capability-by-capability evidence matrix and claim restrictions |
| G5-02 | Independent reference datasets, protocols and metrics are pre-specified | Synthetic reference scripts and validation docs | OPEN — external | Independent domain reviewers | Approve governed truth sets, methods, tolerances, coverage and subgroup analysis |
| G5-03 | Bias, missingness, uncertainty and generalisability are reported | No independent domain report recorded | OPEN | Scientific methods lead + reviewers | Add protocol and results; retain unvalidated status until evidence exists |
| G6-01 | Manuscript claims map to exact code, data, methods and results | paper/manuscript-skeleton.md; publication strategy in D-003 | OPEN | Corresponding author | Create claim-to-evidence matrix before submission |
| G6-02 | Authorship, contributions, conflicts, funding and data/code availability are declared | No completed manuscript declarations recorded | OPEN | All authors + corresponding author | Complete journal-specific declarations and owner review |
| G6-03 | Novelty and journal fit are supported by current literature review | No systematic novelty review recorded | OPEN | Corresponding author + domain co-authors | Conduct reproducible literature/competitor review; avoid priority/best claims without evidence |
| G7-01 | Stop-work, incident, rollback and safe-disablement processes are operational | P0 controls draft and release checklists | OPEN — draft | Project owner + security/privacy owners | Assign decision-makers, test tabletop scenarios and record outcomes |
| G7-02 | Access, secrets, backup/recovery and periodic reviews are governed | Repository/security docs; no completed operational review evidence | OPEN | Operations owner | Inventory access/secrets, test recovery, define review cadence and retain records |
| G7-03 | Governance exceptions and residual risks have accountable acceptance | P6 schema contract only | OPEN | Project owner + risk owner | Record actual risk decisions with scope, rationale, expiry/review date and evidence |

## Current blockers and non-delegable evidence

1. **P0:** remains BLOCKED / NOT APPROVED. No patient/clinical data, human-subject work, individual PGx interpretation, Clinical Mode or regulated deployment.
2. **Independent scientific validation:** synthetic software concordance is not biological/clinical validation.
3. **Legal/licensing/privacy/ethics:** repo owners and code changes cannot substitute for qualified advice, source-specific license decisions or competent ethics determinations.
4. **Independent security review:** no independent penetration/mobile security assessment is recorded.
5. **Device evidence:** CI build/JVM tests do not establish physical-device runtime, lifecycle, accessibility or performance.
6. **Publication:** a paper cannot claim novelty, best-in-class performance, accuracy or impact without reproducible evidence and current comparison.

## Review cadence and evidence retention

- Review this register at every track exit and before every public release or manuscript submission.
- Each status change must include date, reviewer/authority, exact commit or artifact, evidence URI, scope and limitations.
- External evidence must record the issuing organisation/person's qualified role and the exact scope/date; do not upload confidential material without permission.
- Re-open a control when its dependency, intended use, jurisdiction, release artifact or material implementation changes.

**Initial inventory result:** G0 register drafted. G0 is not accepted until owner review, accountable role assignment and evidence links are completed. Track P's exact-head Android build remains pending; strict R → S → I → P → G execution is preserved.
