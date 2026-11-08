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
