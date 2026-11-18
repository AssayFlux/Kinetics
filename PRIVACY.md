# Privacy principles and current status

## Current status
The repository contains an Android research application with local import, encrypted app-private input storage, SQLite job/provenance records, WorkManager orchestration and user-initiated SAF export. The project owner declares institutional ethics approval obtained and has authorized research testing within its scope (D-025, 2026-11-18). The approval record is pending attachment; no independent verification is claimed. There is no account service, telemetry pipeline or remote compute service. CI uses synthetic fixtures only. No independent privacy assessment or real-device privacy audit has passed. This document is not a compliance claim.

## Intended principles
- Offline-first operation; no telemetry by default.
- Local genomic and research data remains on-device in the current Android app. Remote-node processing is not enabled by the current app manifest; any future client-side transfer requires a separately reviewed feature, explicit permission, destination-specific consent and renewed security/privacy/P0 gates.
- No sensitive data in diagnostic logs.
- Encryption at rest and in transit before sensitive workflows.
- Purpose-specific, revocable consent; data minimisation; de-identification where appropriate; secure deletion.
- Human data may be used only within the scope of the institutionally approved protocol and applicable consent/authorization; retain the approval record and qualified jurisdiction-specific review.
- Jurisdiction-specific privacy notices and retention/deletion rules must be approved before deployment.

See NORTH_STAR.md, DECISIONS.md and docs/track-p/p0-evidence-packet.md. Owner-authorized research testing may proceed within the declared institutional approval scope. Clinical deployment, treatment recommendations and unapproved remote processing remain disabled.


## Android local-data inventory (2026-11-18)

The Android Settings screen now explains the current storage boundaries. Imported input payloads use chunked AES-256-GCM in app-private no-backup storage. Job/import metadata and saved analysis-result JSON are stored in app-private SQLite and are **not separately encrypted** by the current implementation. Temporary decrypted input is created in app-private cache for analysis/export and cleaned on normal completion; stale prefixed cache files older than 24 hours are removed at store startup. Appearance, onboarding acknowledgement and the optional local app-lock setting are held in private SharedPreferences. User-selected SAF exports are outside the app's control after export.

The optional biometric/device-credential lock re-authenticates after the Activity is stopped and returns to the foreground. It is a convenience screen lock, not a substitute for encrypted storage or protection against a rooted/compromised device. FLAG_SECURE / Recents suppression is not enabled pending owner-approved threat review. Secure flash erasure and deletion of exported copies are not claimed.

These additions do not constitute an independent privacy/security review, compliance claim, device audit or release approval. See docs/track-u/u2-security-privacy.md for open evidence.


## Owner authorization note — 2026-11-18

The project owner declares that institutional ethics approval has been obtained and authorizes research testing with patient data within that approval's scope. The source approval document, reference number, issuing institution, date and protocol conditions have not yet been attached to this repository. Patient data must not be committed to GitHub, CI, issue/PR attachments, logs or public artifacts. Current Android imported input payloads are encrypted at rest, but SQLite job metadata and saved analysis-result JSON are not separately encrypted; this limitation must be considered in device selection and test-data handling.
