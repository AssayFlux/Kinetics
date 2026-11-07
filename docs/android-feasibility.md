# Android feasibility — R1 in progress

**Status:** IN PROGRESS — Python provisioning correction succeeded; Android arm64 build now reaches Chaquopy dependency resolution but fails because no compatible Biopython distribution is available from the configured indexes  
**Last updated:** 2026-11-07  
**Phase plan:** docs/phase-r1-plan.md  
**Owner gate:** R1 go/no-go review required before R2

## Current evidence boundary

An isolated Android arm64 feasibility app and Chaquopy probe now exist under `android/`. The Gradle configuration targets arm64-v8a and includes Python 3.11 with Biopython, NumPy and SciPy as an R1 experiment. These are prototype dependencies only, not a production architecture or dependency approval.

The first GitHub Actions Android build (run 1381, commit `fe63ecf56538d4e1d494c44a51dfb9b5654b199a`) reached Chaquopy's Python-requirements task and failed because the runner did not have a discoverable Python 3.11 executable. The Python/registry/tests CI job passed. The workflow now explicitly provisions Python 3.11 before Gradle; commit `6705fe8dc27b90e3dea8482b21d89c7fe321afbd`. Workflow run 1384 (commit `3bd4e152faf4007e44cd3fc0de63e5a26ecf065e`) confirms that Python 3.11 setup and Android SDK/NDK provisioning now succeed. The Gradle build then fails at `:app:installDebugPythonRequirements`: pip reports no matching distribution for `biopython` from the configured PyPI and Chaquopy indexes. APK alignment, size reporting and artifact upload are skipped. This is a dependency-availability blocker, not an Android compilation or runtime result.

No APK/AAB, app runtime, emulator or physical-device result is yet accepted as validated. No embedded package import, Rust app call, C++ JNI, scientific engine, RDKit, offline viewer, 16 KB runtime, startup, memory or device result is claimed.

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
- The app probe imports Python, Biopython, NumPy and SciPy and reports versions. This code has not yet executed successfully on Android.
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

### Candidate path (not yet implemented or validated)

1. Keep the current Python 3.11 / arm64-v8a baseline for the first controlled experiment, so the result isolates the current blocker.
2. Check whether upstream Biopython already has an Android-compatible wheel for the exact CPython/ABI target. If not, prototype a reproducible Android wheel build using Chaquopy's documented Python 3.12-and-older build tooling or a compatible upstream recipe.
3. Inspect every compiled extension and linked native dependency in the wheel; do not assume that a successful wheel build proves runtime compatibility or 16 KB page-size compatibility.
4. Install only the locally built, hash-pinned wheel via Chaquopy's documented `--find-links` mechanism. Keep the artifact and build recipe reproducible in CI.
5. Run import and representative sequence/structure parsing and alignment smoke tests on an arm64 emulator, then repeat on a physical arm64 device. Record package size, startup and RSS.
6. If a reproducible, maintainable wheel cannot be built, evaluate a narrower native implementation for the specific required operations while retaining Biopython for desktop/remote workflows only if the architecture and capability registry explicitly describe that difference. This is a fallback proposal, not a decision.

### Licensing note

Biopython's upstream license file identifies the Biopython License Agreement as the license for most files, while some files are explicitly dual-licensed under that agreement or BSD-3-Clause. Do not label the entire package BSD-3-Clause without a file-level/source-release audit. Preserve required notices in source and binary distributions and add the exact upstream license texts to the third-party notices if the dependency is adopted. This is a feasibility finding only; it is not approval to bundle.

### Sources

- Chaquopy FAQ: https://chaquo.com/chaquopy/doc/current/faq.html
- Chaquopy wheel-building instructions: https://github.com/chaquo/chaquopy/tree/master/server/pypi
- Chaquopy package index: https://chaquo.com/pypi-13.1/
- Chaquopy 17 change log (binary-only pip behavior): https://chaquo.com/chaquopy/doc/current/changelog.html
- Biopython installation/build instructions: https://pypi.org/project/biopython/
- Biopython license: https://github.com/biopython/biopython/blob/master/LICENSE.rst

## R1 experiment matrix

| Area | Current status | Required next evidence |
|---|---|---|
| Minimal Compose app / Gradle build | Workflow run 1384 provisions Python 3.11 and SDK/NDK successfully; Gradle stops at Chaquopy's Biopython requirement resolution before APK compilation | Resolve a supported Biopython packaging strategy or select a justified alternative; then successful APK/AAB build and toolchain record |
| Embedded Python runtime | Chaquopy probe configured; not executed | arm64 build/import/startup/RSS/package-size logs |
| Biopython | Run 1384 has no compatible indexed Android distribution; upstream docs indicate a custom Android wheel may be required. No Android package installed. | Check exact wheel availability; prototype reproducible Python 3.11/arm64 wheel build; inspect extensions/ELF/license; import and scientific smoke tests on emulator and physical arm64 device |
| NumPy / SciPy | Declared in R1 probe; not tested on Android | Native wheel ABI, import and numerical smoke tests |
| Rust app FFI | Not implemented/tested | Android arm64 library and Kotlin call test |
| C++17 JNI | Not implemented/tested | NDK build, JNI invocation and numeric correctness test |
| One real scientific engine | Not selected | License review, Android build, real test vector |
| RDKit / alternative | Not tested | arm64 build, dependency/license/size and smoke test |
| Offline Mol* / 3Dmol.js | Not implemented/tested | Bundled viewer renders known structure without network |
| 16 KB ELF / APK alignment | Not tested; workflow check is configured after successful build | ELF inspection, zipalign and 16 KB emulator/device run |
| Cold start / peak memory / package size | Not measured | Repeatable measurements with environment metadata |
| SAF / background / cancellation | Not implemented/tested | Import and job lifecycle tests on Android |

## Device matrix

D-006 is approved: target Android 10+ (API 29), 64-bit ARM (arm64-v8a), with low-end, mid-range and flagship test tiers. This is a target matrix, not verified compatibility across all devices. No physical target device has yet been nominated or provided. Emulator experiments can proceed, but cannot substitute for a real arm64 device; actual supported-device limits remain evidence-dependent.

| Target | Model / SoC / RAM | Android | Page size | Status |
|---|---|---|---|---|
| Emulator | To be recorded | Android 15+ 16 KB image | 16 KB | Not run |
| Physical arm64 | Owner to nominate/provide | To be recorded | To be measured | Blocked on target device |

## Preliminary assessment (not a go/no-go)

- The Android project is build-configured. The host-Python prerequisite is now resolved: run 1384 successfully installs Python 3.11 and Android SDK/NDK.
- The next blocker is Chaquopy's inability to resolve a compatible Biopython Android wheel. Upstream guidance points to a custom Android-wheel build as the preferred experiment if no suitable wheel exists. The build fails before APK compilation; no APK/AAB artifact exists from this run.
- No conclusion is yet possible about overall architecture feasibility, memory fit, APK/AAB size or real-device performance.
- R1 remains in progress. R2 must not start until the full experiment matrix and owner go/no-go review are complete.

## Evidence capture template

For every run record: date; commit; host OS; JDK/Gradle/AGP/Kotlin/SDK/NDK versions; dependency versions and licenses; device model/SoC/RAM/Android/API/ABI/page size; exact command; output/log link; artifact hash/size; cold-start method and repetitions; peak memory method; result (pass/fail/blocked); limitations and reproduction steps.
