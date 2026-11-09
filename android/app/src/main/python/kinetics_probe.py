"""R1-only on-device scientific dependency probe; not a production capability."""

from io import StringIO


def runtime_report():
    import platform
    import sys

    import Bio
    import numpy
    import kinetics
    from kinetics import normalize_small_variant, parse_fasta
    from Bio import SeqIO
    from Bio.Align import PairwiseAligner
    from Bio.PDB import PDBParser

    try:
        import scipy
    except ModuleNotFoundError:
        scipy = None

    fasta = StringIO(">kinetics-r1-smoke\nACGTACGT\n")
    record = next(SeqIO.parse(fasta, "fasta"))
    assert str(record.seq) == "ACGTACGT"
    package_record = parse_fasta(">workbench-smoke\nACGT\n")[0]
    normalized_variant = normalize_small_variant("probe", 4, "A", "AA", "CAAAA")
    assert package_record.sequence == "ACGT"
    assert (normalized_variant["pos"], normalized_variant["ref"], normalized_variant["alt"]) == (
        1, "C", "CA"
    )

    pdb = """\
ATOM      1  N   GLY A   1      11.104  13.207   9.123  1.00 20.00           N
ATOM      2  CA  GLY A   1      12.000  13.800   9.500  1.00 20.00           C
ATOM      3  C   GLY A   1      13.200  13.000  10.000  1.00 20.00           C
TER
END
"""
    structure = PDBParser(QUIET=True).get_structure("kinetics-r1", StringIO(pdb))
    residues = list(structure.get_residues())
    assert len(residues) == 1 and residues[0].resname == "GLY"

    aligner = PairwiseAligner()
    aligner.mode = "global"
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -5
    aligner.extend_gap_score = -1
    alignment = aligner.align("ACGT", "ACCT")[0]
    assert alignment.score == 5.0

    vector = numpy.asarray([3.0, 4.0], dtype=numpy.float64)
    if scipy is None:
        norm = float(numpy.linalg.norm(vector))
        scipy_smoke = "not-installed: no compatible Chaquopy Android wheel"
        scipy_version = None
    else:
        norm = float(scipy.linalg.norm(vector))
        scipy_smoke = "passed"
        scipy_version = scipy.__version__
    assert abs(norm - 5.0) < 1e-12

    return {
        "python": sys.version,
        "kinetics_workbench": kinetics.__version__,
        "kinetics_package_smoke": package_record.sequence,
        "platform": platform.platform(),
        "biopython": Bio.__version__,
        "numpy": numpy.__version__,
        "scipy": scipy_version,
        "scipy_smoke": scipy_smoke,
        "seqio_fasta_smoke": str(record.seq),
        "bio_pdb_residue_smoke": residues[0].resname,
        "biopython_pairwise_alignment_score": float(alignment.score),
        "numpy_linalg_norm": norm,
    }


def analyze_fasta(text: str) -> str:
    """Bounded JSON adapter for the registry-backed local FASTA QC workflow."""
    import json

    from kinetics.workflows import analyze_fasta_text

    return json.dumps(analyze_fasta_text(text), ensure_ascii=False, sort_keys=True)


def analyze_fastq(text: str, phred_offset: int) -> str:
    """Bounded JSON adapter for FASTQ read-quality summaries."""
    import json
    from kinetics.workflows import analyze_fastq_text
    return json.dumps(analyze_fastq_text(text, phred_offset=phred_offset),
                      ensure_ascii=False, sort_keys=True)

def prepare_structure_viewer_source(source_text: str, source_format: str) -> str:
    """Chaquopy adapter for bounded local PDB/mmCIF parsing and viewer preparation."""
    import json

    from kinetics.structure_view import prepare_structure_viewer_source as prepare

    result = prepare(source_text, source_format=source_format)
    return json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def export_structure_viewer_session(source_text: str, source_format: str) -> str:
    """Create a bounded, provenance-bearing offline JSON session for SAF export."""
    from kinetics.structure_view import (
        build_structure_session_export,
        prepare_structure_viewer_source as prepare,
    )

    source_bytes = source_text.encode("utf-8")
    result = prepare(source_text, source_format=source_format)
    return build_structure_session_export(
        source_bytes,
        result["payload"],
        parser_version="kinetics-structure-parser-v1",
    )
