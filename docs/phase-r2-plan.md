# R2 — Android application foundation

**Roadmap item:** Track R / R2  
**Status:** IMPLEMENTATION IN PROGRESS — integrated R1–R10 delivery authorized; verification and phase exit remain gated  
**Owner:** Engineering  
**Depends on:** R1 architecture findings inform implementation; R1 evidence/go-no-go remains required before R2 exit and production readiness  
**Exit gate:** On-device import, cancellable/resumable job, provenance inspection and owner approval

## Objective

Build the usable, offline-first Android application foundation on top of the R1-approved technical architecture. Keep the Android layer thin: UI, storage, file access, lifecycle, job orchestration and security boundaries; scientific algorithms remain in the appropriate Python/Rust/C++ engines.

## Scope and deliverables

1. **Compose application shell**
   - Navigation and feature entry points for Research Mode.
   - Consistent empty, loading, success, partial-result, cancellation and error states.
   - Accessibility, large-text and narrow-screen behavior.
   - Persistent Research use only notice; no clinical mode or patient workflow.
2. **SQLite project store**
   - Versioned schema and migration strategy.
   - Projects, input-file metadata, job state, capability registry cache and provenance records.
   - Transactions, integrity checks, export/backup policy and recovery behavior.
3. **Storage Access Framework**
   - User-mediated import/export via document picker.
   - Stream large files; avoid copying whole inputs into memory.
   - Validate extension, content signature, format and size limits; never trust filenames.
   - Persist URI permissions only where supported and needed; handle revoked permissions.
4. **Provenance**
   - Immutable run record: capability/tool/engine versions, parameters, input hashes, reference/data-pack versions, timestamps, environment and output hashes.
   - Link outputs to inputs and job runs; preserve warnings and uncertainty.
   - Export machine-readable JSON plus human-readable summary.
5. **Job orchestration**
   - WorkManager for durable work with foreground execution only where justified.
   - Explicit queued/running/cancel-requested/cancelled/failed/succeeded states.
   - Cooperative cancellation propagated to Python/Rust/native work.
   - Idempotent checkpoints, restart recovery, bounded retries and no duplicate outputs.
6. **Capability registry**
   - Load the versioned registry; show planned/implemented/validated distinctions.
   - Never present planned entries as runnable tools.
   - Gate invocation on implementation metadata and compatible engine/data packs.
7. **Data-pack manager**
   - Manifest, version, source, license, size, checksum and schema verification.
   - Atomic install/update/rollback; storage budget; offline state.
   - No executable code or native libraries downloaded as data packs.
8. **Local security**
   - Android Keystore-backed key management and authenticated encryption for sensitive local project data.
   - No sensitive content in logs, crash reports or analytics.
   - Explicit export/share boundaries; secure deletion limitations documented.
   - Threat model and security tests before claiming protected-data readiness.

## Required tests

- Compose navigation/state and accessibility tests.
- SQLite schema migration, crash recovery and transaction tests.
- SAF import/export tests for small, large, malformed, truncated and permission-revoked inputs.
- Provenance completeness, stable hashes and tamper-detection tests.
- WorkManager process-death, duplicate scheduling, retry, cancellation and resume tests.
- Registry negative tests: planned tools cannot execute; missing engines/packs block invocation.
- Data-pack checksum, license metadata, rollback and low-storage tests.
- Keystore key-loss/rotation, encryption/decryption, backup exclusion and sensitive-log tests.
- Manual owner-device test on Android 10+ arm64 before phase exit; record model, API, ABI, storage and logs.

## Non-goals and safety

- No patient data, clinical decision support, prescribing, dosing or diagnosis.
- No automatic upload or remote compute without an explicit later-approved consent and security design.
- No executable download/update mechanism.
- No dependency or engine adoption that bypasses the license register.
- R2 does not claim scientific capability validation; that belongs to R3 and later domain phases.

## Exit criteria

R2 is complete only when the app shell, SQLite, SAF, provenance, cancellable/resumable jobs, registry and pack manager work together; required automated tests pass; the owner can import a file, run/cancel/recover a job, inspect provenance and export results on a real target device; security/privacy review findings are resolved or accepted; and the owner explicitly approves the R2 exit gate.

**Owner instruction (2026-11-08):** implement R1–R10 as one integrated delivery; do not stop implementation at R1. Preserve the R1 go/no-go as an evidence/phase-exit gate, not as a reason to defer downstream coding.


## Implementation hardening note — 2026-11-08

The current source prototype requires persistable SAF read access before scheduling an import. Resumable staging is stored as independently authenticated AES-256-GCM chunks under app-private no-backup storage; the worker decrypts chunks only in memory to reconstruct the input hash and verifies the source prefix before appending. Incomplete final records are truncated safely, and legacy plaintext staging files are removed before a new import. Final storage location and provenance are committed in one SQLite transaction. This is source implementation only: Android compilation/runtime, key invalidation and recovery, process-death, SAF provider edge cases, export/recovery, database migration, and owner-device execution remain unverified.
