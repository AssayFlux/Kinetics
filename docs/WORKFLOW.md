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

Use the exact source record ID and measurement column names returned by the inspection step. If all rows use one explicit unit, pass --unit. If units vary by row, pass --unit-column instead.

```bash
python -m kinetics_core.catpred --input data/public/catpred-db/km_processed.csv --target km --record-id-column SOURCE_ID --value-column KM_VALUE --unit mM --sequence-column SEQUENCE --smiles-column SMILES \
  --ph-column PH --temperature-k-column TEMPERATURE_K \
  --assay-id-column ASSAY_ID --doi-column DOI \
  --output-dir data/processed/catpred-db
```

The column names and unit above are examples only; replace them with the actual upstream schema. Optional --ph-column, --temperature-k-column, --assay-id-column, and --doi-column mappings preserve verified assay and publication context. The source record ID column is read as text so leading zeroes remain intact. Repeat for kcat with the kcat source table and its own unit mapping. Do not join the two tables unless the upstream source proves the records represent the same experiment and assay context.

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


## 2b. Audit and persist a canonical snapshot

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
