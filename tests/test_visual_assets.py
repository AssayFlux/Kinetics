from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGO_PATH = ROOT / "Assets" / "Brand Logo.svg"
GIF_PATH = ROOT / "Assets" / "Kinetics.gif"


def test_original_brand_assets_are_preserved() -> None:
    logo = LOGO_PATH.read_text(encoding="utf-8")
    assert len(logo) > 1_000_000
    assert "<svg" in logo[:2_000]
    assert GIF_PATH.is_file()
    assert GIF_PATH.stat().st_size > 100_000


def test_readme_places_animation_immediately_below_logo() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    logo = 'src="Assets/Brand%20Logo.svg"'
    animation = 'src="Assets/Kinetics.gif"'

    assert logo in readme
    assert animation in readme
    logo_end = readme.index(logo) + len(logo)
    animation_start = readme.index(animation)
    between = readme[logo_end:animation_start]
    assert between.count("</p>") == 1
    assert "<p" in between
