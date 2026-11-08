# R5 — Structural biology

**Status:** In progress. Source implementation is not scientific validation or device verification.

## Scope
- PDB and mmCIF atom coordinate ingestion.
- Geometric contacts and coordinate RMSD, with optional rigid-body superposition.
- Added approximate Shrake–Rupley SASA and distance-only heavy-atom candidate screening for N...O hydrogen bonds, canonical Lys/Arg-Asp/Glu salt bridges and Cys SG disulfides. Future: mmCIF dictionary/assembly/symmetry semantics, residue mapping, secondary structure and structure quality checks.

## Current source
Implemented in `python/kinetics/structure.py`. The mmCIF reader currently supports atom-site loops and label/auth identifier fallbacks; the RMSD superposition uses a Horn-quaternion fit.

## Limitations
- mmCIF parser is not a full dictionary or biological assembly implementation.
- No symmetry expansion, missing-residue reconstruction or chemical component interpretation.
- SASA uses generic element radii and finite Fibonacci sampling; interaction screening does not include hydrogen geometry, protonation, solvent or energy calculations.
- Contact definitions and atom selections require explicit method metadata.

## Exit evidence
Reference structures and independently computed coordinate/contact/RMSD concordance; edge cases for alternate locations, chains, insertion codes and units; large-structure benchmarks; offline visualization and device resource measurements; dependency/license review.
