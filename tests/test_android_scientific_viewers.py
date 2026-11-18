import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_explore_routes_to_real_offline_structure_and_chemistry_viewers() -> None:
    ui = (ROOT / "android/app/src/main/java/org/assayflux/kinetics/KineticsUi.kt").read_text()
    viewer = (
        ROOT / "android/app/src/main/java/org/assayflux/kinetics/StructureViewer.kt"
    ).read_text()
    chemistry = (
        ROOT / "android/app/src/main/java/org/assayflux/kinetics/I1ChemistryCard.kt"
    ).read_text()
    assert "U4 · STRUCTURE & CHEMISTRY VIEWERS" in ui
    assert "StructureViewerPreview()" in ui
    assert "LigandGraphPreviewCard()" in ui
    assert "WebViewAssetLoader" in viewer
    assert "settings.blockNetworkLoads = true" in viewer
    assert 'CreateDocument("image/svg+xml")' in viewer
    assert 'CreateDocument("image/png")' in viewer
    assert "I1 · Ligand graph preview" in chemistry
    assert "RDKit sanitization" in chemistry


def test_vcf_research_screen_is_attestation_gated_and_aggregate_only() -> None:
    card = (
        ROOT / "android/app/src/main/java/org/assayflux/kinetics/GenomicsVcfQcCard.kt"
    ).read_text()
    runner = (
        ROOT / "android/app/src/main/java/org/assayflux/kinetics/GenomicsVcfQcRunner.kt"
    ).read_text()
    gate = (
        ROOT / "android/app/src/main/java/org/assayflux/kinetics/U5ResearchGateCard.kt"
    ).read_text()
    assert "enabled = !busy && selectedUri != null && consentConfirmed" in card
    assert "MAX_INPUT_BYTES = 5 * 1024 * 1024" in runner
    assert "sample identifiers and genotype strings" in card
    assert "P0 is NOT APPROVED" in gate
    assert "not bundled or presented as runnable on Android" in gate
    assert "ResearchStore" not in card
    assert "openOutputStream" not in card
    assert "Clinical Mode" not in card



def test_android_vcf_chaquopy_bridge_returns_only_aggregate_qc() -> None:
    bridge_path = ROOT / "android/app/src/main/python/kinetics_probe.py"
    spec = importlib.util.spec_from_file_location("kinetics_probe_u5_test", bridge_path)
    assert spec is not None and spec.loader is not None
    bridge = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bridge)
    fixture = (
        "##fileformat=VCFv4.3\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYNTHETIC_SAMPLE\n"
        "chr1\t10\t.\tA\tG\t50\tPASS\t.\tGT\t0/1\n"
    )
    report = json.loads(bridge.summarize_vcf_research_qc(fixture))
    assert report["record_count"] == 1
    assert report["sample_count"] == 1
    assert report["source_sha256"]
    assert "SYNTHETIC_SAMPLE" not in str(report)
    assert "0/1" not in str(report)
    assert "genotypes" not in report and "samples" not in report
