# R4 — Genomics and sequence analysis

**Status:** In progress. Source implementation is not scientific validation or device verification.

## Scope
- FASTA/FASTQ parsing, including a streaming FASTA iterator and wrapped FASTQ sequence and quality lines.
- Sequence statistics, reverse complement, transcription, k-mer counting and global pairwise alignment.
- FASTQ quality summaries and explicit-offset terminal quality trimming.
- SAM and VCF text parsing with mandatory-field and scalar validation; SAM validation also checks CIGAR query consumption and permits missing QUAL when SEQ is present.\n- Reference-checked minimal/left normalization for literal biallelic A/C/G/T small variants.
- Future: BAM/CRAM, robust VCF normalization/decomposition, adapter trimming, paired-read handling, indexed access and Rust acceleration.

## Current source
Implemented in `python/kinetics/sequence.py` and `python/kinetics/genomics.py`. Regression-test source is in `tests/test_research_primitives.py` and `tests/test_genomics.py`. The streaming iterator is exported as `kinetics.iter_fasta_records`; the reference normalizer is exported as `kinetics.normalize_small_variant`.

## Limitations
- The FASTA text convenience function materializes its returned records; use the iterator API for large inputs.\n- No BAM/CRAM binary decoder.
- Terminal trimming is not adapter trimming or sliding-window quality trimming.
- VCF parsing does not yet normalize/decompose records automatically. The separate normalizer handles only reference-checked biallelic literal A/C/G/T small variants; symbolic alleles, breakends, multi-allelic decomposition, phasing and variant interpretation remain unsupported.
- Global alignment is not a high-throughput mapper.
- No clinical variant interpretation.

## Exit evidence
Independent fixtures and cross-tool concordance; malformed/large-file tests; deterministic provenance; measured runtime/memory; offline Android integration and device evidence; license review. No capability is marked validated until its evidence record is committed.
