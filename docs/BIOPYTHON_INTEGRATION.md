# BioPython integration plan

> **Platform context:** This document describes a focused component of Kinetics. The complete cross-disciplinary scope is catalogued in `docs/SCIENCE_DOMAIN_CATALOGUE_100.md`; catalogue inclusion is not implementation or clinical-validation evidence.


> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

BioPython is the foundational sequence, annotation, alignment, and structure
I/O/analysis toolkit in Kinetics. The project will use the modules below where
they directly support protein engineering, enzyme analysis, and molecular
research. Optional modules and external executables must be capability-detected;
no workflow should silently claim an analysis ran when its dependency is absent.

## Core modules to integrate

| Module | Kinetics responsibility |
|---|---|
| `Bio.Seq` | DNA/RNA/protein sequence objects, transcription, translation, reverse complement |
| `Bio.SeqRecord` | Annotated sequence records and identifiers |
| `Bio.SeqIO` | FASTA, GenBank, EMBL and other sequence format parsing/writing |
| `Bio.SeqUtils` | Sequence utilities, molecular weight and sequence statistics |
| `Bio.SeqUtils.ProtParam` | Amino-acid composition and protein physicochemical descriptors |
| `Bio.Data` | Genetic code and biological data tables |
| `Bio.Align` | Pairwise/multiple alignment objects and alignment algorithms |
| `Bio.AlignIO` | Multiple sequence alignment format I/O |
| `Bio.Align.substitution_matrices` | BLOSUM/PAM and other substitution matrices |
| `Bio.PDB` | PDB/mmCIF parsing, chains, residues, atoms and structural analysis |
| `Bio.PDB.Polypeptide` | Residue/peptide utilities and amino-acid mappings |
| `Bio.PDB.DSSP` | Secondary-structure and accessibility integration when DSSP is installed |
| `Bio.PDB.SASA` | Solvent-accessible surface area via Shrake-Rupley |
| `Bio.PDB.NeighborSearch` | Spatial neighbor searches and contact analysis |
| `Bio.PDB.Superimposer` | Structural superposition and RMSD workflows |
| `Bio.PDB.MMCIF2Dict` | Low-level mmCIF metadata extraction |
| `Bio.PDB.internal` / internal-coordinate APIs | Internal-coordinate representation and geometry workflows, subject to API/version tests |
| `Bio.SearchIO` | Parsing BLAST, HMMER and other sequence-search outputs |
| `Bio.Blast` | BLAST XML/JSON parsing and record handling |
| `Bio.Entrez` | NCBI Entrez retrieval with rate limits, email/tool identity and cached responses |
| `Bio.motifs` | Sequence motif creation, parsing, scoring and analysis |
| `Bio.SeqFeature` | Feature locations, qualifiers and annotations |
| `Bio.Phylo` | Phylogenetic tree parsing, manipulation and visualization data |
| `Bio.SVDSuperimposer` | Coordinate superposition primitives |
| `Bio.Cluster` | Clustering methods for supported biological feature matrices |
| `Bio.Restriction` | Restriction enzyme analysis for DNA construct workflows, optional |
| `Bio.Graphics` | Optional publication-oriented biological diagrams |

## External tools (not BioPython modules)

Integrate through adapters and version checks: BLAST+ and MMseqs2 for sequence
search/clustering; MAFFT for multiple alignment; HMMER for profile searches;
Foldseek for structure search; DSSP for secondary structure; FreeSASA for
surface area when appropriate; PyMOL for visualization; OpenMM for molecular
dynamics; RDKit for chemical representations and descriptors; and specialist
structure-prediction/docking models as separately licensed and validated tools.

## Engineering rules

- Prefer current `Bio.Align` APIs; do not build new code on deprecated
  `Bio.pairwise2` or deprecated command-line application wrappers.
- Keep network retrieval separate from deterministic local analysis. Cache
  requests and respect NCBI policies.
- Preserve original accessions, source database, versions, citations, licenses,
  checksums, and retrieval timestamps.
- Normalize amino-acid alphabets explicitly; handle ambiguous residues,
  modified residues, missing atoms, alternate conformations, and chain IDs.
- Treat predicted structures and computational scores as predictions, not
  experimental observations.
- Pin/test supported BioPython versions and isolate optional integrations.
- Store compact metadata and searchable records in SQLite; store large sequence
  collections, coordinates, embeddings, and arrays in appropriate files or
  columnar/chunked stores, with hashes and paths registered in SQLite.


## Implemented structural-analysis increment (2026-11-06)

The following capabilities are now implemented in `kinetics_core.biopython_tools` and covered by tests:

- PDB/mmCIF structure summaries with source SHA-256, model, chain, atom and polymer-residue counts.
- Residue solvent-accessible surface area using `Bio.PDB.SASA.ShrakeRupley`.
- Heavy-atom residue contacts using `Bio.PDB.NeighborSearch`, with an explicit distance cutoff.
- C-alpha superposition and RMSD using `Bio.PDB.Superimposer` and caller-supplied author residue-number pairs.
- Protein sequence alignment using `Bio.Align.PairwiseAligner` and BLOSUM62.

The browser-based 3Dmol.js viewer is served from the workbench at `/structure-viewer`. It supports PDB/mmCIF file selection, multiple molecular representations, surface visibility, ligand visibility, residue highlighting, geometric contacts and PNG export. See `docs/STRUCTURE_VIEWER_APK_TESTING.md` for installation and Android USB testing instructions.

This increment does not mean every BioPython module in the table above is integrated. BLAST/Entrez adapters, multiple-sequence alignment workflows, phylogenetics, DSSP, automated residue correspondence, and external-tool orchestration still need separate implementation and validation.


The structural-analysis module `kinetics_core.biopython_tools` additionally provides alignment-derived sequence-to-chain mapping, ligand-to-protein geometric contacts, and conservative N-H...O hydrogen-bond detection. Hydrogen bonds are reported only when explicit hydrogen coordinates exist and satisfy distance/angle criteria; no hydrogens or protonation states are inferred. The local workbench exposes these through its structure-analysis and mapping APIs. See `docs/STRUCTURE_VIEWER_APK_TESTING.md` for the exact scope and limitations.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
