# THE  KINETICS

<p align="center">
  <img src="Assets/Brand%20Logo.svg" alt="Kinetics brand logo" width="350">
</p>

<p align="center"><strong>A long-horizon, cross-disciplinary biomedical science and precision-health research platform.</strong></p>
<p align="center">
  <a href="KINETICS_MISSION.md">Foundational mission</a> ·
  <a href="VISION.md">Vision</a> ·
  <a href="ROADMAP.md">Master roadmap</a> ·
  <a href="ARCHITECTURE.md">Architecture</a> ·
  <a href="ENGINEERING_STACK.md">Engineering stack</a> ·
  <a href="CLINICAL_TRANSLATION.md">Clinical translation</a>
</p>

---

## Explore Kinetics

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🧬 Molecular intelligence</h3>
      Connect genes, variants, transcripts, proteins, structures, reactions and molecular interactions to investigate biological mechanisms.
    </td>
    <td width="50%" valign="top">
      <h3>🧪 Therapeutic discovery</h3>
      Build evidence-driven workflows for enzyme kinetics, chemical research, target–ligand analysis and therapeutic candidate exploration.
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🧠 Multi-omics & systems biology</h3>
      Integrate genomic, transcriptomic, proteomic, metabolomic and cellular evidence to study biological variation and disease.
    </td>
    <td width="50%" valign="top">
      <h3>🖥️ 3D & biomedical imaging</h3>
      Plan a native engine for molecular structures, microscopy, medical volumes, spatial analysis and interactive visualization.
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🤖 Kinetics Ecosystem</h3>
      A separate AI project planned to assist research through cited evidence, permission-scoped tools and reproducible workflows.
    </td>
    <td width="50%" valign="top">
      <h3>📱 Scientific foundation first; desktop and Android clients afterwards</h3>
      Complete the cross-domain scientific foundation and stable APIs before building polished end-user applications for desktop and Android. Validate constrained-device performance throughout foundation development.
    </td>
  </tr>
</table>

## The global mission

Kinetics aims to become a comprehensive, connected biomedical-science and precision-health research platform: linking genetics, proteins and structures, chemistry, multi-omics, systems biology, physiology, disease, pharmacology, clinical evidence, imaging and lifestyle research. Its long-term purpose is to help researchers understand biological individuality, discover and validate better interventions, and support more precise prevention and treatment research.

The ambition, build order, data principles and mandatory decision filter are defined in [KINETICS_MISSION.md](KINETICS_MISSION.md). The system foundation comes first; polished applications follow stable scientific data, analysis, security and API foundations. Small Android devices are a first-class performance constraint. This is a multi-year ambition, not a claim that a universal or clinically validated treatment engine exists today.

> **Research and safety boundary:** Kinetics is research software. It does not diagnose, prescribe, select treatment or replace clinicians. Computational predictions and simulations are hypotheses, not medical instructions. Any future clinical function requires a defined intended use, independent clinical validation, appropriate governance and regulatory authorization.

## Scientific domains

<table>
  <tr>
    <td align="center" width="33%">
      <h3>01 · Genomics</h3>
      Variants · Pharmacogenomics · Regulation
    </td>
    <td align="center" width="33%">
      <h3>02 · Proteins</h3>
      Sequences · Structures · Engineering
    </td>
    <td align="center" width="33%">
      <h3>03 · Kinetics</h3>
      Enzymes · Reactions · Assays
    </td>
  </tr>
  <tr>
    <td align="center">
      <h3>04 · Chemistry</h3>
      Compounds · Docking · ADMET research
    </td>
    <td align="center">
      <h3>05 · Systems biology</h3>
      Pathways · Networks · Multi-omics
    </td>
    <td align="center">
      <h3>06 · Imaging</h3>
      Microscopy · Medical images · 3D/4D
    </td>
  </tr>
</table>

These are planned scientific domains, not claims of completed functionality. See the [master roadmap](ROADMAP.md) for phases, dependencies and exit criteria.

## Engineering architecture

<table>
  <tr>
    <th align="center">🐍 Python</th>
    <th align="center">⚙️ C++</th>
    <th align="center">🦀 Rust</th>
  </tr>
  <tr>
    <td valign="top">Scientific computing, bioinformatics, cheminformatics, machine learning, data engineering, APIs and research workflows.</td>
    <td valign="top">Native 3D rendering, molecular visualization, volume rendering, geometry and performance-critical image processing.</td>
    <td valign="top">Secure systems services, concurrency, workflow runtime, data integrity, resource management and portable components.</td>
  </tr>
</table>

Stable, versioned interfaces will connect these layers. Framework choices will be validated through prototypes, licensing review and performance measurements before they become core dependencies.

## The development journey

<table>
  <tr>
    <td align="center" width="25%">
      <h3>Ⅰ · Foundation</h3>
      Architecture, data model, provenance, storage and APIs
    </td>
    <td align="center" width="25%">
      <h3>Ⅱ · Science</h3>
      Omics, proteins, kinetics, chemistry and simulation
    </td>
    <td align="center" width="25%">
      <h3>Ⅲ · Experience</h3>
      C++ visualization, Rust services and desktop workbench
    </td>
    <td align="center" width="25%">
      <h3>Ⅳ · Translation</h3>
      Validation, clinical research pathways and Android
    </td>
  </tr>
</table>

The roadmap is intentionally multi-year. Architecture and functional modules are assembled first; comprehensive training, testing, benchmarking and scientific evaluation follow the planned implementation stages. Security, correctness and safety checks remain continuous throughout development.

## Independent AI — Kinetics Ecosystem

Kinetics Ecosystem is a separate project with its own repository and release cycle. It is not Astronaut and does not depend on Astronaut. Kinetics will eventually expose documented, permission-scoped interfaces for evidence retrieval and approved research-tool orchestration. Read-only access is the default; consequential actions require user authorization. AI must distinguish evidence, measurements, predictions and speculation.

## Research workbench (optional)

A local-first browser workbench is available for project setup, dataset intake, curation, model workflows, job monitoring, reports and artifact review. Install the optional dependencies with `python -m pip install -e ".[workbench]"` and start it using `kinetics-workbench`. It binds only to `127.0.0.1`; it is not a remote multi-user service. See the [workbench guide](docs/WORKBENCH_GUIDE.md) for setup, supported workflows and limitations.

## Existing foundation

The current repository is an enzyme-kinetics research foundation. It includes workflows and utilities for protein embeddings, RDKit molecular fingerprints, Km/kcat baselines, data normalization, provenance, assay context, leakage-aware sequence/scaffold splits, uncertainty/applicability analysis, SQLite experiment metadata and reporting. Existing modules and compatibility paths will be reconciled and migrated deliberately; code presence is not proof of execution, benchmarking or scientific validation.

## Scientific principles

- Preserve raw source data and distinguish it from normalized data, simulations and predictions.
- Record provenance, licenses, versions, units, assay conditions and transformations.
- Make uncertainty, applicability limits, missing evidence and population bias visible.
- Use leakage-resistant evaluation and independent external validation.
- Protect sensitive health/genetic data through consent, minimization, access controls, encryption and retention policies.
- Never infer treatment benefit from a model score alone.

## Repository guide

| Location | Purpose |
|---|---|
| `Assets/` | Brand assets, including the [Brand Logo](Assets/Brand%20Logo.svg) |
| `src/` | Current Python implementation |
| `docs/` | Scientific methods and implementation notes |
| `scripts/` | Explicit data acquisition and inspection tools |
| `tests/` | Software tests |
| `data/`, `models/` | Local workspaces; do not commit private data or large generated artifacts |
| `VISION.md`, `ROADMAP.md` | Long-term direction and phased programme |
| `ARCHITECTURE.md`, `ENGINEERING_STACK.md` | System design and language responsibilities |
| `CLINICAL_TRANSLATION.md` | Evidence, privacy and clinical safety gates |

---

<p align="center"><strong>Build for scientific truth. Engineer for scale. Translate to healthcare only when evidence earns that responsibility.</strong></p>
