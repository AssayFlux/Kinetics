# Security policy

## Current status
Kinetics is an R0 repository scaffold. There is no released application, remote compute node, patient-data workflow or supported security contact channel yet. Do not submit real patient or genomic data as an issue or attachment.

## Reporting
For a suspected vulnerability in this public repository, use GitHub's private vulnerability reporting / Security Advisories feature if enabled for the repository. If it is unavailable, open a minimal public issue that contains no exploit details or sensitive data and request a private reporting route.

## Security commitments for future releases
- Local-first processing and no telemetry by default.
- No genomic or patient data in logs.
- Encryption at rest and authenticated encrypted remote transport before sensitive workflows.
- Dependency and data-pack provenance, pinned versions and license review.
- Threat modelling, secure deletion, consent, access control and incident handling before sensitive-data features.
