# Privacy principles and current status

## Current status
This repository contains no functioning app, account service, telemetry pipeline, patient-data workflow or remote compute service. This document states design requirements; it is not a claim that an implemented product has passed a privacy assessment.

## Intended principles
- Offline-first operation; no telemetry by default.
- Local genomic and research data remains on-device unless the user explicitly configures a remote node and consents to a specific transfer.
- No sensitive data in diagnostic logs.
- Encryption at rest and in transit before sensitive workflows.
- Purpose-specific, revocable consent; data minimisation; de-identification where appropriate; secure deletion.
- Human data requires applicable ethics review or documented exemption and qualified legal review.
- Jurisdiction-specific privacy notices and retention/deletion rules must be approved before deployment.

See NORTH_STAR.md, DECISIONS.md and docs/android-feasibility.md. No patient-related feature may begin before P0.
