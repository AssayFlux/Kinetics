# CI build evidence — 2026-11-08

## Latest verified source revision

- Repository: [AssayFlux/Kinetics](https://github.com/AssayFlux/Kinetics)
- Source commit: `79a24eb00ec7beea30674a591361c2351beaa13d` — `Apply D-015 adaptive theme to local biometric lock screen`.
- Workflow: [run #2039 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42493028735).
- All five jobs passed: Python foundation/registry/tests; pinned host scientific-reference comparisons; pinned RDKit descriptor sanity fixtures; SPDX direct source-dependency inventory; Android ARM64 debug APK/AAB build, package checks and Android JVM unit-test task.
- Android build log: `BUILD SUCCESSFUL`; package-alignment and artifact-hash verification steps passed.
- APK: 69,792,811 bytes; SHA-256 `7029555e9640fd920f22a67890fe921473582affd2538e8aaddd61a261c9e44e`.
- AAB: 39,926,363 bytes; SHA-256 `dd6eb3cc6ddc97c9ed3036b4d6e0747c2e91ef2a6ee57f80eaa4e11e28b8cfa9`.
- Workflow artifact ZIP: 79,991,103 bytes; SHA-256 `4b6211b80b9a50a773bdb38c20ee6f7026e327255844f1eeffeb696bc613d8cd`. This is the ZIP digest, not the APK/AAB digest.
- The exact-source UI change applies the D-015 adaptive Light/Dark/System theme to the local biometric/device-credential app-lock screen. The screen explicitly distinguishes local device unlock from online account sign-in and does not handle biometric templates.

## Previous verification

- [Run #2038](https://github.com/AssayFlux/Kinetics/actions/runs/42486834053), commit `5471974`, passed the complete CI suite and produced an ARM64 debug APK/AAB.
- [Run #2033](https://github.com/AssayFlux/Kinetics/actions/runs/42484179938), commit `037befa`, passed 204 Python tests (4 skipped), pinned host reference comparisons, RDKit sanity fixtures, SPDX direct inventory, Android build/package checks and JVM unit-test task.

## Verification boundaries

- No emulator or physical-device installation/runtime evidence is recorded for run #2039.
- CI compilation does not prove real-device launch, Chaquopy/JNI runtime, SAF lifecycle, WorkManager process-death recovery, Keystore behavior, cold-start or peak-memory performance.
- Android JVM task success is not a substitute for instrumentation/UI tests.
- Debug artifacts are not production-signed release builds.
- Build and software/reference-fixture tests do not establish independent experimental scientific validity, complete dependency licensing or clinical suitability.
- Host reference comparisons establish agreement with selected pinned software fixtures only.

D-016 requires every substantial increment to be built, regression-tested and inspected. Record exact source SHA, workflow, toolchain, artifact hashes, test results and device details; unavailable evidence remains NOT RUN or BLOCKED.
