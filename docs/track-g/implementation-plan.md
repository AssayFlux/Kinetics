# Track G — governance, assurance and publication readiness

**Status:** planning baseline created 2026-11-12; implementation not yet accepted.  
**Sequence:** Track G follows the Track P engineering exit. G planning and inventory may proceed now; G implementation is sequenced after P's exact-head software verification is green.  
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

- **G0 inventory:** initial control/evidence register drafted at `docs/track-g/control-evidence-register.md`, covering G0–G7 controls, current evidence, accountable role categories, next actions and external blockers. It is a draft; named role assignment and owner acceptance remain open.
- **G1–G7 implementation:** not yet accepted as started. Under D-019's strict R → S → I → P → G sequence, implementation proceeds after Track P exact-head software verification. Track P's latest workflow #43131601029 has passed Python (531 passed, 9 optional skips), reference/engine smoke, SPDX and Node security jobs; Android APK/AAB build is still running. No P closure or G implementation start is declared while that job is pending.

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
