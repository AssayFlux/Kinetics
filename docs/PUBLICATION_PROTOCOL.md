# Publication protocol and evidence checklist

> **Platform context:** This document describes a focused component of Kinetics. The complete cross-disciplinary scope is catalogued in `docs/SCIENCE_DOMAIN_CATALOGUE_100.md`; catalogue inclusion is not implementation or clinical-validation evidence.


> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

This is a planned evidence standard. It does not certify that the current model or repository has passed these requirements.

## Dataset provenance
- Cite each upstream dataset and primary publication.
- Store source URL, version, retrieval timestamp, license, and SHA-256 for downloaded files.
- Preserve raw files unchanged and keep normalized data separate.
- Retain primary record IDs and publication references.
- Document all filters, unit conversions, duplicate handling, and missing metadata.
- Verify reuse and redistribution terms independently for every source.

## Leakage-resistant evaluation
- Identify exact duplicates and conflicting measurements.
- Audit sequence similarity and chemical scaffold overlap.
- Use protein-cluster, scaffold, and double-cold splits where feasible.
- Keep external/temporal test data isolated from model selection.
- Record group labels, split seeds, and exact row identifiers.

## Model evaluation
For each target independently, report:
- number of observations and unique proteins/substrates;
- target range and distribution;
- MAE, RMSE, and R-squared on log scale;
- error in original units and fold-error summaries;
- uncertainty calibration and coverage;
- performance by protein, substrate, organism, and assay subgroups where sample size permits;
- failure modes and applicability-domain limitations.

## Reproducible artifacts
A research run should save the dataset manifest, curation configuration, split manifest, feature encoder and version, model configuration, random seeds, package/environment metadata, fitted artifacts, predictions, metrics, diagnostics, and report-generation inputs.

## Claims discipline
A passing software test is not scientific validation. A random split score is not evidence of cold-start generalization. A low error does not establish mechanistic correctness. Publication claims must be limited to independently verified evidence.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
