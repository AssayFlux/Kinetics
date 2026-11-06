# Kinetics-Multi feature-fusion engine

## Scope and scientific boundary

The first Kinetics-Multi model is an independently trained target-specific feature-fusion MLP. It combines:
1. ESM-2 protein sequence embeddings.
2. Morgan chemical fingerprints.
3. Fixed-width molecular graph summaries derived from the per-atom and per-bond tensors.
4. Optional raw assay-context columns, with imputation, scaling and category encoding fitted inside each cross-validation fold.

The graph summary is 24 values per molecule: mean and maximum of the nine atom features, mean of the four directed-bond feature columns, atom count, and undirected bond count. This is a graph-derived descriptor branch; it is **not** a message-passing graph neural network. The MLP learns nonlinear interactions across the concatenated modalities, but does not yet perform residue–atom cross-attention or explicit enzyme–substrate contact modelling.

Km and kcat remain independent prediction tasks. Train one model and archive per target. No rows are paired across targets, and no model is permitted to infer one target from the other.

This implementation is a research software baseline, not a scientifically validated predictor. The absence of a reviewed real dataset release, actual ESM-2 execution evidence, and independent external evaluation remains a hard limitation.

## Training

Use the exact same frozen train, calibration and held-out archives used for the classical baseline comparison:

```bash
kinetics-research fit-multi \
  --train data/features/km_train.npz \
  --test data/features/km_test.npz \
  --calibration-archive data/features/km_calibration.npz \
  --target km \
  --output-dir artifacts/km/kinetics-multi \
  --group-array protein_cluster_id \
  --holdout-group-array protein_cluster_id \
  --holdout-group-array scaffold_id \
  --n-splits 5 \
  --hidden-layers 256,128 \
  --max-iter 500 \
  --git-revision "$(git rev-parse HEAD)"
```

Repeat with the kcat archives and `--target kcat`. Do not select models or tune settings against the final held-out archive. Candidate model selection uses training-only grouped cross-validation when `--group-array` is provided. Without a group array, row-random CV is explicitly diagnostic-only and cannot support cold-start claims.

Each input archive must have its adjacent `.npz.manifest.json` provenance file, with matching archive SHA-256/size, target and row count, and non-empty source, source-version and license declarations. Training/calibration/test partitions must agree on those source/version/license sets. Supply a full 40-character code commit with `--git-revision` (or run in CI with `GITHUB_SHA` set).

The training command validates target identity, representation metadata, graph tensor offsets, row alignment, and all declared train/test group boundaries. If a calibration archive is supplied, it is checked against the training/test group axes and used only for split-conformal residual calibration. The calibration archive must be independent and must not be used for model selection.

## Inference

```bash
kinetics-research predict-multi \
  --model artifacts/km/kinetics-multi/km_kinetics_multi.joblib \
  --features data/features/new_km_candidates.npz \
  --output artifacts/km/kinetics-multi/new_predictions.csv
```

Inference requires a target-labelled feature archive built with the same feature schema, model/tokenizer metadata, chemical fingerprint settings, graph tensor schema and assay-context columns as the trained model. Mismatches are rejected. The output reports predictions in log10 space and canonical units (M for Km; s^-1 for kcat), a nearest-reference applicability-domain warning, plus conformal intervals only when an independent calibration archive was used during training. The applicability warning is a feature-space diagnostic, not a probability of correctness.

**Security:** the model bundle is a joblib artifact, which uses Python pickle serialization. Only load model files produced by a trusted local training run or obtained through a verified trusted artifact channel. Never load untrusted joblib/pickle files.

## Artifacts and provenance

A run writes:
- A target-specific `.joblib` model bundle.
- Held-out predictions CSV.
- Metrics JSON with grouped-CV scores, held-out metrics, convergence warnings, modality list, and limitations.
- A model card.
- An experiment manifest hashing input archives and output artifacts and recording the model configuration and environment.

The model bundle records the target, canonical unit, feature schema, full feature metadata, context schema, base feature dimension, graph-summary schema and optional conformal quantile. Training and inference validate these contracts.

## Validation still required

Automated tests cover graph-summary offsets, malformed bidirectional edge segments, training/held-out group checks, fold-local context preprocessing, artifact creation and inference round-trip. These are software tests on synthetic fixtures. Before any scientific claim:
- Build feature archives from a reviewed, licensed, immutable dataset release.
- Execute the pinned ESM-2 checkpoint and MMseqs2 on that dataset and retain runtime/repeatability evidence.
- Compare classical and Kinetics-Multi models on identical frozen partitions and predeclared metrics.
- Run external source/organism/assay or time-shift tests where supported.
- Evaluate uncertainty coverage, interval width, applicability-domain failure rates and subgroup sample sizes.
- Add residue–atom interaction or message-passing architectures only with clear ablations and leakage-safe validation.

Predictions are computational estimates, not experimental measurements, clinical recommendations, or evidence of mechanism.
