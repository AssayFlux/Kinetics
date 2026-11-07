# Kinetics documentation index

This index maps the repository documentation. The 100-domain catalogue defines the intended platform breadth; individual technical documents remain focused on their named subsystem. Inclusion is not evidence of implementation, verification or clinical validation.

| Document | Purpose |
|---|---|
| README.md | Public overview, scope, build order and safety boundary |
| KINETICS_MISSION.md | Authoritative mission, governance and human-health ambition |
| VISION.md | Long-term product and scientific vision |
| ROADMAP.md | Master programme sequencing and milestones |
| ARCHITECTURE.md | Platform layers, services and contracts |
| ENGINEERING_STACK.md | Technology responsibilities and engineering standards |
| CLINICAL_TRANSLATION.md | Research-to-care evidence and safety gates |
| RESEARCH_BLUEPRINT.md | Initial enzyme-kinetics research and publication plan |
| DATASETS.md | Dataset sources, rights and curation guidance |
| database/seed/README.md | Database seed and bootstrap notes |
| docs/APPLICABILITY_DOMAIN.md | Model applicability-domain methodology |
| docs/ARCHIVE_FIRST_OFFLINE_DATA_ARCHITECTURE.md | Offline archive and selective-access architecture |
| docs/ASSAY_CONTEXT.md | Assay-condition semantics and metadata |
| docs/BIOPYTHON_INTEGRATION.md | Biopython integration boundaries |
| docs/CALIBRATION_AND_CONTEXT_WORKFLOW.md | Calibration and context workflow |
| docs/CONTRIBUTING.md | Contribution and review policy |
| docs/DATABASE_ARCHITECTURE.md | Database schema and persistence design |
| docs/DATA_MODEL.md | Canonical scientific data model |
| docs/DATA_PLATFORM.md | Data platform and ingestion responsibilities |
| docs/EMERGENCY_HUMANITARIAN_RESILIENCE.md | Emergency and humanitarian offline resilience |
| docs/ESM2_REPRESENTATION_CARD.md | ESM-2 representation configuration and provenance |
| docs/IMPLEMENTATION_STATUS.md | Implemented capabilities, evidence and blockers |
| docs/KINETICS_10_STEP_COMPLETION_PROGRAMME.md | Acceptance-based completion programme |
| docs/KINETICS_MULTI.md | Multimodal model design and boundaries |
| docs/MODELING_AND_UNCERTAINTY.md | Model evaluation, calibration and uncertainty |
| docs/MODEL_COMPARISON.md | Model comparison protocol |
| docs/NATIVE_MOLECULAR_ENGINE.md | Native molecular visualization engine |
| docs/OBSERVATION_QUALITY.md | Scientific observation quality rules |
| docs/PARTITION_WORKFLOW.md | Leakage-resistant data partitioning |
| docs/PUBLICATION_PROTOCOL.md | Scientific publication and reproducibility protocol |
| docs/REPORTING_AND_FIGURES.md | Research reporting and figure standards |
| docs/RESEARCHER_OPERATOR_ACCEPTANCE_PROGRAMME.md | Researcher/operator acceptance programme |
| docs/RESEARCH_PAPER_OUTLINE.md | Research paper outline |
| docs/SCIENCE_DOMAIN_CATALOGUE_100.md | Canonical 100-domain scope |
| docs/SCIENTIFIC_ARCHITECTURE.md | Scientific module architecture |
| docs/SEQUENCE_AND_CHEMICAL_SPLITS.md | Protein and chemical split methodology |
| docs/STEP10_RELEASE_READINESS_GATES.md | Release readiness and release gates |
| docs/STEP5_VALIDATION_PROTOCOL.md | Step 5 validation protocol |
| docs/STEP6_IMPLEMENTATION_STATUS.md | Step 6 implementation status |
| docs/STEP7_PRODUCTION_ACCEPTANCE.md | Production acceptance criteria |
| docs/STEP7_RUST_INFRASTRUCTURE.md | Rust infrastructure design and acceptance |
| docs/STEP9_PROTEOMICS_STRUCTURAL_CONTRACT.md | Proteomics and structural data contract |
| docs/STRUCTURE_VIEWER_APK_TESTING.md | Android structure-viewer testing |
| docs/WORKBENCH_GUIDE.md | Research workbench user guide |
| docs/WORKBENCH_UI_ACCEPTANCE.md | Workbench UI acceptance |
| docs/WORKFLOW.md | Research workflow and reproducibility |
| docs/ASSET_PIPELINE.md | Licensed image and pixel-animation pipeline |
| docs/DOCUMENTATION_INDEX.md | Documentation map and status vocabulary |

## Status vocabulary

| Status | Meaning |
|---|---|
| Implemented | Code or documentation exists in the default branch |
| Tested | A named automated or manual test was actually executed and passed |
| Verified | Evidence is recorded and independently reproducible |
| Planned | Documented future work without an implementation claim |
| Blocked | A dependency, dataset, credential, device or independent review is still required |

## Documentation rules

1. Keep each document authoritative for its stated subsystem; avoid duplicating the entire mission in every technical specification.
2. Link subsystem requirements to the 100-domain catalogue where relevant, while preserving domain-specific schemas and semantics.
3. Update implementation status only when code, tests and evidence exist.
4. Record data provenance, licensing, consent, versioning and uncertainty.
5. Separate research support from clinical claims and patient-care use.
6. Keep the foundation-first order: integrate the scientific and platform foundation, build the polished application, then conduct comprehensive acceptance and model training.
