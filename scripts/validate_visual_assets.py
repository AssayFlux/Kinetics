#!/usr/bin/env python3
"""Validate Kinetics' single-animation visual asset policy."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ANIMATION = ROOT / "Assets" / "Future" / "kinetics-science-quest.gif"
ALLOWED_VISUAL = Path("Assets/Future/kinetics-science-quest.gif")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".svg", ".ico"}


def validate() -> list[str]:
    errors: list[str] = []
    if not ANIMATION.is_file():
        errors.append("The one required animation is missing.")
    else:
        try:
            with Image.open(ANIMATION) as image:
                if image.format != "GIF":
                    errors.append(f"Expected GIF, got {image.format}")
                if image.size != (480, 270):
                    errors.append(f"Expected 480x270 animation, got {image.size}")
                if image.n_frames != 48:
                    errors.append(f"Expected 48 frames, got {image.n_frames}")
                if image.info.get("loop") != 0:
                    errors.append("Animation must loop continuously (loop=0)")
                image.seek(0)
                image.verify()
        except Exception as exc:
            errors.append(f"Animation cannot be decoded: {exc}")

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in IMAGE_SUFFIXES and path.relative_to(ROOT) != ALLOWED_VISUAL:
            errors.append(f"Unexpected static or additional visual asset: {path.relative_to(ROOT)}")

    readme = ROOT / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        if text.count("Assets/Future/kinetics-science-quest.gif") != 1:
            errors.append("README must embed the single animation exactly once.")
        if "<!-- KINETICS_ANIMATION -->" not in text:
            errors.append("README animation marker is missing.")

    return errors


def main() -> None:
    errors = validate()
    if errors:
        print("\n".join(f"FAIL: {item}" for item in errors))
        raise SystemExit(1)
    print("PASS: one 480x270, 48-frame, continuously looping GIF; no other image assets.")


if __name__ == "__main__":
    main()
