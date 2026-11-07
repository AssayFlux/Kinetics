from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANIMATION_PATH = "Assets/Future/kinetics-science-quest.gif"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".svg", ".ico"}


def test_readme_embeds_only_the_original_animation() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    image_tags = [line for line in readme.splitlines() if "<img " in line]
    assert len(image_tags) == 1
    assert ANIMATION_PATH in image_tags[0]
    assert "<!-- KINETICS_ANIMATION -->" in readme
    assert "<!-- /KINETICS_ANIMATION -->" in readme
    assert "KINETICS_GALLERY" not in readme


def test_repository_contains_no_other_visual_assets() -> None:
    visual_files = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    }
    assert visual_files == {ANIMATION_PATH}


def test_animation_builder_and_validator_enforce_single_asset() -> None:
    builder = (ROOT / "scripts" / "build_pixel_animation.py").read_text(encoding="utf-8")
    validator = (ROOT / "scripts" / "validate_visual_assets.py").read_text(encoding="utf-8")
    assert "FRAME_COUNT = 48" in builder
    assert "loop=0" in builder
    assert "480, 270" in builder
    assert "IMAGE_SUFFIXES" in validator
    assert "no other image assets" in validator
