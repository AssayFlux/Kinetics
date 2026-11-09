# S7 — Contig assembly QC boundary

`python/kinetics/genome_qc.py` consumes sequence records incrementally and reports contig count, total/longest/shortest lengths, N50/L50, canonical-base GC fraction, ambiguous/N-base counts and short-contig count. It enforces record and total-base budgets and rejects duplicate IDs or invalid IUPAC DNA symbols.

This is assembly-summary QC only. It does not establish completeness, contamination, assembly correctness, gene boundaries, eukaryotic splice models, transcript isoforms, function or pathway annotation. Six-frame ORF candidates remain a separate explicitly selected-code heuristic. Prokaryotic and eukaryotic annotation pipelines require independently curated organism-class datasets and separate validation.
