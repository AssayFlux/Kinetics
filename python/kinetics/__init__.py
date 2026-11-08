"""Kinetics offline research primitives.

Source implementation does not imply independent scientific validation or clinical use.
"""

__version__ = "0.1.0"

from .catalog import GeneEntry, iter_ncbi_gene_info, validate_gene_catalog
from .chemistry import parse_sdf_record, path_fingerprint, tanimoto
from .genomics import SamRecord, fastq_quality_summary, parse_sam, parse_vcf
from .kinetics import fit_michaelis_menten, inhibition_rate, michaelis_menten
from .molecular import primer_properties, scan_spcas9_ngg
from .omics import (
    clr_transform, cpm, cross_omics_correlation, logistic_growth,
    log2_fold_change, pearson, shannon_diversity, simpson_diversity,
)
from .phylo import Node, leaf_names, parse_newick, patristic_distance, upgma
from .protein import protein_descriptors, theoretical_pi
from .sequence import (
    SequenceRecord, kmer_counts, needleman_wunsch, parse_fasta, parse_fastq,
    reverse_complement, sequence_statistics, transcribe,
)
from .structure import Atom, contact_pairs, parse_pdb, rmsd

__all__ = [
    "Atom", "GeneEntry", "Node", "SamRecord", "SequenceRecord",
    "clr_transform", "contact_pairs", "cpm", "cross_omics_correlation",
    "fastq_quality_summary", "fit_michaelis_menten", "inhibition_rate",
    "iter_ncbi_gene_info", "kmer_counts", "leaf_names", "log2_fold_change",
    "logistic_growth", "michaelis_menten", "needleman_wunsch",
    "parse_fasta", "parse_fastq", "parse_newick", "parse_pdb", "parse_sam",
    "parse_sdf_record", "parse_vcf", "patristic_distance", "path_fingerprint",
    "pearson", "primer_properties", "protein_descriptors", "reverse_complement",
    "rmsd", "scan_spcas9_ngg", "sequence_statistics", "shannon_diversity",
    "simpson_diversity", "tanimoto", "theoretical_pi", "transcribe", "upgma",
    "validate_gene_catalog",
]
