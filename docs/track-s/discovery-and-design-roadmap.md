# Track S — Protein, genome and sequence discovery roadmap

**Status (2026-11-08):** Owner-authorized planning and bounded implementation may proceed in parallel with R1–R10. This document defines the intended S scope; it does not claim the capabilities below are implemented. The existing S1 structure-viewer payload contract remains separate.

## Mission

Turn Kinetics into a research workbench that can investigate unfamiliar DNA/RNA/protein sequences, infer and explain candidate biological meaning, compare structures and families, and support constrained computational protein design. Outputs must remain reproducible, uncertainty-aware research hypotheses. A sequence annotation is not proof of function; a designed sequence is not proof of folding, activity, safety or manufacturability.

## Work packages

### S6 — Sequence intelligence and unknown-sequence triage
- Accept large FASTA/FASTQ and annotated genome/contig inputs with streaming, bounded-memory parsing, provenance and format validation.
- Detect likely coding regions, ORFs, splice-aware candidates where evidence permits, and report alternative hypotheses rather than one forced answer.
- Search local, version-pinned gene/protein reference packs; support remote search only through an explicitly configured, consented node/service.
- Provide similarity, domain, motif, conserved-region and family evidence with database/version, alignment coverage, identity, E-values or calibrated scores where applicable.
- Report unknown/no-hit sequences honestly; distinguish no database match from evidence of novelty.
- Exit evidence: curated positive/negative fixtures, reference concordance, reproducible search packs, memory/runtime bounds, calibrated thresholds and explicit false-positive/false-negative analysis.

### S7 — Genome annotation and gene discovery
- Support prokaryotic and eukaryotic workflows as distinct pipelines; do not present bacterial ORF finding as general eukaryotic gene prediction.
- Add contig QC, repeat/low-complexity handling, gene/transcript candidates, coding potential, functional annotation, pathway context and evidence provenance.
- Track genome assembly, coordinates, strand, transcript/isoform, genetic code, database release and coordinate conventions.
- Provide batch-level coverage, unresolved regions, conflicts and annotation confidence.
- Exit evidence: independently curated genomes across organism classes, gene-boundary and functional-annotation metrics, edge-case fixtures, resource benchmarks and versioned datasets.

### S8 — Translation tables and non-standard genetic-code investigation
- Treat “unknown genetic code” as a distinct scientific problem from merely unknown DNA sequence.
- Support explicit NCBI translation-table selection and per-record genetic-code metadata before attempting inference.
- Candidate-code investigation must evaluate codon usage, conserved homologs, coding-frame consistency, stop-codon depletion/reassignment evidence, organelle/taxonomic context and transcript/protein evidence.
- Never silently infer a non-standard code from one short sequence. Return ranked candidate tables, supporting/contradicting evidence, sample-size limits and an unresolved state.
- Exit evidence: organism-specific positive/negative reference sets, independent confirmation, confusion matrices, calibrated abstention thresholds and regression tests for ambiguous/low-coverage cases.

### S9 — Protein family, domain and structure intelligence
- Protein physicochemical properties, signal peptides/transmembrane candidates, motifs, domains, family classification and evolutionary conservation.
- Connect sequence positions to structure residues and variants only with explicit mapping quality and missing-residue handling.
- Structure quality metrics, interfaces, pockets and residue environments must state model-vs-experimental provenance and applicability limits.
- Exit evidence: version-pinned reference families/structures, independent annotation comparisons, mapping tests and low-end device/node benchmarks.

### S10 — Constrained de novo protein design research
- Define a typed design brief: target function or binding objective, length, fold/family constraints, localization, expression host, disallowed motifs, stability/solubility goals and safety exclusions.
- Separate candidate generation from scoring, filtering and validation. Record model/weights/tokenizer versions, prompts/configuration, seeds, hardware/node, sampling settings and all filters.
- Candidate scoring may include sequence plausibility, predicted structure, confidence, aggregation/solubility heuristics, novelty and target-specific computational metrics; each score must disclose calibration and known blind spots.
- Compare candidates against known sequence/structure databases and flag similarity, patent/licensing and biosafety review needs before any downstream use.
- Require a human-reviewed experimental plan and wet-lab measurements before claiming function. No automated claim of a working protein.
- Exit evidence: model and dataset licenses approved; reproducible generation; independent held-out benchmarks; prospective experimental validation; failure analysis; compute/cost limits; biosafety review and owner approval.

## Shared architecture and quality requirements

1. Keep scientific algorithms in versioned Python/Rust domain modules, not Compose UI. Expose typed request/result schemas through the orchestrator and job/provenance store.
2. Large jobs must be cancellable, resumable where scientifically safe, resource-bounded and explicit about local-vs-node execution.
3. Every result carries input hash, tool and database versions, parameters, timestamps, random seeds, warnings, uncertainty, evidence links and limitations.
4. Unknown, unsupported, low-confidence and conflicting outcomes are first-class results; never fill missing evidence with fabricated annotations.
5. Reference packs require source, version/date, license, integrity hash, update policy and offline install/uninstall lifecycle.
6. Remote inference requires explicit user selection, consent, authenticated TLS, data-minimization, node threat model and a clear record of what left the device.
7. Do not bundle model weights, sequence databases or prediction engines until license, redistribution, privacy, ABI, memory, storage and performance reviews pass.
8. No clinical interpretation, patient workflow, autonomous wet-lab execution or unsafe biological design capability is implied. Applicable biosafety, legal and ethics review is a release gate.

## Execution order and dependencies

- S6 starts with reference-pack contracts, sequence evidence schemas and local small-scale baselines; it can use R4 parsers but must not imply exhaustive database coverage.
- S7 depends on R4 format/coordinate correctness and curated genome fixtures.
- S8 depends on S6/S7 reference metadata and independently curated organism-specific translation-table truth sets.
- S9 depends on R5 structure parsing/viewer provenance and validated residue mapping.
- S10 is planning and model/license feasibility only until compute architecture, model/data licenses, benchmark protocol and biosafety review are approved. Full generation and experimental claims are blocked until those gates pass.
- Track S work proceeds alongside R1–R10 only where dependencies are satisfied. No R or S exit gate is waived.

## Current honest baseline

- Existing source foundations include FASTA/FASTQ parsing, basic sequence operations, protein properties, limited PDB/mmCIF atom-site parsing, structure-analysis primitives and a deterministic structure-viewer payload contract.
- These foundations do **not** constitute production genome annotation, comprehensive unknown-gene discovery, non-standard genetic-code inference, advanced structure prediction or de novo protein design.
- S6–S8 now have bounded implementations and tests, while S9 has a conservative exact residue-mapping primitive. These remain in-progress research work packages until source, tests, reference evidence and exit gates are recorded individually; S10 remains feasibility-only and generation-gated.
