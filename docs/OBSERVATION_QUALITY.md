# Observation quality and duplicate audit

> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

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


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
