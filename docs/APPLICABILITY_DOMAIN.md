# Applicability-domain diagnostics

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
