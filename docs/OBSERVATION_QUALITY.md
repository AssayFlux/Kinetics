# Observation quality and duplicate audit

Run `kinetics_core.quality.audit_observations` after source normalization and
before partitioning.

The audit groups only on the exact upstream identity tuple
`(source, source_record_id, target)`. Repeated rows with effectively identical
canonical log10 values are marked `exact_duplicate`; rows with differing values
are marked `conflicting_duplicate`. Every row remains in the annotated table,
and a separate group-level audit is written for review.

Do not automatically average replicates or discard conflicting measurements.
Their interpretation depends on assay identity, publication, enzyme construct,
substrate, pH, temperature, and source-specific record semantics. Similar
sequence/SMILES pairs from different sources are not assumed to be duplicate
experiments. Define and document any replicate aggregation policy before
training, and preserve the raw observations and mapping back to source records.
