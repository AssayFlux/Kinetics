# Release readiness checklist

**Current state: NOT RELEASE READY.** This checklist is an evidence gate, not a declaration that checks have passed.

## Build and supply chain
- [ ] Clean-checkout local debug build succeeds with pinned JDK/Gradle/SDK/NDK/CMake.
- [ ] Gradle distribution checksum and every downloaded wheel checksum are verified.
- [ ] Static direct-dependency inventory is generated with `scripts/generate_source_sbom.py`.
- [ ] Full resolved dependency graph and SPDX/CycloneDX release SBOM (including transitive artifacts, checksums and native libraries) are generated and archived.
- [ ] Every direct/transitive runtime dependency has exact version, source, license and notice review.
- [ ] Native ELF 16 KB alignment and APK alignment verified for every packaged native library.
- [ ] Build provenance includes source commit, toolchain versions, commands, APK/AAB hashes and sizes.
- [ ] Release signing key is generated/stored outside repository; signing and verification procedure is documented.

## Application and data safety
- [ ] Android manifest permissions, backup rules, exported components and cleartext settings reviewed.
- [ ] SAF import/export, revoked permission, interrupted export and provider edge cases tested.
- [ ] SQLite migrations tested from every supported prior schema.
- [ ] Process-death, cancellation, retries, duplicate scheduling and orphan cleanup tested.
- [ ] Keystore invalidation, reinstall, restore and key-loss recovery tested.
- [ ] Data deletion and flash-storage secure-deletion limitations documented.
- [ ] Independent mobile security review completed; no unresolved critical/high findings.

## Accessibility and performance
- [ ] TalkBack, large text, contrast, touch targets, keyboard/switch access, RTL and narrow screens audited.
- [ ] Cold-start, peak RSS, storage, battery and thermal benchmarks recorded across named device tiers.
- [ ] Moto G54 5G Android/API/ABI/page-size and runtime probe logs recorded.
- [ ] 16 KB page-size runtime behavior tested separately from static ELF alignment.

## Scientific integrity
- [ ] Each capability has reference datasets, source release/license, checksums, methods and tolerances.
- [ ] Independent concordance and adversarial input tests pass.
- [ ] Unsupported analyses are visibly blocked; exploratory methods are not labelled validated.
- [ ] PGx definitions and guideline content have source-specific redistribution approval and independent curator review.
- [ ] Clinical gate remains disabled unless separate legal, ethics, regulatory and clinical approvals are documented.

## Owner acceptance
- [ ] All blocking findings resolved or explicitly accepted.
- [ ] Signed artifact hashes and release notes reviewed.
- [ ] Owner explicitly approves the release.
