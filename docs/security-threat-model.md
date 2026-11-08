# Kinetics security and privacy threat model

**Status:** Initial engineering threat model; not an independent security assessment.  
**Scope:** Android Research Mode, app-private imports, encrypted local storage, SAF import/export, WorkManager, Python/native runtime and offline data packs.

## Assets

- Imported research files and derived outputs.
- AES-256-GCM Keystore key material and authenticated encrypted chunks.
- Input/output SHA-256 digests, job metadata and provenance.
- Data-pack bytes, manifests, source/license metadata and installed versions.
- Build inputs, native binaries, signing credentials and release artifacts.

## Trust boundaries

1. SAF document providers and user-selected URIs are external and untrusted.
2. Imported bytes, filenames, MIME types, metadata and data-pack manifests are untrusted.
3. WorkManager input data and persisted SQLite rows are validated before file operations.
4. App-private no-backup storage is the encrypted-at-rest boundary; decrypted analysis/export plaintext must be short-lived and app-private or explicitly written to a user-selected SAF destination.
5. Native libraries, Python wheels, Gradle plugins and transitive dependencies are supply-chain inputs and require pinned provenance and license review.

## Threats and current controls

| Threat | Current control | Residual risk |
|---|---|---|
| Malformed/oversized import | Streaming import, 512 MiB cap, chunk bounds, parser validation | Parser-specific resource exhaustion and provider stalls require fuzzing/benchmarks |
| Tampered encrypted chunk | AES-GCM authentication with job/chunk AAD; whole-file SHA-256 | Keystore key loss/invalidation and backup/restore recovery are not yet fully handled |
| Changed source on resume | Re-hash source prefix before append | Providers may revoke/change access during the operation |
| Path traversal | UUID job IDs, app-private directories, canonical cache-path check, pack ID/version validation | Filesystem race/symlink behavior and Android provider differences need tests |
| Process death | Encrypted partial retention and unique WorkManager recovery | Interrupted export, DB/file reconciliation and orphan cleanup are incomplete |
| Data-pack substitution | Manifest metadata, size cap, checksum over copied stream, immutable installed version | No signed publisher metadata or trust-root policy; checksum alone does not authenticate publisher |
| Sensitive disclosure | No INTERNET permission, cleartext disabled, backup disabled, no telemetry configured | User-initiated SAF export intentionally writes plaintext outside app control |
| Supply-chain compromise | Toolchain version pins and Gradle distribution checksum | Full transitive lock, SBOM, signature verification and license/security review incomplete |
| Rooted/compromised device | Keystore-backed key and app-private storage | Root, instrumentation, memory scraping and OS compromise are out of scope |

## Security invariants

- Never log imported content, plaintext, keys, tokens or complete sensitive paths.
- Reject unknown encrypted-file versions and authentication failures; never silently downgrade.
- Do not load executable code or native libraries from data packs.
- Do not upload research content or telemetry.
- Do not claim secure deletion on flash storage; document logical deletion limitations.
- Clinical workflows remain disabled.

## Required next assessment

Perform source review and adversarial tests for parser limits, URI permission revocation, concurrent workers, cancellation, process death at every file/DB transition, keystore invalidation, interrupted SAF export, schema migration, storage exhaustion and data-pack rollback. Obtain independent mobile security review before release.
