# Android feasibility — R1 in progress

**Status:** IN PROGRESS — custom Biopython 1.88 / CPython 3.11 / arm64 wheel build is wired into CI; first attempt found an upstream SONAME alias collision before compilation, now patched in the CI checkout; retry and subsequent APK/runtime/device evidence pending  
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

### Implemented CI experiment (not yet validated)

1. Keep the current Python 3.11 / arm64-v8a baseline for this controlled experiment.
2. Added `android/biopython-wheel/meta.yaml`, pinned to Biopython 1.88, and a CI step which checks out Chaquopy 17.2.0, downloads its Python 3.11.17 target and NumPy 1.26.2 Android wheel, and invokes Chaquopy's documented `build-wheel.py` for arm64-v8a.
3. Updated the Android Gradle pip configuration to consume the generated local wheel using --find-links, with Biopython and NumPy versions pinned. The first wheel-build attempt exposed an upstream Chaquopy 17.2.0 build-tool collision: its SONAME alias loop tries to create libpython.so twice when both stable-ABI and version-specific Python libraries are present. The CI workflow now applies a narrow, assertion-checked local patch to use ln -sf for that alias, so the version-specific alias wins. The Python 3.11 NumPy 1.26.2 wheel available in Chaquopy's index dates from 2023; Chaquopy warns that older Android wheels may not be 16 KB-page compatible. This is an explicit risk to test, not a compatibility claim. If it fails, the next candidate is a newer Android wheel or a Python 3.13+ build path.
4. The workflow prints the wheel SHA-256 and proceeds to APK/AAB build only if the cross-build succeeds.
5. Still required: inspect every compiled extension and linked native dependency; run import and representative sequence/structure parsing and alignment smoke tests on an arm64 emulator; repeat on a physical arm64 device; record package size, startup and RSS.
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
| Minimal Compose app / Gradle build | Workflow run 1384 stopped before APK compilation at Biopython resolution. CI now cross-builds a pinned Android wheel before Gradle; outcome pending | Successful wheel build, APK/AAB build, alignment check, artifact hash/size and toolchain record |
| Embedded Python runtime | Chaquopy probe configured; not executed | arm64 build/import/startup/RSS/package-size logs |
| Biopython | First CI attempt downloaded source and prepared cross-build but failed in Chaquopy's SONAME alias step before compiling Biopython; CI now applies a narrow alias-collision patch and retries | Successful wheel build; extension/ELF inspection; runtime import, SeqIO FASTA and Bio.PDB parsing test vectors on emulator and physical arm64 device |
| NumPy / SciPy | NumPy 1.26.2 cp311 arm64 wheel is a pinned build input; its 2023 build date creates a known 16 KB alignment risk. SciPy remains untested on Android | Inspect every packaged ELF; if NumPy is not 16 KB compatible, rebuild/select a newer supported stack; import and numerical smoke tests |
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
- The prior package-resolution blocker has been replaced by a custom-wheel build experiment. The first attempt reached the cross-build preparation stage but failed in Chaquopy's SONAME alias loop before Biopython compilation; the workflow now applies an assertion-checked alias patch. No APK/AAB artifact or Android runtime result is claimed.
- No conclusion is yet possible about overall architecture feasibility, memory fit, APK/AAB size or real-device performance.
- R1 remains in progress. R2 must not start until the full experiment matrix and owner go/no-go review are complete.

## Evidence capture template

For every run record: date; commit; host OS; JDK/Gradle/AGP/Kotlin/SDK/NDK versions; dependency versions and licenses; device model/SoC/RAM/Android/API/ABI/page size; exact command; output/log link; artifact hash/size; cold-start method and repetitions; peak memory method; result (pass/fail/blocked); limitations and reproduction steps.
