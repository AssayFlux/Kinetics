from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _gallery_categories() -> list[list[str]]:
    source = (ROOT / "scripts" / "import_science_gallery.py").read_text(encoding="utf-8")
    module = ast.parse(source)
    node = next(item for item in module.body if isinstance(item, ast.Assign) and any(
        isinstance(target, ast.Name) and target.id == "CATEGORIES" for target in item.targets
    ))
    return ast.literal_eval(node.value)


def test_science_gallery_defines_100_unique_domains() -> None:
    categories = _gallery_categories()
    assert len(categories) == 100
    slugs = [row[0] for row in categories]
    assert len(set(slugs)) == 100
    assert all(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) for slug in slugs)


def test_gallery_license_filter_excludes_restricted_commons_licenses() -> None:
    source = (ROOT / "scripts" / "import_science_gallery.py").read_text(encoding="utf-8")
    match = re.search(r"LICENSE_OK\s*=\s*re\.compile\(([^,]+)", source)
    assert match is not None
    pattern = ast.literal_eval(match.group(1))
    allowed = re.compile(pattern, re.IGNORECASE)
    assert allowed.search("CC0 1.0")
    assert allowed.search("Public domain")
    assert allowed.search("CC BY 4.0")
    assert allowed.search("CC BY-SA 4.0")
    assert not allowed.search("CC BY-NC-SA 4.0")
    assert not allowed.search("CC BY-ND 4.0")


def test_readme_does_not_embed_uncommitted_png_gallery_paths() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "100-domain scientific atlas" in readme
    assert "deliberately avoids embedding absent PNG paths" in readme
    assert "<!-- KINETICS_GALLERY_START -->" in readme
    assert "<!-- KINETICS_GALLERY_END -->" in readme
    assert not re.search(r"<img[^>]+Assets/Future/PNG/[^>]+>", readme)


def test_pixel_animation_builder_and_validator_are_present() -> None:
    builder = ROOT / "scripts" / "build_pixel_animation.py"
    validator = ROOT / "scripts" / "validate_visual_assets.py"
    assert builder.is_file()
    assert validator.is_file()
    source = builder.read_text(encoding="utf-8")
    assert "FRAMES=32" in source
    assert "loop=0" in source
