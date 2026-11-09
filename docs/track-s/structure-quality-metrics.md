# S2 — Structure quality metrics and badge policy

## Current implementation

`python/kinetics/structure_quality.py` reports atom/residue counts, supported/unknown element coverage, bounded nonbonded steric-overlap candidates and severe-overlap counts. A spatial cell index bounds candidate enumeration; callers can cap atom and candidate-pair counts.

The report deliberately returns `quality_badge: not_assessed`. This metric is not MolProbity clashscore and does not provide Ramachandran/rotamer, bond geometry, resolution/R-free or pLDDT/PAE measures. It excludes same-residue pairs because the shared Atom model does not preserve bond topology. Unknown elements are counted and excluded rather than assigned guessed radii.

## Exit evidence still required

- Fixed experimental and predicted structure sets with trusted reference reports.
- Independent clashscore/Ramachandran/rotamer/geometry concordance and prespecified tolerances.
- Model-vs-experimental provenance and resolution/R-free/pLDDT/PAE ingestion.
- Calibrated badge thresholds, false-positive/false-negative review and uncertainty reporting.
- Large-structure memory/runtime benchmarks and low-end Android integration.
- User-visible explanations for every badge and missing metric.

Until those are complete, UI must show metrics as screening observations and use a neutral "not assessed" state rather than good/fair/poor.
