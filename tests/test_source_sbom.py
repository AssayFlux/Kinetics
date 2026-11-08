from __future__ import annotations

from pathlib import Path

from scripts.generate_source_sbom import generate


def test_source_sbom_includes_host_only_validation_dependencies() -> None:
    root = Path(__file__).resolve().parents[1]
    document = generate(root)
    packages = {package["name"].casefold(): package for package in document["packages"]}
    for name in ("numpy", "scipy"):
        assert name in packages
        assert "validation/requirements-scipy.txt" in packages[name]["comment"]
        assert "not Android runtime" in packages[name]["comment"]
    assert "biopython" in packages
    assert "also used by host-only validation dependency" in packages["biopython"]["comment"]
    assert "not Android runtime" not in packages["biopython"]["comment"]
