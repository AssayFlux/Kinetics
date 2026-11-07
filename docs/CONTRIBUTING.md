# Contributing to Kinetics

> **Platform context:** This document describes a focused component of Kinetics. The complete cross-disciplinary scope is catalogued in `docs/SCIENCE_DOMAIN_CATALOGUE_100.md`; catalogue inclusion is not implementation or clinical-validation evidence.


> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

## Scientific contributions

Changes to data curation, units, model equations, feature representations, or evaluation protocols must include:
- the scientific rationale;
- source citations or primary references;
- assumptions and applicability limits;
- provenance and license implications;
- a description of how the change affects reproducibility.

## Data handling

Do not commit raw datasets, trained weights, cached embeddings, or generated result directories. Keep upstream files unchanged. Add source metadata and license/citation notes before introducing a dataset adapter. Never merge Km and kcat records based only on similar identifiers.

## Code organization

Keep source acquisition, schema validation, numerical methods, model fitting, and reporting as separate concerns. Prefer typed interfaces and explicit configuration. Avoid hidden downloads or network access during import. Optional dependencies should be imported lazily and produce actionable errors.

## Research integrity

Do not describe a feature as validated until the final verification stage is complete. Do not use random-split metrics as evidence of cold-start generalization. Preserve rejected-row audits and document data transformations. Never commit credentials, private data, or third-party artifacts without redistribution rights.

## External project boundary

Kinetics owns the scientific data contracts, research workflows and permission-scoped APIs. The separate Kinetics Ecosystem project may integrate through documented, versioned interfaces; do not bundle an assistant runtime into the scientific core or grant it implicit access to private data or consequential operations.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
