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

The current source prototype requires persistable SAF read access before scheduling an import. Resumable staging is stored as independently authenticated AES-256-GCM chunks under app-private no-backup storage; the worker decrypts chunks only in memory to reconstruct the input hash and verifies the source prefix before appending. Incomplete final records are truncated safely, and legacy plaintext staging files are removed before a new import. Final storage location and provenance are committed in one SQLite transaction. A private-cache materialization helper verifies the final hash and can scope plaintext use to a callback with finally-based cleanup; it is not yet connected to an analysis dispatcher or SAF export. This is source implementation only: Android compilation/runtime, key invalidation and recovery, process-death, SAF provider edge cases, full export/recovery, database migration and owner-device execution remain unverified.


### R2 continued source hardening — 2026-11-08

The data-pack installer now revalidates programmatically supplied manifest fields (including rejecting dot-segment IDs/versions), uses a unique app-private temporary file, hashes the exact byte stream while copying it, checks declared size and checksum before finalization, and refuses an already-installed version. This closes the prior separate hash-then-copy time-of-check/time-of-use gap. The store also removes only stale, uniquely-prefixed plaintext analysis cache files older than 24 hours at startup, and empty imports are rejected. These remain source-only changes; Android compilation, concurrency, filesystem atomicity, crash recovery and device behavior are unverified.


### R2 SAF export and schema migration increment — 2026-11-08

Added a user-mediated Storage Access Framework CreateDocument export path for completed imports. Export streams authenticated AES-GCM chunks directly to the chosen destination without creating a plaintext cache file. It performs a complete authentication and SHA-256 pass before releasing plaintext, then authenticates again while streaming to detect source changes. Added a v2-to-v3 SQLite migration that adds export metadata and a provenance index. This source path is not yet Android-compiled or exercised against real SAF providers; provider partial-file cleanup, process death during export, migration fixtures, key invalidation and full lifecycle recovery remain verification gates.


### SAF export failure cleanup — 2026-11-08

The Android export flow now opens newly created SAF destinations in truncate mode and, if authenticated decryption/hash verification or stream writing fails, attempts to delete the incomplete document through `DocumentsContract.deleteDocument`. The UI reports whether the provider confirmed deletion. If the provider does not support deletion, it explicitly warns that a partial destination may remain and must be removed manually before retrying. This is best-effort provider-dependent cleanup, not a guarantee of secure erasure or universal SAF rollback. Device/provider tests remain outstanding.


### Imported FASTA QC vertical slice — 2026-11-09 (R Step 1)

A completed, hash-verified FASTA import can now launch a unique WorkManager analysis job from its Home/Work job card. The worker authenticates/decrypts the stored KDAT input through the existing private-cache helper, enforces a 1 MB byte/character bound, runs the local FASTA QC adapter, removes the temporary plaintext in a `finally` path, and transactionally persists the JSON result with tool/version, explicit parameters, source SHA-256 and timestamp in schema v4 `analysis_results`. Saved result JSON is inspectable from the job card. The worker deliberately rejects FASTQ because Phred+33/64 must be selected explicitly by the user.

This is an initial R2→R4 integration slice, not the full R2 exit: analysis-result SAF export, lifecycle/migration/recovery tests, result rendering, larger-file streaming, UI error/retry states, exact-source CI and device/provider tests remain to be completed in R Step 2.
