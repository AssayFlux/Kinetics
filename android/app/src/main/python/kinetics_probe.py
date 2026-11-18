"""R1-only on-device scientific dependency probe; not a production capability."""

import json
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



def run_android_basic_capability(capability_id: str, sequence_text: str) -> str:
    """Explicit allow-list for bounded Android sequence/protein utilities."""
    import json

    if not isinstance(sequence_text, str) or len(sequence_text) > 1_000_000:
        raise ValueError("Sequence input must be text within the 1,000,000-character limit")
    if not isinstance(capability_id, str):
        raise ValueError("Capability ID must be a string")

    if capability_id == "protein.descriptors":
        from kinetics.protein import protein_descriptors
        sequence = "".join(sequence_text.split()).upper()
        if len(sequence) > 100_000:
            raise ValueError("Protein sequence exceeds the 100,000-residue mobile limit")
        result = protein_descriptors(sequence)
        limitations = [
            "Assumes an unmodified linear peptide with free termini",
            "Average residue masses are used",
            "Theoretical pI is an approximate model, not an experimental measurement",
        ]
    elif capability_id == "molecular.primer_screen":
        from kinetics.molecular import primer_properties
        sequence = "".join(sequence_text.split()).upper()
        result = primer_properties(sequence)
        limitations = [
            "Wallace-rule melting temperature is a rough estimate only",
            "No salt, magnesium, concentration, hairpin or primer-dimer model",
            "Not a primer design recommendation or wet-lab validation",
        ]
    elif capability_id == "molecular.crispr_pam":
        from kinetics.molecular import scan_spcas9_ngg
        sequence = "".join(sequence_text.split()).upper()
        if len(sequence) > 1_000_000:
            raise ValueError("DNA sequence exceeds the 1,000,000-base mobile limit")
        result = scan_spcas9_ngg(sequence, strand="both")
        limitations = [
            "Reports SpCas9 NGG PAM locations only",
            "No guide efficacy, off-target, editing outcome or safety prediction",
        ]
    elif capability_id == "sequence.global_alignment":
        from kinetics.sequence import needleman_wunsch
        parts = [line.strip() for line in sequence_text.splitlines() if line.strip()]
        if len(parts) != 2:
            raise ValueError("Enter exactly two non-empty sequences on separate lines")
        if (len(parts[0]) + 1) * (len(parts[1]) + 1) > 250_000:
            raise ValueError("Alignment exceeds the 250,000-cell mobile limit")
        result = needleman_wunsch(parts[0], parts[1], max_cells=250_000)
        limitations = [
            "Global linear-gap alignment with fixed default scoring",
            "One deterministic optimal traceback is returned; this is not a clinical or variant interpretation",
        ]
    elif capability_id == "genome.contig_assembly_qc":
        from kinetics.genome_qc import summarize_contigs
        from kinetics.sequence import iter_fasta_records
        records = iter_fasta_records(sequence_text.splitlines())
        result = summarize_contigs(records, max_records=10_000, max_total_bases=1_000_000)
        limitations = [
            "Assembly statistics only; no gene prediction, taxonomic assignment or functional annotation",
            "Mobile input is capped at 1 MB, 10,000 records and 1,000,000 total bases",
        ]
    elif capability_id == "structure.sasa":
        from kinetics.structure import parse_pdb, solvent_accessible_surface_area
        atoms = parse_pdb(sequence_text, include_hetero=False)
        if len(atoms) > 2_000:
            raise ValueError("Mobile SASA is limited to 2,000 parsed atoms")
        result = solvent_accessible_surface_area(atoms)
        limitations = [
            "Approximate Shrake–Rupley surface sampling with default probe and point count",
            "No hydrogens, atom-specific radii, residue-relative accessibility or calibrated quality grade",
        ]
    elif capability_id == "structure.interaction_candidates":
        from kinetics.structure import interaction_candidates, parse_pdb
        atoms = parse_pdb(sequence_text, include_hetero=False)
        if len(atoms) > 5_000:
            raise ValueError("Mobile interaction screening is limited to 5,000 parsed atoms")
        result = interaction_candidates(atoms)
        limitations = [
            "Distance-only geometric candidates; no hydrogen placement, energetics or binding-affinity prediction",
            "Mobile pairwise screening is limited to 5,000 parsed atoms",
        ]
    elif capability_id == "microbiome.diversity":
        from kinetics.omics import shannon_diversity, simpson_diversity
        try:
            counts = [float(part.strip()) for part in sequence_text.split(",") if part.strip()]
        except ValueError as exc:
            raise ValueError("Enter comma-separated numeric abundance counts") from exc
        if len(counts) > 10_000:
            raise ValueError("Mobile diversity analysis is limited to 10,000 abundance values")
        result = {
            "sample_count": len(counts),
            "shannon": shannon_diversity(counts),
            "gini_simpson": simpson_diversity(counts),
        }
        limitations = [
            "Diversity indices depend on the supplied count vector and sampling design",
            "No taxonomic classification, differential abundance or clinical interpretation",
        ]
    elif capability_id == "omics.logistic_growth":
        import json
        from kinetics.omics import logistic_growth
        try:
            parameters = json.loads(sequence_text)
            timepoints = parameters["timepoints"]
            result_values = logistic_growth(
                timepoints,
                [0.0] * len(timepoints),
                carrying_capacity=parameters["carrying_capacity"],
                growth_rate=parameters["growth_rate"],
                initial=parameters["initial"],
            )
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(
                "Provide JSON keys timepoints, carrying_capacity, growth_rate and initial"
            ) from exc
        result = {"timepoints": timepoints, "predicted_counts": result_values}
        limitations = [
            "Deterministic logistic model only; no parameter fitting or confidence intervals",
            "Parameters and output units must be interpreted in the context of the study design",
        ]
    elif capability_id == "sequence.explicit_genetic_code_translation":
        from kinetics.genetic_code import translate_coding_sequence
        try:
            parameters = json.loads(sequence_text)
            sequence = parameters["sequence"]
            table_id = parameters.get("table_id", 1)
            frame = parameters.get("frame", 0)
            cds = parameters.get("cds", False)
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(
                "Provide JSON with sequence and optional table_id, frame and cds"
            ) from exc
        if not isinstance(sequence, str) or len(sequence) > 100_000:
            raise ValueError("Coding sequence must be text within the 100,000-base mobile limit")
        result = translate_coding_sequence(
            sequence, table_id=table_id, frame=frame, cds=cds,
        )
        limitations = [
            "Caller-selected NCBI genetic code only; the organism's code is not inferred",
            "Translation does not identify coding regions or variants",
        ]
    elif capability_id == "kinetics.inhibition_rate":
        import math
        from kinetics.kinetics import inhibition_rate
        try:
            parameters = json.loads(sequence_text)
            substrate = float(parameters["substrate"])
            inhibitor = float(parameters["inhibitor"])
            vmax = float(parameters["vmax"])
            km = float(parameters["km"])
            ki = float(parameters["ki"])
            mode = parameters["mode"]
            ki_uncompetitive = parameters.get("ki_uncompetitive")
            if ki_uncompetitive is not None:
                ki_uncompetitive = float(ki_uncompetitive)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise ValueError(
                "Provide numeric substrate, inhibitor, vmax, km, ki and a valid mode in JSON"
            ) from exc
        values = [substrate, inhibitor, vmax, km, ki]
        if ki_uncompetitive is not None:
            values.append(ki_uncompetitive)
        if not all(math.isfinite(value) for value in values):
            raise ValueError("Inhibition model parameters must be finite numbers")
        rate = inhibition_rate(
            substrate, inhibitor, vmax, km, ki, mode, ki_uncompetitive,
        )
        result = {"rate": rate, "mode": mode}
        limitations = [
            "Deterministic idealized inhibition equation; no parameter fitting or confidence intervals",
            "Mixed inhibition requires an explicit ki_uncompetitive value",
            "Units must be consistent and model choice must be justified experimentally",
        ]
    elif capability_id == "phylo.upgma":
        from kinetics.phylo import to_newick, upgma
        try:
            parameters = json.loads(sequence_text)
            labels = parameters["labels"]
            distance_matrix = parameters["distance_matrix"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(
                "Provide JSON with labels and distance_matrix"
            ) from exc
        if not isinstance(labels, list) or len(labels) > 200:
            raise ValueError("UPGMA requires a list of 2–200 unique labels")
        if not isinstance(distance_matrix, list):
            raise ValueError("distance_matrix must be a square numeric matrix")
        root = upgma(distance_matrix, labels)
        result = {"newick": to_newick(root), "leaf_count": len(labels)}
        limitations = [
            "UPGMA assumes an ultrametric/equal-rate evolutionary process",
            "Tree topology depends entirely on the supplied distance matrix",
            "No sequence alignment, distance estimation or bootstrap support is performed",
        ]
    elif capability_id == "omics.normalisation":
        from kinetics.omics import clr_transform, cpm
        try:
            parameters = json.loads(sequence_text)
            matrix = parameters["matrix"]
            method = parameters["method"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Provide JSON with method and matrix") from exc
        if not isinstance(matrix, list) or not matrix or len(matrix) > 500:
            raise ValueError("Matrix must contain 1–500 feature rows")
        if any(not isinstance(row, list) or len(row) > 500 for row in matrix):
            raise ValueError("Matrix rows must contain at most 500 samples")
        if sum(len(row) for row in matrix) > 50_000:
            raise ValueError("Matrix exceeds the 50,000-value mobile limit")
        if method == "cpm":
            result = cpm(matrix)
        elif method == "clr":
            pseudocount = float(parameters.get("pseudocount", 0.5))
            result = clr_transform(matrix, pseudocount=pseudocount)
        else:
            raise ValueError("method must be 'cpm' or 'clr'")
        limitations = [
            "Transformation only; no batch correction, filtering, imputation or differential testing",
            "CPM and CLR have different assumptions; select based on study design",
        ]
    elif capability_id == "omics.cross_correlation":
        from kinetics.omics import cross_omics_correlation
        try:
            parameters = json.loads(sequence_text)
            first = parameters["first"]
            second = parameters["second"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Provide JSON with first and second feature-by-sample matrices") from exc
        if not isinstance(first, list) or not isinstance(second, list) or not first or not second:
            raise ValueError("Both omics inputs must be non-empty feature-by-sample matrices")
        if len(first) > 200 or len(second) > 200:
            raise ValueError("Each matrix is limited to 200 features")
        if any(not isinstance(row, list) or not row for row in first + second):
            raise ValueError("Every omics feature row must be a non-empty list")
        sample_count = len(first[0])
        if sample_count < 3 or any(len(row) != sample_count for row in first + second):
            raise ValueError("All features must have the same order and at least three matched samples")
        if sum(len(row) for row in first + second) > 100_000:
            raise ValueError("Omics matrices exceed the 100,000-value mobile limit")
        result = cross_omics_correlation(first, second)
        limitations = [
            "Pairwise Pearson correlations only; no multiple-testing correction or causal inference",
            "Rows must be features and columns must be matched samples in identical order",
            "Small sample counts and outliers can make correlations unstable",
        ]
    elif capability_id == "phylo.jukes_cantor_nj":
        from kinetics.phylo import leaf_names, neighbor_joining_from_alignment, to_newick
        try:
            parameters = json.loads(sequence_text)
            sequences = parameters["sequences"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Provide JSON with a named sequences object") from exc
        if not isinstance(sequences, dict) or not 3 <= len(sequences) <= 20:
            raise ValueError("Neighbour joining requires 3–20 named aligned sequences")
        if any(
            not isinstance(name, str) or not name.strip() or not isinstance(value, str)
            for name, value in sequences.items()
        ):
            raise ValueError("Sequences must be non-empty named entries containing aligned DNA strings")
        if sum(len(value) for value in sequences.values()) > 200_000:
            raise ValueError("Aligned sequences exceed the 200,000-base aggregate mobile limit")
        root = neighbor_joining_from_alignment(sequences, minimum_sites=20)
        result = {"newick": to_newick(root), "leaf_count": len(leaf_names(root))}
        limitations = [
            "Uses the Jukes–Cantor substitution model and caller-supplied alignment",
            "No alignment generation, model selection, bootstrap support or phylogenetic confidence",
        ]
    elif capability_id in {"protein.hmmscan_domain_evidence", "protein.hmmscan_domtblout_evidence"}:
        from kinetics.hmmer import parse_hmmscan_domtblout
        try:
            parameters = json.loads(sequence_text)
            domtblout = parameters["domtblout"]
            hmmer_version = parameters["hmmer_version"]
            profile_pack = parameters["profile_pack"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(
                "Provide JSON with domtblout, hmmer_version and profile_pack metadata"
            ) from exc
        if not isinstance(domtblout, str) or len(domtblout.encode("utf-8")) > 900_000:
            raise ValueError("HMMER domtblout must be text within the 900 KB mobile limit")
        if not isinstance(profile_pack, dict):
            raise ValueError("profile_pack metadata must be a JSON object")
        result = parse_hmmscan_domtblout(
            domtblout.splitlines(),
            hmmer_version=hmmer_version,
            profile_pack=profile_pack,
            max_lines=20_000,
            max_line_bytes=16_384,
            max_domains=10_000,
        )
        limitations = [
            "Parses supplied HMMER domtblout only; no HMMER search is executed",
            "Profile metadata and declared SHA-256 are caller-supplied and are not independently verified",
            "Domain matches are candidate evidence, not confirmed protein function or orthology",
        ]
    elif capability_id == "protein.hmmer_domain_candidate_ranking":
        from kinetics.hmmer_rank import rank_hmmer_domain_candidates
        try:
            parameters = json.loads(sequence_text)
            evidence = parameters["evidence"]
            thresholds = {
                "max_independent_evalue": parameters["max_independent_evalue"],
                "min_profile_coverage": parameters["min_profile_coverage"],
                "min_query_coverage": parameters["min_query_coverage"],
                "min_accuracy": parameters["min_accuracy"],
            }
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Provide parsed HMMER evidence and all four ranking thresholds") from exc
        result = rank_hmmer_domain_candidates(
            evidence,
            **thresholds,
            max_candidates=10_000,
        )
        limitations = [
            "Thresholds are caller-selected and are not calibrated by this module",
            "Ranking does not establish protein family, domain function or orthology",
            "Profile database licensing and provenance require separate approval",
        ]
    elif capability_id == "genome.gff3_annotation_import":
        from kinetics.gff3 import parse_gff3
        if len(sequence_text.encode("utf-8")) > 1_000_000:
            raise ValueError("GFF3 input exceeds the 1 MB mobile limit")
        result = parse_gff3(
            sequence_text.splitlines(),
            max_lines=100_000,
            max_features=50_000,
            max_attribute_bytes=16_384,
            max_total_attribute_bytes=8 * 1024 * 1024,
        )
        limitations = [
            "Structural annotation validation only; no gene function or variant effect is inferred",
            "Feature, parent-graph and coordinate checks are bounded to 50,000 features",
        ]
    elif capability_id == "genome.gff3_transcript_cds_reconstruction":
        from kinetics.gff3 import parse_gff3
        from kinetics.gff3_transcripts import reconstruct_gff3_cds
        try:
            parameters = json.loads(sequence_text)
            gff3_text = parameters["gff3"]
            contigs = parameters["contigs"]
            table_id = parameters.get("table_id", 11)
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Provide JSON with gff3, contigs and optional table_id") from exc
        if not isinstance(gff3_text, str) or not isinstance(contigs, dict):
            raise ValueError("gff3 must be text and contigs must be a name-to-sequence object")
        if len(gff3_text.encode("utf-8")) > 1_000_000:
            raise ValueError("GFF3 annotation exceeds the 1 MB mobile limit")
        if len(contigs) > 1_000 or sum(
            len(value) for value in contigs.values() if isinstance(value, str)
        ) > 1_000_000:
            raise ValueError("Contigs are limited to 1,000 sequences and 1 MB total bases")
        annotation = parse_gff3(
            gff3_text.splitlines(),
            max_lines=100_000,
            max_features=50_000,
            max_attribute_bytes=16_384,
            max_total_attribute_bytes=8 * 1024 * 1024,
        )
        result = reconstruct_gff3_cds(
            annotation,
            contigs,
            table_id=table_id,
            max_transcripts=10_000,
            max_total_cds_bases=1_000_000,
        )
        limitations = [
            "CDS reconstruction follows supplied GFF3 coordinates and phases; annotation quality is not inferred",
            "Only complete canonical CDSs with valid caller-selected table translation can pass CDS validation",
            "No gene function, expression, pathogenicity or clinical interpretation is performed",
        ]
    elif capability_id == "protein.fixed_width_motif_scan":
        import hashlib
        from kinetics.protein_motifs import MotifPack, scan_protein_motif_pack
        try:
            parameters = json.loads(sequence_text)
            query = parameters["query"]
            motifs = parameters["motifs"]
            name = parameters["name"]
            version = parameters["version"]
            license_id = parameters["license"]
            source = parameters["source"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(
                "Provide query, motifs, name, version, license and source in JSON"
            ) from exc
        if not isinstance(query, str) or len(query) > 100_000:
            raise ValueError("Protein query is limited to 100,000 residues")
        if not isinstance(motifs, list) or len(motifs) > 2_000:
            raise ValueError("Caller-supplied motif list is limited to 2,000 entries")
        pack_bytes = json.dumps(
            {"schema_version": 1, "motifs": motifs},
            ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")
        if len(pack_bytes) > 512 * 1024:
            raise ValueError("Motif pack exceeds the 512 KiB mobile limit")
        pack = MotifPack(
            name=name,
            version=version,
            license=license_id,
            source=source,
            content_sha256=hashlib.sha256(pack_bytes).hexdigest(),
        )
        result = scan_protein_motif_pack(
            query,
            pack_bytes,
            motif_pack=pack,
            max_pack_bytes=512 * 1024,
            max_motifs=2_000,
            max_query_residues=100_000,
            max_comparisons=5_000_000,
            max_hits=10_000,
        )
        limitations = [
            "Only caller-supplied motifs are searched; this is not a complete domain database",
            "A matching motif is a sequence-pattern observation, not proof of function or activity",
            "Source and licence metadata are user-supplied and are not independently verified",
        ]
    elif capability_id == "genome.prokaryotic_orf_candidate_scan":
        from kinetics.genome_orf import scan_contig_orf_candidates
        from kinetics.sequence import iter_fasta_records
        records = iter_fasta_records(sequence_text.splitlines())
        result = scan_contig_orf_candidates(
            records,
            table_id=11,
            min_protein_length=30,
            max_contigs=1_000,
            max_total_bases=1_000_000,
            max_total_orfs=500,
            max_candidate_pairs_total=100_000,
        )
        limitations = [
            "Candidate enumeration only; not a gene caller or functional annotation pipeline",
            "Uses explicit NCBI table 11; organism-specific code is not inferred",
            "Genome-wide budget: 1,000 contigs, 1 MB bases, 500 ORFs and 100,000 candidate pairs",
        ]
    elif capability_id == "kinetics.bootstrap_intervals":
        from kinetics.kinetics import bootstrap_michaelis_menten
        try:
            parameters = json.loads(sequence_text)
            substrates = parameters["substrates"]
            rates = parameters["rates"]
            replicates = parameters.get("replicates", 100)
            confidence_level = parameters.get("confidence_level", 0.95)
            seed = parameters.get("seed", 0)
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(
                "Provide JSON with substrate and rate arrays; optional replicates, confidence_level and seed"
            ) from exc
        if not isinstance(substrates, list) or not isinstance(rates, list):
            raise ValueError("substrates and rates must be numeric arrays")
        if len(substrates) != len(rates) or not 3 <= len(rates) <= 100:
            raise ValueError("Provide 3–100 paired substrate/rate observations")
        if not isinstance(replicates, int) or isinstance(replicates, bool) or not 100 <= replicates <= 500:
            raise ValueError("Mobile bootstrap replicates must be between 100 and 500")
        result = bootstrap_michaelis_menten(
            substrates,
            rates,
            replicates=replicates,
            confidence_level=confidence_level,
            seed=seed,
            grid_size=10,
        )
        limitations = [
            "Exploratory paired percentile bootstrap; assumes independent identically distributed observations",
            "Does not address model misspecification, measurement error or study design",
            "A numerical interval is not a clinical or regulatory decision threshold",
        ]
    elif capability_id == "protein.design_brief_validation":
        from kinetics.protein_design import validate_protein_design_brief
        try:
            brief = json.loads(sequence_text)
        except json.JSONDecodeError as exc:
            raise ValueError("Protein design brief must be valid JSON") from exc
        result = validate_protein_design_brief(brief)
        limitations = [
            "Brief validation only; no amino-acid sequence is generated or ranked",
            "Model, weight, dataset licence, safety and independent review gates remain mandatory",
            "A validated brief does not establish biological safety, function or experimental success",
        ]
    elif capability_id in {"structure.geometry_screen_metrics", "structure.pdb_geometry"}:
        from kinetics.structure import parse_pdb
        from kinetics.structure_quality import structure_geometry_metrics
        atoms = parse_pdb(sequence_text, include_hetero=False)
        if len(atoms) > 2_000:
            raise ValueError("Mobile structure geometry is limited to 2,000 parsed atoms")
        result = structure_geometry_metrics(
            atoms,
            max_atoms=2_000,
            max_candidate_pairs=100_000,
            max_reported_clashes=20,
        )
        limitations = [
            "Geometry screen only; no experimental validation or structure-quality certification",
            "Atom pairs in the same residue are excluded because bond topology is unavailable",
            "Unknown elements are excluded rather than assigned estimated radii",
        ]
    elif capability_id == "phylo.nj_site_bootstrap":
        from kinetics.phylo import bootstrap_neighbor_joining_from_alignment, to_newick
        try:
            parameters = json.loads(sequence_text)
            sequences = parameters["sequences"]
            replicates = parameters.get("replicates", 100)
            seed = parameters.get("seed", 0)
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Provide JSON with aligned sequences and optional replicates/seed") from exc
        if not isinstance(sequences, dict) or not 4 <= len(sequences) <= 10:
            raise ValueError("Mobile NJ bootstrap requires 4–10 named aligned sequences")
        if sum(len(value) for value in sequences.values() if isinstance(value, str)) > 50_000:
            raise ValueError("Alignment exceeds the 50,000-base aggregate mobile limit")
        if not isinstance(replicates, int) or isinstance(replicates, bool) or not 100 <= replicates <= 200:
            raise ValueError("Mobile bootstrap replicates must be between 100 and 200")
        result = bootstrap_neighbor_joining_from_alignment(
            sequences, replicates=replicates, seed=seed, minimum_sites=20,
        )
        result["tree"] = to_newick(result["tree"])
        result["leaf_count"] = len(sequences)
        limitations = [
            "Exploratory Jukes–Cantor + neighbour-joining site bootstrap, not maximum-likelihood inference",
            "Input must be a pre-aligned homologous nucleotide alignment",
            "Support denominator excludes failed replicate trees; failure counts are returned",
        ]
    elif capability_id == "structure.exact_sequence_mapping":
        from kinetics.sequence_structure import map_exact_chain_sequence
        from kinetics.structure import parse_pdb
        try:
            parameters = json.loads(sequence_text)
            query = parameters["sequence"]
            chain_id = parameters["chain_id"]
            pdb_text = parameters["pdb"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Provide JSON with sequence, chain_id and pdb") from exc
        if not isinstance(pdb_text, str) or len(pdb_text) > 1_000_000:
            raise ValueError("PDB text exceeds the 1 MB mobile limit")
        atoms = parse_pdb(pdb_text, include_hetero=False)
        result = map_exact_chain_sequence(
            query, atoms, chain_id=chain_id,
            max_query_residues=5_000, max_structure_residues=5_000, max_atoms=20_000,
        )
        limitations = [
            "Exact unique chain-sequence mapping only; insertion-code-aware mapping is unsupported",
            "Coordinate correspondence only; no structural, functional or clinical effect is predicted",
        ]
    elif capability_id == "structure.chain_interface_contacts":
        from kinetics.sequence_structure import chain_interface_contacts
        from kinetics.structure import parse_pdb
        try:
            parameters = json.loads(sequence_text)
            chain_a = parameters["chain_a"]
            chain_b = parameters["chain_b"]
            pdb_text = parameters["pdb"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Provide JSON with chain_a, chain_b and pdb") from exc
        if not isinstance(pdb_text, str) or len(pdb_text) > 1_000_000:
            raise ValueError("PDB text exceeds the 1 MB mobile limit")
        atoms = parse_pdb(pdb_text, include_hetero=False)
        result = chain_interface_contacts(
            atoms, chain_a=chain_a, chain_b=chain_b,
            max_atoms=5_000, max_candidate_pairs=100_000, max_residue_pairs=10_000,
        )
        limitations = [
            "Heavy-atom geometric contact counts only; not an interface energy or affinity estimate",
            "No hydrogen placement, solvent, biological assembly or functional effect is inferred",
        ]
    elif capability_id == "structure.alignment_coordinate_mapping":
        from kinetics.structure import parse_pdb
        from kinetics.structure_alignment import map_chain_sequence_by_alignment
        try:
            parameters = json.loads(sequence_text)
            query = parameters["sequence"]
            chain_id = parameters["chain_id"]
            pdb_text = parameters["pdb"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Provide JSON with sequence, chain_id and pdb") from exc
        if not isinstance(pdb_text, str) or len(pdb_text) > 1_000_000:
            raise ValueError("PDB text exceeds the 1 MB mobile limit")
        atoms = parse_pdb(pdb_text, include_hetero=False)
        result = map_chain_sequence_by_alignment(
            query, atoms, chain_id=chain_id,
            minimum_identity=0.8, minimum_structure_coverage=0.8,
            max_query_residues=2_000, max_structure_residues=2_000,
            max_atoms=10_000, max_alignment_cells=250_000,
        )
        limitations = [
            "Ambiguous optimal placements abstain rather than choosing arbitrarily",
            "Only identical aligned residues are mapped; no structural or functional effect is predicted",
            "Alignment thresholds are fixed at 80% identity and 80% structure coverage",
        ]
    elif capability_id == "structure.variant_coordinate_mapping":
        from kinetics.sequence_structure import map_variant_to_structure
        from kinetics.structure import parse_pdb
        try:
            parameters = json.loads(sequence_text)
            query = parameters["sequence"]
            chain_id = parameters["chain_id"]
            position = parameters["position"]
            reference = parameters["reference"]
            alternate = parameters["alternate"]
            pdb_text = parameters["pdb"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(
                "Provide JSON with sequence, chain_id, position, reference, alternate and pdb"
            ) from exc
        if not isinstance(pdb_text, str) or len(pdb_text) > 1_000_000:
            raise ValueError("PDB text exceeds the 1 MB mobile limit")
        atoms = parse_pdb(pdb_text, include_hetero=False)
        result = map_variant_to_structure(
            query, atoms, chain_id=chain_id,
            variant_position_1based=position,
            reference_amino_acid=reference,
            alternate_amino_acid=alternate,
            max_query_residues=2_000, max_structure_residues=2_000, max_atoms=10_000,
        )
        limitations = [
            "Coordinate correspondence only; no pathogenicity, stability, functional or clinical effect is predicted",
            "Requires a unique exact sequence match to the requested PDB chain",
            "Insertion-code-aware residue mapping is unsupported by the current atom model",
        ]
    elif capability_id in {
        "sequence.exact_reference_search",
        "sequence.local_alignment_reference_search",
        "sequence.local_fasta_exact_search",
        "sequence.local_fasta_alignment_search",
    }:
        import hashlib
        from kinetics.sequence import iter_fasta_records
        from kinetics.sequence_reference import (
            ReferencePack, exact_reference_search, local_alignment_reference_search,
        )
        try:
            parameters = json.loads(sequence_text)
            query = parameters["query"]
            fasta = parameters["reference_fasta"]
            sequence_type = parameters["sequence_type"]
            name = parameters["name"]
            version = parameters["version"]
            license_id = parameters["license"]
            source = parameters["source"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(
                "Provide query, reference_fasta, sequence_type and source/license metadata"
            ) from exc
        if not isinstance(fasta, str) or len(fasta.encode("utf-8")) > 1_000_000:
            raise ValueError("Caller-supplied reference FASTA exceeds the 1 MB mobile limit")
        pack = ReferencePack(
            name=name,
            version=version,
            license=license_id,
            source=source,
            content_sha256=hashlib.sha256(fasta.encode("utf-8")).hexdigest(),
        )
        references = iter_fasta_records(fasta.splitlines())
        if capability_id in {"sequence.exact_reference_search", "sequence.local_fasta_exact_search"}:
            result = exact_reference_search(
                query, references, sequence_type=sequence_type, reference_pack=pack,
                max_records=1_000, max_total_residues=1_000_000, max_query_residues=100_000,
            )
        else:
            result = local_alignment_reference_search(
                query, references, sequence_type=sequence_type, reference_pack=pack,
                max_records=500, max_total_residues=250_000, max_query_residues=1_000,
                max_alignment_cells=250_000, max_total_alignment_cells=2_000_000,
                max_hits=50,
            )
        limitations = [
            "Caller-supplied local FASTA only; the app does not download or independently verify this pack",
            "Exact search reports exact full-length matches only; local alignment is exploratory identity scoring",
            "No E-values, calibrated homology, family/domain membership or functional annotation",
            "A no-hit result is not evidence of novelty",
        ]
    elif capability_id == "genome.orf_candidate_scan":
        from kinetics.orf import find_orf_candidates
        sequence = "".join(sequence_text.split()).upper()
        if len(sequence) > 1_000_000:
            raise ValueError("Genome sequence exceeds the 1,000,000-base mobile limit")
        result = find_orf_candidates(
            sequence,
            table_id=11,
            min_protein_length=30,
            max_orfs=200,
            max_sequence_bases=1_000_000,
            max_open_starts=10_000,
            max_candidate_orf_pairs_total=100_000,
        )
        limitations = [
            "Heuristic complete ORF enumeration only; not a gene prediction or annotation pipeline",
            "Uses explicitly selected NCBI genetic code table 11; no genetic-code inference",
            "Eukaryotic genes with introns are not represented by this ORF scan",
        ]
    elif capability_id == "kinetics.michaelis_menten":
        import math
        from kinetics.kinetics import michaelis_menten
        parts = [part.strip() for part in sequence_text.split(",")]
        if len(parts) != 3:
            raise ValueError("Enter substrate concentration, Vmax and Km as three comma-separated numbers")
        try:
            substrate, vmax, km = (float(part) for part in parts)
        except ValueError as exc:
            raise ValueError("All three Michaelis–Menten inputs must be numeric") from exc
        if not all(math.isfinite(value) for value in (substrate, vmax, km)):
            raise ValueError("Michaelis–Menten inputs must be finite numbers")
        result = {"rate": michaelis_menten(substrate, vmax, km),
                  "substrate": substrate, "vmax": vmax, "km": km}
        limitations = [
            "Deterministic model calculation only; no parameter fitting or uncertainty estimate",
            "Units must be consistent across substrate, Vmax and Km",
        ]
    elif capability_id == "structure.prediction_envelope_validation":
        from kinetics.structure_prediction import validate_prediction_envelope
        try:
            parameters = json.loads(sequence_text)
            sequence = parameters["sequence"]
            envelope = parameters["envelope"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Provide JSON with sequence and prediction envelope") from exc
        if not isinstance(sequence, str) or not isinstance(envelope, dict):
            raise ValueError("Sequence must be text and envelope must be a JSON object")
        result = validate_prediction_envelope(
            sequence,
            envelope,
            max_residues=5_000,
            max_payload_bytes=1_000_000,
        )
        limitations = [
            "Envelope validation only; no structure prediction is performed",
            "Model accuracy, confidence calibration, licensing and node trust are not independently assessed",
            "A structurally valid prediction record is not experimental or clinical validation",
        ]
    elif capability_id in {"phylo.newick", "phylo.newick_export"}:
        from kinetics.phylo import leaf_names, parse_newick, to_newick
        root = parse_newick(sequence_text)
        leaves = leaf_names(root)
        result = {"leaf_count": len(leaves), "leaves": leaves, "normalized_newick": to_newick(root)}
        limitations = [
            "Parses caller-supplied Newick topology and branch lengths only",
            "Does not infer a tree or assess evolutionary model fit",
        ]
    else:
        raise ValueError("This capability is not exposed by the Android basic runner")

    return json.dumps({
        "capability_id": capability_id,
        "result": result,
        "limitations": limitations,
    }, ensure_ascii=False, sort_keys=True)


def analyze_ligand_sdf_graph(source_text: str):
    """Android bridge returning JSON for the bounded offline ligand graph preview."""
    from kinetics.chemistry import analyze_sdf_graph

    return json.dumps(analyze_sdf_graph(source_text), sort_keys=True)



def summarize_vcf_research_qc(text: str) -> str:
    """Android bridge for aggregate-only, bounded VCF syntax/QC; no genotype output."""
    from kinetics.genomics import summarize_vcf_qc

    return json.dumps(summarize_vcf_qc(text), ensure_ascii=False, sort_keys=True)
