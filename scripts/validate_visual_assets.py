#!/usr/bin/env python3
"""Validate downloaded scientific gallery assets and the pixel animation."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "Assets" / "Future" / "PNG"
MANIFEST = ROOT / "Assets" / "Future" / "ATTRIBUTION.json"
ANIMATION = ROOT / "Assets" / "Future" / "kinetics-science-quest.gif"
LICENSE_PATTERN = re.compile(r"^(?:CC0|Public domain|CC BY(?:-SA)?(?: |$))", re.I)


def categories() -> list[list[str]]:
    source = (ROOT / "scripts" / "import_science_gallery.py").read_text(encoding="utf-8")
    module = ast.parse(source)
    node = next(
        item for item in module.body
        if isinstance(item, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "CATEGORIES" for target in item.targets)
    )
    return ast.literal_eval(node.value)


def validate_gallery(strict: bool) -> list[str]:
    errors: list[str] = []
    expected = categories()
    records = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else []
    by_file = {record.get("file"): record for record in records if record.get("file")}
    if strict and len(expected) != 100:
        errors.append(f"Expected 100 configured domains, found {len(expected)}")
    if strict and len(by_file) != 100:
        errors.append(f"Expected 100 unique attribution records, found {len(by_file)}")

    for number, (slug, _query) in enumerate(expected, 1):
        relative = f"Assets/Future/PNG/{number:03d}-{slug}.png"
        path = ROOT / relative
        record = by_file.get(relative)
        if not path.is_file():
            if strict:
                errors.append(f"Missing image: {relative}")
            continue
        if not record:
            errors.append(f"Image has no attribution record: {relative}")
            continue
        if not LICENSE_PATTERN.match(record.get("license", "")):
            errors.append(f"Unapproved license: {relative}")
        if not record.get("source_page", "").startswith("https://"):
            errors.append(f"Missing source page: {relative}")
        if not record.get("url", "").startswith("https://"):
            errors.append(f"Missing original image URL: {relative}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if record.get("sha256") != digest:
            errors.append(f"SHA-256 mismatch: {relative}")
        try:
            with Image.open(path) as image:
                if image.format != "PNG" or image.size != (1024, 1024):
                    errors.append(f"Expected 1024x1024 PNG: {relative}")
                image.verify()
        except Exception as exc:
            errors.append(f"Unreadable image {relative}: {exc}")

    if strict and len(list(GALLERY.glob("*.png"))) != 100:
        errors.append("Strict gallery requires exactly 100 PNG files")
    return errors


def validate_animation() -> list[str]:
    if not ANIMATION.is_file():
        return [f"Missing animation: {ANIMATION.relative_to(ROOT)}"]
    try:
        with Image.open(ANIMATION) as image:
            if image.format != "GIF" or image.n_frames != 32:
                return [f"Expected a 32-frame GIF, got {image.format} with {image.n_frames} frames"]
            if image.size != (320, 120):
                return [f"Unexpected GIF dimensions: {image.size}"]
            if image.info.get("loop") != 0:
                return ["GIF must loop forever (loop=0)"]
    except Exception as exc:
        return [f"Invalid GIF: {exc}"]
    return []


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict-gallery", action="store_true")
    args = parser.parse_args()
    errors = validate_gallery(args.strict_gallery) + validate_animation()
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        raise SystemExit(1)
    print("PASS: gallery metadata/checksums and 32-frame looping animation.")


if __name__ == "__main__":
    main()
