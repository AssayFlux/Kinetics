# Track G — data-flow and information-asset inventory

**Status:** source-level initial inventory, not a completed privacy assessment.  
**Evidence inspected:** Android app manifest, app Gradle configuration, security threat model, privacy policy and release checklist as present on 2026-11-12.

## Current architecture observations

The Android manifest declares one exported launcher activity and no permissions. In particular, no INTERNET permission is declared in the inspected manifest. The application sets `allowBackup=false` and `usesCleartextTraffic=false`. No dedicated `backup_rules.xml` or `data_extraction_rules.xml` file was found at the inspected source paths; Android-version/OEM backup behavior must still be verified from the merged manifest and on-device. These are source observations, not installed-device proof.

The app build config embeds Python 3.11 with pinned Biopython 1.88 and NumPy 1.26.2 wheels from the repository's local wheel directory. App dependencies include Compose, WorkManager, WebKit and biometric libraries. A dependency declaration does not prove a feature is reachable or that a data flow exists.

## Information assets and flows

| Flow ID | Data / asset | Entry point | Processing / storage | Exit / recipient | Classification | Current control evidence | Open verification |
|---|---|---|---|---|---|---|---|
| DF-01 | User-selected research input | Android Storage Access Framework (SAF) picker | Streaming import; encrypted app-private storage; SQLite job/provenance metadata | Remains app-private unless user exports | User research data; potentially sensitive | Threat model describes bounded import and encrypted storage | Verify URI grants, provider revocation, plaintext lifetime, actual device behavior |
| DF-02 | Analysis plaintext / working buffers | Internal worker/runtime | In-memory processing and temporary app-private work files as required by workflow | Cleanup after processing; no remote transfer evidenced by app manifest | Sensitive derived research content | Threat model prohibits plaintext logging and requires short-lived private plaintext | Audit all worker/native/Python temporary-file paths and crash remnants |
| DF-03 | Encrypted inputs and result metadata | Internal worker and persistence layer | App-private files and SQLite | No automatic cloud backup intended; no backup permission/config evidence in inspected manifest | Confidential research data | `allowBackup=false` in source manifest | Verify Android 12+ data-extraction rules, OEM behavior, database/WAL and external cache |
| DF-04 | User-requested result export | Export action / SAF create-document flow | Serialize result and provenance | User-selected document provider/location; potentially outside app control | User-controlled disclosure | Explicit export is described in architecture and release checklist | Verify confirmation, destination display, partial-write handling, redaction and deletion limits |
| DF-05 | Logs and diagnostics | App, workers, native/Python libraries | Android logcat / CI logs | Device owner / CI platform | Operational metadata; must exclude content/secrets | Threat model and privacy policy prohibit sensitive content in logs | Static scan and runtime log review on device; test exception paths |
| DF-06 | Third-party dependencies and data packs | Build-time repositories and user/local pack import | Build cache, APK/AAB, app-private pack storage | Pack use within local workflows; no executable data-pack loading | Software supply-chain material | Version pins, source SBOM and pack checks exist | Resolve full graph, verify hashes/signatures, license review and rollback tests |
| DF-07 | Optional remote-node boundary | Separate node-worker contracts and future pairing UI scope | No app-side network path evidenced in inspected manifest | Not enabled by current manifest evidence | Potentially sensitive transfer | UI threat model says network off by default; app manifest has no INTERNET permission | Keep disabled; any future network feature requires separate design, permissions, consent and P0/privacy gate |
| DF-08 | Account, telemetry and analytics | No source flow identified in inspected policy/configuration | No service or telemetry pipeline identified in PRIVACY.md | None identified | Not collected by declared design | PRIVACY.md states no account service or telemetry pipeline | Re-scan source, merged manifest and network traffic before each release |

## Prohibited data and processing

Until P0 is formally approved, do not collect, import, store, export, process or transmit patient/clinical data or identifiable human-subject research data. Do not enable individual PGx interpretation, diagnosis, treatment/dosing recommendations or Clinical Mode. Synthetic fixtures and public datasets must still pass their own provenance, license and intended-use checks.

## Required classification and handling rules

- **Public:** public project documentation and source code; still subject to license and security review.
- **Internal:** build logs, issue metadata and non-sensitive operational records; avoid secrets and personal data.
- **Confidential research:** user-provided sequences, structures, chemistry inputs and derived outputs; app-private, minimised and never logged.
- **Prohibited pending P0:** patient/clinical records, identifiable human-subject data, patient-specific PGx/clinical interpretation and clinical decision-support outputs.

## Data subject / user controls

| Operation | Current design position | Required verification / disclosure |
|---|---|---|
| Access | User controls local device and app files | No server-side access feature is identified |
| Export | Explicit user-selected SAF destination | Explain that exported copies leave app control |
| Delete | App-visible encrypted files and metadata may be removed | Do not promise physical flash erasure or deletion of external copies |
| Backup / restore | Android backup disabled in source manifest | Test device transfer, OEM backup and restore behavior |
| Retention | No central retention service identified | Define local retention defaults and user-facing controls before release |
| Consent | No patient/human-subject use allowed | Any future study requires ethics and qualified legal review |

## Release gates

1. Inspect merged manifest from the exact APK/AAB, not just source manifest.
2. Trace all filesystem, SQLite, SAF, cache, log, WebView, native and Python read/write paths.
3. Test revoked URI permission, process death, cancellation, low storage, partial export, backup/restore and deletion on named devices.
4. Capture network permission and traffic evidence; any new network path triggers a new privacy/security review.
5. Complete qualified jurisdiction-specific advice and owner approval before any personal or human data workflow.
