"""Static contract checks for Android-to-Python capability exposure."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI = (ROOT / "android/app/src/main/java/org/assayflux/kinetics/KineticsUi.kt").read_text()
RUNNER = (ROOT / "android/app/src/main/java/org/assayflux/kinetics/AndroidBasicCapabilityRunner.kt").read_text()
PROBE = (ROOT / "android/app/src/main/python/kinetics_probe.py").read_text()


def test_simple_sequence_capabilities_are_explicitly_exposed_on_android():
    expected = (
        "protein.descriptors",
        "molecular.primer_screen",
        "molecular.crispr_pam",
    )
    for capability_id in expected:
        assert capability_id in UI
        assert capability_id in RUNNER
        assert capability_id in PROBE


def test_android_sequence_runner_is_allow_listed_and_bounded():
    assert "capabilityId in supported" in RUNNER
    assert "MAX_INPUT_CHARS = 1_000_000" in RUNNER
    assert "1_000_000" in PROBE
    assert 'else:\n        raise ValueError("This capability is not exposed by the Android basic runner")' in PROBE


def test_pam_and_primer_limitations_are_returned_with_results():
    assert "No guide efficacy, off-target, editing outcome or safety prediction" in PROBE
    assert "No salt, magnesium, concentration, hairpin or primer-dimer model" in PROBE

def test_orf_kinetics_and_newick_are_bounded_explicit_android_routes():
    for capability_id in ("genome.orf_candidate_scan", "kinetics.michaelis_menten", "phylo.newick"):
        assert capability_id in UI
        assert capability_id in RUNNER
        assert capability_id in PROBE
    assert "max_candidate_orf_pairs_total=100_000" in PROBE
    assert "math.isfinite" in PROBE
    assert "normalized_newick" in PROBE

def test_alignment_assembly_structure_and_omics_routes_are_bounded():
    expected = (
        "sequence.global_alignment",
        "genome.contig_assembly_qc",
        "structure.sasa",
        "structure.interaction_candidates",
        "microbiome.diversity",
        "omics.logistic_growth",
    )
    for capability_id in expected:
        assert capability_id in UI
        assert capability_id in RUNNER
        assert capability_id in PROBE
    assert "max_cells=250_000" in PROBE
    assert "max_total_bases=1_000_000" in PROBE
    assert "5,000 parsed atoms" in PROBE
