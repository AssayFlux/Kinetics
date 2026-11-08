#!/usr/bin/env bash
# Reproducible Android arm64 debug APK/AAB build for Linux x86_64 hosts (local or GitHub Actions).
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
ANDROID_DIR="$ROOT_DIR/android"
CHAQUOPY_VERSION="17.2.0"
CHAQUOPY_COMMIT="1f63c93d8beaf7062fbe51888ab9235475df3bb8"
BIOPYTHON_VERSION="1.88"
BIOPYTHON_COMMIT="d7e4b8b19399668b09442a5b35765d9186b5f665"
BIOPYTHON_DIR="${BIOPYTHON_DIR:-$HOME/.cache/kinetics/biopython-$BIOPYTHON_VERSION}"
GRADLE_VERSION="8.13"
GRADLE_SHA256="20f1b1176237254a6fc204d8434196fa11a4cfb387567519c61556e8710aed78"
GRADLE_CACHE_DIR="${GRADLE_CACHE_DIR:-$HOME/.cache/kinetics/gradle-$GRADLE_VERSION}"
PYTHON_TARGET="3.11.17-0"
NUMPY_WHEEL="numpy-1.26.2-0-cp311-cp311-android_21_arm64_v8a.whl"
NDK_VERSION="28.2.13676358"
BUILD_TOOLS_VERSION="36.0.0"
CHAQUOPY_DIR="${CHAQUOPY_DIR:-$HOME/.cache/kinetics/chaquopy-$CHAQUOPY_VERSION}"

fail() { echo "ERROR: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || fail "Missing command: $1"; }

# The pinned Chaquopy wheel-builder and NDK host tools are Linux x86_64 only.
# Detect unsupported hosts before downloading toolchains or modifying caches.
HOST_OS="$(uname -s)"
HOST_ARCH="$(uname -m)"
if [[ "${PREFIX:-}" == *com.termux* || -n "${TERMUX_VERSION:-}" ]]; then
  fail "Termux on Android is not a supported APK-build host for this pinned toolchain. Build on Linux x86_64 or x86_64 WSL2; use Termux only for post-build device installation/log collection."
fi
[[ "$HOST_OS" == "Linux" ]] || fail "Unsupported build host: $HOST_OS. Use Linux x86_64 or x86_64 WSL2."
[[ "$HOST_ARCH" == "x86_64" ]] || fail "Unsupported build-host architecture: $HOST_ARCH. The pinned Chaquopy/NDK toolchain requires x86_64."

need java
need python
need git
need tar
need curl
need cargo
need rustup
need patchelf
need patch
need sha256sum

[[ -n "${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}" ]] || fail "Set ANDROID_HOME or ANDROID_SDK_ROOT."
SDK_ROOT="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}"
[[ -d "$SDK_ROOT/ndk/$NDK_VERSION" ]] || fail "Install Android NDK $NDK_VERSION under $SDK_ROOT/ndk."
[[ -x "$SDK_ROOT/build-tools/$BUILD_TOOLS_VERSION/zipalign" ]] || fail "Install Android build-tools $BUILD_TOOLS_VERSION."
[[ -d "$SDK_ROOT/platforms/android-36" ]] || fail "Install Android SDK platform android-36."
[[ -d "$SDK_ROOT/cmake/3.22.1" ]] || fail "Install Android CMake 3.22.1."
python -c 'import sys; assert sys.version_info[:3] == (3, 11, 17), sys.version' || fail "Use Python 3.11.17 exactly."
java -version 2>&1 | grep -q '17\.' || fail "Use JDK 17."

# Fetch a checksum-pinned Gradle distribution rather than trusting a host-installed gradle.
GRADLE_BIN="$GRADLE_CACHE_DIR/gradle-$GRADLE_VERSION/bin/gradle"
GRADLE_MARKER="$GRADLE_CACHE_DIR/.gradle-$GRADLE_VERSION.sha256"
GRADLE_MARKER_VALID="false"
if [[ -f "$GRADLE_MARKER" ]] && [[ "$(cat "$GRADLE_MARKER")" == "$GRADLE_SHA256" ]]; then
  GRADLE_MARKER_VALID="true"
fi
if [[ ! -x "$GRADLE_BIN" || "$GRADLE_MARKER_VALID" != "true" ]]; then
  mkdir -p "$GRADLE_CACHE_DIR"
  archive="$GRADLE_CACHE_DIR/gradle-$GRADLE_VERSION-bin.zip"
  # Prefer Gradle's direct distribution CDN; the services.gradle.org redirect
  # can traverse GitHub release assets and intermittently return gateway errors.
  if ! curl --fail --location --retry 3 --retry-all-errors \
    "https://downloads.gradle.org/distributions/gradle-$GRADLE_VERSION-bin.zip" \
    --output "$archive"; then
    rm -f "$archive"
    curl --fail --location --retry 3 --retry-all-errors \
      "https://services.gradle.org/distributions/gradle-$GRADLE_VERSION-bin.zip" \
      --output "$archive"
  fi
  actual="$(sha256sum "$archive" | awk '{print $1}')"
  [[ "$actual" == "$GRADLE_SHA256" ]] || fail "Gradle distribution checksum mismatch: $actual"
  rm -rf "$GRADLE_CACHE_DIR/gradle-$GRADLE_VERSION"
  python - "$archive" "$GRADLE_CACHE_DIR" <<'PY'
import sys, zipfile
with zipfile.ZipFile(sys.argv[1]) as archive:
    archive.extractall(sys.argv[2])
PY
  # Python's zipfile extraction does not reliably restore Unix executable bits.
  chmod +x "$GRADLE_BIN"
  printf '%s\n' "$GRADLE_SHA256" > "$GRADLE_MARKER"
fi
"$GRADLE_BIN" --version | grep -q "Gradle $GRADLE_VERSION" || fail "Pinned Gradle $GRADLE_VERSION unavailable."

NDK_BIN="$SDK_ROOT/ndk/$NDK_VERSION/toolchains/llvm/prebuilt/linux-x86_64/bin"
[[ -d "$NDK_BIN" ]] || fail "This script currently supports Linux/WSL2 x86_64 hosts only."
export CARGO_TARGET_AARCH64_LINUX_ANDROID_LINKER="$NDK_BIN/aarch64-linux-android29-clang"

echo "[1/6] Build Rust arm64 static library"
rustup target add aarch64-linux-android
cargo build --locked --manifest-path "$ANDROID_DIR/native-rust/Cargo.toml" --target aarch64-linux-android --release

echo "[2/6] Prepare pinned Chaquopy wheel builder"
if [[ ! -d "$CHAQUOPY_DIR/.git" ]]; then
  rm -rf "$CHAQUOPY_DIR"
  mkdir -p "$(dirname "$CHAQUOPY_DIR")"
  git clone --depth 1 --branch "$CHAQUOPY_VERSION" https://github.com/chaquo/chaquopy.git "$CHAQUOPY_DIR"
fi
[[ "$(git -C "$CHAQUOPY_DIR" rev-parse HEAD)" == "$CHAQUOPY_COMMIT" ]] || fail "Chaquopy source revision differs from the pinned commit."
python - "$CHAQUOPY_DIR" <<'PY'
import sys
from pathlib import Path
root = Path(sys.argv[1])
builder = root / "server/pypi/build-wheel.py"
source = builder.read_text()
old = 'run(f"ln -s {filename} {reqs_lib_dir}/{link_filename}")'
new = 'run(f"ln -sf {filename} {reqs_lib_dir}/{link_filename}")'
if old not in source and new not in source:
    raise SystemExit("Chaquopy SONAME patch anchor changed; inspect upstream before proceeding")
if old in source:
    builder.write_text(source.replace(old, new, 1))
wrapper = builder.with_name("compiler-wrapper.py")
wrapper_source = wrapper.read_text()
safe_old = 'valid_dirs = [abspath(f"{dirname(sys.argv[0])}/../..")]'
safe_new = 'valid_dirs = [abspath(f"{dirname(sys.argv[0])}/../.."), abspath(os.environ["KINETICS_LOCAL_BUILD_ROOT"])]'
if safe_old in wrapper_source:
    wrapper.write_text(wrapper_source.replace(safe_old, safe_new, 1))
elif safe_new not in wrapper_source:
    raise SystemExit("Chaquopy compiler-wrapper patch anchor changed; inspect upstream before proceeding")
PY
export KINETICS_LOCAL_BUILD_ROOT="$ROOT_DIR"
cd "$CHAQUOPY_DIR"
bash target/download-target.sh "maven/com/chaquo/python/target/$PYTHON_TARGET"
python -m pip install -r server/pypi/requirements.txt
mkdir -p "server/pypi/dist/numpy"
curl --fail --location --retry 3 \
  "https://chaquo.com/pypi-13.1/numpy/$NUMPY_WHEEL" \
  --output "server/pypi/dist/numpy/$NUMPY_WHEEL"

echo "[3/6] Cross-build pinned Biopython $BIOPYTHON_VERSION Android arm64 wheel"
if [[ ! -d "$BIOPYTHON_DIR/.git" ]]; then
  rm -rf "$BIOPYTHON_DIR"
  mkdir -p "$(dirname "$BIOPYTHON_DIR")"
  git clone --filter=blob:none --no-checkout https://github.com/biopython/biopython.git "$BIOPYTHON_DIR"
fi
git -C "$BIOPYTHON_DIR" fetch --depth 1 origin "$BIOPYTHON_COMMIT"
git -C "$BIOPYTHON_DIR" checkout --detach "$BIOPYTHON_COMMIT"
[[ "$(git -C "$BIOPYTHON_DIR" rev-parse HEAD)" == "$BIOPYTHON_COMMIT" ]] || fail "Biopython source revision differs from the pinned commit."
BIOPYTHON_SOURCE_DIR="$BIOPYTHON_DIR/source"
rm -rf "$BIOPYTHON_SOURCE_DIR"
mkdir -p "$BIOPYTHON_SOURCE_DIR"
git -C "$BIOPYTHON_DIR" archive "$BIOPYTHON_COMMIT" | tar -x -C "$BIOPYTHON_SOURCE_DIR"
BIOPYTHON_RECIPE="$CHAQUOPY_DIR/server/pypi/kinetics-biopython-recipe"
rm -rf "$BIOPYTHON_RECIPE"
mkdir -p "$BIOPYTHON_RECIPE"
cp "$ANDROID_DIR/biopython-wheel/meta.yaml" "$BIOPYTHON_RECIPE/meta.yaml"
python - "$BIOPYTHON_RECIPE/meta.yaml" "$BIOPYTHON_SOURCE_DIR" <<'PY'
import json, sys
from pathlib import Path
recipe = Path(sys.argv[1])
source = json.dumps(str(Path(sys.argv[2]).resolve()))
recipe.write_text(recipe.read_text() + f"\nsource:\n  path: {source}\n")
PY
cd "$CHAQUOPY_DIR/server/pypi"
python build-wheel.py --python 3.11 --abi arm64-v8a "$BIOPYTHON_RECIPE"
mkdir -p "$ANDROID_DIR/app/libs/python-wheels"
cp dist/biopython/*.whl "$ANDROID_DIR/app/libs/python-wheels/"

echo "[4/6] Build local debug APK and AAB"
cd "$ANDROID_DIR"
"$GRADLE_BIN" --no-daemon --stacktrace :app:assembleDebug :app:bundleDebug

echo "[5/6] Check APK ZIP alignment and native ELF alignment"
APK="$ANDROID_DIR/app/build/outputs/apk/debug/app-debug.apk"
AAB="$ANDROID_DIR/app/build/outputs/bundle/debug/app-debug.aab"
[[ -f "$APK" && -f "$AAB" ]] || fail "Expected APK/AAB output is missing."
"$SDK_ROOT/build-tools/$BUILD_TOOLS_VERSION/zipalign" -c -P 16 -v 4 "$APK"
python "$ROOT_DIR/scripts/check_android_elf_alignment.py" "$APK" "$AAB"

echo "[6/6] Record local artifact hashes and sizes"
ls -lh "$APK" "$AAB"
sha256sum "$APK" "$AAB"
echo "ANDROID ARM64 BUILD COMPLETE. No emulator or physical-device test was run."
