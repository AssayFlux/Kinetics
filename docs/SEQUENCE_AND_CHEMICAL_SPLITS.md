# Protein and chemical grouping for evaluation

> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

## Protein sequence clusters

The optional sequence-clustering utility wraps MMseqs2. Record the tool version, sequence identity threshold, coverage threshold, coverage mode, command, and mapping output. For a cold-start evaluation, split by cluster IDs rather than individual rows. Threshold choice is a scientific design decision and should be justified and reported.

## Chemical scaffolds

The chemical utility computes RDKit Bemis-Murcko scaffold keys. Acyclic compounds are grouped by canonical isomeric SMILES rather than assigning every acyclic molecule to one empty scaffold. Record RDKit version and standardization rules. Scaffold splits are one view of chemical generalization and do not guarantee absence of all chemical similarity leakage.

## Double-cold evaluation

A strict double-cold test set contains records whose protein cluster and substrate scaffold are both held out. Records in cross-quadrants (held-out protein with seen scaffold, or seen protein with held-out scaffold) are excluded from both train and test for that evaluation. Report the number of excluded records and held-out groups; do not silently fold them into either partition.

## Reproducibility

Persist the exact group mapping and split manifest. Never recompute groups silently between model runs. A change in sequence clustering threshold, RDKit version, chemical standardization, or grouping policy creates a new benchmark definition.
