# U2 — Security and privacy surfaces

**Disposition:** PARTIAL — implementation additions are in source; security acceptance remains OPEN.
**Scope:** Android Research Mode only. This document is an engineering record, not a security certification or privacy compliance claim.

## Implemented in this work package

- The optional biometric/device-credential app lock now re-locks after the Activity enters the stopped lifecycle state and requests authentication when the Activity returns to the foreground. Authentication errors and cancellation leave the workspace locked and expose a retry path. This remains a convenience screen lock, not an encryption boundary.
- Settings now presents a local-data inventory that distinguishes encrypted research inputs from SQLite metadata and analysis results, private preferences, temporary plaintext cache files and user-selected exports.
- The disclosure explicitly states that SQLite job/provenance metadata and saved analysis JSON are not separately encrypted by the current implementation.
- The disclosure states that secure flash erasure and deletion of exported copies cannot be guaranteed.
- The disclosure states that FLAG_SECURE / Recents screenshot suppression is not enabled pending explicit threat review and owner approval.
- Deleting a job now also requests cancellation of its uniquely named analysis WorkManager job before removing app-managed data.
- Existing fail-closed Keystore-loss handling remains authoritative: ciphertext is preserved and jobs are marked recovery-required; no replacement key is generated to pretend old ciphertext can be recovered.
- Existing encrypted orphan inventory remains read-only; it does not automatically delete files.

## Data inventory and trust boundary

| Data | Current location | Protection / limitation |
|---|---|---|
| Imported research input | noBackupFilesDir/research-inputs/*.kdat | Chunked AES-256-GCM; per-job/chunk AAD; app-private; Keystore key |
| Partial encrypted import | noBackupFilesDir/research-imports/*.encpart | Encrypted chunks; resumable only while source grant and key remain usable |
| Job and import metadata | kinetics-research.db | App-private SQLite; not separately encrypted |
| Analysis result and parameters | analysis_results table in SQLite | App-private SQLite; currently plaintext JSON |
| Temporary decrypted analysis input | App-private cache | Deleted by normal cleanup; stale prefixed files older than 24 hours are cleaned at store startup; crash residue can exist until cleanup |
| Preferences | Private SharedPreferences | App-private; not encrypted separately |
| Exported input/result/provenance | User-selected SAF destination | Outside app control after export |

The source manifest declares allowBackup=false and no INTERNET permission. Merged-manifest, runtime traffic and device/OEM verification are still required before those source-level facts can be treated as deployment evidence.

## Explicitly not implemented or not accepted

- No FLAG_SECURE / Recents suppression until owner-facing impact and threat review approve the policy.
- No claim of encrypted SQLite metadata or encrypted analysis results.
- No claim of secure deletion from flash storage.
- No recovery of ciphertext if the original Android Keystore key is permanently lost.
- No independent mobile security assessment, penetration test, privacy review, or physical-device validation.
- No claim that the biometric prompt protects against rooted, instrumented or OS-compromised devices.

## Required closure evidence

1. Lifecycle tests for background/foreground, prompt cancellation, failed biometric attempt, device-credential fallback, lockout and process recreation on supported API levels.
2. Instrumented tests on named Android devices for biometric and credential flows.
3. Merged-manifest audit, backup/restore behavior and runtime network capture.
4. Fault-injection tests for Keystore invalidation, encrypted partials, orphan cleanup and deletion transaction boundaries.
5. A reviewed threat decision for screenshot/Recents behavior and an owner-approved disclosure.
6. Decision on whether SQLite metadata and result JSON require application-layer encryption before release.
7. Independent security/privacy assessment and retest against the exact release artifact.

**Decision:** U2 remains PARTIAL / REVIEW REQUIRED. The code now discloses current limitations rather than implying that all local data is encrypted.
