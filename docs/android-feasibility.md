# Android feasibility — R1 in progress

**Current status (2026-11-08):** R1 remains IN PROGRESS. Historical CI runs 1471 and 1481 built arm64 debug APK/AAB artifacts and passed static APK/ELF alignment checks. These are historical build/package results only. No fresh local APK build is claimed, and Android runtime/device tests, SciPy, a separately evaluated scientific engine, RDKit/alternative, offline viewer and performance measurements remain unresolved.

**Owner build/test instruction (2026-11-08):** GitHub Actions must not build APK/AAB files or run Android emulator/device tests. The owner intends to build the debug APK locally first and defer physical-device testing until later. GitHub Actions now runs host-side Python, registry, lint, type and unit-test checks only. Do not restore Android build/test jobs without a new explicit owner instruction.

**Phase plan:** docs/phase-r1-plan.md  
**Owner gate:** R1 go/no-go review required before R2

## Current evidence boundary

An isolated Android arm64 feasibility app and Chaquopy probe now exist under `android/`. The Gradle configuration targets arm64-v8a and includes Python 3.11, Biopython and NumPy for the current APK probe. SciPy is tracked separately as a required but currently unavailable R1 candidate. These are prototype dependencies only, not a production architecture or dependency approval.

Historical runs 1381 and 1384 exposed host-Python provisioning and then Biopython package-resolution blockers; both have been addressed. The current CI cross-build successfully creates a pinned Biopython 1.88 Android wheel (SHA-256 `cdf569ea13eb9314e43afeb9bbd3dbdbf95616d138f775a2e12e4cb7ba0cecbf`). Gradle consumed that wheel and NumPy 1.26.2 successfully after SciPy was removed from the immediate APK probe. It progressed through Python packaging, Android resource processing and stopped at Kotlin compilation because Java bytecode target 1.8 did not match Kotlin target 17. The build configuration is being aligned to JVM 17. SciPy remains an unresolved architecture requirement. No APK/AAB artifact exists yet.

No Android app runtime, emulator or physical-device result is yet accepted as validated. No successful on-device Python import, Rust app call, C++ JNI, scientific engine, RDKit, offline viewer, 16 KB runtime, startup, memory or device result is claimed.

## Initial research findings

### Android 16 KB page sizes

- Android 15 and later support 16 KB page-size devices. Native shared libraries must have compatible ELF segment alignment; prebuilt native libraries need separate verification/rebuild.
- Android's current guidance says NDK r28 and later produce 16 KB-aligned shared libraries by default. Older NDK versions require explicit linker flags and additional care.
- Android documents emulator-based 16 KB testing and checking the runtime page size with `adb shell getconf PAGE_SIZE`; APK alignment can be checked with `zipalign -c -P 16 -v 4`.
- Google's published requirement applies to updates targeting Android 15 / API 35 or higher on 64-bit devices from 2027-02-01.
- Every transitive native dependency must be inspected, not only Kinetics' own JNI library.

Sources:
- Android Developers, Support 16 KB page sizes: https://developer.android.com/guide/practices/page-sizes
- Android Developers, 16 KB emulator and validation instructions: https://developer.android.com/guide/practices/page-sizes

### Embedded Python candidate: Chaquopy

- Chaquopy 17.2 is configured in the isolated R1 prototype with Python 3.11.
- The app probe imports Python, Biopython and NumPy, runs a FASTA parsing and numerical smoke test, and reports SciPy availability without masking ABI/import failures. It has not yet executed successfully on Android.
- Package availability and native ABI compatibility remain unproven until the Gradle build and runtime probe succeed.
- Chaquopy remains an R1 candidate only; no production selection or release bundling approval is implied.

Sources:
- Chaquopy documentation: https://chaquo.com/chaquopy/documentation/
- Version compatibility: https://chaquo.com/chaquopy/doc/current/versions.html
- Licensing: https://chaquo.com/chaquopy/license/
- Package availability FAQ: https://chaquo.com/chaquopy/doc/current/faq.html
- Upstream license: https://github.com/chaquo/chaquopy/blob/master/LICENSE.txt

## Biopython packaging investigation — 2026-11-07

### Finding

The run-1384 failure is consistent with a package-format/ABI gap, not a missing Python interpreter. Chaquopy's current FAQ classifies “No matching distributions” as a package/version not available for Android. Its current package documentation explains that Android-native packages require compatible Android wheels; the Chaquopy index contains many native packages but does not list Biopython. Biopython's upstream installation guidance says source builds require Python development headers and a C compiler, so a generic source distribution cannot be assumed to install in the Android build environment.

Chaquopy 17's pip behavior is particularly important: it uses binary-only resolution for normal index installs. Its documentation describes building Android wheels with its package-build tooling (for Python 3.12 and older) or cibuildwheel (Python 3.13+), then supplying the resulting wheel through a local `--find-links` directory. Therefore, simply changing the pip index, loosening the version, or adding a source URL is not an evidence-based fix.

### Implemented CI experiment (Biopython wheel and arm64 APK/AAB built)

1. Keep the current Python 3.11 / arm64-v8a baseline for this controlled experiment.
2. Added `android/biopython-wheel/meta.yaml`, pinned to Biopython 1.88, and a CI step which checks out Chaquopy 17.2.0, downloads its Python 3.11.17 target and NumPy 1.26.2 Android wheel, and invokes Chaquopy's documented `build-wheel.py` for arm64-v8a.
3. Updated the Android Gradle pip configuration to consume the generated local wheel using --find-links, with Biopython and NumPy versions pinned. The first complete wheel build succeeded, but the following Gradle package-resolution run found no compatible SciPy distribution in the configured Chaquopy indexes. The R1 APK probe therefore tests Biopython and NumPy while reporting SciPy as unavailable; SciPy remains a required architecture candidate and is not declared supported or dropped. The initial wheel-build attempts exposed two upstream Chaquopy 17.2.0 build-tool issues. First, its SONAME alias loop tried to create libpython.so twice when both stable-ABI and version-specific Python libraries were present; CI now applies an assertion-checked ln -sf patch so the version-specific alias wins. Second, compiler-wrapper.py rejected the checked-out wheel build's own host library path as outside its safe directories, stripping -L and -I arguments; CI now adds only GITHUB_WORKSPACE as an allowed safe root for those build paths. Both are local, pinned-toolchain compatibility patches and require review if the builder is upgraded. The Python 3.11 NumPy 1.26.2 wheel available in Chaquopy's index dates from 2023; Chaquopy warns that older Android wheels may not be 16 KB-page compatible. This is an explicit risk to test, not a compatibility claim. If it fails, the next candidate is a newer Android wheel or a Python 3.13+ build path.
4. The workflow prints the wheel SHA-256 and proceeds to APK/AAB build only if the cross-build succeeds.
5. Still required: execute the Python/Biopython/NumPy probe including SeqIO and Bio.PDB tests on an arm64 emulator and physical arm64 device; record startup and RSS. Static packaged ELF alignment has been inspected.
6. If the custom wheel build fails or is not maintainable, evaluate a narrower native implementation for the specific required operations while retaining Biopython for desktop/remote workflows only if the architecture and capability registry explicitly describe that difference. This remains a fallback proposal, not a decision.

### Licensing note

Biopython's upstream license file identifies the Biopython License Agreement as the license for most files, while some files are explicitly dual-licensed under that agreement or BSD-3-Clause. Do not label the entire package BSD-3-Clause without a file-level/source-release audit. Preserve required notices in source and binary distributions and add the exact upstream license texts to the third-party notices if the dependency is adopted. This is a feasibility finding only; it is not approval to bundle.

### Sources

- Chaquopy FAQ: https://chaquo.com/chaquopy/doc/current/faq.html
- Chaquopy wheel-building instructions: https://github.com/chaquo/chaquopy/tree/master/server/pypi
- Chaquopy package index: https://chaquo.com/pypi-13.1/
- Chaquopy 17 change log (binary-only pip behavior and 16 KB wheel caveat): https://chaquo.com/chaquopy/doc/current/changelog.html
- Chaquopy legacy wheel-builder instructions for Python 3.12 and older: https://github.com/chaquo/chaquopy/blob/17.2.0/server/pypi/README-old.md
- Chaquopy 17.2.0 Python runtime version table: https://github.com/chaquo/chaquopy/blob/17.2.0/product/buildSrc/src/main/java/com/chaquo/python/internal/Common.java
- Biopython installation/build instructions: https://pypi.org/project/biopython/
- Biopython license: https://github.com/biopython/biopython/blob/master/LICENSE.rst

## R1 experiment matrix

| Area | Current status | Required next evidence |
|---|---|---|
| Minimal Compose app / Gradle build | CI run 1454 successful; debug APK 63 MiB, AAB 36 MiB; artifact uploaded | On-device install/launch, startup/RSS and repeatable release-build assessment |
| Embedded Python runtime | Chaquopy 17.2 / Python 3.11 packaged; app APK/AAB built; runtime not executed | On-device import/startup/RSS logs |
| Biopython | Custom Biopython 1.88 wheel built and packaged; Bio.PDB, SeqIO and PairwiseAligner probes added; runtime not executed | Run FASTA and PDB parser tests on emulator and physical arm64 device; license file audit |
| NumPy | NumPy 1.26.2 packaged; all inspected APK/AAB native ELF PT_LOAD segments pass 16 KB alignment | Runtime import/numerical smoke test on emulator and physical arm64 device; assess wheel age/maintenance |
| SciPy | Gradle resolution failed: no compatible distribution on the configured Chaquopy indexes for CPython 3.11 / arm64-v8a | Evaluate a custom Android wheel or a documented on-device alternative; otherwise define an explicit on-device vs remote-compute capability boundary and obtain owner approval |
| Rust app FFI | Rust static library cross-compiled successfully and linked into packaged arm64 JNI library in CI; exported Rust symbol verified in artifact; runtime call pending | Run `sumSquares(3,4)=25` on emulator and physical device; cancellation/timeout test |
| C++17 JNI | CMake/NDK built and packaged `libkinetics_native.so`; both JNI entry points exported and 16 KB aligned; runtime invocation pending | Run numeric correctness test on emulator and physical device; sanitizer-capable host tests |
| One real scientific engine | Biopython `Bio.Align.PairwiseAligner` added as a real sequence-alignment algorithm test (global alignment score 5.0 for ACGT vs ACCT); Android runtime not executed | Run the fixed alignment vector on arm64 Android; record algorithm/version/license and limits; decide whether a separate domain engine is needed |
| RDKit / alternative | Not tested | arm64 build, dependency/license/size and smoke test |
| Offline Mol* / 3Dmol.js | Not implemented/tested | Bundled viewer renders known structure without network |
| 16 KB ELF / APK alignment | `zipalign -P 16` passed; all 22 native ELF libraries in APK and AAB are AArch64 with PT_LOAD alignment 0x4000 | Run app on 16 KB Android emulator/device and confirm runtime page size |
| Cold start / peak memory / package size | APK 63 MiB; AAB 36 MiB; cold start and RSS not measured | Repeatable measurements on emulator and low/mid/flagship physical devices |
| SAF / background / cancellation | Not implemented/tested | Import and job lifecycle tests on Android |

## Device matrix

D-006 is approved: target Android 10+ (API 29), 64-bit ARM (arm64-v8a), with low-end, mid-range and flagship test tiers. This is a target matrix, not verified compatibility across all devices. No physical target device has yet been nominated or provided. Emulator experiments can proceed, but cannot substitute for a real arm64 device; actual supported-device limits remain evidence-dependent.

| Target | Model / SoC / RAM | Android | Page size | Status |
|---|---|---|---|---|
| Emulator | To be recorded | Android 15+ 16 KB image | 16 KB | Not run |
| Physical arm64 | Owner to nominate/provide | To be recorded | To be measured | Blocked on target device |

## Preliminary assessment (not a go/no-go; updated after CI run 1481)

- The host-Python prerequisite, Biopython wheel build, JVM target mismatch and subsequent APK/AAB packaging blockers have been resolved in CI.
- CI run 1481 successfully built the arm64 debug APK and AAB, built the pinned Biopython 1.88 arm64 wheel, compiled Rust and C++17 JNI, and passed APK ZIP plus static ELF 16 KB alignment checks. APK is 63 MiB; AAB is 36 MiB.
- Static artifact inspection proves packaging/alignment only. It does not establish Android app launch, native calls, Python/Biopython/NumPy imports, 16 KB kernel runtime, cold-start, peak memory or physical-device compatibility.
- SciPy is still unavailable in the current Chaquopy Android package path. No conclusion is yet possible about the complete intended architecture until the remaining R1 experiments are run.
- R1 remains in progress. R2 must not start until the full experiment matrix and owner go/no-go review are complete.

## Evidence capture template

For every run record: date; commit; host OS; JDK/Gradle/AGP/Kotlin/SDK/NDK versions; dependency versions and licenses; device model/SoC/RAM/Android/API/ABI/page size; exact command; output/log link; artifact hash/size; cold-start method and repetitions; peak memory method; result (pass/fail/blocked); limitations and reproduction steps.


## CI run 1454 — arm64 build and static package inspection

- Workflow: https://github.com/AssayFlux/Kinetics/actions/runs/42383161737
- Commit: `87a5b6f0fcae54de6858bc32d7472379ba09ccc7`
- Android arm64 job and Python foundation job: both successful.
- Python foundation: Ruff, mypy, registry validation, reproduction stub and all 11 unit tests passed.
- Chaquopy 17.2.0 / Python 3.11.17-0, Biopython 1.88 custom arm64 wheel, NumPy 1.26.2; SciPy was not installed.
- Debug APK: 65,388,299 bytes (about 62.3 MiB); debug AAB: 37,573,255 bytes (about 35.8 MiB).
- Downloaded workflow artifact archive: 75,463,086 bytes; GitHub artifact digest: `sha256:48c14aa1e8f642f2c44ee11b1c69ec605ac3b92e599588b7351a496edd7eda04`.
- Extracted APK SHA-256: `a6cd53256acfa8d408ef3fddbf8da37c98367f9dbcd082fe9c68ebcb4d53152b`.
- Extracted AAB SHA-256: `def0e546c518f721d839b2c4238df1a95bca75db269ca3206645e3a8c0b46dda`.
- APK ZIP alignment passed with build-tools 36.0.0 `zipalign -c -P 16 -v 4`.
- Independent inspection of both archives found 22 native shared libraries per archive, all ELF64 little-endian AArch64. Every PT_LOAD segment had `p_align=0x4000` (16,384 bytes). A repeatable repository checker is now in CI.
- Interpretation: build, packaging and static 16 KB ELF alignment pass. This does not establish app launch, native loading, Python imports, or operation on a 16 KB kernel/device.

## Outstanding R1 exit blockers

The R1 exit criteria in `docs/phase-r1-plan.md` are not met. No arm64 emulator or physical device run is available in this session. SciPy remains unresolved. Rust FFI and C++17 JNI prototypes have now cross-compiled, linked and packaged successfully in CI; static symbol and 16 KB alignment checks passed. Device runtime remains pending. A real scientific engine, RDKit/alternative, offline molecular viewer, SAF/background/cancellation, cold-start and memory measurements remain unimplemented or untested. Biopython's file-level license audit and production redistribution approval are also outstanding. Do not start R2 or declare an R1 go/no-go until these outcomes and the owner review are recorded.


## Native-language prototype additions

A minimal Rust static library and C++17 JNI bridge now exist under `android/native-rust/` and `android/app/src/main/cpp/`. The Kotlin `NativeProbe` exposes two test functions which should both return 25 for inputs 3 and 4. CI cross-compiles Rust for `aarch64-linux-android`, then Gradle/CMake links the Rust static library into an arm64 JNI shared object. This is an FFI feasibility probe only: it is not a scientific engine, and no on-device invocation has yet been observed. The resulting shared library must also pass the 16 KB ELF check in CI.


## CI run 1471 — Rust/C++ integration and repeatable ELF gate

- Workflow: https://github.com/AssayFlux/Kinetics/actions/runs/42384355517
- Commit: `2683a4f2212f3337593a1ac0ff0d59cc4105f986`
- Both Python foundation and Android arm64 jobs completed successfully.
- Rust target `aarch64-linux-android` cross-compilation passed.
- Gradle/CMake compiled and linked the C++17 JNI shared library with the Rust static library.
- Android probe exports verified in the packaged `libkinetics_native.so`: `Java_org_assayflux_kinetics_NativeProbe_rustSumSquares`, `Java_org_assayflux_kinetics_NativeProbe_cppSumSquares`, and `kinetics_rust_sum_squares`.
- APK: 65,405,092 bytes; SHA-256 `fca08d6ba9b0b0cecb63f93d9f6c0cdeb7d115253cb80a227fd009ea57cabf09`.
- AAB: 37,577,400 bytes; SHA-256 `1c27e74a9501e32c2381ca387f4de88c2a2373d7da38efd28ca59ed563db1509`.
- Workflow artifact archive: 75,471,020 bytes; digest `sha256:38f0f76879623d2a243c69dbce0208d9fb2fe646c4370ca2936adef6786e6143`.
- Both APK and AAB contain 23 native ELF libraries. Independent inspection found all are ELF64 little-endian AArch64, and every PT_LOAD segment in every library has at least 16 KB alignment. The CI checker passed for both artifacts, as did `zipalign -c -P 16 -v 4`.
- This proves cross-compilation, linking, packaging, exported symbol presence and static ELF alignment. It does not prove JNI calls execute correctly on Android; no emulator or physical-device runtime has been run.


## Owner/device validation runbook

The build artifacts are available from CI run 1471. Download the `kinetics-r1-android-arm64` artifact from the workflow page, extract `apk/debug/app-debug.apk`, and connect one Android 10+ arm64 phone with USB debugging enabled.

Capture the device identity and page size before installing:

```sh
adb devices
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.product.cpu.abi
adb shell getconf PAGE_SIZE
```

Install and launch the debug APK:

```sh
adb install -r app-debug.apk
adb logcat -c
adb shell am force-stop org.assayflux.kinetics
adb shell am start -W -n org.assayflux.kinetics/.MainActivity
adb logcat -d -s KineticsR1
adb shell dumpsys meminfo org.assayflux.kinetics
```

The expected native line is `Rust FFI: 25.0; C++17 JNI: 25.0`. The Python report should show successful Python/Biopython/NumPy imports, FASTA parsing, one GLY PDB residue, PairwiseAligner score 5.0 and NumPy norm 5.0. SciPy is expected to report unavailable in this prototype. Capture the complete log, screenshot, model/SoC/RAM, Android/API, ABI, page size, cold-start time and memory. Repeat launch/memory measurements at least five times after a clean force-stop and record every result, including failures.

A device reporting page size 16384 is a 16 KB runtime target. A device reporting 4096 is still useful for the Android 10+ baseline but does not replace a 16 KB emulator/device test. Repeat on representative low-end, mid-range and flagship arm64 devices before proposing a support matrix. Do not interpret CI static ELF alignment as a runtime pass.


## CI run 1481 — integrated arm64 build and static alignment re-confirmed

- Workflow: https://github.com/AssayFlux/Kinetics/actions/runs/42384785011
- Commit: `a7c3fd885f408bfcd46d487d58f96358129b03b2`.
- Both workflow jobs passed: Python foundation/registry/tests and R1 Android arm64 feasibility build.
- Android steps passed: Rust arm64 cross-compilation; pinned Chaquopy 17.2.0 wheel-builder preparation; Biopython 1.88 arm64 wheel build; Gradle debug APK/AAB build; APK ZIP alignment; static native ELF alignment; artifact upload.
- APK: 63 MiB. AAB: 36 MiB. Uploaded artifact: 75,471,340 bytes; artifact ID 13579510157; digest `sha256:1c545a16edbea1453652d7c7321af4610764ad897ec39f04fdf5b66908db45fc`.
- The ELF checker reports a minimum PT_LOAD alignment of 16,384 bytes for every inspected native library in both APK and AAB. Rust and C++ JNI symbols are present in the packaged arm64 library.
- The workflow does not boot an Android emulator and does not execute the APK. Therefore Python runtime, JNI runtime, 16 KB page-size runtime, startup, RSS and device support remain unverified.

## R1 status after run 1481

Build and static package evidence is green. R1 is **not complete**. Outstanding: 16 KB emulator runtime; Android arm64 physical-device runtime; Python/Biopython/NumPy runtime tests; Rust/C++ invocation; SciPy decision/packaging experiment; separate domain scientific engine evaluation; RDKit or alternative; offline Mol*/3Dmol.js; SAF import/background/cancellation; repeatable cold-start and peak RSS; Biopython file-level license audit and third-party redistribution review. No R1 go/no-go has been issued.


## Owner workflow directive — 2026-11-08

- APK/AAB building is removed from GitHub Actions. The historical run records below are retained as immutable historical evidence.
- Android emulator testing is removed from GitHub Actions. No automated emulator runtime pass is claimed.
- Local debug APK build is the next build route when the owner is ready. Physical-device testing is deferred by owner instruction.
- Device-dependent rows remain pending; they are not silently waived from R1 exit criteria.
- The local build guide is [docs/local-android-build.md](local-android-build.md), using [scripts/build_android_local.sh](../scripts/build_android_local.sh). The local build must record the source commit, JDK/Gradle/AGP/Kotlin/SDK/NDK/CMake/Rust versions, dependency/wheel inputs, APK/AAB hashes and sizes, and build logs. If the custom Biopython wheel path cannot be reproduced locally, record that blocker instead of substituting an unverified package.


## Host-only source CI run 42428857132 — 2026-11-08

- Workflow: https://github.com/AssayFlux/Kinetics/actions/runs/42428857132
- Commit: `aeaeee1b2f8075ce944cf1092f3d0d14c676aa70`.
- Python foundation job completed successfully.
- Pre-commit configuration validation, Ruff, mypy (7 source files), registry validation and all 11 unit tests passed.
- Reproduction stub ran and correctly reported no reproduction jobs registered.
- Android artifact gate reported the owner-directed local-only build/test boundary.
- `bash -n scripts/build_android_local.sh` passed.
- No APK/AAB build, emulator or Android runtime test was run in this workflow, as instructed.


## Host-only source CI run 42428935274 — 2026-11-08

- Workflow: https://github.com/AssayFlux/Kinetics/actions/runs/42428935274
- Commit: `6580e4b254aafa09da4543b490b7af4b457d9637`.
- Pre-commit configuration, Ruff, mypy, registry validation and all 11 unit tests passed.
- Reproduction stub, owner-directed local-only Android artifact gate and local build-script `bash -n` syntax check passed.
- No APK/AAB build or Android runtime test was run in GitHub Actions.
