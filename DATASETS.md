# Public enzyme-kinetics datasets

Kinetics will use public datasets first. Raw downloads are intentionally kept out of Git; download them locally into `data/public/` and preserve the source files unchanged. **Access is not necessarily anonymous:** the current CatPred-DB Hugging Face page is gated and requires a signed-in user to agree to share account contact details before file access. Do not bypass the gate or use another person's token.

## Primary benchmark: CatPred-DB

- Project: https://github.com/maranasgroup/CatPred-DB
- Dataset card: https://huggingface.co/datasets/RosettaCommons/CatPred-DB
- Published framework: CatPred, Nature Communications (2025), https://doi.org/10.1038/s41467-025-57215-9
- Public processed tables include separate Km and kcat datasets, plus random and sequence-clustered splits.
- The current Hugging Face dataset card declares CC-BY-4.0 for the dataset files, but its file access is gated. A license label is not a substitute for reviewing the exact pinned revision's access conditions and underlying source terms. The journal article separately carries a CC-BY-NC-ND rights statement; do not confuse the article's license with the dataset card's data license. Inspect the exact pinned dataset revision and underlying BRENDA/SABIO source terms before redistribution.
- Dataset card reports 41,174 Km records and 23,197 kcat records. These are separate parameter-specific datasets; do not assume that a Km record and a kcat record are paired observations.

For the first reproducible baseline, download the processed Km and kcat tables and their published sequence-cluster test splits. Use the published split files only for benchmark comparison; create separate, documented training/validation partitions for model development. Avoid treating random-split scores as evidence of generalization.

Run:

```bash
python scripts/download_public_datasets.py --source catpred-db
python scripts/inspect_public_datasets.py --input-dir data/public/catpred-db
```

The download script saves a manifest containing separate pinned dataset/processing revisions, source URLs, retrieval time, byte counts and SHA-256 hashes. It downloads the random train/validation/test files and the published sequence-cluster test files (kcat 20/40/60/80/99%; Km 40/60/80/99%). It does not modify, merge or relabel upstream data.

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

Start with CatPred-DB's published processed CSVs and sequence-clustered test splits. Inspect the pinned snapshot before running the canonical adapter; its aggregate targets and upstream unit caveats are documented below. Cache protein embeddings once, use a compact baseline first, and avoid downloading large structure/model artifacts until they are justified.

No dataset is committed to this repository, and no model has been trained from these downloads yet. The pinned snapshot must be acquired by an account that has explicitly accepted the current gate; this repository cannot accept those terms or share account details on a researcher's behalf.


## Canonical normalization adapter

The adapter follows the documented CatPred-DB fields where available: `sequence`, `uniprot`, Km `substrate_smiles`, kcat `reactant_smiles`, `value`, `log10_value`, `log10km_mean`, `log10kcat_max`, `temperature`, `ph`, `ec`, `taxonomy_id`, `sequence_source`, and published split/cluster columns. The published table schema does not define a native per-row source record ID, DOI, or assay ID. If no source ID column is documented for the pinned snapshot, the adapter generates a deterministic file-hash/target/row locator and explicitly labels it as an import locator, not an upstream experimental record ID.

The dataset card documents `temperature` in degrees Celsius; the adapter converts it to kelvin. The upstream merge script creates `log10kcat_max` as the maximum log10 kcat across sequence/substrate groups and `log10km_mean` as the mean log10 Km (a geometric mean on the linear scale). The row-level `value` and `log10_value` fields are not the aggregate target; the adapter exponentiates the target-specific aggregate field and preserves the representative row fields separately. The upstream merge script clips Km to [1e-8, 1e4] mM and kcat to [1e-6, 1e6] s^-1 before calculating the aggregate columns. These are source-aggregated benchmark values, not individual assay-level observations. Underlying replicate values and full assay provenance are not reconstructed. The CatPred pipeline convention is Km in mM and kcat in s^-1. The adapter requires that target-specific unit declaration and normalizes Km to M. However, the upstream processing code does not retain BRENDA per-row units, and its SABIO kcat conversion for min^-1 multiplies by 60 (opposite to the standard conversion to s^-1). The curation manifest records this unit-quality warning; CatPred kcat should not be treated as an independently validated absolute reference until source-level unit provenance is audited. Ki is excluded from Km/kcat imports.

Example for the pinned CatPred train split (the unit conventions and upstream caveat are documented in the manifest):

```bash
python -m kinetics_core.catpred \
  --input data/public/catpred-db/km/km_train.csv --target km --unit mM \
  --source-version 44409e6 --processing-revision 931583821ff875e873002730fbbdf1047acfde77 \
  --license-id CC-BY-4.0 \
  --output-dir data/processed/catpred-db/km
```

Run kcat separately using `kcat/kcat_train.csv` and `--unit s^-1`. Preserve the source train/validation/test partitions; do not concatenate them. Treat the kcat absolute scale as provisional until the upstream SABIO unit conversion is audited. The adapter retains source accessions, sequences, substrate SMILES, EC/taxonomy annotations, sequence source, and published split/cluster labels. Missing DOI, assay IDs, or organism names remain missing. Do not treat published split labels as newly generated clusters or merge published test partitions into training.
