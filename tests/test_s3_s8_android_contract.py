from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON_BRIDGE = ROOT / "android/app/src/main/python/kinetics_probe.py"
ANDROID_JAVA = ROOT / "android/app/src/main/java/org/assayflux/kinetics"


def test_s3_s8_chaquopy_bridge_exposes_bounded_python_dispatchers() -> None:
    source = PYTHON_BRIDGE.read_text(encoding="utf-8")
    assert "def analyze_ligand_site(" in source
    assert "def analyze_apo_pockets(" in source
    assert "def infer_genetic_code_from_fasta(" in source
    assert "parse_pdb(source_text, include_hetero=True)" in source
    assert "parse_mmcif(source_text, include_hetero=True)" in source
    assert "len(fasta_text) > 1_000_000" in source
    assert "len(records) >= 1_000" in source
    assert "infer_genetic_code_candidates(records, min_records=3, min_codons=90)" in source


def test_s3_s8_android_runner_enforces_limits_and_calls_python_dispatchers() -> None:
    source = (ANDROID_JAVA / "S3S8Runner.kt").read_text(encoding="utf-8")
    assert "MAX_STRUCTURE_BYTES = 16 * 1024 * 1024" in source
    assert "MAX_FASTA_CHARS = 1_000_000" in source
    assert 'callAttr("analyze_ligand_site"' in source
    assert 'callAttr("analyze_apo_pockets"' in source
    assert 'callAttr("infer_genetic_code_from_fasta"' in source
    assert "cutoffAngstrom.isFinite()" in source


def test_s3_s8_explore_cards_are_real_registry_gated_actions() -> None:
    ui = (ANDROID_JAVA / "KineticsUi.kt").read_text(encoding="utf-8")
    cards = (ANDROID_JAVA / "S3S8ResearchCards.kt").read_text(encoding="utf-8")
    assert 'item { StructureSiteAnalysisCard() }' in ui
    assert 'item { GeneticCodeInferenceCard() }' in ui
    assert 'it.id == "structure.ligand_site_candidates"' in ui
    assert 'it.id == "structure.apo_pocket_candidates"' in ui
    assert 'it.id == "sequence.genetic_code_candidate_inference"' in ui
    assert 'ActivityResultContracts.OpenDocument()' in cards
    assert "S3S8Runner.analyzeLigandSite" in cards
    assert "S3S8Runner.analyzeApoPockets" in cards
    assert "S3S8Runner.inferGeneticCode" in cards
    assert "No affinity, specificity, mechanism or function is inferred." in cards
    assert "no organism-specific genetic code is assigned" in cards
