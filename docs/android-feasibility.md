# Android feasibility — not yet tested

Last reviewed: 2026-11-07

No Android device/emulator feasibility spike has been completed in this repository. All entries below are **not tested**, not pass/fail.

| Spike | Required evidence | Status | Decision |
|---|---|---|---|
| Android + embedded Python | Gradle app starts; Chaquopy imports Biopython and executes sequence operation on arm64 | Not tested | Pending |
| Rust FFI | FASTA parser called from app via UniFFI/JNI on arm64 and x86_64 emulator | Not tested | Pending |
| C++ JNI | CMake/NDK kernel called from app; sanitizers/reference tests | Not tested | Pending |
| External engine | One real engine bundled and executed on arm64; licensing and Play policy checked | Not tested | Pending |
| RDKit / alternative | Package install, ABI, feature coverage, size and runtime feasibility | Not tested | Pending |
| 16 KB pages | Inspect every native library in APK/AAB and enforce CI alignment | Not tested | Pending |
| 4 GB device budget | APK/AAB size, cold start, peak RSS, thermal/battery and cancellation tests | Not tested | Pending |

## Constraints to verify

- Python package compatibility must be measured package-by-package on arm64; desktop wheels are not evidence of Android support.
- Rust targets: arm64-v8a primary and x86_64 emulator; select UniFFI or JNI after a minimal proof.
- C++ uses Android NDK/CMake and JNI.
- External executable engines must be bundled or run on a user-configured Remote Compute Node; do not download executable code at runtime.
- Data packs are distinct from engines and must have source, license, version, size, checksum and schema.
- All native libraries must meet the applicable 16 KB page-size requirement for the target distribution.
- Baseline device: 4 GB RAM, mid-range arm64. Jobs must be bounded, cancellable and resumable.

## Go/no-go gate

Do not proceed to a broad Android engine rollout until each technology has measured results, device logs, reproducible build instructions, size/memory measurements, licensing review and an explicit recommendation. User approval is required for the Phase 1 go/no-go decision.
