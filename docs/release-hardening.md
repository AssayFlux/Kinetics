# R10 — release hardening and distribution gate

**Status:** implementation checklist in progress. This document is not a release approval.

## Build and signing
- [ ] Reproduce the owner-requested local arm64 debug build from a clean checkout; archive exact commit, JDK/Gradle/AGP/Kotlin/SDK/NDK versions, command, logs, APK/AAB sizes and SHA-256.
- [ ] Verify every packaged native library's ELF class, architecture, PT_LOAD alignment and APK ZIP alignment.
- [ ] Test on a 16 KB page-size Android environment when the owner begins the later test campaign; static alignment is not runtime proof.
- [ ] Create a separate release signing key outside the repository and CI; document custody, backup, rotation and recovery. Never commit keystore files or passwords.
- [ ] Build a signed release AAB locally only after R1–R3 readiness and R10 security/privacy gates; verify signature and reproducibility.
- [ ] Produce SBOM, dependency notices, source/license inventory and third-party attributions.

## Accessibility and UX
- [ ] TalkBack navigation and meaningful control labels.
- [ ] Dynamic font scaling, high contrast, keyboard/switch access, touch target sizes and landscape/narrow-screen layouts.
- [ ] Clear empty/loading/partial/success/cancelled/failed states and actionable error recovery.
- [ ] Persistent Research Mode notice; no clinical mode or patient workflow.

## Performance and reliability
- [ ] Define cold-start, memory, CPU, storage and job-runtime budgets for low/mid/flagship tiers.
- [ ] Benchmark representative small/medium/large files; report repeated measurements and peak RSS.
- [ ] Process-death, low-storage, permission revocation, source-file mutation, cancellation, resume and crash-recovery tests.
- [ ] ANR, native crash, memory pressure, corrupted database and failed migration tests.
- [ ] Verify no unbounded allocation of imported files and no sensitive content in logs.

## Privacy and security
- [ ] Threat model covering local data, SAF URI permissions, Keystore key loss, backups, exports and data packs.
- [ ] Verify authenticated encryption on sensitive stored payloads; test tampering and key invalidation.
- [ ] Verify no telemetry/network permissions or unexpected outbound requests in offline Research Mode.
- [ ] Review deletion semantics, cache cleanup, retention, export/share and crash-report behavior.
- [ ] Review data-pack signature/checksum/source/license policy and rollback behavior.
- [ ] Resolve all high/critical findings or record explicit owner risk acceptance.

## Scientific and legal release controls
- [ ] Every public capability has independent reference evidence and reproducible validation record.
- [ ] Catalogue presence is not presented as implemented/validated; PGx and patient workflows remain blocked by P0.
- [ ] Complete file-level/transitive dependency and dataset license audit; preserve notices and source obligations.
- [ ] Confirm privacy notice, intended use, limitations, jurisdictional review and publication claims.
- [ ] Owner approves version, release notes, signed artifact, distribution channel and public claims.

## Distribution
Permitted channel candidates remain GitHub release assets and/or F-Droid only after channel-specific review. No automatic publishing. No release is authorized by this checklist alone.
