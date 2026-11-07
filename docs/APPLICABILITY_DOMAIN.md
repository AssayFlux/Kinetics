# Applicability-domain diagnostics

> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

`kinetics_core.applicability.ApplicabilityDomain` provides a lightweight
feature-space warning for query observations.

It robustly scales each feature using the median and interquartile range of the
reference training set, then measures each query's distance to its nearest
training reference. The warning threshold is the configured quantile of
leave-one-out nearest-neighbour distances within that reference set.

This is **not** a calibrated probability of correctness, a confidence score,
or proof of chemical/protein novelty. It can be sensitive to representation,
feature dimension, dataset density, and the reference population. Always report
the feature representation, threshold quantile, reference size, and split
design. Fit on training data only; do not use final test observations to set
the threshold.
