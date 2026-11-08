# R8 — Omics and multi-omics

**Status:** In progress. Current statistical routines are exploratory.

## Scope
- CPM and CLR transformations; Pearson and cross-omics correlation; fold changes; diversity metrics and logistic growth.
- Exploratory two-group Welch unequal-variance testing with Student-t p-values and Benjamini–Hochberg q-values for pre-normalized/log-scale features.
- Future: count-aware differential-expression models, covariates, batch effects, paired/repeated-measure designs, robust compositional methods, pathway analysis and multi-omics integration.

## Current source
Implemented in `python/kinetics/omics.py`. Inputs are checked for finite values and invalid dimensions.

## Limitations
- Welch tests require independent biological samples and pre-normalized/log-scale input.
- No negative-binomial count model, design matrix, batch correction or repeated-measures inference.
- CPM/CLR alone do not resolve compositional bias or confounding.
- Multiple-testing correction covers only the feature family supplied to the function.

## Exit evidence
Independent synthetic and public reference datasets; null calibration, power, false-discovery and effect-size checks; covariate/design tests; reference-tool concordance; reproducible provenance and performance benchmarks.
