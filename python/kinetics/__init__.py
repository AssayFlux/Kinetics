"""Kinetics offline research primitives.

Source implementation does not imply independent scientific validation or clinical use.
"""

__version__ = "0.1.0"

from .catalog import (
    GeneEntry, iter_ncbi_gene_info, iter_ncbi_gene_info_file, search_gene_catalog, validate_gene_catalog,
)
from .chemistry import (
    graph_descriptors, parse_sdf_record, path_fingerprint, substructure_match, tanimoto,
)
from .genomics import SamRecord, fastq_quality_summary, parse_sam, parse_vcf
from .kinetics import (
    eadie_hofstee, fit_michaelis_menten, hanes_woolf, inhibition_rate,
    lineweaver_burk, michaelis_menten,
)
from .molecular import primer_properties, scan_spcas9_ngg
from .omics import (
    clr_transform, cpm, cross_omics_correlation, logistic_growth,
    log2_fold_change, pearson, shannon_diversity, simpson_diversity,\n    welch_differential_expression,
)
from .phylo import Node, leaf_names, parse_newick, patristic_distance, upgma
from .protein import protein_descriptors, theoretical_pi
from .sequence import (
    SequenceRecord, kmer_counts, needleman_wunsch, parse_fasta, parse_fastq,
    reverse_complement, sequence_statistics, transcribe, trim_fastq_ends,
)
from .structure import Atom, contact_pairs, parse_mmcif, parse_pdb, rmsd

__all__ = [
    "Atom", "GeneEntry", "Node", "SamRecord", "SequenceRecord",
    "clr_transform", "contact_pairs", "cpm", "cross_omics_correlation",
    "eadie_hofstee", "fastq_quality_summary", "fit_michaelis_menten",
    "graph_descriptors", "hanes_woolf", "inhibition_rate",
    "iter_ncbi_gene_info", "iter_ncbi_gene_info_file", "kmer_counts", "leaf_names", "lineweaver_burk",
    "log2_fold_change", "logistic_growth", "michaelis_menten",
    "needleman_wunsch", "parse_fasta", "parse_fastq", "parse_newick",
    "parse_mmcif", "parse_pdb", "parse_sam", "parse_sdf_record", "parse_vcf",
    "patristic_distance", "path_fingerprint", "pearson", "primer_properties",
    "protein_descriptors", "reverse_complement", "rmsd", "scan_spcas9_ngg",
    "sequence_statistics", "shannon_diversity", "trim_fastq_ends", "simpson_diversity",
    "substructure_match", "tanimoto", "theoretical_pi", "transcribe", "upgma",
    "search_gene_catalog", "validate_gene_catalog", "welch_differential_expression",
]
