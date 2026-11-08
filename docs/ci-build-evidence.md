# CI build evidence — 2026-11-08

## Latest verified source revision

- Repository: [AssayFlux/Kinetics](https://github.com/AssayFlux/Kinetics)
- Source commit: `037befa8e9d22099e250dd22d3c4d772a6457034`
- Workflow: [run #2033 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42484179938)
- Python foundation/registry/tests: **204 passed, 4 skipped**.
- Pinned host scientific-reference comparisons: passed.
- Pinned RDKit descriptor sanity fixtures: passed.
- SPDX direct source-dependency inventory: passed; unresolved/transitive dependencies remain explicitly unresolved.
- Android ARM64 debug APK/AAB: Kotlin compilation, packaging and static APK/ELF alignment checks passed; Android JVM unit-test task completed successfully.
- APK: 69,793,535 bytes; SHA-256 `c902baada3c912e8ae5a166173e96e731c555b43ec2236031a8456c489ea990e`.
- AAB: 39,922,964 bytes; SHA-256 `f224d81850d1cb2858233ef9f82f7ed96969fc40712a96144e5b7757382c4f4d`.
- Workflow artifact ZIP: 79,984,064 bytes; SHA-256 `20c8e277605afab518f1f7cbb33fbabb71b8da3b9dfed504aab91f3b95caa22a`. This is the ZIP digest, not the APK/AAB digest.
- The verified build contains the FASTA and FASTQ Explore QC cards and their Python bridge. The FASTQ fixture line-ending defect in run #2032 was corrected in commit `037befa`; run #2033 is the successful exact-source build.

## Recent failure and repair history

- [Run #2028](https://github.com/AssayFlux/Kinetics/actions/runs/42480571753), commit `d9d6930`, failed Kotlin compilation due to the malformed `CapabilityEntry` declaration. Repaired in `282392d`; [run #2029](https://github.com/AssayFlux/Kinetics/actions/runs/42482496247) passed.
- [Run #2031](https://github.com/AssayFlux/Kinetics/actions/runs/42482779634), commit `129f93f`, passed the FASTA vertical-slice build.
- [Run #2032](https://github.com/AssayFlux/Kinetics/actions/runs/42484079010), commit `dffcd39`, built the Android artifact but failed Python tests because FASTQ sample strings contained literal backslash-n sequences instead of newline characters.
- Commit `037befa` corrected the sample and regression-fixture line endings; run #2033 passed all five jobs.

## Verification boundaries

- No emulator or physical-device installation/runtime evidence is recorded.
- CI compilation does not prove real-device launch, Chaquopy/JNI runtime, SAF lifecycle, WorkManager process-death recovery, Keystore behavior, cold-start or peak-memory performance.
- Android JVM task success is not a substitute for instrumentation/UI tests.
- Debug artifacts are not production-signed release builds.
- Build and software/reference-fixture tests do not establish independent experimental scientific validity, complete dependency licensing or clinical suitability.
- Host reference comparisons establish agreement with selected pinned software fixtures only.

D-016 requires every substantial increment to be built, regression-tested and inspected. Record exact source SHA, workflow, toolchain, artifact hashes, test results and device details; unavailable evidence remains NOT RUN or BLOCKED.
