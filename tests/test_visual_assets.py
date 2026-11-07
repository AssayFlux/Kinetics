from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGO_PATH = ROOT / "Assets" / "Brand Logo.svg"


def test_original_brand_logo_is_preserved() -> None:
    logo = LOGO_PATH.read_text(encoding="utf-8")
    assert len(logo) > 1_000_000
    assert "<svg" in logo[:2_000]
    assert "guilloche" not in logo.lower() or "<svg" in logo[:2_000]


def test_readme_uses_the_original_brand_logo() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Assets/Brand%20Logo.svg" in readme
    assert "KINETICS_ANIMATION" not in readme
    assert ".gif" not in readme.lower()
