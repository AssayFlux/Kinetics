# CI build evidence — 2026-11-08

## Latest source revision

- Repository: [AssayFlux/Kinetics](https://github.com/AssayFlux/Kinetics)
- Source commit: `d9d693040bf6ad83fdc01aca363dce7e3b5fb521`
- Workflow: [run #2028 — failed](https://github.com/AssayFlux/Kinetics/actions/runs/42480571753)
- Failure: Android Kotlin compilation in `android/app/src/main/java/org/assayflux/kinetics/KineticsUi.kt`, where `CapabilityEntry` was incorrectly declared as `@Composable private private data class`.
- Passed before the Android failure: Python foundation/tests, registry checks/catalogue generation, pinned scientific-reference comparisons, RDKit descriptor sanity fixtures and SPDX source inventory.
- Not run because compilation failed: Android JVM tests, APK/AAB packaging and artifact checks.
- No APK/AAB exists for this source revision.

## Previous successful build (not current source)

- Workflow: [run #2027](https://github.com/AssayFlux/Kinetics/actions/runs/42479673744)
- Source commit: `c3b047914d2ed729062cb2415591aaee1cc6a564`
- Result: arm64 debug APK/AAB built and package alignment checks passed.
- This artifact predates commit #2028 and must not be presented as containing the current Explore catalogue changes or later UI work.

## Verification boundaries

- No emulator or physical-device installation/runtime evidence is recorded.
- CI compilation does not prove launch, embedded Python import, JNI invocation, SAF lifecycle, WorkManager process-death recovery, Keystore behavior, cold-start or peak-memory performance.
- Debug artifacts are not signed release builds.
- Build success and unit tests do not establish independent scientific validity, complete dependency licensing or clinical suitability.

D-016 requires every substantial increment to be built, regression-tested and inspected before acceptance. Record exact source SHA, workflow, toolchain, artifact hash, test results and device details; explicitly mark unavailable evidence as not run or blocked.
