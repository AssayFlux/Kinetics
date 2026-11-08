#!/usr/bin/env bash
# Local-only Android arm64 debug build. This script is never invoked by GitHub Actions.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ANDROID_DIR="$ROOT_DIR/android"
CHAQUOPY_VERSION="17.2.0"
PYTHON_TARGET="3.11.17-0"
NUMPY_WHEEL="numpy-1.26.2-0-cp311-cp311-android_21_arm64_v8a.whl"
NDK_VERSION="28.2.13676358"
BUILD_TOOLS_VERSION="36.0.0"
CHAQUOPY_DIR="${CHAQUOPY_DIR:-$HOME/.cache/kinetics/chaquopy-$CHAQUOPY_VERSION}"

fail() { echo "ERROR: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || fail "Missing command: $1"; }

need java
need python
need git
need curl
need cargo
need rustup
need gradle
need patchelf
need patch

[[ -n "${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}" ]] || fail "Set ANDROID_HOME or ANDROID_SDK_ROOT."
SDK_ROOT="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}"
[[ -d "$SDK_ROOT/ndk/$NDK_VERSION" ]] || fail "Install Android NDK $NDK_VERSION under $SDK_ROOT/ndk."
[[ -x "$SDK_ROOT/build-tools/$BUILD_TOOLS_VERSION/zipalign" ]] || fail "Install Android build-tools $BUILD_TOOLS_VERSION."
[[ -d "$SDK_ROOT/platforms/android-36" ]] || fail "Install Android SDK platform android-36."
[[ -d "$SDK_ROOT/cmake/3.22.1" ]] || fail "Install Android CMake 3.22.1."
python -c 'import sys; assert sys.version_info[:2] == (3, 11), sys.version' || fail "Use Python 3.11."
java -version 2>&1 | grep -q '17\.' || fail "Use JDK 17."
gradle --version | grep -q 'Gradle 8.13' || fail "Use Gradle 8.13."

NDK_BIN="$SDK_ROOT/ndk/$NDK_VERSION/toolchains/llvm/prebuilt/linux-x86_64/bin"
[[ -d "$NDK_BIN" ]] || fail "This script currently supports Linux/WSL2 x86_64 hosts only."
export CARGO_TARGET_AARCH64_LINUX_ANDROID_LINKER="$NDK_BIN/aarch64-linux-android29-clang"

echo "[1/6] Build Rust arm64 static library"
rustup target add aarch64-linux-android
cargo build --manifest-path "$ANDROID_DIR/native-rust/Cargo.toml" --target aarch64-linux-android --release

echo "[2/6] Prepare pinned Chaquopy wheel builder"
if [[ ! -d "$CHAQUOPY_DIR/.git" ]]; then
  mkdir -p "$(dirname "$CHAQUOPY_DIR")"
  git clone --depth 1 --branch "$CHAQUOPY_VERSION" https://github.com/chaquo/chaquopy.git "$CHAQUOPY_DIR"
fi
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

echo "[3/6] Cross-build Biopython 1.88 Android arm64 wheel"
cd "$CHAQUOPY_DIR/server/pypi"
python build-wheel.py --python 3.11 --abi arm64-v8a "$ANDROID_DIR/biopython-wheel"
mkdir -p "$ANDROID_DIR/app/libs/python-wheels"
cp dist/biopython/*.whl "$ANDROID_DIR/app/libs/python-wheels/"

echo "[4/6] Build local debug APK and AAB"
cd "$ANDROID_DIR"
gradle --no-daemon :app:assembleDebug :app:bundleDebug

echo "[5/6] Check APK ZIP alignment and native ELF alignment"
APK="$ANDROID_DIR/app/build/outputs/apk/debug/app-debug.apk"
AAB="$ANDROID_DIR/app/build/outputs/bundle/debug/app-debug.aab"
[[ -f "$APK" && -f "$AAB" ]] || fail "Expected APK/AAB output is missing."
"$SDK_ROOT/build-tools/$BUILD_TOOLS_VERSION/zipalign" -c -P 16 -v 4 "$APK"
python "$ROOT_DIR/scripts/check_android_elf_alignment.py" "$APK" "$AAB"

echo "[6/6] Record local artifact hashes and sizes"
ls -lh "$APK" "$AAB"
sha256sum "$APK" "$AAB"
echo "LOCAL BUILD COMPLETE. No emulator or physical-device test was run."
