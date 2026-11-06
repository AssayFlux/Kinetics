# KINETICS

<p align="center"><img src="Assets/Brand%20Logo.svg" alt="Kinetics brand logo" width="500"></p>
<p align="center"><strong>A long-horizon biomedical research, molecular discovery and therapeutic-translation platform.</strong></p>

<p align="center">[Vision](VISION.md) · [Master roadmap](ROADMAP.md) · [Architecture](ARCHITECTURE.md) · [Engineering stack](ENGINEERING_STACK.md) · [Clinical translation](CLINICAL_TRANSLATION.md)</p>

## The ambition

Kinetics aims to connect biology across scales—from genes, variants, proteins and molecular interactions to cells, tissues, disease mechanisms, therapeutic candidates, imaging and treatment-response evidence—in one reproducible scientific environment.

The long-term goal is to accelerate discovery and the research that may enable more precise, effective and safer treatment. This is a multi-year ambition, not a claim that a universal treatment engine exists today.

**Current status and safety:** Kinetics is research software. It does not diagnose, prescribe, select treatment or replace clinicians. Computational predictions and simulations are hypotheses, not medical instructions. Any future clinical function requires a defined intended use, independent clinical validation, appropriate governance and regulatory authorization.

## Planned scientific domains

- Genomics, variant interpretation and pharmacogenomics
- Transcriptomics, epigenomics, single-cell and spatial biology
- Proteomics, protein engineering and structural biology
- Enzyme kinetics and biochemical reaction systems
- Cheminformatics, target–ligand research and therapeutic discovery
- Molecular simulation, docking and physical modelling
- Disease mechanisms, pathways and systems biology
- Multi-omics integration and biological individuality
- Biomedical imaging, microscopy, 3D/4D visualization and image analysis
- Pharmacology, PK/PD and treatment-response research
- Experimental study design, evidence synthesis and reproducible reporting

These are roadmap areas, not claims of completed functionality. See [ROADMAP.md](ROADMAP.md) for phased plans and exit criteria.

## Engineering: Python + C++ + Rust

| Technology | Responsibility |
|---|---|
| **Python** | Scientific methods, bioinformatics, data engineering, machine learning, APIs, workflows and research orchestration |
| **C++** | Native 3D rendering, molecular visualization, volume rendering, geometry and performance-critical image analysis |
| **Rust** | Secure systems services, concurrency, workflow runtime, data integrity, resource management and portable components |

Stable, versioned interfaces connect the layers. We will prototype before committing to major frameworks and use established scientific libraries where they reduce risk. The first full product is a desktop research workbench; Android is a later client built on stable APIs and portable components.

## Independent AI: Kinetics Ecosystem

Kinetics Ecosystem is a separate AI project with its own repository and release cycle. It is not Astronaut and does not depend on Astronaut. Kinetics will eventually expose documented, permission-scoped interfaces for evidence retrieval and approved research-tool orchestration. Read-only access is the default; consequential actions require user authorization. AI must distinguish evidence, measurements, predictions and speculation.

## Existing foundation

The current repository is an enzyme-kinetics research foundation. It includes workflows and utilities for protein embeddings, RDKit molecular fingerprints, Km/kcat baselines, data normalization, provenance, assay context, leakage-aware sequence/scaffold splits, uncertainty/applicability analysis, SQLite experiment metadata and reporting. Existing modules and compatibility paths will be reconciled and migrated deliberately; code presence is not proof of execution, benchmarking or scientific validation.

## Development sequence

1. Establish governance, system contracts and the new architecture.
2. Strengthen the core platform, data model, provenance, storage and APIs.
3. Expand scientific domains incrementally, beginning with the existing kinetics foundation.
4. Build the C++ visualization/imaging engine and Rust systems services behind stable interfaces.
5. Develop the desktop research workbench.
6. Connect the separate Kinetics Ecosystem AI through permission-scoped APIs.
7. Assemble end-to-end research workflows.
8. Run comprehensive software verification, training, benchmarking and scientific validation after the implementation programme is assembled.
9. Pursue clinical translation only through independent evidence, ethics, quality systems and regulatory gates.
10. Deliver Android after desktop contracts and shared components are stable.

## Scientific principles

- Preserve raw source data and distinguish it from normalized data and predictions.
- Record provenance, licenses, versions, units, assay conditions and transformations.
- Make uncertainty, applicability limits, missing evidence and population bias visible.
- Use leakage-resistant evaluation and independent external validation.
- Protect sensitive health/genetic data through consent, minimization, access controls, encryption and retention policies.
- Never infer treatment benefit from a model score alone.

## Repository guide

- `Assets/` — brand assets, including [Brand Logo](Assets/Brand%20Logo.svg)
- `src/` — current Python implementation
- `docs/` — scientific methods and implementation notes
- `scripts/` — explicit data acquisition and inspection tools
- `tests/` — software tests
- `data/`, `models/` — local workspaces; do not commit private data or large generated artifacts
- `VISION.md`, `ROADMAP.md`, `ARCHITECTURE.md`, `ENGINEERING_STACK.md` — long-term direction

**Build for scientific truth. Engineer for scale. Translate to healthcare only when evidence earns that responsibility.**
