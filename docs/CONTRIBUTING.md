# Contributing to Kinetics

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

## Astronaut boundary

Kinetics remains standalone. Do not add Astronaut dependencies, services, or code until the project owner explicitly authorizes integration.
