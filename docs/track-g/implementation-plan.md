# Track G — governance, assurance and publication readiness

**Status:** Track G implementation in progress (2026-11-12); G0–G7 engineering controls are being built and audited. Formal Track G acceptance remains OPEN.  
**Sequence:** Track G follows the Track P engineering exit. Track U follows Track G in the current **R → S → I → P → G → U** order (D-023). P's software workflow #43131601029 passed 9/9 jobs on commit `553056b3c51373913e8c8936802971fbd532f4e0`. The subsequent README-only main workflow #43135437515 is pending; current-head G acceptance therefore still requires its own exact-head CI. G engineering work has started under the owner's instruction. Further U implementation begins only after G's two-step gate is assessed and reported. Existing partial U0–U3 work is retained as a pre-existing baseline.  
**Scope:** research-only governance for the unreleased Kinetics platform. This plan is not a legal opinion, ethics determination, security certification, QMS certification, regulatory clearance or publication endorsement.

## 1. Purpose

Track G turns Kinetics' existing governance principles into verifiable, maintained controls. It must connect project claims to evidence, make residual risks visible, and prevent software status from being confused with scientific, device, legal, privacy or regulatory acceptance.

G is a cross-cutting assurance track. It does not authorize patient data, human-subject research, clinical interpretation, clinical decision support, remote sensitive-data processing or regulated deployment. P0 remains NOT APPROVED unless and until its independent prerequisites and formal owner decision are satisfied.

## 2. Existing baseline inspected

The repository already contains:
- Root Apache-2.0 project license and a third-party inventory with candidate-only engine assessments.
- Source-dependency SPDX generation and CI checks, plus a generated source dependency SBOM.
- Initial G0 control/evidence register at `docs/track-g/control-evidence-register.md`, covering G0–G7 controls and open external blockers; owner acceptance and named role assignment remain pending.
- Engineering threat models at `governance/threat-model.md` and `docs/security-threat-model.md`, both explicitly not independent assessments.
- `SECURITY.md` and `PRIVACY.md` with unreleased-project boundaries and future requirements.
- Dataset intake policy, validation evidence index, pinned synthetic/software-reference comparison jobs and reproducibility manifests.
- P0 evidence packet, P-specific control drafts, risk-control schema and jurisdiction evidence contracts.
- Research Mode and patient-data restrictions in P-track documentation and schemas.

These are useful foundations, not evidence that all controls are operating or independently approved. The third-party register itself states that no scientific engine/model/database is approved for product bundling.

## 3. Current execution status (2026-11-12)

- **P prerequisite evidence:** workflow #43131601029 completed successfully with 9/9 jobs on commit `553056b3c51373913e8c8936802971fbd532f4e0`. This is the recorded P software verification evidence; it does not close P0 or external gates. A later README-only workflow #43135437515 is pending at the time of this update.
- **G0:** canonical register, status vocabulary, role/cadence model and initial requirements traceability are present. Owner acceptance of governance policy and named non-owner role appointments remain open.
- **G1:** security threat model now has a canonical app/data/native/WebView/supply-chain scope; UI threat cases are maintained as a scoped supplement. A 16-case security verification matrix exists; fuzzing, device tests, vulnerability-channel exercise and independent assessment remain open.
- **G2:** source-only SPDX limitations are explicit; exact artifact/data/model license decisions and resolved transitive dependency coverage remain open. No scientific engine/model/database is approved for bundling.
- **G3:** requirements traceability, blank CAPA register and release evidence controls are present; test-level coverage, operating review records and QMS applicability advice remain open.
- **G4:** source-level data-flow inventory reflects the inspected manifest and policies; merged-manifest, provider/device behavior, qualified privacy advice and jurisdiction decisions remain open.
- **G5:** generated capability-claims matrix covers 130 registry entries and does not imply scientific validation; independent truth sets, subgroup analysis and reviewer-approved protocols remain open.
- **G6:** publication integrity protocol and existing empty claim ledger are linked; authorship declarations, reproducible literature review and peer/editor decisions remain open.
- **G7:** incident/stop-work/rollback/access/recovery procedures and tabletop templates exist; no tabletop, access review or recovery exercise is claimed complete.
- **Track U:** remains sixth in the approved order and does not start until G's two-step gate is assessed and reported.

## 4. Work packages

| ID | Work package | Engineering deliverables | Independent / owner evidence still required |
|---|---|---|---|
| G0 | Governance map and claims register | Canonical control/evidence index; accountable role per control; status vocabulary; traceability from requirement to implementation, test, reviewer and decision | Owner acceptance of governance policy and named accountable people |
| G1 | Security assurance | Threat-model reconciliation; attack-surface inventory; security requirements; abuse-case tests; vulnerability and incident workflow; release security checklist | Independent mobile/application security assessment, remediation review and owner residual-risk decision |
| G2 | Licensing and supply chain | Exact dependency inventory; direct/transitive SBOM; license and notice mapping; source/data/model register; reproducible SBOM generation; provenance and update policy | Exact-artifact legal/license review, data redistribution decisions and explicit owner approval for each bundled component |
| G3 | Software quality system | Requirements-to-test traceability; design/code review records; change control; defect/CAPA workflow; build provenance; release checklist; evidence retention | QMS applicability advice and owner approval; external audit/certification only if actually required and obtained |
| G4 | Privacy and data governance | Data-flow and asset inventory; data classification; minimisation, retention, deletion, backup/export and access-control requirements; privacy test matrix | Qualified privacy/legal assessment, lawful-basis and jurisdiction decisions, DPIA where applicable |
| G5 | Scientific integrity and bias | Capability claims register; validation protocol templates; dataset provenance; subgroup/coverage and missingness reporting; uncertainty/abstention rules; benchmark separation | Independent domain reviewers, governed truth sets, approved protocols and actual validation results |
| G6 | Publication and research integrity | Manuscript claim-to-evidence matrix; methods/reproducibility checklist; authorship/contribution and conflict-of-interest declarations; citation and data/code availability plan | Author approvals, external peer review and journal/editor decisions |
| G7 | Operational governance | Incident response, stop-work, change/rollback, release authorization, access review, backup/recovery and periodic governance review records | Named responsible operators, tested exercises and owner acceptance |

## 5. Execution order

1. **G0 — inventory and evidence map:** reconcile existing policies, schemas, scripts, CI jobs and evidence records; identify duplicates and missing owners.
2. **G1 — security:** resolve the two threat-model documents into one canonical control map without deleting history; add testable abuse cases and vulnerability response evidence.
3. **G2 — licensing/supply chain:** make the SBOM complete for the actual build graph, distinguish source inventory from resolved/bundled artifacts, and prohibit unreviewed engine/model/data bundling.
4. **G3 — quality:** add traceability and release/defect controls proportionate to a research-only software project.
5. **G4 — privacy/data:** verify current no-patient-data boundary and document all app data flows, storage/export/backup behavior and retention decisions.
6. **G5 — scientific integrity:** ensure each capability's claims are no stronger than its evidence; establish independent benchmark protocols and subgroup reporting.
7. **G6 — publication:** prepare a manuscript evidence matrix only after methods/results are reproducible; do not write unsupported novelty, accuracy or impact claims.
8. **G7 — operations:** test governance workflows and establish periodic review.

Each package will be implemented in small auditable increments, with exact-head CI and separate external evidence status.

## 6. Mandatory invariants

- Research Mode only; patient/clinical data and human-subject activity remain prohibited until all applicable approvals and the formal P0 gate are complete.
- No Clinical Mode, patient-specific interpretation, diagnosis, treatment/dosing recommendation or clinical claims.
- Publicly accessible does not mean licensed for redistribution or commercial use.
- An SPDX file is not proof that every binary, transitive dependency, dataset, model weight, font or asset has been cleared.
- A threat model is not an independent security assessment; a passing CI job is not a penetration test.
- A schema or checklist is not an approval, risk acceptance, ethics decision, regulatory classification or QMS certification.
- Synthetic software-reference agreement is not biological/clinical validation or proof of scientific novelty.
- A manuscript claim must point to reproducible data, code, methods and evidence at the exact release/commit.
- Unknown, missing, conflicting or unreviewed evidence remains open; do not convert it to pass by wording.

## 7. Initial exit criteria

Track G engineering scope can be considered implemented only when:
- Every governance control has a stable identifier, accountable role, evidence location, status and review cadence.
- Security, licensing, quality, privacy, scientific integrity and publication claim controls are mapped to tests or explicit external evidence gates.
- SBOM and dependency/license inventories are reproducible and their coverage limitations are explicit.
- Data flows and prohibited-data boundaries are tested, not merely described.
- A release/manuscript claim matrix links every material claim to exact evidence.
- CI passes on the exact final revision and the owner accepts the engineering scope.

Track G overall acceptance remains open until required independent reviews, legal/privacy determinations, owner risk decisions and operational exercises are evidenced. This does not supersede or unlock P0.

## 8. First audit backlog

- Reconcile `governance/threat-model.md` with `docs/security-threat-model.md`; choose one canonical maintained control set and link the other as history or a scoped supplement.
- Determine whether `sbom/source-dependencies.spdx.json` represents source declarations only or the complete resolved/bundled build graph; document gaps and add binary/artifact coverage where feasible.
- Extend `docs/third-party.md` from candidate notes into a per-artifact decision register with exact version, hash, source, license text, attribution, redistribution status, transitive coverage and reviewer evidence.
- Reconcile the current `SECURITY.md` statement about R1–R10 being in progress with the actual track-specific software audit states.
- Add a capability-to-evidence index covering implementation, tests, synthetic references, independent scientific validation, device verification, licensing and release status.
- Inventory Android data flows, permissions, exported components, backup behavior, SAF exports, logs and any optional network/remote-node path.
- Establish a manuscript claims matrix before drafting performance, novelty, accuracy, offline capability or clinical relevance claims.

## 9. Change control

This plan is the Track G planning baseline. Amendments must preserve the distinction between engineering implementation and external acceptance. Any change that would enable patient/clinical data, human-subject activity or Clinical Mode requires a separate formal P0 review and explicit owner decision; Track G work cannot grant that permission.


## 10. Implementation record (2026-11-12)

The following repository artifacts now form the G engineering baseline:
- `docs/track-g/roles-and-review-cadence.md` — accountable role model and review triggers; non-owner appointments are explicitly unassigned.
- `docs/track-g/dependency-decision-register.csv` — exact candidate versions/scopes and unresolved license/hash decisions.
- CI Android job now archives the resolved Gradle debug runtime graph, Cargo dependency tree, Cargo.lock digest and hashes of cached Maven artifacts; this is raw dependency evidence, not yet a complete SPDX SBOM or license clearance.
- `docs/track-g/requirements-traceability.csv` — G0–G7 requirement-to-control map.
- `docs/track-g/capa-register.csv` — blank corrective/preventive action register; no fictitious findings inserted.
- `docs/track-g/security-verification-matrix.md` — 16 security/device/supply-chain verification cases with honest OPEN/PARTIAL status.
- `docs/track-g/data-flow-inventory.md` — source-level inventory based on the inspected manifest and policy files.
- `docs/track-g/capability-claims-matrix.csv` and `scripts/generate_governance_claims.py` — 130 capability entries, conservative claim wording, validation/device/license gaps.
- `docs/track-g/publication-integrity.md` — claim, authorship, reproducibility and submission protocol.
- `docs/track-g/operational-controls.md` — incident, stop-work, access, backup/recovery and tabletop procedures.
- `scripts/check_governance.py` and `tests/test_governance.py` — structural validation of governance artifacts and control traceability.

These files are implementation evidence, not evidence that external reviews or operating exercises have passed. The exact-head CI result and any failures must be appended after the final G code/doc increment.
