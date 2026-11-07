# Android feasibility — R1 in progress

**Status:** IN PROGRESS — first Android CI build attempted; blocked by missing host Python executable; workflow correction committed and awaiting rerun  
**Last updated:** 2026-11-07  
**Phase plan:** docs/phase-r1-plan.md  
**Owner gate:** R1 go/no-go review required before R2

## Current evidence boundary

An isolated Android arm64 feasibility app and Chaquopy probe now exist under `android/`. The Gradle configuration targets arm64-v8a and includes Python 3.11 with Biopython, NumPy and SciPy as an R1 experiment. These are prototype dependencies only, not a production architecture or dependency approval.

The first GitHub Actions Android build (run 1381, commit `fe63ecf56538d4e1d494c44a51dfb9b5654b199a`) reached Chaquopy's Python-requirements task and failed because the runner did not have a discoverable Python 3.11 executable. The Python/registry/tests CI job passed. The workflow now explicitly provisions Python 3.11 before Gradle; commit `6705fe8dc27b90e3dea8482b21d89c7fe321afbd`. The rerun result must be recorded before drawing any build conclusion.

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

## R1 experiment matrix

| Area | Current status | Required next evidence |
|---|---|---|
| Minimal Compose app / Gradle build | Android project and CI job present; first build blocked finding host Python 3.11; workflow fix committed | Successful build log, APK/AAB, toolchain versions |
| Embedded Python runtime | Chaquopy probe configured; not executed | arm64 build/import/startup/RSS/package-size logs |
| Biopython | Declared in R1 probe; not tested on Android | Android package resolution and import/test vectors |
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

D-006 remains open. No physical target device has been nominated or provided. Emulator experiments can proceed, but cannot substitute for a real arm64 device. The supported-device matrix remains undecided.

| Target | Model / SoC / RAM | Android | Page size | Status |
|---|---|---|---|---|
| Emulator | To be recorded | Android 15+ 16 KB image | 16 KB | Not run |
| Physical arm64 | Owner to nominate/provide | To be recorded | To be measured | Blocked on target device |

## Preliminary assessment (not a go/no-go)

- The Android project is now build-configured, but the first build did not reach compilation because the CI host Python prerequisite was missing.
- Explicitly provisioning Python 3.11 is the first corrective action; the subsequent CI run will determine whether the prototype dependency resolution/build advances.
- No conclusion is yet possible about overall architecture feasibility, memory fit, APK/AAB size or real-device performance.
- R1 remains in progress. R2 must not start until the full experiment matrix and owner go/no-go review are complete.

## Evidence capture template

For every run record: date; commit; host OS; JDK/Gradle/AGP/Kotlin/SDK/NDK versions; dependency versions and licenses; device model/SoC/RAM/Android/API/ABI/page size; exact command; output/log link; artifact hash/size; cold-start method and repetitions; peak memory method; result (pass/fail/blocked); limitations and reproduction steps.
