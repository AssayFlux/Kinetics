# Local Android arm64 debug build

This is the reproducible manual build route for a Linux x86_64 machine or Linux x86_64 WSL2 environment. The owner has separately authorized GitHub Actions to run the same pinned arm64 APK/AAB build and automated package/JVM checks. CI artifacts are unsigned debug outputs; CI does not install the app on the owner's phone or establish physical-device runtime compatibility.\n\n> **Termux warning:** Termux running directly on an Android phone is not a supported build host for the current pinned toolchain. The build requires Linux x86_64 host binaries (including the NDK `linux-x86_64` toolchain and pinned Chaquopy wheel builder). Android Termux normally reports an Android/aarch64 host, and `proot-distro` on the same phone does not turn it into x86_64 Linux. The build script now detects Termux and unsupported OS/architectures immediately, before downloads or cache changes. Do not try to work around this by substituting random Gradle, NDK, Python wheels or native binaries.

## Prerequisites

- Linux x86_64 or WSL2 x86_64 (the current pinned Chaquopy wheel-build toolchain expects this host).
- JDK 17.
- Gradle 8.13.
- Python 3.11 and pip.
- Git, curl, patch, patchelf, Rust stable/rustup and Cargo.
- Android SDK platform 36, build-tools 36.0.0, NDK 28.2.13676358 and CMake 3.22.1.
- Set `ANDROID_HOME` (or `ANDROID_SDK_ROOT`) to the Android SDK root.
- Enough disk space for the Android toolchain, Chaquopy source/target and native build outputs.

Install the Android SDK components with Android Studio SDK Manager or `sdkmanager`. Accept the Android SDK licences. The build script downloads and verifies its own Gradle 8.13 distribution; it requires **Python 3.11.17 exactly**. Confirm `java -version`, `python --version`, `rustc --version` and `cargo --version` before starting.\n\nIf your only computer is an Android phone, use the authorized GitHub Actions build artifact rather than trying to run this x86_64-host script directly in Termux. Termux can download/transfer the APK, install it through Android's package installer (subject to Android's install-source permission), and collect logs; it is not the build host for this pinned script.

## Build

From the repository root:

```bash
chmod +x scripts/build_android_local.sh
scripts/build_android_local.sh
```

The script:
1. Cross-compiles the Rust arm64 static library.
2. Checks out the pinned Chaquopy 17.2.0 wheel builder and applies two assertion-checked compatibility patches used in the historical experiment.
3. Downloads the pinned Python 3.11 target and NumPy Android wheel.
4. Builds the Biopython 1.88 arm64 wheel.
5. Runs Gradle locally to build the debug APK and debug AAB.
6. Checks APK ZIP alignment and all packaged native ELF segment alignments.
7. Prints local APK/AAB sizes and SHA-256 hashes.

The script deliberately stops if an expected toolchain version, patch anchor or artifact is missing. Do not bypass those checks by installing an arbitrary wheel or silently changing versions.

## Outputs

- APK: `android/app/build/outputs/apk/debug/app-debug.apk`
- AAB: `android/app/build/outputs/bundle/debug/app-debug.aab`

These are local build outputs and should not be committed. Record the commit, complete build log, toolchain versions, artifact sizes and SHA-256 hashes in `docs/android-feasibility.md` after the owner performs the build.

## Important limits

- A successful local build and static alignment check do not prove that the application launches or that JNI/Python imports execute.
- No emulator or physical-device test is performed by this script. The Actions workflow also does not currently run an Android emulator: the APK is arm64-only, and JVM unit tests plus static package checks are not substitutes for Android runtime tests.
- Owner physical-device testing remains deferred. Do not mark runtime or device verification as passed without the actual device logs.
- SciPy is not included in the current prototype and remains an R1 architecture question.
- The Biopython and NumPy versions are feasibility pins, not approved production dependencies. Their license and ABI review remains required.
- If the local Chaquopy wheel build fails, retain the complete error output and stop; do not substitute an unverified dependency.
