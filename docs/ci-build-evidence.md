# CI build evidence — 2026-11-08

## Latest successful integrated run

- Repository: [AssayFlux/Kinetics](https://github.com/AssayFlux/Kinetics)
- Workflow run: [#1650](https://github.com/AssayFlux/Kinetics/actions/runs/42450892141)
- Source commit: `b5a591aa2b0545188409eacc0eb76043b4143fb8`
- Result: both jobs succeeded (Python foundation/tests and Android arm64 build/JVM tests).
- Build host: GitHub Actions Linux x86_64; JDK 17; Python 3.11.17; Android SDK 36; NDK 28.2.13676358; CMake 3.22.1; Rust stable with `aarch64-linux-android`.
- Artifact archive: `kinetics-android-arm64-debug-b5a591aa2b0545188409eacc0eb76043b4143fb8` (76,660,231 bytes; archive SHA-256 `9c32298574d2d7081274daaee5ae63828103cf47adbfbd19b0bc7d0db476867d`).

## Individual outputs

| Output | Size (bytes) | SHA-256 |
|---|---:|---|
| `app-debug.apk` | 66,786,657 | `10896f91f622e979a1155c19263f825ccf5ee15e386d39ea1a56f28dd34c6056` |
| `app-debug.aab` | 38,153,856 | `21aa978efcb65ad1e6040a398d1faf7fe1bc6c06d895fe12603860130d4a6ffa` |

The APK/AAB were built, inspected and uploaded by the workflow. The AAB's native ELF load segments were checked for 16 KB alignment; APK ZIP alignment was checked. Android JVM unit tests passed.

## What this evidence does not establish

- No emulator or physical-device test was run.
- No app launch, embedded Python runtime import on Android, JNI invocation on device, SAF workflow, WorkManager process-death recovery, Keystore behavior, cold-start or peak-memory measurement is claimed.
- This is an unsigned debug build, not a signed release or Play-ready artifact.
- Build success does not validate scientific correctness, production dependency licensing, or device support.

Reproduce from a clean checkout using `scripts/build_android_local.sh` on the pinned Linux x86_64 host setup documented in `docs/local-android-build.md`, then run the Android JVM task and `python scripts/check_android_artifacts.py`.
