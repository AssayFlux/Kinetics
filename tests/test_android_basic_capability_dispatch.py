"""Static contract checks for Android-to-Python capability exposure."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "android/app/src/main/python"))
import kinetics_probe  # noqa: E402

UI = (ROOT / "android/app/src/main/java/org/assayflux/kinetics/KineticsUi.kt").read_text()
RUNNER = (
    ROOT / "android/app/src/main/java/org/assayflux/kinetics/AndroidBasicCapabilityRunner.kt"
).read_text()
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
    expected_error = (
        'else:\n        raise ValueError("This capability is not exposed by the '
        'Android basic runner")'
    )
    assert expected_error in PROBE


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

def test_all_new_capabilities_are_reported_as_android_connected():
    status_block = UI.split("val androidWorkflowAvailable", 1)[1].split("Frame(", 1)[0]
    for capability_id in (
        "genome.orf_candidate_scan",
        "kinetics.michaelis_menten",
        "phylo.newick",
        "sequence.global_alignment",
        "genome.contig_assembly_qc",
        "structure.sasa",
        "structure.interaction_candidates",
        "microbiome.diversity",
        "omics.logistic_growth",
        "sequence.explicit_genetic_code_translation",
        "kinetics.inhibition_rate",
        "phylo.upgma",
    ):
        assert f'"{capability_id}"' in status_block

def _run_probe(capability_id: str, input_text: str):
    import json

    payload = json.loads(kinetics_probe.run_android_basic_capability(capability_id, input_text))
    assert payload["capability_id"] == capability_id
    assert "limitations" in payload
    return payload["result"]


def test_android_probe_dispatch_runs_all_exposed_capabilities_on_host():
    assert _run_probe("protein.descriptors", "MKWVTFISLLFLFSSAYS")["length"] == 18
    assert _run_probe("molecular.primer_screen", "ATGCGTACGTAGCTAGCT")["length"] == 18
    assert isinstance(_run_probe("molecular.crispr_pam", "AACCGGTTACGGTAGGCTAACCGG"), list)

    orf_sequence = "ATG" + "GCT" * 29 + "TAA"
    orf_result = _run_probe("genome.orf_candidate_scan", orf_sequence)
    assert orf_result["sequence_length"] == len(orf_sequence)
    assert _run_probe("kinetics.michaelis_menten", "10,100,5")["rate"] > 0
    assert _run_probe("phylo.newick", "((A:0.1,B:0.2):0.3,C:0.4);")["leaf_count"] == 3

    alignment = _run_probe("sequence.global_alignment", "ACGTACGT\nACGTCGTT")
    assert "score" in alignment
    assembly = _run_probe("genome.contig_assembly_qc", ">a\nACGTACGTACGT\n>b\nGGGGCCCC")
    assert isinstance(assembly, dict)

    pdb = (
        "ATOM      1  CA  GLY A   1      12.000  13.800   9.500  1.00 20.00           C\n"
        "TER\nEND\n"
    )
    assert _run_probe("structure.sasa", pdb)
    assert _run_probe("structure.interaction_candidates", pdb)

    diversity = _run_probe("microbiome.diversity", "12,8,5")
    assert diversity["sample_count"] == 3
    growth = _run_probe(
        "omics.logistic_growth",
        '{"timepoints":[0,1,2],"carrying_capacity":100,"growth_rate":0.5,"initial":5}',
    )
    assert len(growth["predicted_counts"]) == 3


def test_android_probe_rejects_unknown_capability_and_malformed_parameters():
    import pytest

    with pytest.raises(ValueError, match="not exposed"):
        kinetics_probe.run_android_basic_capability("unknown.tool", "ACGT")
    with pytest.raises(ValueError, match="three comma-separated"):
        kinetics_probe.run_android_basic_capability("kinetics.michaelis_menten", "10,100")
    with pytest.raises(ValueError, match="two non-empty sequences"):
        kinetics_probe.run_android_basic_capability("sequence.global_alignment", "ACGT")

def test_translation_inhibition_and_upgma_routes_execute_and_validate():
    translated = _run_probe(
        "sequence.explicit_genetic_code_translation",
        '{"sequence":"ATGGCTTAA","table_id":1,"frame":0,"cds":true}',
    )
    assert translated["protein"].startswith("MA")
    inhibited = _run_probe(
        "kinetics.inhibition_rate",
        '{"substrate":10,"inhibitor":2,"vmax":100,"km":5,"ki":1,"mode":"competitive"}',
    )
    assert inhibited["rate"] > 0
    tree = _run_probe(
        "phylo.upgma",
        '{"labels":["A","B","C"],"distance_matrix":[[0,2,4],[2,0,4],[4,4,0]]}',
    )
    assert tree["leaf_count"] == 3
    assert tree["newick"].endswith(";")

def test_translation_inhibition_and_upgma_routes_are_allow_listed():
    for capability_id in (
        "sequence.explicit_genetic_code_translation",
        "kinetics.inhibition_rate",
        "phylo.upgma",
    ):
        assert capability_id in UI
        assert capability_id in RUNNER
        assert capability_id in PROBE

def test_omics_normalisation_correlation_and_jc_nj_routes_execute():
    normalized = _run_probe(
        "omics.normalisation",
        '{"method":"cpm","matrix":[[10,20],[30,40]]}',
    )
    assert len(normalized) == 2
    correlations = _run_probe(
        "omics.cross_correlation",
        '{"first":[[1,2,3],[3,2,1]],"second":[[2,4,6]]}',
    )
    assert len(correlations) == 2
    tree = _run_probe(
        "phylo.jukes_cantor_nj",
        '{"sequences":{"A":"ACGTACGTACGTACGTACGT","B":"ACGTACGTACGTACGTACGA","C":"ACGTACGTACGTACGTACGG"}}',
    )
    assert tree["leaf_count"] == 3
    assert tree["newick"].endswith(";")

def test_gff3_import_and_cds_reconstruction_routes_execute():
    gff3 = (
        "##gff-version 3\n"
        "chr1\tKinetics\tgene\t1\t9\t.\t+\t.\tID=g1\n"
        "chr1\tKinetics\tmRNA\t1\t9\t.\t+\t.\tID=t1;Parent=g1\n"
        "chr1\tKinetics\tCDS\t1\t9\t.\t+\t0\tID=c1;Parent=t1"
    )
    imported = _run_probe("genome.gff3_annotation_import", gff3)
    assert imported["schema"] == "kinetics.gff3-annotation-import.v1"
    reconstructed = _run_probe(
        "genome.gff3_transcript_cds_reconstruction",
        __import__("json").dumps({
            "gff3": gff3,
            "contigs": {"chr1": "ATGGCTTAA"},
            "table_id": 11,
        }),
    )
    assert reconstructed
