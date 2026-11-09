# Privacy principles and current status

## Current status
The repository now contains an Android Research Mode application prototype with local import, encrypted app-private storage, SQLite job/provenance records, WorkManager orchestration and user-initiated SAF export. It has no account service, telemetry pipeline, patient-data workflow or remote compute service. CI verifies source/build checks, but no independent privacy assessment or real-device privacy audit has passed. This document states design requirements and is not a compliance claim.

## Intended principles
- Offline-first operation; no telemetry by default.
- Local genomic and research data remains on-device unless the user explicitly configures a remote node and consents to a specific transfer.
- No sensitive data in diagnostic logs.
- Encryption at rest and in transit before sensitive workflows.
- Purpose-specific, revocable consent; data minimisation; de-identification where appropriate; secure deletion.
- Human data requires applicable ethics review or documented exemption and qualified legal review.
- Jurisdiction-specific privacy notices and retention/deletion rules must be approved before deployment.

See NORTH_STAR.md, DECISIONS.md and docs/android-feasibility.md. No patient-related feature may begin before P0.
