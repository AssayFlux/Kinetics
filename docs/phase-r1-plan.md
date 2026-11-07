# R1 — Android feasibility phase plan

**Roadmap item:** Track R / R1  
**Status:** In progress — feasibility investigation and test harness preparation  
**Owner:** Engineering + Project owner  
**Started:** 2026-11-07  
**Depends on:** R0 foundation and approved direction baseline  
**Exit gate:** Evidence-backed go/no-go matrix; explicit owner decision required before R2

## Objective

Determine by reproducible experiments whether the planned Android architecture can run on a defined arm64 device and emulator within memory, startup, package-size, offline and Android platform constraints. This phase is a feasibility study, not an application feature release.

## Required experiments

1. **Android baseline:** establish Gradle/AGP/Kotlin/SDK/NDK/JDK versions; build a minimal Compose shell; capture APK/AAB size, build reproducibility and Android target/min SDK choices as proposals, not owner-approved support commitments.
2. **Embedded Python:** integrate a pinned Python 3.10+ Android-compatible runtime for arm64; import and execute Python plus Biopython (SeqIO, Bio.PDB and PairwiseAligner) and NumPy/SciPy candidates; record ABI, wheel/native-library compatibility, startup, peak RSS and package contribution. No unsupported wheel is assumed to work.
3. **Rust:** compile a minimal Rust library for Android arm64, call it from the app through the intended JNI/FFI boundary, and test correctness and cancellation/timeout behaviour.
4. **C++17/JNI:** build and call a minimal numeric kernel through JNI; run correctness tests and sanitizer-capable host tests. Record NDK and ABI details.
5. **One real scientific engine:** select a small, license-compatible candidate only after inspecting upstream license, Android build support, binary/runtime constraints and scientific test vectors. Do not bundle GPL/AGPL or other restrictive terms without owner approval. A stub is not an engine feasibility pass.
6. **RDKit or alternative:** evaluate Android arm64 build feasibility, native dependency graph, binary size, license and smoke-test correctness. No library is selected for product inclusion by this experiment alone.
7. **Offline WebView:** load a locally bundled minimal Mol*/3Dmol.js viewer and a known small structure without network access; measure WebView/WebGL support on emulator and physical device.
8. **Android constraints:** verify 16 KB page-size compatibility for every native shared object and packaged executable where applicable; inspect APK/AAB contents and size; test cold start, peak memory/RSS, background execution, cancellation, SAF file import and offline behaviour.

## Evidence protocol

For each experiment record exact source revision, dependency and toolchain versions; device model, SoC, RAM, Android/API version, ABI and page size; emulator image and host runner details; exact commands, build configuration and raw logs/artifact paths; pass/fail/blocked outcome, measured values, limitations and reproduction instructions.

No device result may be inferred from an emulator. No build-time check is described as physical-device validation. No performance or compatibility claim is made without measurements.

## Device and scope constraints

- D-006 is approved: target Android 10+ (API 29), 64-bit ARM (arm64-v8a), with low-end, mid-range and flagship test tiers. This is a target matrix, not verified compatibility across all devices. Initial experiments may use a documented emulator and owner-provided arm64 device; the supported-device matrix cannot be approved until representative target devices are tested.
- No new programming language is introduced. Use only the approved Kotlin, Python, Rust, C/C++ and JS/TS plan.
- No executable is downloaded at runtime. Pin all sources and inspect licenses before bundling.
- No patient-data or clinical functionality. Research Mode only; P0 remains blocked.
- No data packs or production engine are adopted without source, license and owner review.

## Deliverables

- docs/android-feasibility.md: experiment matrix, environment, raw evidence links, measured package/startup/memory results, limitations and go/no-go recommendation.
- Minimal isolated prototypes/harnesses only where needed to test a specific R1 question; keep them out of production architecture until accepted.
- CI jobs for reproducible host-side checks and Android build/artifact inspection where feasible.
- License/dependency notes in docs/third-party.md for every candidate actually evaluated.

## Exit criteria

R1 is complete only when:
1. A real arm64 device and emulator have been tested or any unavailable test is explicitly marked blocked with reason and owner action.
2. Python/Biopython, Rust app call, C++ JNI, one actual scientific engine, RDKit/alternative and offline viewer have measured outcomes.
3. 16 KB alignment, APK/AAB size, cold start and memory have evidence or explicit blockers.
4. A consolidated go/no-go matrix states feasible, infeasible, conditional or untested for each subsystem.
5. Risks, licenses, binary size, performance and maintenance implications are documented.
6. The owner reviews and explicitly approves the R1 go/no-go decision.

**Stop at the R1 exit gate. Do not start R2 until the owner approves the R1 recommendation. R3 depends on R2 and is not to be started in parallel.**
