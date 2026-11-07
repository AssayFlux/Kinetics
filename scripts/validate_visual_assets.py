#!/usr/bin/env python3
"""Validate the 100 PNG gallery, attribution manifest and animated GIF."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"Assets"/"Future"/"PNG"
MANIFEST=ROOT/"Assets"/"Future"/"ATTRIBUTION.json"
GIF=ROOT/"Assets"/"Future"/"kinetics-science-quest.gif"
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--strict-gallery",action="store_true")
    args=parser.parse_args()
    files=list(OUT.glob("*.png")) if OUT.exists() else []
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else []
    attributed={x.get("file") for x in manifest}
    errors=[]
    for path in files:
        try:
            with Image.open(path) as image: image.verify()
            if f"Assets/Future/PNG/{path.name}" not in attributed: errors.append(f"Missing attribution: {path.name}")
        except Exception as exc: errors.append(f"Invalid PNG {path.name}: {exc}")
    if args.strict_gallery and (len(files)!=100 or len(attributed)<100): errors.append("Gallery is not complete: expected 100 PNGs and 100 attribution records")
    if not GIF.exists(): errors.append("Missing animated GIF")
    else:
        try:
            with Image.open(GIF) as image:
                if image.format!="GIF" or image.size!=(640,240) or image.n_frames<24 or image.info.get("loop")!=0:
                    errors.append("GIF dimensions, frame count or infinite-loop metadata are invalid")
        except Exception as exc: errors.append(f"Invalid GIF: {exc}")
    print(f"PNG files: {len(files)}/100 | attribution records: {len(manifest)}")
    if errors:
        print("\n".join("ERROR: "+e for e in errors)); raise SystemExit(1)
    print("Visual asset validation passed.")
if __name__=="__main__": main()
