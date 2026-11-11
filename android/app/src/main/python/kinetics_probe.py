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


def prepare_structure_viewer_import(source_text: str, source_format: str) -> str:
    """Parse once and return viewer payload, provenance and bounded session export."""
    import json

    from kinetics.structure_view import (
        build_structure_session_export,
        prepare_structure_viewer_source as prepare,
    )

    source_bytes = source_text.encode("utf-8")
    result = prepare(source_text, source_format=source_format)
    result["session_export_json"] = build_structure_session_export(
        source_bytes,
        result["payload"],
        parser_version="kinetics-structure-parser-v1",
    )
    return json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _analysis_provenance(source_text: str, source_format: str, tool_id: str, parameters: dict):
    import hashlib
    from datetime import datetime, timezone

    import kinetics

    return {
        "source_sha256": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
        "source_format": source_format,
        "tool_id": tool_id,
        "tool_version": kinetics.__version__,
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "parameters": parameters,
    }


def _parse_structure_atoms(source_text: str, source_format: str):
    from kinetics.structure import parse_mmcif, parse_pdb

    if not isinstance(source_text, str) or len(source_text.encode("utf-8")) > 16 * 1024 * 1024:
        raise ValueError("Structure input must be text within the 16 MiB limit")
    if source_format == "pdb":
        return parse_pdb(source_text, include_hetero=True)
    if source_format == "mmcif":
        return parse_mmcif(source_text, include_hetero=True)
    raise ValueError("Structure format must be pdb or mmcif")


def analyze_ligand_site(
    source_text: str,
    source_format: str,
    ligand_chain: str,
    ligand_residue_number: int,
    ligand_residue_name: str,
    cutoff_angstrom: float = 5.0,
) -> str:
    """Run the bounded S3 explicit-ligand geometric site candidate screen."""
    import json

    from kinetics import ligand_site_candidates

    atoms = _parse_structure_atoms(source_text, source_format)
    result = ligand_site_candidates(
        atoms,
        ligand_chain=ligand_chain,
        ligand_residue_number=ligand_residue_number,
        ligand_residue_name=ligand_residue_name,
        cutoff_angstrom=cutoff_angstrom,
    )
    result["provenance"] = _analysis_provenance(
        source_text,
        source_format,
        "structure.ligand_site_candidates",
        {
            "ligand_chain": ligand_chain,
            "ligand_residue_number": ligand_residue_number,
            "ligand_residue_name": ligand_residue_name,
            "cutoff_angstrom": cutoff_angstrom,
        },
    )
    return json.dumps(result, ensure_ascii=False, sort_keys=True)


def analyze_apo_pockets(source_text: str, source_format: str) -> str:
    """Run the bounded S3 apo probe-grid concavity candidate screen."""
    import json

    from kinetics import apo_pocket_candidates

    atoms = _parse_structure_atoms(source_text, source_format)
    result = apo_pocket_candidates(atoms)
    result["provenance"] = _analysis_provenance(
        source_text,
        source_format,
        "structure.apo_pocket_candidates",
        {
            "grid_spacing_angstrom": 1.0,
            "small_probe_radius_angstrom": 1.4,
            "large_probe_radius_angstrom": 3.0,
            "generic_atom_radius_angstrom": 1.7,
            "max_grid_points": 250000,
            "max_distance_checks": 5000000,
        },
    )
    return json.dumps(result, ensure_ascii=False, sort_keys=True)


def infer_genetic_code_from_fasta(fasta_text: str, complete_cds: bool = False) -> str:
    """Run S8 candidate-table screening on bounded caller-supplied FASTA records."""
    import json

    from kinetics import infer_genetic_code_candidates
    from kinetics.sequence import iter_fasta_records

    if not isinstance(fasta_text, str) or len(fasta_text) > 1_000_000:
        raise ValueError("FASTA input must be text within the 1,000,000-character limit")
    if not isinstance(complete_cds, bool):
        raise ValueError("complete_cds must be a boolean")
    records = []
    for record in iter_fasta_records(fasta_text.splitlines()):
        if len(records) >= 1_000:
            raise ValueError("FASTA input exceeds the 1,000-record S8 limit")
        records.append({
            "id": record.identifier,
            "sequence": record.sequence,
            "complete_cds": complete_cds,
        })
    result = infer_genetic_code_candidates(records, min_records=3, min_codons=90)
    from kinetics.genetic_code import GENETIC_CODES

    result["provenance"] = _analysis_provenance(
        fasta_text,
        "fasta",
        "sequence.genetic_code_candidate_inference",
        {
            "complete_cds": complete_cds,
            "min_records": 3,
            "min_codons": 90,
            "candidate_table_ids": sorted(GENETIC_CODES),
        },
    )
    return json.dumps(result, ensure_ascii=False, sort_keys=True)



def analyze_ligand_sdf_graph(source_text: str):
    """Android bridge returning JSON for the bounded offline ligand graph preview."""
    from kinetics.chemistry import analyze_sdf_graph

    return json.dumps(analyze_sdf_graph(source_text), sort_keys=True)
