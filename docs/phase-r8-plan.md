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


### R8 count-model source increment

Added an exploratory NB2 log-link GLM for raw integer counts with condition effect, numeric covariates (including caller-encoded batch dummy variables), median-of-ratios size factors when possible, library-size fallback, per-feature method-of-moments dispersion, IRLS fitting, Wald tests and BH q-values. This is not a DESeq2/edgeR replacement: dispersion is not moderated/shrunk, p-values are asymptotic, repeated measures and robust outlier handling are absent, and the model requires independent samples with a full-rank design. Regression-test source was added but not executed. Independent simulation/reference calibration is mandatory before validation status.


### Count-aware model increment

An exploratory NB2 log-link GLM now accepts raw integer counts, size factors, numeric covariates and caller-encoded batch indicators. It uses unmoderated per-feature moment dispersion and asymptotic Wald tests with BH correction. It is not DESeq2/edgeR-equivalent and is not validated for small-sample inference, repeated measures or outlier-heavy designs.
