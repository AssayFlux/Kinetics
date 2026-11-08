# R6 — Computational chemistry

**Status:** In progress. Graph descriptors and fingerprints are exploratory only.

## Scope
- Multi-record SDF V2000 parsing and conservative V3000 atom/bond parsing with coordinate, identifier and bond validation.
- Bounded graph descriptors, exact element/bond-order substructure matching and path fingerprints/Tanimoto similarity.
- Future: approved production chemistry engine, stereochemistry, aromaticity, valence/sanitization, implicit hydrogens, protonation/tautomer handling, SMILES, substructure semantics, conformers and property calculations.

## Current source
Implemented in `python/kinetics/chemistry.py`. Resource caps apply to substructure traversal and path fingerprints.

## Limitations
- V3000 support is limited to basic atom/bond graph records; stereochemical and other V3000 attributes are not interpreted. Robust SMILES is not implemented.
- No stereochemical interpretation or aromaticity model.
- Molecular formula and mass are based on explicit parsed atoms; implicit hydrogens are not inferred.
- Fingerprints are custom exploratory graph paths, not ECFP/Morgan fingerprints.

## Exit evidence
Reference SDF/SMILES corpus; concordance against an owner-approved engine; stereochemical and valence edge cases; deterministic descriptor/fingerprint definitions; adversarial resource-limit tests; license and Android ABI review.
