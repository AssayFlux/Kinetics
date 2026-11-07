# Android feasibility — R1 in progress

**Status:** IN PROGRESS — research findings recorded; implementation experiments and device tests not yet run  
**Last updated:** 2026-11-07  
**Phase plan:** docs/phase-r1-plan.md  
**Owner gate:** R1 go/no-go review required before R2

## Current evidence boundary

The repository still has no Android application project, APK/AAB, emulator run or physical-device run. No embedded Python/Biopython, Rust app call, C++ JNI, scientific engine, RDKit, offline viewer, 16 KB runtime, startup, memory or package-size result is claimed. The findings below are desk research and inform experiment design only.

## Initial research findings

### Android 16 KB page sizes

- Android 15 and later support 16 KB page-size devices. Native shared libraries must have compatible ELF segment alignment; prebuilt native libraries need separate verification/rebuild.
- Android's current guidance says NDK r28 and later produce 16 KB-aligned shared libraries by default. Older NDK versions require explicit linker flags and additional care.
- Android documents emulator-based 16 KB testing and checking the runtime page size with adb shell getconf PAGE_SIZE; APK alignment can be checked with zipalign -c -P 16 -v 4.
- Google Play's published requirement states that updates targeting Android 15 / API 35 or higher must support 16 KB page sizes on 64-bit devices, with a deadline of 2027-02-01.
- These requirements mean every transitive native dependency (including Python scientific wheels, Rust/C++ libraries and any engine) must be inspected, not only Kinetics' own JNI library.

Sources:
- Android Developers, Support 16 KB page sizes: https://developer.android.com/guide/practices/page-sizes
- Android Developers, 16 KB emulator and validation instructions: https://developer.android.com/guide/practices/page-sizes

### Embedded Python candidate: Chaquopy

- Chaquopy currently documents Gradle integration and Kotlin/Java ↔ Python APIs, and advertises a package ecosystem including SciPy.
- Its version table currently lists Chaquopy 17.2 as supporting Python 3.10–3.15, AGP 7.3–9.5 and minimum Android API 24.
- Chaquopy states that versions 12.0.1 and later are free/open source with restrictions removed. The upstream license file is MIT.
- Package availability is not universal: Chaquopy's FAQ directs users to verify Android wheels and build unsupported packages themselves. Therefore Biopython, NumPy and SciPy versions must be tested as actual Android arm64 packages, not assumed available because they install on desktop.
- Candidate only; no Gradle plugin or runtime has been added to the app, and no dependency has been selected for production.

Sources:
- Chaquopy documentation: https://chaquo.com/chaquopy/documentation/
- Version compatibility: https://chaquo.com/chaquopy/doc/current/versions.html
- Licensing: https://chaquo.com/chaquopy/license/
- Package availability FAQ: https://chaquo.com/chaquopy/doc/current/faq.html
- Upstream license: https://github.com/chaquo/chaquopy/blob/master/LICENSE.txt

## R1 experiment matrix

| Area | Current status | Required next evidence |
|---|---|---|
| Minimal Compose app / Gradle build | Not tested | Build log, toolchain versions, APK/AAB |
| Embedded Python runtime | Candidate identified; not tested | arm64 build/import/startup/RSS/package-size logs |
| Biopython | Not tested | Android wheel/build availability and import/test vectors |
| NumPy / SciPy | Candidate ecosystem exists; exact versions not tested | Native wheel ABI, import and numerical smoke tests |
| Rust app FFI | Not tested | Android arm64 library and Kotlin call test |
| C++17 JNI | Not tested | NDK build, JNI invocation and numeric correctness test |
| One real scientific engine | Not selected | License review, Android build, real test vector |
| RDKit / alternative | Not tested | arm64 build, dependency/license/size and smoke test |
| Offline Mol* / 3Dmol.js | Not tested | Bundled viewer renders a known structure with network disabled |
| 16 KB ELF / APK alignment | Not tested | ELF inspection, zipalign and 16 KB emulator/device run |
| Cold start / peak memory / package size | Not tested | Repeatable measurements with environment metadata |
| SAF / background / cancellation | Not tested | Import and job lifecycle tests on Android |

## Device matrix

D-006 remains open. No physical target device has been nominated or provided. Emulator experiments can proceed, but cannot substitute for a real arm64 device. The supported-device matrix remains undecided.

| Target | Model / SoC / RAM | Android | Page size | Status |
|---|---|---|---|---|
| Emulator | To be recorded | Android 15+ 16 KB image | 16 KB | Not run |
| Physical arm64 | Owner to nominate/provide | To be recorded | To be measured | Blocked on target device |

## Preliminary assessment (not a go/no-go)

- 16 KB support is a mandatory design constraint and appears technically testable with documented Android tooling.
- Chaquopy is a credible embedded-Python candidate, but scientific package and native ABI compatibility is unresolved.
- No conclusion is yet possible about overall architecture feasibility, memory fit, APK/AAB size or real-device performance.
- R1 remains in progress. R2 must not start until the full experiment matrix and owner go/no-go review are complete.

## Evidence capture template

For every run record: date; commit; host OS; JDK/Gradle/AGP/Kotlin/SDK/NDK versions; dependency versions and licenses; device model/SoC/RAM/Android/API/ABI/page size; exact command; output/log link; artifact hash/size; cold-start method and repetitions; peak memory method; result (pass/fail/blocked); limitations and reproduction steps.
