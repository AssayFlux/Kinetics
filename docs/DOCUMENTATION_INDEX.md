# Kinetics documentation index

This index is the entry point for maintained project documentation. The [foundational mission](../KINETICS_MISSION.md) is authoritative for purpose and boundaries; the [master roadmap](../ROADMAP.md) defines long-term programmes; the [10-step completion programme](KINETICS_10_STEP_COMPLETION_PROGRAMME.md) tracks the current engineering sequence; and [implementation status](IMPLEMENTATION_STATUS.md) records what is actually present and what evidence is still missing.

A document describes requirements or design unless it explicitly links implementation and evidence. Catalogue inclusion, a prototype, a fixture test or a CI pass is not automatically scientific validation, production deployment or clinical authorization.

## Project direction and architecture

| Document | Authority / purpose |
|---|---|
| [KINETICS_MISSION.md](../KINETICS_MISSION.md) | Authoritative mission, principles and human-health ambition |
| [VISION.md](../VISION.md) | Long-term scientific and product vision |
| [ROADMAP.md](../ROADMAP.md) | Fifteen long-term programmes, dependencies and universal gates |
| [ARCHITECTURE.md](../ARCHITECTURE.md) | Platform layers, component boundaries and interoperability |
| [ENGINEERING_STACK.md](../ENGINEERING_STACK.md) | Technology responsibilities and engineering standards |
| [CLINICAL_TRANSLATION.md](../CLINICAL_TRANSLATION.md) | Separate research-to-care evidence and safety gates |
| [SCIENCE_DOMAIN_CATALOGUE_100.md](SCIENCE_DOMAIN_CATALOGUE_100.md) | Canonical 100-domain intended-scope register |
| [SCIENTIFIC_ARCHITECTURE.md](SCIENTIFIC_ARCHITECTURE.md) | Scientific modules, evidence and data relationships |
| [APPLICABILITY_DOMAIN.md](APPLICABILITY_DOMAIN.md) | Applicability-domain diagnostics |

## Current planning and status

| Document | Purpose |
|---|---|
| [KINETICS_10_STEP_COMPLETION_PROGRAMME.md](KINETICS_10_STEP_COMPLETION_PROGRAMME.md) | Active engineering completion and acceptance sequence |
| [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) | Current repository status snapshot and blockers |
| [IMPLEMENTATION_HISTORY.md](IMPLEMENTATION_HISTORY.md) | Preserved dated implementation notes; historical, not current authority |
| [STEP10_RELEASE_READINESS_GATES.md](STEP10_RELEASE_READINESS_GATES.md) | Executable release-evidence requirements and release decision policy |
| [STEP7_PRODUCTION_ACCEPTANCE.md](STEP7_PRODUCTION_ACCEPTANCE.md) | Production deployment, isolation, security and recovery acceptance |
| [STEP7_RUST_INFRASTRUCTURE.md](STEP7_RUST_INFRASTRUCTURE.md) | Rust infrastructure design and implementation boundaries |
| [STEP6_IMPLEMENTATION_STATUS.md](STEP6_IMPLEMENTATION_STATUS.md) | Native C++ molecular engine foundation and limitations |
| [STEP9_PROTEOMICS_STRUCTURAL_CONTRACT.md](STEP9_PROTEOMICS_STRUCTURAL_CONTRACT.md) | Protein/structure records, coordinate adapters and acceptance plan |
| [RESEARCHER_OPERATOR_ACCEPTANCE_PROGRAMME.md](RESEARCHER_OPERATOR_ACCEPTANCE_PROGRAMME.md) | Researcher/operator acceptance and usability programme |
| [WORKBENCH_UI_ACCEPTANCE.md](WORKBENCH_UI_ACCEPTANCE.md) | Workbench UI, accessibility and interaction acceptance |

## Scientific data and knowledge

| Document | Purpose |
|---|---|
| [DATASETS.md](../DATASETS.md) | Public enzyme-kinetics dataset sources, rights and curation caveats |
| [DATA_MODEL.md](DATA_MODEL.md) | Canonical kinetic observation semantics |
| [DATA_PLATFORM.md](DATA_PLATFORM.md) | Cross-domain scientific data platform design |
| [DATABASE_ARCHITECTURE.md](DATABASE_ARCHITECTURE.md) | SQLite, artifact storage and migration architecture |
| [KNOWLEDGE_INGESTION.md](KNOWLEDGE_INGESTION.md) | Source acquisition, licensing, indexing and retrieval |
| [KNOWLEDGE_INGESTION_STRUCTURE.md](KNOWLEDGE_INGESTION_STRUCTURE.md) | Knowledge-ingestion subsystem directory/data-flow map |
| [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md) | Repository-wide directory ownership and layout |
| [ARCHIVE_FIRST_OFFLINE_DATA_ARCHITECTURE.md](ARCHIVE_FIRST_OFFLINE_DATA_ARCHITECTURE.md) | Offline archive and selective-access design |
| [EMERGENCY_HUMANITARIAN_RESILIENCE.md](EMERGENCY_HUMANITARIAN_RESILIENCE.md) | Offline resilience, emergency knowledge and safety requirements |
| [OBSERVATION_QUALITY.md](OBSERVATION_QUALITY.md) | Measurement and observation quality rules |
| [ASSAY_CONTEXT.md](ASSAY_CONTEXT.md) | Assay-condition semantics and metadata |
| [PUBLICATION_PROTOCOL.md](PUBLICATION_PROTOCOL.md) | Publication and reproducibility evidence checklist |

## Modeling, validation and research methods

| Document | Purpose |
|---|---|
| [BIOPYTHON_INTEGRATION.md](BIOPYTHON_INTEGRATION.md) | Biopython integration boundaries |
| [ESM2_REPRESENTATION_CARD.md](ESM2_REPRESENTATION_CARD.md) | ESM-2 configuration, intended use and provenance |
| [KINETICS_MULTI.md](KINETICS_MULTI.md) | Feature-fusion model design and limitations |
| [MODELING_AND_UNCERTAINTY.md](MODELING_AND_UNCERTAINTY.md) | Modeling, calibration and uncertainty design |
| [MODEL_COMPARISON.md](MODEL_COMPARISON.md) | Model-family comparison protocol |
| [PARTITION_WORKFLOW.md](PARTITION_WORKFLOW.md) | Leakage-resistant data partitioning |
| [SEQUENCE_AND_CHEMICAL_SPLITS.md](SEQUENCE_AND_CHEMICAL_SPLITS.md) | Protein and chemical split methodology |
| [CALIBRATION_AND_CONTEXT_WORKFLOW.md](CALIBRATION_AND_CONTEXT_WORKFLOW.md) | Assay context, calibration and applicability workflow |
| [STEP5_VALIDATION_PROTOCOL.md](STEP5_VALIDATION_PROTOCOL.md) | Predeclared scientific validation and benchmarking protocol |
| [REPORTING_AND_FIGURES.md](REPORTING_AND_FIGURES.md) | Research reports and figure standards |
| [RESEARCH_PAPER_OUTLINE.md](RESEARCH_PAPER_OUTLINE.md) | Initial enzyme-kinetics manuscript outline |

## Application, operations and contribution

| Document | Purpose |
|---|---|
| [WORKFLOW.md](WORKFLOW.md) | End-to-end enzyme-kinetics research workflow |
| [WORKBENCH_GUIDE.md](WORKBENCH_GUIDE.md) | Local research workbench setup and usage |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Scientific and software contribution rules |
| [ASSET_PIPELINE.md](ASSET_PIPELINE.md) | Brand and static UI asset ownership/policy |
| [README-UI-LAYOUTS.md](../Assets/README-UI-LAYOUTS.md) | Cross-platform HTML/CSS layout measurements |
| [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md) | Directory map and ownership |

## Status vocabulary

| Status | Meaning |
|---|---|
| Present | Code, schema, configuration or documentation exists in the inspected branch |
| CI-verified | A named workflow run passed for a specific commit and scope |
| Real-data validated | A reviewed, licensed real dataset was processed and evaluated reproducibly |
| Independently reviewed | A qualified reviewer examined the stated evidence |
| Production deployed | A live environment exists and operational checks were performed |
| Clinically validated | A defined intended use passed appropriate clinical evidence, governance and authorization |
| Planned | Specified future work without an implementation claim |
| Blocked | A required dataset, credential, device, approval, independent review or other dependency is unavailable |

## Documentation rules

1. Keep one authority for each concern: mission, vision, roadmap, active completion programme, current implementation status and subsystem specification.
2. Technical documents should define their own scope and link to the mission; do not copy the full mission into every specification.
3. Keep subsystem-specific structure maps inside `docs/`; the repository-wide map is `REPOSITORY_STRUCTURE.md`.
4. Use dated historical notes only as an audit trail. The current status register supersedes stale historical statements.
5. Update implementation claims only when code and relevant test/evidence links support them. Explicitly distinguish Python adapters, native C++ components, workbench features and deployment candidates.
6. Preserve domain-specific units, identifiers, source rights, consent restrictions, uncertainty and provenance.
7. Separate research support from diagnosis, prescribing and patient-care claims.
8. Add every maintained document to this index; remove or redirect obsolete documents instead of leaving duplicate authorities.
