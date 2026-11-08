# Security policy

## Current status
Kinetics is an unreleased research application under active development. R0 is complete; R1–R10 remain in progress. CI can produce unsigned arm64 debug APK/AAB artifacts, but no production release, independent security assessment, supported security contact channel, remote compute node or patient-data workflow exists. Do not submit real patient or genomic data as an issue or attachment.

## Reporting
For a suspected vulnerability in this public repository, use GitHub's private vulnerability reporting / Security Advisories feature if enabled for the repository. If it is unavailable, open a minimal public issue that contains no exploit details or sensitive data and request a private reporting route.

## Security commitments for future releases
- Local-first processing and no telemetry by default.
- No genomic or patient data in logs.
- Encryption at rest and authenticated encrypted remote transport before sensitive workflows.
- Dependency and data-pack provenance, pinned versions and license review.
- Threat modelling, secure deletion, consent, access control and incident handling before sensitive-data features.
