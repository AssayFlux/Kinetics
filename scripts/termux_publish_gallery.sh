#!/data/data/com.termux/files/usr/bin/bash
# Generate the complete square scientific-art gallery and publish it from Termux.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
BRANCH="$(git branch --show-current)"
if [ "$BRANCH" != "main" ]; then
  echo "Please switch to main first: git switch main"
  exit 1
fi
echo "Updating main before generating assets..."
git pull --ff-only origin main
if ! python -c "from PIL import Image" >/dev/null 2>&1; then
  echo "Installing Pillow..."
  if command -v pkg >/dev/null 2>&1; then
    pkg install -y python-pillow || python -m pip install --upgrade Pillow
  else
    python -m pip install --upgrade Pillow
  fi
fi
python scripts/generate_futuristic_gallery.py
python scripts/build_pixel_animation.py
python scripts/validate_visual_assets.py --strict-gallery
git add README.md Assets/Future/PNG Assets/Future/ARTWORK_MANIFEST.json Assets/Future/ATTRIBUTION.json Assets/Future/kinetics-science-quest.gif
if git diff --cached --quiet; then
  echo "No changes to publish."
  exit 0
fi
git commit -m "Add 100 square futuristic scientific illustrations"
git push origin main
echo "Published all 100 square PNG images and the looping pixel animation."
