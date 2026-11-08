# Track I — Research boundaries and evidence gates

**Status:** governance and implementation contract. No clinical capability is implied.

## I1 — Molecular descriptors

Descriptor calculations must state the chemical representation, canonicalization policy, protonation/tautomer assumptions, stereochemistry handling, aromaticity model, units and engine/version. Preserve raw input and parsed structure. Invalid valence, unsupported elements, ambiguous stereochemistry and parse warnings must be visible. Cross-engine agreement is not assumed; compare against pinned reference fixtures and report tolerances per descriptor.

## I2 — Docking

Remain gated until a supported engine, exact version, licence, reproducible installation, receptor/ligand preparation protocol, protonation policy, search-space definition, random seeds and independent redocking/cross-docking benchmarks are approved. Scores are not binding affinities or proof of activity.

## I3 — Molecular dynamics

Remain gated until engine and force-field licences, parameter provenance, hardware requirements, deterministic/reproducible protocol, equilibration, replicate strategy and independent validation are documented. A trajectory is not evidence of biological efficacy.

## I4 — ADMET / PK / PD / PBPK

Maintain a source-and-model inventory with applicability domain, training-data provenance, version, units, calibration, uncertainty and external validation. Out-of-domain inputs must trigger abstention. Predictions are research hypotheses and must not be used for treatment or dosing decisions.

## I5 — Variant and virtual-cohort research

Use public, appropriately licensed, non-patient datasets only during preparation. Define ancestry/population limitations, missingness, ascertainment, linkage/phasing assumptions, uncertainty and fairness checks. Do not infer an individual's clinical risk or recommend treatment.

## Hard boundary

P0 remains blocked. No patient data, human-subject recruitment, clinical interpretation, diagnosis, treatment recommendation or clinical mode until the project owner has approved documented legal, ethics, privacy/security and qualified-adviser prerequisites. No wording in this file waives that gate.
