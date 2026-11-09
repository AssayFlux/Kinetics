# R4 — Genomics and sequence analysis

**Status:** In progress. Source implementation and Android CI build evidence are not independent scientific validation or device verification.

## Scope
- FASTA/FASTQ parsing, including a streaming FASTA iterator and wrapped FASTQ sequence and quality lines.
- Sequence statistics, reverse complement, transcription, k-mer counting and global pairwise alignment.
- FASTQ quality summaries and explicit-offset terminal quality trimming.
- SAM and VCF text parsing with mandatory-field and scalar validation; SAM validation also checks CIGAR query consumption and permits missing QUAL when SEQ is present.
- Reference-checked minimal/left normalization for literal biallelic A/C/G/T small variants. A separate `ReferenceSequence` contract binds synthetic reference sequence bytes to assembly/accession/release/contig, 1-based-closed coordinates, retrieval timestamp and SHA-256; normalized output retains that provenance.
- Bounded lazy BAM core-field decoder for gzip/BGZF-compatible BAM streams; optional host-side pysam/HTSlib adapter for BAM/CRAM with explicit local reference for CRAM.
- Android Explore integration: bounded FASTA QC (record length, GC fraction and ambiguous-symbol count) and bounded FASTQ read-quality summary (explicit Phred+33/Phred+64, read/base counts, mean Phred and Q20/Q30 fractions) through the embedded Python adapter. These are local analysis cards, not yet the full SAF-import → durable job → result/provenance/export workflow.

## Current source
- Domain workflows: `python/kinetics/sequence.py`, `python/kinetics/genomics.py`, `python/kinetics/workflows.py`.
- Android bridge: `android/app/src/main/python/kinetics_probe.py` and `android/app/src/main/java/org/assayflux/kinetics/SequenceQcRunner.kt`.
- Explore UI: `android/app/src/main/java/org/assayflux/kinetics/KineticsUi.kt`.
- Regression tests: `tests/test_research_primitives.py`, `tests/test_genomics.py`, `tests/test_fasta_workflow.py`.
- Exact Android CI evidence for the FASTA/FASTQ cards: [run #2033](https://github.com/AssayFlux/Kinetics/actions/runs/42484179938), source `037befa8e9d22099e250dd22d3c4d772a6457034`.

## Limitations
- FASTQ Phred offset is explicit user input; no encoding inference is performed.
- Android text-card inputs are capped at 1,000,000 characters; the Python workflow also caps reads and aggregate bases. The current UI does not provide a large-file streaming FASTQ import path.
- No adapter detection/trimming, sliding-window trimming, paired-read rescue, variant calling or clinical interpretation is performed by these QC cards.
- FASTA text convenience function materializes its returned records; use the iterator API for large inputs.
- BAM decoder exposes core SAM-like fields only and currently materializes each compressed BAM record block (bounded to 64 MiB); auxiliary tags are skipped. CRAM remains unsupported in Android and requires a reviewed htslib/CRAM engine.
- Terminal trimming is not adapter trimming or sliding-window quality trimming.
- VCF parsing does not yet normalize/decompose records automatically. The separate normalizer handles only reference-checked biallelic literal A/C/G/T small variants; symbolic alleles, breakends, multi-allelic decomposition, phasing and variant interpretation remain unsupported. The build-pinned wrapper currently accepts only explicitly classified synthetic non-patient fixtures; authoritative reference-pack intake, full assembly validation and scientific concordance remain open.
- Global alignment is not a high-throughput mapper.
- No clinical variant interpretation.

## Exit evidence
Independent fixtures and cross-tool concordance; malformed/large-file tests; deterministic provenance; measured runtime/memory; offline Android integration and device evidence; license review. No capability is marked validated until its evidence record is committed.


### Imported FASTA QC execution path — 2026-11-09 (R Step 1)

The Explore FASTA text-card remains a bounded convenience path. A second path now connects an already imported, authenticated FASTA research job to a WorkManager worker and durable analysis-result record. The worker applies 1 MB input bounds, uses the registered `analyze_fasta` Python adapter, persists result JSON with the exact source import digest and tool parameters, and exposes the saved result on the Home/Work job card. FASTQ is not automatically dispatched: explicit Phred offset selection remains mandatory. This slice has not yet passed exact-source CI or device verification.
