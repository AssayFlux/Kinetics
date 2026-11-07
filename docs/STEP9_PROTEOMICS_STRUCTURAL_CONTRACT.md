# Step 9 — Proteomics and structural-biology domain contract

> **Platform context:** This document describes a focused component of Kinetics. The complete cross-disciplinary scope is catalogued in `docs/SCIENCE_DOMAIN_CATALOGUE_100.md`; catalogue inclusion is not implementation or clinical-validation evidence.


> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

**Status: versioned sequence/structure records, provenance-checked PDB and mmCIF coordinate parsing, and evidence-linked C-alpha distances are implemented; broader domain acceptance remains open.**

## Why this is the first expansion

Proteomics and structural biology are the lowest-risk first expansion from the existing protein-sequence, ESM-2, molecular-identity and native-scene foundations. This is a sequencing decision, not a claim that these foundations already provide proteomics analysis. Genomics, transcriptomics, imaging, multi-omics and pharmacology remain separate future domains with their own contracts and validation plans.

## Scope of the first increment

The first independently testable domain should ingest and validate protein sequence and structure evidence, then expose provenance-preserving summaries for downstream research. It must not infer clinical significance or treat predicted structures as experimental observations.

In scope, in order:

1. Protein sequence records with explicit source accession, organism/taxonomy, isoform, sequence checksum and source revision.
2. Structure records for PDB and mmCIF, with experimental/predicted status, source identifier, model, chain, residue mapping, coordinate units and source-file checksum.
3. Chain-to-sequence mapping as an explicit artifact. Unmapped, ambiguous, engineered, chimeric and incomplete regions must remain visible; never silently renumber or fill residues.
4. Structure-quality metadata (resolution or prediction confidence only where supplied by the source), missing residues/atoms, alternate conformations, ligands, covalent links and assembly context.
5. Derived features such as secondary structure, solvent accessibility and residue contacts only when a named, versioned tool actually computes them. Store tool/version/parameters and coordinate conventions.
6. A researcher-facing evidence report that distinguishes source facts, computed descriptors, model predictions and hypotheses.

Out of scope for the first increment: de novo structure prediction, mutation pathogenicity, clinical interpretation, molecular dynamics claims, docking claims, and causal/function assertions.

## Versioned record contracts

All records are UTF-8 JSON objects or equivalent typed Python values. Every schema carries an integer major version; incompatible semantic changes require a major version bump. Unknown fields may be preserved as source metadata but must not alter validated semantics.

### Protein sequence record (schema 1)

Required:
- `record_id`: stable internal ID, not a source accession.
- `source`: source name, source record ID, immutable source revision, retrieval timestamp, source URL/citation, license/access statement.
- `sequence`: uppercase amino-acid sequence under an explicitly declared alphabet policy.
- `sequence_sha256`: SHA-256 of the normalized sequence bytes.
- `organism`: taxon ID when known; scientific name and strain/isolate as source-provided values.
- `isoform`: explicit source isoform or null; null must not be interpreted as canonical isoform.
- `normalization`: algorithm/version and every transformation applied.

Reject rather than guess invalid residues, accession collisions, unrecorded sequence edits or missing source identity.

### Structure record (schema 1)

Required:
- `record_id`, `source`, `source_file_sha256`, `format` (`pdb` or `mmcif`), `coordinate_unit` (angstrom), `structure_kind` (`experimental`, `predicted`, or `other`), `model_id`, `chain_id`.
- `sequence_mapping`: mapping algorithm/version, reference sequence record ID and checksum, mapped residue pairs, unmapped reference residues, unmapped structure residues and ambiguity/rejection reasons.
- `quality`: source-reported resolution, confidence fields and missingness only; never synthesize absent quality values.
- `context`: assembly, ligand, alternate-location and covalent-link metadata where present.

The source file remains immutable. Parsed coordinates and normalized representations are derived artifacts with their own hashes. Coordinate transforms must be explicit, invertible where possible, and recorded with source and destination frames.

### Derived feature artifact (schema 1)

Required:
- input record IDs and hashes;
- feature name and schema version;
- software name/version, parameters and reference database versions;
- residue/atom indexing convention and coordinate frame;
- output file hash, units and missing-value semantics;
- warnings, rejected records and coverage statistics.

A feature must never be joined to a sequence/structure by row order alone. Joins use stable record IDs plus explicit residue/atom mappings.

## Evidence and uncertainty rules

- Experimental and predicted structures are separate evidence classes throughout storage, UI, export and reports.
- Resolution, pLDDT or other confidence scores are source-specific and not interchangeable.
- Missing coordinates, unresolved residues, chain ambiguity and construct mutations are first-class warnings.
- Computed descriptors are not experimental measurements.
- Similarity, conservation or contact-derived results are not causal proof.
- Every claim in a report links to the source record or derived artifact that supports it.
- No clinical, diagnostic or treatment recommendation is in scope.

## Adapter interface

An adapter must expose four explicit operations: source capability declaration; acquisition of an immutable source snapshot; parsing/normalization into the versioned records above; and validation that returns accepted records plus machine-readable rejections. Network access is opt-in, host allow-listed and credential-scoped. Adapter code must not scrape undocumented endpoints or bypass source gates.

Adapters must declare supported formats, source/license restrictions, maximum input size, network behavior, identifier namespace, normalization policy and all external tool dependencies. Parsing untrusted structure files must be bounded by file size, atom/residue count, execution time and memory limits.

## Acceptance plan

A first release is eligible for review only after all of the following evidence exists:

- schema fixtures for valid, malformed, ambiguous and incomplete records;
- parser conformance tests for PDB and mmCIF, including alternate locations, multiple models, insertion codes, chain IDs and explicit residue mapping;
- round-trip and hash-integrity tests proving source files are not modified;
- tests proving experimental and predicted evidence never collapse into one class;
- independent reference checks against reviewed structures and sequence mappings;
- license/access inventory for every source and tool;
- deterministic feature generation or documented numerical tolerance on supported environments;
- benchmark report with coverage, failure modes, runtime and memory;
- researcher review of reports and warnings.

Until these gates pass, the implemented PDB/record subset must not be described as a complete proteomics or structural-biology workbench.

## Implemented validation layer (2026-11-06)

The `kinetics_core.proteomics` module now implements versioned protein-sequence, structure, residue-mapping, and derived-feature records with deterministic sequence hashing and explicit provenance. Residue mappings are validated against sequence accession/length and structure ID/chain. This does not yet parse coordinate files, generate mappings, compute features, or validate scientific accuracy; those remain acceptance work.

## Coordinate adapter increment (2026-11-06)

A strict fixed-column PDB adapter now verifies the exact coordinate-file SHA-256 before parsing ATOM/HETATM records. It retains model, chain, author residue number, insertion code, alternate location, occupancy, B-factor, and coordinates. The C-alpha distance utility requires two explicit sequence-to-structure mappings, validates their sequence identity and chain/residue identity, selects alternate locations deterministically, and records coordinate digest, model frame, parameter digest, tool version, and mapping evidence IDs.

The adapter intentionally does not parse mmCIF, infer residue alignments, expand biological assemblies, reconstruct missing residues, or estimate coordinate uncertainty. Experimental/predicted status remains supplied explicitly in the structure record. Tests use a small deterministic PDB fixture; this is parser/contract validation, not biological validation or a real-data benchmark.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
