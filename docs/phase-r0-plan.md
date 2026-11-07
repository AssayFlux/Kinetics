# R0 — Foundations phase plan
**Roadmap item:** Track R / R0  
**Status:** R0 implementation and automated checks complete; awaiting owner acceptance of exit gate  
**Owner:** Engineering + Project owner  
**Date:** 2026-11-07

## Objective
Establish a minimal, auditable repository foundation whose empty-skeleton CI can pass. No scientific capabilities, clinical features, license selection or Android feasibility claims are part of R0.

## Deliverables
1. Preserve existing assets and approved direction files.
2. Keep the owner-supplied master in docs/origin as read-only history.
3. Maintain NORTH_STAR, ROADMAP, DECISIONS and SESSION_LOG; keep six owner decisions open.
4. Add minimal Part 6 repository skeleton without unapproved languages, engines, data or clinical functionality.
5. Add parseable capabilities/registry.yaml with no false validated/device-verified entries.
6. Add scripts/check_registry.py and tests for missing references, validation evidence, device logs and clinical gating.
7. Add scripts/reproduce-all stub that clearly reports no evidence jobs are registered.
8. Add CI for available lint/type/test/native-build checks, registry validation, 16 KB alignment and size budgets. Missing toolchains must be explicit blockers, never fake passes.
9. Add pre-commit configuration for approved tools (ruff, black, mypy, clippy/rustfmt, clang-format, ktlint when components exist).
10. Add only necessary architecture/security/third-party documentation. Do not choose or add project LICENSE text.

## Exclusions
No patient-related feature, real patient data, human-participant work, clinical claim, license selection, jurisdiction choice, paper framing/venue, adviser selection, PGx gene selection, target-device commitment, new language, engine/tier/model/data pack, Android feasibility claim or scientific validation.

## Acceptance criteria — R0 exit gate
- Skeleton matches approved layout; no secrets, binaries or datasets committed.
- Registry parses and references are internally consistent.
- Checker tests reject validated without validation/benchmark, device_verified without device log, missing references and clinical mode without Part 12 evidence/flag.
- reproduce-all stub exits transparently because no evidence jobs exist.
- CI workflows are present and actual CI run is green on empty skeleton; no skipped check is represented as passed.
- Native/Android, 16 KB and size checks are run or explicitly blocked pending toolchain/device.
- No project LICENSE selected.
- ROADMAP and SESSION_LOG reflect actual evidence.
- Stop and report to owner; do not proceed to R1 without explicit approval.

## Execution sequence
1. Owner approved the direction baseline on 2026-11-07; NORTH_STAR remains unchanged.
2. Added minimal repository skeleton, empty registry, evidence checker and checker tests.
3. Added reproduce-all stub, CI workflow, pre-commit hooks and development tooling.
4. Added explicit R0 blocker reporting for native/Android/16 KB/size checks.
5. GitHub Actions run 1373 completed successfully: pre-commit config validation, Ruff, mypy, registry validation, 11 unit tests and reproduce-all passed.
6. Android/native, 16 KB and size checks are explicitly blocked/not applicable pending R1 toolchains and named devices.
7. Update roadmap/session log with observed results; stop for owner approval. Do not begin R1 without explicit approval.
