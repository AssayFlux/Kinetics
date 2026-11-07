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

if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Your working tree is not clean."
  echo "Commit or stash your existing work before running this publisher."
  exit 1
fi

echo "[1/6] Updating main without overwriting local work..."
git pull --ff-only origin main

echo "[2/6] Checking image dependencies..."
if ! python -c "from PIL import Image" >/dev/null 2>&1; then
  pkg install -y python python-pillow
fi
python -c "from PIL import Image; print('Pillow OK')"

echo "[3/6] Acquiring missing or checksum-invalid domain images..."
# No --overwrite: verified downloads are retained and the job resumes safely.
python scripts/import_science_gallery.py --start 1 --end 100

echo "[4/6] Building the colourful looping science-runner GIF..."
python scripts/build_pixel_animation.py

echo "[5/6] Strictly validating all 100 images, attribution and animation..."
python scripts/validate_visual_assets.py --strict-gallery
python - <<'PY'
import ast
import hashlib
import json
import re
from pathlib import Path
from PIL import Image

root = Path(".")
source = (root / "scripts/import_science_gallery.py").read_text(encoding="utf-8")
module = ast.parse(source)
node = next(
    item for item in module.body
    if isinstance(item, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == "CATEGORIES" for t in item.targets)
)
categories = ast.literal_eval(node.value)
out = root / "Assets/Future/PNG"
manifest_path = root / "Assets/Future/ATTRIBUTION.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
by_file = {item.get("file"): item for item in manifest if item.get("file")}

errors = []
if len(categories) != 100:
    errors.append(f"Expected exactly 100 configured domains, found {len(categories)}")
if len(manifest) != 100 or len(by_file) != 100:
    errors.append(f"Expected 100 unique attribution entries, found {len(manifest)}")
titles = []
for number, (slug, _query) in enumerate(categories, 1):
    name = f"{number:03d}-{slug}.png"
    rel = f"Assets/Future/PNG/{name}"
    path = out / name
    record = by_file.get(rel)
    if not path.is_file():
        errors.append(f"MISSING image: {rel}")
        continue
    if not record:
        errors.append(f"MISSING attribution: {rel}")
        continue
    if record.get("number") != number:
        errors.append(f"Wrong domain number in attribution: {rel}")
    if not record.get("title") or not record.get("source_page", "").startswith("https://"):
        errors.append(f"Missing original source title/page: {rel}")
    if not record.get("url", "").startswith("https://"):
        errors.append(f"Missing original image URL: {rel}")
    license_name = record.get("license", "")
    if not re.match(r"^(CC0|Public domain|CC BY(?:-SA)?(?: |$))", license_name, re.I):
        errors.append(f"Unapproved/missing license '{license_name}': {rel}")
    titles.append(record.get("title"))
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != record.get("sha256"):
        errors.append(f"SHA-256 mismatch: {rel}")
    try:
        with Image.open(path) as image:
            if image.format != "PNG" or image.size != (1024, 1024):
                errors.append(f"Wrong format/dimensions {image.format} {image.size}: {rel}")
            image.verify()
    except Exception as exc:
        errors.append(f"Unreadable image {rel}: {exc}")

if len(set(titles)) != 100:
    errors.append(f"Expected 100 distinct source images; found {len(set(titles))} unique titles")
actual_pngs = list(out.glob("*.png"))
if len(actual_pngs) != 100:
    errors.append(f"Expected exactly 100 gallery PNG files, found {len(actual_pngs)}")

if errors:
    print("\n".join("FAIL: " + error for error in errors))
    raise SystemExit(1)

print("PASS: 100/100 unique domain images.")
print("PASS: 100 square 1024x1024 PNGs; all files decode successfully.")
print("PASS: 100 source pages, image URLs, accepted licenses and SHA-256 checksums.")
PY

git diff --check
git add README.md Assets/Future/PNG Assets/Future/ATTRIBUTION.json Assets/Future/kinetics-science-quest.gif

if git diff --cached --quiet; then
  echo "No new image files or gallery metadata to publish."
  exit 0
fi

echo "[6/6] Committing and pushing verified assets..."
git commit -m "Add 100 verified real scientific domain images"
git push origin main

echo "SUCCESS: 100 verified scientific images and attribution records pushed to origin/main."
