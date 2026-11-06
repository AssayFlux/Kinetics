# Step 10 — Integration and release-readiness gates

**Status: release-control specification; no production deployment or release sign-off is implied.**

## Release principles

A release is a reproducible, reviewable snapshot of software and its evidence. A green unit-test suite is necessary but not sufficient. No release may claim scientific validity, security certification, disaster recovery, clinical readiness or supported-platform compatibility without the corresponding recorded evidence.

## Release candidate manifest

Every release candidate must publish a machine-readable manifest containing:

- semantic version, source commit SHA and build timestamp;
- Python/Rust/C++ toolchain versions and supported OS/architecture matrix;
- dependency lock or fully resolved dependency inventory, licenses and vulnerability scan result;
- wheel/source distribution hashes and native binary hashes;
- API/schema versions and database migration range;
- test workflow URLs and exact commit SHA tested;
- dataset/model/representation revisions used in any included scientific evaluation;
- known limitations, unsupported features and unresolved risk IDs;
- SBOM location and signature/attestation status where signing is configured.

The manifest must distinguish `not_run`, `blocked`, `passed`, `failed` and `waived`; a waiver requires named approver, rationale, expiry and compensating control. Missing evidence is never treated as pass.

## Mandatory release gates

### 1. Build and compatibility
- Build wheel and source distribution from a clean checkout.
- Install the wheel in a clean environment without repository checkout paths.
- Exercise every advertised CLI entry point and packaged resource.
- Test supported Python versions and OS/architecture combinations.
- Verify API and serialized-artifact compatibility against the declared support window.
- Test upgrade from each supported prior schema and reject forward/unknown schema versions safely.

### 2. Scientific integrity and reproducibility
- Run the documented source-to-report workflow on a reviewed, licensed immutable dataset.
- Verify all source, dataset, feature, model, prediction and report hashes.
- Record code revision, environment, configuration, seeds, split groups and external tool/model revisions.
- Audit protein/chemical/assay/source/time leakage for the declared evaluation.
- Report target units, missingness, subgroup coverage, uncertainty coverage and width, applicability warnings and failure cases.
- Keep synthetic/fixture results clearly separate from real-data evidence.
- Require independent scientific review before making performance claims.

### 3. Security and privacy
- Review threat model, authentication/authorization, tenant isolation and least privilege.
- Test cross-tenant reads/writes, path traversal, symlink escape, upload limits, content-type handling, CSRF/origin controls and artifact integrity.
- Verify secrets never enter logs, manifests, errors or debug output; use managed secret storage in deployed profiles.
- Verify audit events are durable, append-only, access-controlled and tamper-evident.
- Scan dependencies, containers and generated artifacts; triage every critical/high finding.
- Document data classification, lawful basis, source terms, retention, export and deletion controls.

### 4. Runtime and resilience
- Measure representative CPU/GPU, RAM/VRAM, disk and latency/throughput under declared workloads.
- Test cancellation during queued, running and finalization phases.
- Test worker crash, lease expiry, duplicate delivery, retry exhaustion and idempotent replay.
- Restore encrypted backups into an isolated environment; verify hashes, database consistency, artifact readability and measured recovery time.
- Demonstrate rollback to the previous release and database compatibility.
- Record resource quotas and prove they are enforced rather than merely configured.

### 5. User acceptance and operations
- Run researcher task-based usability sessions and keyboard/screen-reader/zoom checks.
- Verify errors, progress, cancellation and recovery are understandable.
- Publish install, upgrade, rollback, backup/restore, incident response and troubleshooting procedures.
- Obtain engineering, security, data-governance and scientific sign-offs from accountable reviewers.

## Release decision

Release decision is one of:
- **GO**: all mandatory gates passed; no unresolved critical security or data-integrity issue.
- **CONDITIONAL**: only explicitly waivable non-critical gates remain; each has a named owner, expiry, compensating control and visible release limitation.
- **NO-GO**: any mandatory gate failed, is unknown, or is blocked by missing authorization/evidence.

Clinical or regulated use is always outside this general research release decision and requires its own governance, validation and authorization.

## Current known blockers (2026-11-06)

| Area | Current evidence | Release consequence |
|---|---|---|
| Step 2 real data | CatPred gate requires researcher acceptance; no immutable real snapshot/release recorded | NO-GO for scientific benchmark claims |
| Step 3 execution | Pinned ESM-2 and MMseqs2 not run on reviewed real data | NO-GO for representation reproducibility claims |
| Step 4/5 science | No real-data model comparison/external validation | NO-GO for predictive performance claims |
| Step 7 production | Production OIDC/JWT, managed secrets, distributed worker leases/quotas, network artifact service, durable audit and encrypted recovery drill remain open | NO-GO for remote multi-tenant production |
| Step 8 acceptance | Researcher/screen-reader UAT, desktop upgrade/rollback and real-workload performance/recovery remain open | Local engineering foundation only; not accepted as complete |
| Step 9 | Domain contracts and validation evidence are not yet implemented/approved | No expanded-domain capability claim |
| Step 10 | This checklist is a control specification; release evidence and sign-offs have not been assembled | No production release sign-off |

## Evidence retention

Store the release manifest, CI URLs, SBOM, vulnerability triage, test reports, benchmark outputs, recovery logs, user-acceptance findings, signed review decisions and release notes under a versioned release-evidence directory. Every report must identify its source commit and must not be edited in place after sign-off; corrections create a superseding evidence record.

## Executable manifest evaluator (2026-11-06)

The `kinetics_core.release_gate` module validates the candidate version, source commit SHA, required gate inventory, evidence references, and waiver metadata. Missing, not-run, blocked, or failed mandatory gates produce NO-GO; a valid non-critical waiver produces CONDITIONAL; all passed gates produce GO. The evaluator always sets `release_signoff: false`. It does not inspect external evidence, deploy software, run security scans, perform recovery, or replace accountable human sign-off.
