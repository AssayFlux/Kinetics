#!/data/data/com.termux/files/usr/bin/bash
# Download real, openly licensed scientific images and publish the 100-image gallery.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

BRANCH="$(git branch --show-current)"
if [ "$BRANCH" != "main" ]; then
  echo "Switch to main first: git switch main"
  exit 1
fi

echo "Updating repository..."
git pull --ff-only origin main

if ! python -c "from PIL import Image" >/dev/null 2>&1; then
  echo "Installing Pillow..."
  pkg install -y python-pillow || python -m pip install --upgrade Pillow
fi

echo "Downloading real, openly licensed images from Wikimedia Commons..."
python scripts/import_science_gallery.py --start 1 --end 100 --overwrite

echo "Checking the gallery..."
python - <<'PY'
import json
from pathlib import Path
from PIL import Image

root = Path(".")
out = root / "Assets/Future/PNG"
manifest = json.loads((root / "Assets/Future/ATTRIBUTION.json").read_text())
files = sorted(out.glob("*.png"))
errors = []
if len(files) != 100:
    errors.append(f"Expected 100 PNGs, found {len(files)}")
if len(manifest) != 100:
    errors.append(f"Expected 100 attribution records, found {len(manifest)}")
for path in files:
    try:
        with Image.open(path) as im:
            if im.format != "PNG" or im.size != (1024, 1024):
                errors.append(f"{path}: expected 1024x1024 PNG, got {im.format} {im.size}")
            im.verify()
    except Exception as exc:
        errors.append(f"{path}: {exc}")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("PASS: 100 real-source 1024x1024 PNGs; 100 attribution records.")
PY

git add README.md Assets/Future/PNG Assets/Future/ATTRIBUTION.json
if git diff --cached --quiet; then
  echo "No new gallery changes to publish."
  exit 0
fi
git commit -m "Import 100 real openly licensed scientific images"
git push origin main
echo "Published real scientific image gallery."
