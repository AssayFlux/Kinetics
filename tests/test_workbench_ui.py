"""Static acceptance checks for the researcher-facing workbench surfaces.

These checks protect the responsive/accessibility contract in CI. They do not
replace browser automation or acceptance on physical desktop/mobile devices.
"""
from pathlib import Path

STATIC = Path(__file__).parents[1] / "src" / "kinetics_core" / "workbench" / "static"


def test_workbench_has_responsive_and_accessible_foundations():
    html = (STATIC / "index.html").read_text(encoding="utf-8")
    assert 'name="viewport"' in html
    assert "@media(max-width:1050px)" in html
    assert "@media(max-width:680px)" in html
    assert "prefers-reduced-motion:reduce" in html
    assert 'role="status"' in html
    assert 'aria-live="polite"' in html
    assert ":focus-visible" in html
    assert 'for="project"' in html
    assert 'for="dataset-file"' in html
    assert 'for="command"' in html


def test_workbench_exposes_the_complete_research_flow():
    html = (STATIC / "index.html").read_text(encoding="utf-8")
    for feature in (
        "Project workspace",
        "Dataset intake",
        "Research workflow",
        "Dataset registry",
        "Experiment registry",
        "Jobs and experiment history",
        "Artifact browser",
        "workflowExamples",
        "/api/v1/projects/",
        "/api/v1/experiments",
    ):
        assert feature in html


def test_structure_viewer_has_mobile_and_accessibility_controls():
    html = (STATIC / "structure-viewer.html").read_text(encoding="utf-8")
    assert 'name="viewport"' in html
    assert "@media(max-width:900px)" in html
    assert "@media(max-width:520px)" in html
    assert "prefers-reduced-motion:reduce" in html
    assert 'aria-label="Interactive three-dimensional molecular structure"' in html
    assert 'role="status"' in html
    for feature in (
        "Cartoon / ribbon",
        "Export PNG",
        "Calculate contacts",
        "Align and map residues",
        "Analyze structure evidence",
    ):
        assert feature in html
