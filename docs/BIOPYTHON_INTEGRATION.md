# BioPython integration plan

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
