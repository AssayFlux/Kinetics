# Public database retrieval and scientific format rulebook

**Status:** Connector foundation specified; Android direct HTTPS adapters added for NCBI Gene search, NCBI nucleotide/protein FASTA retrieval, UniProtKB search/FASTA retrieval and RCSB PDB mmCIF retrieval. A user-facing search/import workflow, persistent provenance store, offline cache policy, broader database coverage and full parser/engine integration remain open.

## Product contract

Users search and retrieve public reference records from inside Kinetics. They are not asked to manually download a file in a browser. Retrieval is an app-managed network operation, followed by parsing and analysis on-device or by an explicitly selected Kinetics engine. Network access is opt-in by action, HTTPS-only, bounded and source-attributed. The app must continue to explain when a feature requires internet access and preserve the offline workflows.

The current Android adapters accept only public search terms and accessions. Never send imported patient sequences, VCFs, sample identifiers, research-job metadata or other user data to a public database. No telemetry or account service is introduced by this design.

## Database adapter registry

| Source | Search / lookup | Retrieved representation | Initial Kinetics use |
|---|---|---|---|
| NCBI Gene / Entrez | E-utilities Gene search + summary | JSON metadata | Gene discovery and accession navigation |
| NCBI Nucleotide | E-utilities efetch | FASTA | Reference nucleotide sequence |
| NCBI Protein | E-utilities efetch | FASTA | Reference protein sequence |
| UniProtKB | REST search | JSON | Protein discovery and metadata |
| UniProtKB | accession endpoint | FASTA | Protein sequence |
| RCSB PDB | entry ID lookup | mmCIF | Experimental structure coordinates and metadata |

Next adapters, each requiring source-specific tests and provenance: ENA, Ensembl, UCSC, PDBj, AlphaFold DB, PubChem, ChEBI, wwPDB chemical component dictionary, GEO and SRA. A source is not enabled merely because it is listed here; check API terms, rate limits, attribution, data licence, privacy and intended-use fit first.

## Retrieval pipeline

1. Search: validate a public query locally, call the selected source adapter and show source/accession/title/organism.
2. Select: user explicitly chooses a result. Show record type, source and whether it is experimental, curated or predicted where known.
3. Retrieve: HTTPS allow-list, no redirects to arbitrary hosts, connection/read timeouts, response-size cap, strict status checking.
4. Verify: compute SHA-256 on exact received bytes; record UTC retrieval time, endpoint, accession, format and source release/version where supplied.
5. Parse: use a format-specific parser into a typed canonical model; reject malformed/truncated/unsupported records rather than silently repairing them.
6. Process: dispatch only to a registered Kinetics capability with declared input/output schema and resource ceiling.
7. Present: show result, limitations, provenance and whether output is retrieved, transformed, computed or predicted.
8. Cache: cache only after the user chooses the retention policy; keep source payload separate from derived results, expose delete/clear controls and never silently sync.
9. Export: optional SAF export with provenance; not required for normal use.

## Rulebook: canonical models and parser obligations

### Sequence records
Canonical SequenceRecord: stable source ID, accession/version, molecule type (DNA/RNA/protein), alphabet, raw sequence, normalized sequence, header/annotations, organism/taxonomy, source URL, retrieved timestamp, source release, SHA-256 and parser version.

- FASTA: record boundaries, preserve description, validate alphabet and empty records, support multi-record files and bounded line lengths.
- FASTQ: four-line logical records, sequence/quality length equality, explicit Phred+33/Phred+64 selection where ambiguous, reject malformed records.
- GenBank / EMBL: preserve feature coordinates, strand, qualifiers, accession.version and sequence checksum.
- UniProt JSON: retain primary accession, entry name, recommended protein name, gene names, organism, sequence length, sequence version and cross-references.
- GFF3 / BED: coordinate convention is explicit (GFF3 is 1-based inclusive; BED is 0-based half-open); never mix them.
- VCF: retain reference assembly, contig, coordinate, REF/ALT, FILTER and INFO provenance. Do not infer a genotype or phenotype from a reference record.

### Structure records
Canonical StructureRecord: source and accession, structure method, resolution (when reported), experimental/predicted flag, assembly ID, entity/chain IDs, model number, residue identifiers, atom names, elements, Cartesian coordinates in Å, occupancy, B-factor, alternate location, missing residues, ligand/component IDs, biological assembly metadata, source version, retrieval timestamp, payload checksum and parser version.

- PDB legacy format: fixed-column parser; preserve MODEL, TER, chain, insertion code, alternate location, occupancy and B-factor.
- PDBx/mmCIF: dictionary-aware tokenisation and loop parsing; preserve entity/assembly and author-vs-label identifiers; support large loop tables with streaming/bounds.
- SDF/MOL: atom/bond graph, bond order, charge, stereochemistry and conformer coordinates; validate valence and sanitisation separately.
- Never label a predicted structure as experimentally determined. Keep prediction method/model version and confidence metrics distinct from crystallographic resolution.
- A sequence alone is not an experimentally observed 3D structure. Any folding output is a prediction and must be labelled as such.

### Chemistry records
Canonical MoleculeRecord: source ID, canonical/isomeric SMILES where valid, InChI/InChIKey where licensed/tool-supported, atoms, bonds, formal charges, stereochemistry, conformers, units, source/version and checksum. A generated conformer is a computed geometry, not an experimental structure.

## Engine rulebook

Each operation is registered with: stable capability ID; accepted canonical model/schema version; output schema; engine name/version/build hash; parameters; CPU/RAM/time ceilings; cancellation behavior; deterministic/reproducibility policy; validation fixtures; known limitations; and scientific reference comparisons.

Sequence: parse → alphabet/type validation → coordinate-aware feature annotation → QC/alignment/translation/ORF/variant operations. Translation requires an explicit genetic-code table and frame; reverse translation is non-unique and must not be represented as recovery of the original DNA sequence.

Structure: parse coordinates → validate geometry → select model/chain/assembly → render atoms/bonds/cartoon/surface → compute explicitly named measurements. Structure prediction, docking and molecular dynamics are separate capabilities with independent model/force-field, licence, hardware and validation gates.

## Provenance record

Every fetched record should retain: source ID/name, exact request URL (redact query values if sensitive), accession, source release/version or ETag/Last-Modified, UTC retrieved time, MIME type, byte count, SHA-256, parser/version, licence and terms URL, user-selected retention policy, and downstream engine/version/parameters. Do not persist a public record until the user has chosen to save it.

## Implementation boundary

The initial Android client is a transport adapter only. It does not yet expose a complete in-app search screen, persistent cache, mmCIF parser, or automatic dispatch into sequence/structure engines. Those are separate implementation steps and must not be described as complete until the UI and exact-source tests exist. The public-data catalogue remains metadata-only; source-specific reuse terms must be reviewed before bulk mirroring or redistribution.
