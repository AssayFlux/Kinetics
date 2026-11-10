# S7 — Genome annotation foundations

## Bounded six-frame ORF candidate scan

The ORF scanner enumerates complete start-to-stop candidates on both strands under an explicitly selected NCBI translation table. It enforces sequence, open-start, output and total candidate-pair ceilings. It remains a heuristic candidate generator, not a gene caller.

## GFF3 annotation import

The GFF3 v3 reader validates nine-column structure, 1-based inclusive coordinates, finite scores, strand/phase syntax, unique IDs, resolvable parent edges, parent containment, acyclic hierarchy, sequence-region bounds and explicit resource budgets. It reports feature-type counts without claiming annotation correctness.

It does not infer organism class, predict genes, interpret embedded FASTA, translate CDS, validate splice biology or assign function. GFF3 import is not a substitute for separate prokaryotic and eukaryotic annotation pipelines. Those predictors and independent organism-diverse benchmarks remain open.
