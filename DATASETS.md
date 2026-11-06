# Public enzyme-kinetics datasets

Kinetics will use public datasets first. Raw downloads are intentionally kept out of Git; download them locally into `data/public/` and preserve the source files unchanged.

## Primary benchmark: CatPred-DB

- Project: https://github.com/maranasgroup/CatPred-DB
- Dataset card: https://huggingface.co/datasets/RosettaCommons/CatPred-DB
- Published framework: CatPred, Nature Communications (2025), https://doi.org/10.1038/s41467-025-57215-9
- Public processed tables include separate Km and kcat datasets, plus random and sequence-clustered splits.
- The Hugging Face dataset card identifies the dataset as CC BY 4.0. Retain attribution and verify the source repository's current data terms before redistribution.
- Dataset card reports 41,174 Km records and 23,197 kcat records. These are separate parameter-specific datasets; do not assume that a Km record and a kcat record are paired observations.

For the first reproducible baseline, download the processed Km and kcat tables and their published sequence-cluster test splits. Use the published split files only for benchmark comparison; create separate, documented training/validation partitions for model development. Avoid treating random-split scores as evidence of generalization.

Run:

```bash
python scripts/download_public_datasets.py --source catpred-db
python scripts/inspect_public_datasets.py --input-dir data/public/catpred-db
```

The download script saves a manifest containing source URLs, retrieval time, byte counts and SHA-256 hashes. It does not modify, merge or relabel the upstream data.

## Additional sources

### BRENDA

- Download: https://brenda-enzymes.info/download.php
- License: CC BY 4.0; the download page requires explicit acceptance of the license before download.
- Includes curated enzyme functional and kinetic information. Preserve attribution and original references. Review the latest release notes and data schema before parsing.

### SABIO-RK

- Portal and export/API documentation: https://sabiork.h-its.org/ui/export-api
- Curated reaction-level kinetics with experimental context and machine-readable exports.
- Public access and export are available, but check the current SABIO-RK terms for the intended use and redistribution before incorporating records into a redistributed dataset. Do not assume that all third-party database terms are identical.

### Supporting identifiers

- UniProt: https://www.uniprot.org/ — protein sequence and accession mapping.
- PubChem: https://pubchem.ncbi.nlm.nih.gov/ — compound identifiers and structures.
- Rhea: https://www.rhea-db.org/ — curated biochemical reaction identifiers.

These are supporting annotation sources, not substitutes for measured Km or kcat observations.

## Curation policy

1. Preserve every original record, source identifier, publication reference and license/provenance field.
2. Store raw data unchanged; write normalized tables to a separate derived-data directory.
3. Normalize Km to molar (M) and kcat to s^-1 in the research master table. Convert units only when the source unit is explicit and unambiguous.
4. Keep Km and kcat as separate observations unless the source explicitly links them to the same enzyme construct, substrate/reaction and compatible assay conditions.
5. Retain pH, temperature, organism, sequence/accession, mutations, substrate identity, reaction context and assay notes when available.
6. Resolve protein sequences and substrate structures using stable identifiers; log ambiguous or failed mappings rather than guessing.
7. Deduplicate exact repeats, but do not collapse distinct assay conditions or biological constructs into a single value without a documented rule.
8. Exclude Ki, IC50, Vmax and catalytic-efficiency values from Km/kcat target columns. They are different quantities.
9. Make train/validation/test grouping explicit. Report random, protein-cluster, chemical-scaffold and double-cold-start results where the fields permit.
10. Record dataset version, retrieval date, hashes, license, attribution and all filtering decisions.

## Compute-conscious plan

Start with CatPred-DB's published processed CSVs and small sequence-clustered test splits. Inspect their columns and units before writing the canonical adapter. Cache protein embeddings once, use a compact baseline first, and avoid downloading large structure/model artifacts until they are justified.

No dataset is committed to this repository, and no model has been trained from these downloads yet.


## Canonical normalization adapter

The research package provides a target-specific adapter. First inspect the upstream CSV columns using the existing inspection script. Then map the exact source identifier and measurement columns explicitly:

```bash
python -m kinetics_core.catpred --input data/public/catpred-db/km_processed.csv --target km --record-id-column SOURCE_ID --value-column KM_VALUE --unit mM --sequence-column SEQUENCE --ph-column PH --temperature-k-column TEMPERATURE_K \
  --assay-id-column ASSAY_ID --doi-column DOI --output-dir data/processed/catpred-db
```

Replace the example column names and unit with the exact fields observed in the downloaded file. Do not assume the example names exist upstream. Run the adapter separately for kcat with its own source file and explicit unit. The adapter writes accepted observations, rejected rows with reasons, and a JSON manifest containing the source-file hash and mapping configuration. It does not pair Km and kcat records.
