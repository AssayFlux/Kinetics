# Modeling and uncertainty design

## Independent targets

Km and kcat are modeled independently. Each target has its own canonical observations, feature archive, fitted model, held-out evaluation, and uncertainty calibration. No implicit row-wise pairing is required.

## Feature representation

The current baseline combines a protein sequence embedding (ESM-2) and a substrate Morgan fingerprint. Feature archives preserve source record IDs and feature-encoder settings. Cache keys include model name, sequence limit, fingerprint radius/size, sequence, and substrate structure.

## Evaluation strategy

Grouped cross-validation should use sequence-cluster or scaffold group identifiers. Row-random cross-validation is retained only as a diagnostic and must be labelled accordingly. Final cold-start evaluation must use held-out protein groups, held-out substrate scaffolds, or a strict double-cold partition. Model selection must not use the final held-out benchmark.

## Metrics

For each target, report:
- log10-scale MAE, RMSE, and R-squared;
- original-unit MAE and RMSE;
- median absolute relative error and median fold error;
- sample counts and target distribution;
- subgroup performance and failure cases.

Do not combine Km and kcat into a single unqualified score.

## Uncertainty

The research layer includes split-conformal interval utilities on the log10 target scale. Calibration data must be separate from training data, and the exchangeability assumptions and split design must be stated. Empirical coverage and interval width must be reported on a held-out evaluation set. Conformal intervals do not repair distribution shift or poor applicability-domain coverage.


## Kinetics-Multi feature-fusion baseline

The first multimodal model is a target-specific MLP over ESM-2 embeddings, Morgan fingerprints, 24 pooled RDKit molecular graph descriptors, and optional raw assay context. Numeric imputation/scaling and categorical encoding are fitted inside each CV fold. This is nonlinear feature fusion, not a message-passing GNN or explicit residue–atom interaction model. Train and evaluate it on the exact same frozen archives as the classical baselines; see [KINETICS_MULTI.md](KINETICS_MULTI.md). Synthetic software tests do not establish predictive validity.
