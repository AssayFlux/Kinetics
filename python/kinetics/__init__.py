"""Kinetics offline research primitives. All capabilities remain unvalidated until evidence is recorded."""

__version__ = "0.1.0"

from .kinetics import fit_michaelis_menten, inhibition_rate, michaelis_menten
from .protein import protein_descriptors, theoretical_pi
from .sequence import (
    SequenceRecord,
    kmer_counts,
    needleman_wunsch,
    parse_fasta,
    parse_fastq,
    reverse_complement,
    sequence_statistics,
    transcribe,
)

__all__ = [
    "SequenceRecord", "fit_michaelis_menten", "inhibition_rate", "kmer_counts",
    "michaelis_menten", "needleman_wunsch", "parse_fasta", "parse_fastq",
    "protein_descriptors", "reverse_complement", "sequence_statistics",
    "theoretical_pi", "transcribe",
]
