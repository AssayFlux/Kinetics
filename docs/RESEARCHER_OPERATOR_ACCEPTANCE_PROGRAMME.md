# Researcher and operator acceptance and training programme

**Status:** programme definition only. Completion requires recorded sessions and evidence; publishing this procedure is not proof that training or acceptance occurred.

## 1. Purpose and boundaries

Validate the integrated Kinetics scientific and operational platform before starting an end-user application. This programme covers data stewardship, scientific workflows, models and uncertainty, workbench/API, execution, operations, accessibility and support. It does not authorize clinical, diagnostic or regulated use.

Every session records the tested source commit, environment, dataset/model revisions, participant role, facilitator, date, scenario, expected and actual result, defects, retest evidence and sign-off. Use synthetic fixtures until dataset licensing and access are explicitly approved. Never upload confidential or licensed material to an unapproved environment.

## 2. Entry criteria

Do not start production-like acceptance until:
- A versioned deployment candidate and rollback target exist.
- Authentication, tenant isolation and least-privilege roles are configured.
- Data classification and dataset/model access are approved.
- Scientific worker handlers are real, allow-listed and tested; a no-op health check does not qualify.
- Per-job CPU, memory, wall-clock, disk and concurrency limits are enforced at the execution boundary, not merely accepted by the API.
- Job status, cancellation, artifact integrity and append-only audit behavior are observable.
- Backup restoration has been rehearsed in an isolated environment.
- Known limitations and open security/scientific risks are disclosed.

A missing entry criterion means BLOCKED, never PASSED.

## 3. Researcher curriculum

### R1 — Data and provenance
Teach source records vs canonical observations vs derived features vs predictions/reports; stable source IDs, versions, licenses, units, assay conditions, missingness, duplicate/conflicting/censored observations, immutable snapshots and provenance manifests.

**Exercise:** import a reviewed fixture, inspect validation/rejection reports, trace observations to source records and export provenance.

**Pass:** every selected observation is traceable; units and source metadata are retained; rejected rows are accounted for; data use is authorized.

### R2 — Sequence, structure and chemistry
Teach supported sequence/PDB/mmCIF formats, explicit residue mappings, coordinate digests, molecular identifiers, stereochemistry and unsupported structural inferences.

**Exercise:** validate fixture records; inspect digest mismatch, unknown chain, invalid mapping and invalid molecule failures.

**Pass:** valid records retain evidence references; invalid records fail safely; unsupported assembly/alignment/quality inferences are not presented as facts.

### R3 — Features, models and uncertainty
Teach pinned model revisions, feature-cache identity, train/calibration/test separation, group-aware splits, leakage checks, calibration, uncertainty and applicability warnings.

**Exercise:** build features on a permitted benchmark, train a baseline, evaluate on untouched holdout data, inspect uncertainty coverage/width and reproduce from the run manifest.

**Pass:** exact code/model/dataset/configuration revisions are captured; leakage checks pass; limitations are visible; claims match evidence.

### R4 — Prediction and reporting
Teach request validation, supported-domain boundaries, uncertainty interpretation, provenance display and report export.

**Exercise:** run in-domain and out-of-domain predictions, inspect warnings and report provenance, reproduce under documented deterministic settings.

**Pass:** reports link inputs, features, model and source revisions; warnings are visible; predictions are not treated as experimental facts.

### R5 — Workbench and API
Teach authentication, workspace organization, job submission/progress/cancellation, retries, artifacts, audit history and API versioning.

**Exercise:** submit a job, inspect state transitions, cancel a running job, retrieve its artifact and verify cross-tenant access is denied.

**Pass:** cancellation is terminal; artifacts are hash-verified; unauthorized access is denied and audited.

## 4. Operator curriculum

### O1 — Deployment and configuration
Practice immutable image references, identity-provider metadata, managed secrets, database migrations, network boundaries, TLS, KMS and least-privilege IAM. Deploy to non-production, verify readiness and roll back.

### O2 — Worker and queue operations
Practice queue depth, capacity, leases, heartbeats, retries, failure states, tenant quotas and resource telemetry. Terminate a worker mid-job, verify lease recovery, duplicate safety and cancellation, and prove CPU/memory/time limits at the OS/container boundary.

**Pass:** no lost or silently duplicated successful result; crash recovery is observable; quotas are enforced and measured.

### O3 — Monitoring and incident response
Use structured logs, metrics, traces, correlation IDs, alerts and audit records. Inject identity-provider, storage, dependency and worker failures; execute incident runbooks and preserve evidence.

### O4 — Backup, restore and continuity
Perform encrypted database/artifact backup, checksum verification, isolated restore, object-version reconciliation and integrity validation. Measure RTO/RPO against approved targets and run a minimal research workflow on the restored copy.

**Pass:** approved RTO/RPO demonstrated; database and artifact integrity verified; restore logs and approver sign-off retained.

### O5 — Security and access administration
Practice user provisioning/deprovisioning, secret rotation, role/scope review, denied-access investigation, tenant offboarding and audit retention. Test revoked credentials, cross-tenant access, upload limits and escalation.

## 5. Accessibility and usability acceptance

Run task-based sessions with keyboard-only navigation, screen reader, zoom/reflow and high-contrast settings. Include job submission, progress, error recovery, cancellation, report inspection and artifact download. Record assistive technology, browser/OS, completion, blockers, severity and retest. Critical workflows must not depend on color alone, pointer-only interaction, inaccessible status announcements or inaccessible errors. Recruit participants with relevant access needs; automated scans alone are insufficient.

## 6. Test and evidence matrix

| Layer | Required evidence | Acceptance |
|---|---|---|
| Unit/property | deterministic, boundary and invalid-input tests | required checks pass |
| Integration | API, DB, artifacts, identity, model/tool adapters | contracts and failures pass |
| End-to-end | source-to-report workflows | reproducible and provenance-complete |
| Security | threat review, tenant tests, scans, penetration test | no unresolved critical/high findings without approved disposition |
| Performance | representative latency, throughput, CPU/RAM/VRAM/disk | measured against published workload targets |
| Resilience | crash, retry, lease, cancellation, dependency failure | correct, observable recovery |
| Recovery | encrypted backup restore and integrity | approved RTO/RPO demonstrated |
| Scientific | licensed immutable benchmark, independent review, leakage/calibration | claims match evidence |
| Researcher UAT | signed role-based task scripts and defect log | critical tasks pass |
| Accessibility | manual assistive-technology sessions and retests | critical blockers resolved |
| Operations | deploy, incident, rollback and restore exercises | runbooks executable by trained operators |

## 7. Session record template

Create an immutable record per session containing: session ID/programme version; date/facilitator/participant role (avoid unnecessary personal data); source commit/image digest/configuration/environment; dataset/model/tool revisions and license approval; scenario IDs and expected outcomes; actual outcomes and evidence hashes; defects/severity/owner/tracking reference; retest and superseded evidence; PASSED/FAILED/BLOCKED decision; reviewer and accountable sign-off.

Do not mark a session PASSED because the software was demonstrated by its author. The intended role must complete the task using published instructions.

## 8. Exit criteria

Researcher acceptance, operator readiness and accessibility acceptance are separate gates. Each requires completed sessions, resolved critical defects and named accountable reviewers. Unrun or blocked sessions remain NO-GO. Only non-critical items may be waived under release policy, with approver, rationale, expiry and compensating control.

Programme completion requires all role-based sessions run against the release candidate; independent completion of critical workflows; security/scientific/accessibility/recovery evidence tied to the exact source commit; critical/high defects resolved or formally dispositioned; and researcher, operations, security and scientific sign-offs.

## 9. Current limitations

This document defines training and acceptance; it does not record completed sessions, accessibility testing, production operator training, independent scientific review or recovery-drill evidence. A cloud scientific executor and enforced per-job sandbox are prerequisites; a no-op worker is insufficient. Real licensed benchmarks require approved access and immutable snapshots. Keep these limitations visible until evidence exists.
