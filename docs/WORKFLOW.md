# End-to-end research workflow

This guide describes the intended order of operations. It is documentation for the implemented utilities, not a report that the workflow has been executed or validated.

## 1. Acquire and inspect public data

Download the public CatPred-DB tables using the existing downloader, then inspect the source columns before selecting mappings:

```bash
python scripts/download_public_datasets.py --source catpred-db
python scripts/inspect_public_datasets.py --input-dir data/public/catpred-db
```

Review the current dataset card and upstream repository terms. Keep raw files unchanged.

## 2. Normalize each target independently

The CatPred merge script groups by sequence and substrate, stores the maximum log10 kcat as `log10kcat_max`, and stores the mean log10 Km as `log10km_mean` (a geometric mean on the linear scale). The representative `value` field is not the aggregate target. The upstream merge script clips Km values to [1e-8, 1e4] mM and kcat values to [1e-6, 1e6] s^-1 before aggregation; these bounds are recorded in the curation manifest. These are source-aggregated benchmark statistics, not individual assay measurements. The canonical record stores `measurement_kind=source_aggregated` and the target-specific aggregation method. Underlying replicate measurements are not recoverable from this table.

The documented CatPred-DB schema does not define a native source row identifier, DOI, or assay ID. When no native ID exists in the pinned snapshot, the adapter creates a deterministic file-hash/target/row locator and labels it as an import locator, not an upstream experimental ID. Km uses the aggregate target `log10km_mean`; kcat uses `log10kcat_max`. The adapter exponentiates the aggregate target to recover its linear value in the CatPred convention (Km in mM; kcat in s^-1), then normalizes Km to M. The separate `value` and `log10_value` fields are preserved as published representative-row fields; they are not substituted for the aggregate target. Km tables use `substrate_smiles`; kcat tables use `reactant_smiles`. Celsius `temperature` is converted to kelvin.

```bash
python -m kinetics_core.catpred \
  --input data/public/catpred-db/km/km_train.csv --target km \
  --unit mM --source-version 44409e6 --processing-revision 931583821ff875e873002730fbbdf1047acfde77 \
  --license-id CC-BY-4.0 \
  --output-dir data/processed/catpred-db/km
```

Repeat separately for kcat using its own file, `--unit s^-1`, and the same pinned revision. The upstream CatPred processing code has a kcat conversion caveat: its SABIO-RK `min^-1` conversion multiplies by 60, whereas conversion to `s^-1` ordinarily divides by 60. BRENDA row units are also not retained in the aggregate table. The adapter records this warning in the curation manifest; do not treat CatPred kcat as an independently validated absolute reference until the original source records are audited. Preserve the source train/validation/test partitions; do not concatenate them into one split. The adapter preserves every source column, including accession, taxonomy, sequence provenance, reaction fields, and published cluster labels. Missing DOI, assay IDs, and organism names remain missing.

### Legacy paired-row CSV migration (only when the source really contains paired measurements)

If an existing local dataset stores Km and kcat in the same row, convert it explicitly rather than joining independently sourced target tables. Supply the real source record ID column and the units used by that file. The raw file is left untouched; the command refuses to overwrite it and writes a SHA-256 provenance manifest beside the canonical CSV.

```bash
kinetics-research import-legacy \
  --input data/legacy/paired.csv \
  --output data/processed/legacy/observations.csv \
  --source legacy-dataset \
  --source-record-id-column SOURCE_RECORD_ID \
  --km-unit uM \
  --kcat-unit min^-1 \
  --source-version v1 \
  --license-id CC-BY-4.0
```

Replace the example source, ID column, units, version, and license with verified metadata. The adapter preserves Km and kcat independently and will reject missing source IDs or invalid measurements. It does not create synthetic record IDs. If your source stores Km and kcat in separate tables, continue to normalize them independently in Step 2 instead.


## 2b. Normalize identities and review duplicates

Validate sequence symbols, canonicalize substrate SMILES with RDKit while preserving stereochemistry, and generate deterministic content hashes. These hashes are internal content identities, not UniProt or PubChem accessions. Invalid supplied identities are returned in a row-level rejection table; missing identities remain missing. Keep source accessions and raw source strings.

```bash
kinetics-research normalize-identities \
  --input data/processed/catpred-db/km/km_observations.csv \
  --output-dir data/processed/catpred-db/km/identities
```

Run `kinetics-research audit`. Exact repeats and conflicting duplicate source IDs are annotated and retained; no averaging or silent overwrite occurs. Cross-source identity/value/context matches are separately reported as potential duplicate candidates. Review candidates against assay context before release; similar enzyme/substrate pairs are not automatically duplicate experiments.

## 2c. Create and verify an immutable release

Create a release only after curator review and verification of the exact source version, dataset license, citation, and units. The release combines all rejection audits, retains the acquisition and curation manifests, writes a data card and quality reports, and hashes each artifact. Existing release directories cannot be overwritten.

```bash
kinetics-research release \
  --observations data/processed/catpred-db/km/identities/observations_with_identities.csv \
  --rejected data/processed/catpred-db/km/km_rejected_rows.csv \
  --rejected data/processed/catpred-db/km/identities/identity_rejected_rows.csv \
  --output-dir data/releases/catpred-km-train-v1 \
  --dataset-id catpred-km-train-v1 --dataset-name "CatPred Km train split" \
  --source CatPred-DB --source-version 44409e6 \
  --license-id CC-BY-4.0 \
  --citation "Boorla and Maranas, Nat Commun (2025), doi:10.1038/s41467-025-57215-9" \
  --source-url https://huggingface.co/datasets/RosettaCommons/CatPred-DB \
  --source-manifest data/public/catpred-db/manifest.json \
  --source-manifest data/processed/catpred-db/km/km_curation_manifest.json \
  --source-manifest data/processed/catpred-db/km/identities/identity_manifest.json

kinetics-research verify-release --release-dir data/releases/catpred-km-train-v1
```

The Hugging Face dataset card declares CC-BY-4.0 for the dataset. The journal article's rights statement is CC-BY-NC-ND and is not interchangeable with the dataset card's data license; underlying source databases may carry additional conditions. The release manifest records the license as operator-supplied and requiring manual source-term review. A generated row locator is not a source-level experimental citation.

## 2d. Audit and persist a canonical snapshot

After normalization or the legacy migration above, audit the canonical table and persist the audited rows to SQLite. Assign a new dataset ID to each immutable source snapshot. The persistence command rechecks the canonical schema, positive finite values, duplicate status, and target-specific canonical units before writing.

```bash
kinetics-research audit \
  --input data/processed/legacy/observations.csv \
  --output-dir data/processed/legacy/audit

kinetics-research persist \
  --input data/processed/legacy/audit/observations_audited.csv \
  --database data/kinetics.sqlite3 \
  --dataset-id legacy-release-2026-01 \
  --name "Legacy kinetics release 2026-01" \
  --source legacy-dataset \
  --version 2026-01 \
  --license-id CC-BY-4.0
```

Use the actual verified source version, license, citation, and dataset ID. The database stores canonical numeric values and units in the measurement table, while preserving the original value/unit, source record ID, target, and row metadata in each measurement's JSON metadata. Dataset IDs are immutable: replaying the same file and metadata is idempotent; changing content or metadata requires a new dataset ID. Imports are committed atomically, so a failed batch does not leave a partially imported snapshot. SQLite is for metadata and measurement records, not large embeddings or model tensors.

## 3. Add grouping metadata

Use MMseqs2 to produce sequence-cluster assignments and RDKit to derive chemical scaffold identifiers. Merge these mappings back by stable source record ID. Preserve the tool versions and parameters.

```python
import pandas as pd
from kinetics_core.sequence_clustering import cluster_sequences
from kinetics_core.chemistry import annotate_scaffolds

observations = pd.read_csv("data/processed/catpred-db/km_observations.csv")
mapping_path, cluster_manifest = cluster_sequences(
    observations,
    output_dir="data/processed/sequence_clusters",
    min_sequence_identity=0.4,
    coverage=0.8,
)
mapping = pd.read_csv(mapping_path).rename(
    columns={"cluster_representative_record_id": "protein_cluster_id"}
)
observations = observations.merge(
    mapping, on="source_record_id", how="left", validate="one_to_one"
)
observations = annotate_scaffolds(observations, smiles_column="smiles")
```

The example assumes sequence and source record ID fields exist. If either is missing, do not invent it; resolve the source mapping first.

## 4. Create leakage-aware partitions

For a protein-cluster holdout, use grouped_holdout. For strict protein-and-substrate cold-start evaluation, use double_cold_holdout and retain the returned excluded cross-quadrant rows and manifest.

```python
from kinetics_core.splitting import double_cold_holdout

train, test, excluded, split_manifest = double_cold_holdout(
    observations,
    protein_group_column="protein_cluster_id",
    substrate_group_column="scaffold_id",
    test_fraction=0.2,
    random_state=42,
)
```

Do not use a final held-out benchmark for hyperparameter selection.

## 5. Generate target-specific features

Build Km and kcat archives independently. Pass grouping columns so their labels remain available for grouped cross-validation and leakage checks.

```python
from kinetics_core.features import ObservationFeatureBuilder

builder = ObservationFeatureBuilder(cache_dir="data/cache")
builder.transform_frame(
    train, target="km", output_path="data/features/km_train.npz",
    group_columns=("protein_cluster_id", "scaffold_id"),
)
builder.transform_frame(
    test, target="km", output_path="data/features/km_test.npz",
    group_columns=("protein_cluster_id", "scaffold_id"),
)
```

Use a shared encoder configuration and cache. Repeat for kcat using its own target table and split manifest.

## 6. Fit and report models (final execution stage)

The model-fitting function is implemented but must not be run until the implementation stage is complete and the project owner authorizes the final training/testing stage.

When that stage begins, use grouped CV and explicitly check both protein and scaffold holdout axes:

```python
from kinetics_core.modeling import fit_target_model

fit_target_model(
    "data/features/km_train.npz",
    "data/features/km_test.npz",
    target="km",
    output_dir="artifacts/km",
    group_array="protein_cluster_id",
    holdout_group_arrays=("protein_cluster_id", "scaffold_id"),
)
```

This example is a workflow template, not a recommended final model configuration. Hyperparameter selection, calibration, external validation, and statistical reporting must be designed before execution.

## 7. Inference and uncertainty

Use the target-specific saved model for inference. A conformal quantile may only be supplied after it has been estimated on a separate calibration set and its assumptions documented.

```python
from kinetics_core.prediction import predict_one

result = predict_one(
    sequence="PROTEIN_SEQUENCE",
    smiles="SUBSTRATE_SMILES",
    model_path="artifacts/km/km_model.joblib",
    target="km",
)
```

Predictions are computational estimates, not experimental measurements. Record the model version, source context, and applicability limitations with downstream use.


## Protein and chemical representations (Step 3)

Feature archives are generated from the canonical one-observation-per-row table after identity normalization. The default protein encoder is `facebook/esm2_t6_8M_UR50D`, pinned to model and tokenizer revision `8c576d2aba1b27317e9321c8491d72f00d1b110a`. The encoder uses residue mean pooling and excludes BOS, EOS, and padding tokens. It rejects empty, over-length, or unsupported sequences rather than silently truncating them. The baseline extra (PyTorch and Transformers) is required for new ESM inference.

The chemical vector is a 2,048-bit Morgan fingerprint (radius 2) with chirality included by default. The feature archive also carries a packed molecular graph: atom features include atomic number, degree, charge, hydrogens, aromaticity, CIP stereochemistry, hybridization, isotope and mass; bond features include bond type, conjugation, ring membership and stereo. Bonds are stored as two directed edges, with per-molecule atom/edge offsets. RDKit canonical isomeric SMILES are used for cache identity; the pipeline does not silently strip salts, normalize tautomers, or collapse stereoisomers. The scaffold grouping convention is deliberately different: Bemis-Murcko scaffold IDs ignore stereochemistry so stereoisomers are assigned to the same scaffold group. The current Murcko helper does not offer a stereochemistry-sensitive scaffold mode; use a separately specified chemical grouping method if that is the declared benchmark question.

Feature cache keys include the feature schema, protein model/tokenizer revisions and settings, chemical fingerprint parameters, RDKit/Python/scientific-library versions, normalized sequence, and canonical isomeric SMILES. Cache files use non-pickle NPZ arrays and atomic replacement. Feature generation is batched with a configurable bounded batch size.

Each feature archive has an adjacent `.manifest.json` containing the feature schema and configuration, source/source-version/license identifiers when present, aligned row-identity hashes, archive SHA-256, and runtime metadata. The NPZ archive retains source record IDs, source labels (when supplied), normalized sequences, original and canonical SMILES, target values, packed molecular graph tensors and offsets, and requested grouping arrays. Inference mode and immutable model revisions improve reproducibility; bitwise identity across different hardware or library builds is not promised.

MMseqs2 clustering validates sequence alphabets and unique non-empty record IDs before execution. The resulting manifest records the MMseqs2 version, command and thresholds, input FASTA hash, cluster mapping hash, and a check that every input record was assigned exactly once. The MMseqs2 executable is an external dependency and is not installed by the Python package.

Example feature generation is available through the Python API:

```python
import pandas as pd
from kinetics_core.features import ObservationFeatureBuilder

observations = pd.read_csv("data/curated/observations.csv")
builder = ObservationFeatureBuilder(cache_dir="data/cache/esm2-morgan")
builder.transform_frame(
    observations,
    target="km",
    output_path="data/features/km_features.npz",
    group_columns=("protein_cluster_id", "scaffold_id"),
    batch_size=16,
)
```

Do not generate train/test-specific transforms from combined data if those transforms learn parameters. ESM-2 and Morgan representations are fixed pretrained/algorithmic transforms; any learned dimensionality reduction, feature selection, normalization, or imputation must be fitted on the training partition only. Retain the cluster/scaffold split manifest alongside every feature/model artifact.
