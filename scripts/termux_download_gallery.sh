#!/data/data/com.termux/files/usr/bin/bash
# Acquire, validate and publish one real, licensed scientific image for each of 100 domains.
set -Eeuo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "ERROR: Run this script from inside your Kinetics Git repository."
  exit 1
}
cd "$ROOT"

REMOTE="$(git remote get-url origin)"
if [[ "$REMOTE" != *"AssayFlux/Kinetics"* ]]; then
  echo "ERROR: origin is not AssayFlux/Kinetics: $REMOTE"
  echo "Check your Git remote before publishing."
  exit 1
fi

BRANCH="$(git branch --show-current)"
if [[ "$BRANCH" != "main" ]]; then
  echo "ERROR: Switch to main first: git switch main"
  exit 1
fi

MARKER=".kinetics-gallery-download-in-progress"
if [[ -f "$MARKER" ]]; then
  echo "Resuming an interrupted Kinetics gallery download..."
  while IFS= read -r line; do
    path="${line:3}"
    case "$path" in
      "$MARKER"|Assets/Future/PNG/*|Assets/Future/ATTRIBUTION.json|README.md|Assets/Future/kinetics-science-quest.gif)
        ;;
      *)
        echo "ERROR: Unexpected local change while resuming: $path"
        echo "No files were discarded. Inspect git status before continuing."
        exit 1
        ;;
    esac
  done < <(git status --porcelain)
else
  if [[ -n "$(git status --porcelain)" ]]; then
    echo "ERROR: Your working tree is not clean."
    echo "Commit or stash your existing work before starting the gallery download."
    exit 1
  fi
  echo "[1/6] Updating main without overwriting local work..."
  git pull --ff-only origin main
  touch "$MARKER"
fi

echo "[2/6] Checking image dependencies..."
if ! python -c "from PIL import Image" >/dev/null 2>&1; then
  pkg install -y python python-pillow
fi
python -c "from PIL import Image; print('Pillow OK')"

echo "[3/6] Acquiring missing or checksum-invalid domain images..."
# No --overwrite: verified downloads are retained and the job resumes safely.
set +e
python scripts/import_science_gallery.py --start 1 --end 100
gallery_result=$?
set -e
if [[ "$gallery_result" -ne 0 && "$gallery_result" -ne 2 ]]; then
  echo "ERROR: Image acquisition failed with exit code $gallery_result."
  exit "$gallery_result"
fi
if [[ "$gallery_result" -eq 2 ]]; then
  echo "Partial gallery: downloaded images will be published; missing domain cells stay blank."
fi

echo "[4/6] Building the colourful looping science-runner GIF..."
python scripts/build_pixel_animation.py

echo "[5/6] Strictly validating all 100 images, attribution and animation..."
python scripts/validate_visual_assets.py
python - <<'PY'
import json
from pathlib import Path

manifest = json.loads(Path("Assets/Future/ATTRIBUTION.json").read_text(encoding="utf-8"))
print(f"PASS: {len(manifest)}/100 attributed image records are available.")
print("PASS: every existing image passed file, license, dimension and checksum validation.")
print("Unacquired domains remain blank in README.md.")
PY

git diff --check
git add README.md Assets/Future/PNG Assets/Future/ATTRIBUTION.json Assets/Future/kinetics-science-quest.gif

if git diff --cached --quiet; then
  echo "No new image files or gallery metadata to publish."
  exit 0
fi

echo "[6/6] Committing and pushing verified assets..."
rm -f "$MARKER"
git commit -m "Add 100 verified real scientific domain images"
git push origin main

echo "SUCCESS: verified downloaded images, attribution and README gallery pushed to origin/main."
