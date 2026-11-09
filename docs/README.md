# Documentation guide

This is the navigation index for the Kinetics repository. Use the living decision and roadmap files as the authority; session notes and archived instructions are historical evidence, not competing plans.

## 1. Project direction and decisions

| Purpose | Canonical document |
|---|---|
| Product purpose and scope | [North Star](../NORTH_STAR.md) |
| Master plan and track order | [Roadmap](../ROADMAP.md) |
| Approved decisions and supersessions | [Decision log](../DECISIONS.md) |
| Original owner-supplied master (read-only history) | [Archived master](origin/KINETICS_MASTER.md) |
| Session-by-session engineering record | [Session log](../SESSION_LOG.md) |

## 2. Architecture and engineering

| Purpose | Document |
|---|---|
| System boundaries and component architecture | [Architecture](architecture.md) |
| Language ownership and cross-stack contracts | [Engineering integration standard](ENGINEERING_INTEGRATION_STANDARD.md) |
| Android feasibility and platform constraints | [Android feasibility](android-feasibility.md) |
| Scientific engine selection and decision gates | [Scientific engine decisions](scientific-engine-decisions.md) |
| Local build reproduction | [Local Android build](local-android-build.md) |
| Third-party dependency and license register | [Third-party inventory](third-party.md) |

## 3. Track implementation and audit

| Track | Canonical documents |
|---|---|
| R — Research platform | [R0](phase-r0-plan.md), [R1](phase-r1-plan.md), [R2](phase-r2-plan.md), [R3](phase-r3-plan.md), [R4](phase-r4-plan.md), [R5](phase-r5-plan.md), [R6](phase-r6-plan.md), [R7](phase-r7-plan.md), [R8](phase-r8-plan.md), [R9](phase-r9-plan.md), [R10](phase-r10-plan.md), [R-track audit](r-track-audit-2026-11-09.md), [R2 recovery matrix](track-r2/recovery-test-matrix.md) |
| S — Structure, sequence and discovery | [S roadmap](track-s/discovery-and-design-roadmap.md), [S1 viewer](track-s/structure-viewer-contract.md), [S2 quality metrics](track-s/structure-quality-metrics.md), [S4 prediction boundary](track-s/structure-prediction-boundary.md), [S6 unknown-sequence evidence](track-s/unknown-sequence-evidence-contract.md), [S7 contig QC](track-s/genome-contig-qc.md) |
| I — In-silico laboratory | [Research boundaries](track-i/research-boundaries.md) |
| P — Precision medicine preparation | [Public-data-only boundary](track-p/public-data-only-preparation.md), [public dataset catalog](track-p/public-dataset-catalog.md) |
| UI / design system | [UI/UX specification](android-ui-ux-spec.md), [UI document set](ui/ui-spec.md), [root UI spec](../KINETICS_UI_SPEC.md) |

## 4. Validation, security and release

| Purpose | Canonical document |
|---|---|
| Dataset intake and validation policy | [Validation index](../validation/README.md) |
| CI and artifact evidence | [CI build evidence](ci-build-evidence.md) |
| Threat model | [Security threat model](security-threat-model.md) |
| Security reporting | [Security policy](../SECURITY.md) |
| Privacy and data handling | [Privacy policy](../PRIVACY.md) |
| Accessibility test plan | [Accessibility plan](accessibility-test-plan.md) |
| Release hardening | [Release hardening](release-hardening.md) |
| Release gate checklist | [Release checklist](release-checklist.md) |

## 5. Governance and historical material

- [Historical parallel-track protocol](parallel-track-execution.md) is **superseded by D-019** and must not be followed.
- [Original master](origin/KINETICS_MASTER.md) is preserved as read-only historical source.
- [Change history](../CHANGELOG.md) records user-visible project changes.
- [Paper skeleton](../paper/manuscript-skeleton.md) is a planning artifact, not a claim of publication readiness.

## Status vocabulary

- **Implemented:** source path and automated tests exist.
- **Regression-tested:** the named automated tests pass on the cited revision.
- **Validated:** independent reference/benchmark evidence exists and is linked.
- **Device-verified:** dated evidence exists for a named device and build.
- **Accepted/done:** the full phase exit criteria and required owner approval are recorded.
- **Blocked:** a named dependency or formal gate prevents the next action.

Never upgrade one status to another without the corresponding evidence.
