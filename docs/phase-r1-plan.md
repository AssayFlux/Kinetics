# R1 — Android and scientific-stack feasibility

**Roadmap item:** Track R / R1  
**Status:** IN PROGRESS — historical cross-build/static-package evidence exists; complete runtime and scientific feasibility evidence does not  
**Owner:** Engineering + Project owner  
**Started:** 2026-11-07  
**Depends on:** R0 foundation and approved direction baseline  
**Exit gate:** Evidence-backed feasibility matrix and explicit owner go/no-go before R2

## Objective

Establish whether the approved Android-native architecture can support the required scientific stack on Android 10+ arm64 devices, with honest limits for memory, startup, storage, offline operation, native ABI compatibility and scientific correctness. R1 is a feasibility phase, not a product-release claim.

## Owner instruction — build and test workflow

Effective 2026-11-08:
- GitHub Actions must not build APK/AAB artifacts and must not boot or test Android emulators.
- GitHub Actions remains for host-side Python, registry, lint, type and unit-test checks only.
- The debug APK is to be built locally when the owner is ready. Physical-device testing is deferred until the owner chooses to perform it.
- Historical GitHub build artifacts and their static inspection records remain historical evidence; they are not a reason to restore Android build/test jobs to GitHub Actions.
- Do not claim an APK has been freshly built locally, or that Android runtime/device tests passed, unless the actual local build/logs are supplied and inspected.

## Required feasibility work

1. **Android baseline:** document Gradle/AGP/Kotlin/SDK/NDK/JDK versions, Compose shell, min SDK 29, arm64-v8a ABI, local build reproducibility and APK/AAB size.
2. **Embedded Python:** test pinned Python, Biopython (SeqIO, Bio.PDB, PairwiseAligner), NumPy and SciPy availability/packaging. Resolve SciPy or document a clearly scoped alternative only after owner approval.
3. **Rust:** compile the planned Android arm64 library, invoke through the real app FFI boundary, and test correctness, errors, cancellation and resource limits.
4. **C++17/JNI:** build and invoke the JNI bridge; retain host-side correctness tests and inspect native ABI/alignment.
5. **Scientific sequence engine:** cross-build and test a real engine such as Parasail only after pinned source, license, ABI, algorithmic test vectors and maintenance costs are reviewed. Biopython's PairwiseAligner smoke test alone does not complete this criterion.
6. **Chemistry engine:** evaluate RDKit or a viable alternative, including transitive licenses, Android buildability, binary footprint, supported operations and reference test vectors.
7. **Offline structure viewer:** package Mol* or an alternative as local assets and test loading a known structure with networking disabled; record WebView/WebGL limitations and worker behavior.
8. **Android file and lifecycle constraints:** assess SAF import, background execution, cancellation, restart/resume, offline behavior, cold start and peak memory.
9. **16 KB support:** inspect all packaged ELF objects and APK alignment, then distinguish static alignment evidence from runtime behavior on a 16 KB Android kernel.
10. **Licensing:** complete file-level and transitive dependency license audits before any production redistribution decision.

## Existing evidence (historical; not a phase pass)

- CI run 1471 built an arm64 debug APK/AAB, cross-compiled Rust, linked the C++17 JNI bridge, and passed static ELF 16 KB alignment and APK ZIP alignment checks. Its artifact hashes and measurements are retained in `docs/android-feasibility.md`.
- CI run 1481 repeated the arm64 APK/AAB build and static alignment checks.
- These records establish historical cross-build, packaging and static alignment only. They do not establish a fresh local build, Android runtime execution, physical-device compatibility, scientific-engine feasibility, cold-start or peak memory.
- Biopython 1.88 custom arm64 wheel was built in the historical CI experiment. Gradle now pins NDK 28.2.13676358 to match the local build script. SciPy was not installed and remains unresolved.
- Rust/C++ JNI symbols were present in the historical APK; successful invocation on an Android device is not established.
- Parasail, RDKit and Mol* remain evaluation candidates, not approved production dependencies.

## Evidence protocol

Record exact source revision, toolchain and dependency versions, license status, command, output/log, artifact hash/size, device model/SoC/RAM/Android/API/ABI/page size, repeated timing/memory measurements, pass/fail/blocked result, limitations and reproduction instructions. Emulator evidence never substitutes for physical-device evidence. Static ELF inspection never substitutes for runtime testing.

## Device scope

D-006 sets the target at Android 10+ (API 29), 64-bit ARM (arm64-v8a), with low-end, mid-range and flagship test tiers. This is a target, not a verified compatibility claim. Owner identified a Motorola Moto G54 5G as the first physical test handset on 2026-11-08. Device testing remains deferred under the build-first / test-later instruction; keep those rows blocked until the local APK is built and the owner supplies actual device logs. Capture exact Android/API, SoC, RAM, ABI and page size from the connected phone.

## Deliverables

- `docs/android-feasibility.md`: experiment matrix, historical evidence, current blockers, local build procedure and eventual owner-device runbook.
- Minimal isolated prototypes for each R1 feasibility question; the app shell now exposes a manual embedded-Python and Rust/C++ JNI smoke-probe action. No prototype is silently promoted to production.
- `docs/third-party.md`: exact dependency versions, source/license review and approval status.
- A consolidated go/no-go matrix with feasible, infeasible, conditional or untested outcomes.

## Exit criteria

R1 is complete only when:
1. Android arm64 local build is reproduced and its APK/AAB contents, size and hashes are recorded.
2. Embedded Python/Biopython/NumPy and the SciPy decision are evidenced.
3. Rust FFI and C++ JNI calls are executed and verified on Android.
4. A real scientific sequence engine is built and tested against reference vectors.
5. RDKit or an alternative and the offline viewer have measured outcomes.
6. SAF, background work, cancellation/resume, cold-start, memory and offline constraints have evidence or explicit owner-approved scope.
7. 16 KB static and runtime evidence are distinguished and recorded.
8. Dependency redistribution risks and licenses are audited.
9. The go/no-go matrix and limitations are reviewed and explicitly approved by the owner.

**R2 remains blocked until R1 evidence is complete and the owner approves the R1 go/no-go.**
