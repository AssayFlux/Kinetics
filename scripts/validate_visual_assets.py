#!/usr/bin/env python3
"""Validate all 100 square PNG artworks, their manifest and the animated GIF."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Install Pillow first: python -m pip install Pillow") from exc
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"Assets"/"Future"/"PNG"
MANIFEST=ROOT/"Assets"/"Future"/"ARTWORK_MANIFEST.json"
GIF=ROOT/"Assets"/"Future"/"kinetics-science-quest.gif"
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--strict-gallery",action="store_true")
    args=parser.parse_args()
    files=sorted(OUT.glob("*.png")) if OUT.exists() else []
    records=json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else []
    expected={x.get("file") for x in records}
    errors=[]
    for path in files:
        try:
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                if image.format!="PNG" or image.size!=(1024,1024):
                    errors.append(f"Not a 1024x1024 PNG: {path.name}")
            if str(path.relative_to(ROOT)) not in expected:
                errors.append(f"Missing artwork manifest record: {path.name}")
        except Exception as exc:
            errors.append(f"Invalid PNG {path.name}: {exc}")
    if args.strict_gallery and (len(files)!=100 or len(records)!=100):
        errors.append(f"Gallery incomplete: {len(files)} PNGs and {len(records)} records; expected 100 each")
    if len(records)!=len(files):
        errors.append("Artwork manifest count does not match PNG count")
    if not GIF.exists():
        errors.append("Missing animated GIF")
    else:
        try:
            with Image.open(GIF) as image:
                if image.format!="GIF" or image.size!=(640,240) or image.n_frames<24 or image.info.get("loop")!=0:
                    errors.append("GIF dimensions, frame count or infinite-loop metadata are invalid")
        except Exception as exc:
            errors.append(f"Invalid GIF: {exc}")
    print(f"Square PNG files: {len(files)}/100 | artwork records: {len(records)}")
    if errors:
        print("\n".join("ERROR: "+e for e in errors))
        raise SystemExit(1)
    print("Visual asset validation passed.")
if __name__=="__main__":
    main()
