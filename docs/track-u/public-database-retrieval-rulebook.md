# Public database retrieval and scientific format rulebook

**Status (2026-11-18):** Android Home search/retrieval is integrated for NCBI Gene, NCBI Nucleotide, NCBI Protein, UniProtKB and RCSB PDB-by-ID. Retrieved FASTA is encrypted locally and passed to the existing on-device FASTA QC workflow; retrieved RCSB mmCIF is encrypted locally and passed to the existing Python parser and offline structure viewer. Exact-head CI, device acceptance, provider rate-limit/retry behavior, complete source licence metadata and broader database coverage remain open.

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

## Android integration status — 2026-11-18

### Implemented in source
- Home exposes NCBI Gene, NCBI Nucleotide, NCBI Protein, UniProtKB and RCSB PDB-by-ID search/retrieval controls.
- Public retrieval uses allow-listed HTTPS hosts, GET-only requests, timeouts, response byte ceilings, strict accession checks and no automatic redirects.
- Sequence records are fetched as FASTA, SHA-256 checked, encrypted in app-private no-backup storage using the existing Android Keystore AES-GCM chunk format, and indexed in a separate SQLite metadata store.
- Retrieved FASTA is passed to the existing embedded Python `kinetics_probe.analyze_fasta` workflow; analysis JSON is retained with the public record. This is the existing bounded research QC workflow, not a new alignment/annotation engine.
- RCSB mmCIF is encrypted and indexed, then passed to the existing `prepare_structure_viewer_import` Python adapter and offline WebView structure viewer. The viewer's 16 MiB parser limit remains authoritative.
- Saved public records are listed on Home and can be deleted. Deletion removes the encrypted payload and its index row.
- Only public search terms and accessions are sent to providers. Patient inputs and private research metadata are not uploaded.

### Not yet complete / not claimed
- NCBI Gene search currently returns metadata; gene-to-transcript/protein ELink resolution is not yet wired into the result action.
- Saved records are listed and deletable, but there is not yet a complete saved-record reopen/reanalyse browser.
- The public record metadata index and analysis JSON are app-private SQLite but are not encrypted at rest; only raw source payloads use the Android Keystore AES-GCM file format.
- Explicit user cancellation, retry/backoff, ETag/source-release capture, licence/terms metadata, cache quota/eviction and background WorkManager retrieval are not yet implemented.
- RCSB search by molecule/protein/organism is not yet implemented; retrieval currently requires a four-character PDB entry ID.
- ENA, Ensembl, PubChem, AlphaFold DB, GEO, SRA and additional providers remain future adapters.
- The structure pipeline reuses the existing bounded coordinate parser/viewer. It does not infer bonds, biological assemblies, secondary structure or confidence.
- Sequence retrieval invokes the existing FASTA QC workflow only. It does not automatically run every sequence capability.

The public-data catalogue remains descriptive metadata. A source is not enabled for bulk mirroring or redistribution until its terms, licence, attribution, rate limits and intended-use requirements are reviewed. CI success does not establish provider availability or scientific validity.
