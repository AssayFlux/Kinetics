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


## R-track imported FASTA analysis integration — 2026-11-09

### Exact-source CI evidence (integration revision before final audit patch)
- Source commit: `fc8b667951626447d951931bbfd1f901867405be`.
- Workflow: [run #2093 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42551582986).
- All five jobs passed: Python foundation/registry/tests; pinned host scientific-reference comparisons; pinned host RDKit descriptor sanity fixtures; Android ARM64 debug APK/AAB build, package checks and JVM unit tests; declared source dependency SPDX inventory.
- Android Gradle build: `BUILD SUCCESSFUL`; `:app:testDebugUnitTest` — `BUILD SUCCESSFUL`; APK ZIP alignment and native ELF alignment checks passed.
- APK: 69,875,191 bytes; SHA-256 `29db7d4014eeba7e6ab0ac57465c636f74cddbfe3b673a19c5e355c1b5e9387b`.
- AAB: 39,951,888 bytes; SHA-256 `24ce93b67a3eeb1946e1e2c51ef181032422a637cd6f595d9716eef737b8c607`.
- Workflow artifact ZIP: 80,045,596 bytes; SHA-256 `d79ef58563583f5c7f3ce0b45cbefa53f9a91c86b98b1076a8f22531d52b276c`; artifact ID `13645517097`. This digest is for the uploaded ZIP, not the APK/AAB.
- The successful build contains the imported FASTA WorkManager worker, schema-v4 durable analysis result, SHA-256 provenance, job-card inspection and SAF analysis JSON export.
- Follow-on exact-source audit commit: `2ea102719fc37354f18def85bb329a60a885ee2a`; [workflow run #2094 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42552040285). All five jobs passed, including Python foundation/registry/tests, pinned host scientific references, RDKit descriptor fixtures, SPDX inventory, and Android ARM64 APK/AAB build + JVM tests.
- Android build log: `BUILD SUCCESSFUL`; `:app:testDebugUnitTest` — `BUILD SUCCESSFUL`; APK ZIP/native ELF alignment and artifact verification passed.
- APK: 69,875,059 bytes; SHA-256 `d6b7bd05090519761bb1771b82c41f14b3c3ff2d834a1844d2ec0052babbb82b`.
- AAB: 39,951,809 bytes; SHA-256 `9c09035e9588e4af42554418c7f02e1efca2d84441f328b237f29c758c6c261f`.
- This confirms the result-digest revalidation, result-size guard and bounded preview on `2ea1027`. A later documentation/schema-only commit is being verified separately.

### Final R Step 2 audit changes (CI passed on `2ea1027`)
- Analysis export now requires current job state `succeeded` and exact equality between the current job digest and analysis-record digest.
- Worker checks non-empty record list and caps serialized output at 2,000,000 characters before persistence.
- Job-card preview is limited to 12,000 characters; full JSON is available via explicit export.

### Verification boundaries
- JVM test task is green for both `fc8b667` and `2ea1027`; no dedicated SQLite migration, analysis worker lifecycle, SAF provider failure, process-death or instrumentation test has yet been added for this vertical slice.
- No emulator or physical-device installation/runtime test is recorded. CI artifact existence is not device acceptance.
- No independent experimental validation or clinical suitability is implied.


### Exact-source private plaintext cleanup regression — 2026-11-09
Commit `c157bb5a09d9dcc17a8bc7a57b60129d58e4866a`, [workflow run #2100 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42553589465). All five CI jobs passed, including Android ARM64 debug APK/AAB packaging, APK/native alignment checks, Android JVM tests, Python foundation/registry tests, pinned scientific reference fixtures, RDKit sanity fixtures and SPDX inventory.
- Android JVM task: `:app:testDebugUnitTest` — BUILD SUCCESSFUL.
- APK: 69,875,783 bytes; SHA-256 `74275b4552fdab7e009bc067cbb27263e7296f860bb17b52257bbd20cbbd7462`.
- AAB: 39,953,164 bytes; SHA-256 `c89ad4bb971e9d76410592ba7d76655c7c029b63ce74c5895203edc0a1e7dc7b`.
- Artifact ZIP: 80,047,831 bytes; SHA-256 `c10568ef4d18f28ea9313b159e7b967103f29728661ce91b448e53c087107e0a`; artifact ID `13646870988`.
- New JVM regression tests verify temporary plaintext deletion after failed materialization, consumer exceptions and successful analysis.
- CI validates build/package/JVM and host checks only. It does not prove Android device runtime, secure erasure, database migration or end-to-end WorkManager/SAF lifecycle.
