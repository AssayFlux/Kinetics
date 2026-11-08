# R2 recovery and SAF verification matrix

**Status:** test plan only. No physical-device or emulator result is implied.

The following scenarios must be executed on supported Android API levels and
recorded with device/API/build identity, result, logs, and artifact hashes before
R2 can exit. Automated JVM tests and CI package builds do not replace these checks.

| ID | Scenario | Expected result | Evidence required |
|---|---|---|---|
| R2-01 | Import a small SAF document | Persistent read grant, streamed encrypted import, source SHA-256 and provenance row | Device log + exported hash comparison |
| R2-02 | Cancel before WorkManager starts the worker | Job reaches resumable `cancelled`; no stuck `cancel_requested` row | DB state + WorkManager state |
| R2-03 | Cancel during a chunk write | Only authenticated complete chunks are retained; resume verifies source prefix | Encrypted partial inspection + resumed hash |
| R2-04 | Kill process during import, then relaunch | Unique work recovery does not duplicate workers; completed chunks are authenticated before resume | Process-death trace + final SHA-256 |
| R2-05 | Revoke SAF permission before resume | Resume is blocked with explicit permission error; existing ciphertext is preserved | DB state + file hash |
| R2-06 | Source content changes between attempts | Resume refuses append and preserves the encrypted partial | Source-prefix mismatch log + partial hash |
| R2-07 | Corrupt/truncate a final encrypted record | Only a torn final record is truncated; authentication failure in a complete record is preserved and escalated | Before/after ciphertext hashes |
| R2-08 | Keystore alias definitely missing | Completed and partial ciphertext is retained; state becomes `recovery_required`; no replacement key is generated | Keystore state + ciphertext hashes |
| R2-09 | Keystore inspection unavailable | No key-loss conclusion or destructive action is taken | Injected Keystore failure log |
| R2-10 | Export to SAF destination successfully | Full authentication/hash pass precedes plaintext output; exported bytes match original | Exported file SHA-256 |
| R2-11 | Export fails mid-stream and provider supports deletion | Incomplete destination is deleted and reported accurately | Provider result + destination absence |
| R2-12 | Export fails and provider refuses deletion | User is told partial data may remain and must remove it manually | UI capture + provider behavior |
| R2-13 | Upgrade database v1 → v2 → v3 | Schema and existing job/provenance rows remain valid | Migration fixture + device DB inspection |
| R2-14 | Orphan encrypted staging/final files | Reconciliation identifies files without matching job rows without deleting ciphertext automatically | Inventory report + no-loss proof |
| R2-15 | Delete a completed or partial job | App-owned ciphertext and metadata are removed; external exports are unaffected; no secure-erasure claim | File/DB inspection + UI confirmation |
| R2-16 | Abrupt process death leaves plaintext analysis cache | Only app-prefixed stale cache files older than the documented threshold are cleaned | Cache inventory before/after |

## Known limits and safeguards

- Keystore loss is not cryptographic recovery. Without the original key, preserved
  ciphertext cannot be decrypted; the app must not silently generate a replacement.
- SAF providers differ. A failed export may leave a partial destination when
  document deletion is unsupported.
- Flash storage deletion is not guaranteed secure erasure.
- The current automated Android JVM suite does not execute real SAF providers,
  Android Keystore lifecycle, WorkManager process death, or schema migrations.
- R2 remains in progress until the matrix is executed and reviewed; do not mark
  these scenarios passed from source inspection alone.
