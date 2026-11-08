# R7 — Phylogenetics

**Status:** In progress. Distance-tree methods are exploratory.

## Scope
- Newick parsing, quoted labels, leaf listing and patristic distances.
- UPGMA and neighbour-joining from validated distance matrices.
- Future: sequence alignment integration, substitution models, maximum-likelihood/Bayesian inference, bootstrap support, tree search, interactive offline viewers and safe tree rendering.

## Current source
Implemented in `python/kinetics/phylo.py`. Non-finite/negative input distances and negative inferred neighbour-joining limbs are rejected rather than silently clipped.

## Limitations
- UPGMA assumes an ultrametric clock-like distance structure.
- Neighbour joining is distance-based and does not infer a substitution model.
- No bootstrap support, likelihood inference or tree viewer.

## Exit evidence
Published reference matrices/trees, independent topology and branch-length concordance, tie/degenerate cases, large-tree performance, provenance and offline visualization tests.


### R7 model-based distance increment

Added Jukes–Cantor 1969 nucleotide distance estimation with pairwise deletion of ambiguous/gap columns, minimum comparable-site requirements and explicit saturation rejection. Added a neighbour-joining-from-alignment entry point that constructs a model-corrected distance matrix before tree inference. This is a simple substitution model, not maximum likelihood or Bayesian inference; it has no rate heterogeneity, codon model, bootstrap or model selection. Regression-test source was added but not executed.


### Model-corrected nucleotide distances

Jukes–Cantor 1969 distances with pairwise deletion and saturation rejection now feed neighbour joining from aligned DNA sequences. This is a simple distance correction, not maximum-likelihood/Bayesian inference, rate heterogeneity, model selection or bootstrap support.

### Nonparametric site-bootstrap increment

Added deterministic, seeded alignment-column resampling for Jukes-Cantor + neighbour-joining split support. Reports requested, successful and failed replicate counts and computes support only over successful trees; invalid/saturated/negative-limb replicates are not silently repaired. This remains an exploratory distance-bootstrap utility, not maximum-likelihood/Bayesian inference. Independent reference concordance and execution of the regression tests remain required.
