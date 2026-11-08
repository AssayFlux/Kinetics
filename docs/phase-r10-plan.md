# R10 — Hardening, performance, security and release readiness

**Status:** In progress. No release or device-support claim is implied.

## Scope
- Offline-by-default manifest and network permission review.
- Android Keystore encryption, app-private storage, backup exclusion and data lifecycle.
- Registry integrity, provenance, reproducible builds and dependency/license inventory.
- Accessibility, crash recovery, migration safety, process-death handling and threat modelling.
- Performance, memory, battery and thermal benchmarks on named devices.
- Release signing, SBOM, vulnerability review, privacy documentation and release checklist.

## Current source
- `scripts/check_registry.py` validates capability references, implementation paths, evidence status, validation records, device logs and clinical gates. `scripts/generate_source_sbom.py` emits an SPDX 2.3 inventory of declared direct dependencies with unresolved/transitive items explicitly marked NOASSERTION.
- `scripts/check_android_config.py` checks offline manifest settings, pinned SDK/NDK/ABI and build guardrails.
- `scripts/build_android_local.sh` is the reproducible Linux x86_64 build path. Gradle 8.13 is SHA-256 pinned and the Chaquopy 17.2.0 source commit is pinned. GitHub Actions run the same script for an unsigned arm64 debug build; no emulator or physical-device test is run.
- The Compose home and research-job list expose screen-reader descriptions for the home/status and merged job/state summaries; this is an initial accessibility affordance, not a completed accessibility audit.

## Outstanding
- Android runtime, migration, crash/process-death and Moto G54 5G verification (CI APK/AAB build and static inspection now pass).
- Accessibility audit, performance/memory/thermal benchmarks, independent security review, full transitive dependency/SBOM and license resolution.
- Release signing and privacy/data-deletion evidence.

## Exit evidence
All checks reproducible from a clean checkout; independent security review; dated device logs; measured benchmarks; signed release artifacts and owner acceptance. Never mark device-verified or validated without matching registry evidence.
