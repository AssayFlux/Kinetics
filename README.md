<p align="center">
  <img src="Assets/Brand%20Logo.svg" width="350" alt="Kinetics original brand mark">
</p>
<h1 align="center">KINETICS</h1>
<p align="center"><strong>CONNECTING SCIENCE · ADVANCING HEALTH · PROTECTING HUMANITY</strong><br>
An evidence-centred scientific infrastructure for connected biomedical research.</p>
<p align="center">
  <img src="https://github.com/AssayFlux/Kinetics/actions/workflows/ci.yml/badge.svg" alt="CI">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Rust-infrastructure-000000?logo=rust" alt="Rust infrastructure">
  <img src="https://img.shields.io/badge/C%2B%2B-17-00599C?logo=cplusplus" alt="C++17">
  <img src="https://img.shields.io/badge/Research--first-not%20clinical%20software-6D28D9" alt="Research-first">
</p>
<p align="center">
  Overview · Capabilities · 100 domains · Architecture · Get started · Assets · Project status
</p>

---

## Overview

**Kinetics** is an open, interoperable research platform being developed to connect biological data, biomedical science, computational methods and evidence across molecular, cellular, organismal and population scales.

The long-term system is intended to support data acquisition and curation, reproducible analysis, scientific modelling, structural and molecular workflows, evidence synthesis, and resilient research infrastructure. This repository contains a growing engineering foundation; the full cross-disciplinary vision is a multi-stage programme, not a claim that all 100 domains or clinical capabilities are already implemented.

| Project dimension | Direction |
|---|---|
| Mission | Connect science, advance evidence-centred health research and preserve essential knowledge |
| Scientific scope | 100 research domains spanning biology, medicine, engineering and public health |
| Biological scale | Molecules → genes → proteins → cells → tissues → organs → people → populations |
| Core principles | Provenance, reproducibility, interoperability, uncertainty, privacy and human oversight |
| Build order | Integrate foundations → build the application → comprehensive testing, training and acceptance |
| Device strategy | Desktop and constrained hardware, including low-resource Android, are design considerations |
| Intended use | Research and engineering infrastructure; not an autonomous clinician, diagnostic device or prescribing system |

**Important:** a domain in the catalogue is a statement of intended scope. It does not imply a working adapter, available dataset, validated model, regulatory clearance or clinical utility.

## Capabilities

The table distinguishes code already present from work that still needs real-world evidence.

| Area | Implemented foundation | Remaining acceptance work |
|---|---|---|
| Scientific data | Canonical observations, source metadata, units, identity checks and provenance manifests | Reviewed real datasets, source-level audits and broader adapters |
| Curation and releases | Quality audits, duplicate/conflict reports, immutable dataset releases and SHA-256 verification | Real licensed release and independent source review |
| Protein and chemistry features | Pinned ESM-2 configuration, Morgan fingerprints, molecular graph features and feature archives | Execute pinned models on reviewed data; measure repeatability and resource use |
| Evaluation | Grouped protein/scaffold partitions, baseline comparison, uncertainty utilities and reporting | Real-data benchmarks, external validation and cluster-aware scientific conclusions |
| Multimodal modelling | Feature-fusion MLP using precomputed protein, chemical and assay-context features | Real-data execution and independent scientific evaluation; it is not a message-passing GNN |
| Research workbench | Local-first browser UI, project workspaces, bounded jobs, artifact verification and reports | Researcher/screen-reader acceptance, real-data workflow and install/upgrade testing |
| Molecular structures | C++17 PDB parsing/scene foundation, validated mappings and provenance-checked PDB C-alpha distance utility | mmCIF, automated alignment, independent structure checks and full interactive 3D rendering |
| Rust services | Job, artifact, audit, identity and cloud-integration foundations | Live deployment, scientific task handlers, per-job isolation and recovery/security drills |
| Release governance | Executable release-gate evaluator and documented evidence requirements | Complete evidence manifest, SBOM, signed reviews and human release decision |

See Implementation status (`docs/IMPLEMENTATION_STATUS.md`) for the detailed capability register and limitations.

## Complete 100-domain scientific catalogue

The following tables reproduce the complete domain register, including every domain name and its scientific / healthcare scope. Catalogue inclusion defines intended integration scope; it is not a claim of completed implementation, validated models or clinical readiness.

### 1. Molecular foundations

| # | Domain | Scientific / healthcare scope |
|---:|---|---|
| 1 | Genomics | Genome structure, sequencing, variation and population-scale genomic analysis. |
| 2 | Genetics | Inheritance, gene function, genetic variation and genotype–phenotype relationships. |
| 3 | Transcriptomics | RNA abundance, splicing, regulation and expression profiling. |
| 4 | Proteomics | Protein abundance, modification, interactions and mass-spectrometry profiling. |
| 5 | Structural biology | Macromolecular structures, complexes, folding and cryo-EM. |
| 6 | Cell biology | Cellular organization, signalling, organelles and cell-state imaging. |
| 7 | Molecular biology | DNA/RNA/protein mechanisms, PCR, cloning and molecular assays. |
| 8 | Biochemistry | Biomolecules, reactions, metabolism and biochemical mechanisms. |
| 9 | Epigenetics | DNA methylation, chromatin, histone marks and gene regulation. |
| 10 | Systems biology | Pathways, networks, feedback, multiscale and quantitative models. |

### 2. Omics and living systems

| # | Domain | Scientific / healthcare scope |
|---:|---|---|
| 11 | Metabolomics | Small-molecule profiles, metabolic flux and biochemical phenotyping. |
| 12 | Lipidomics | Lipid species, membranes, signalling and lipid metabolism. |
| 13 | Glycomics | Glycans, glycosylation, glycoproteins and carbohydrate biology. |
| 14 | Metagenomics | Community DNA, microbial diversity and functional profiling. |
| 15 | Single-cell biology | Single-cell sequencing, cell atlases and cellular heterogeneity. |
| 16 | Spatial omics | Spatial transcriptomics, tissue maps and molecular neighbourhoods. |
| 17 | Developmental biology | Embryogenesis, morphogenesis, differentiation and development. |
| 18 | Stem-cell biology | Pluripotency, differentiation, stem-cell niches and cell therapy research. |
| 19 | Microbiome science | Host-associated microbial communities and host–microbe interactions. |
| 20 | Regenerative medicine | Tissue repair, cell replacement and regeneration research. |

### 3. Microbes, immunity and disease

| # | Domain | Scientific / healthcare scope |
|---:|---|---|
| 21 | Microbiology | Microorganisms, microbial physiology and laboratory methods. |
| 22 | Virology | Virus structure, replication, host response and viral evolution. |
| 23 | Immunology | Innate/adaptive immunity, immune cells, antibodies and inflammation. |
| 24 | Bacteriology | Bacterial structure, physiology, pathogenesis and diagnostics. |
| 25 | Mycology | Fungi, fungal pathogenesis, ecology and antifungal research. |
| 26 | Parasitology | Protozoa, helminths, vectors and host–parasite biology. |
| 27 | Vaccinology | Vaccine platforms, immunogenicity, adjuvants and evaluation. |
| 28 | Antimicrobial resistance | Resistance mechanisms, surveillance and antimicrobial stewardship research. |
| 29 | Infectious diseases | Pathogens, transmission, host response and infectious disease research. |
| 30 | Oncology | Cancer biology, tumour microenvironments, biomarkers and therapeutics. |

### 4. Molecular design and therapeutics

| # | Domain | Scientific / healthcare scope |
|---:|---|---|
| 31 | Pharmacology | Drug targets, mechanisms, dose response and pharmacological evidence. |
| 32 | Medicinal chemistry | Molecular design, synthesis, SAR and lead optimization. |
| 33 | Enzymology | Enzyme mechanisms, kinetics, inhibition and catalysis. |
| 34 | Protein engineering | Protein design, directed evolution, stability and function. |
| 35 | Biophysics | Molecular forces, binding, dynamics and quantitative biophysical assays. |
| 36 | Molecular simulation | Molecular dynamics, docking and computational biophysics. |
| 37 | Chemical biology | Chemical probes, biomolecular interactions and chemical tools. |
| 38 | Pharmacogenomics | Gene–drug variation, pharmacogenetic evidence and response research. |
| 39 | Clinical pharmacology | Human drug exposure, response, dose and safety evidence. |
| 40 | Toxicology | Chemical hazards, mechanisms of toxicity and safety assessment. |

### 5. Human biology and specialties

| # | Domain | Scientific / healthcare scope |
|---:|---|---|
| 41 | Anatomy | Human structures, organs, tissues and anatomical relationships. |
| 42 | Physiology | Normal function of organs, tissues and integrated systems. |
| 43 | Pathology | Disease-related structural and functional changes in tissues. |
| 44 | Cardiology | Heart, circulation, cardiovascular mechanisms and imaging. |
| 45 | Neuroscience | Brain, spinal cord, neural circuits and nervous-system function. |
| 46 | Endocrinology | Hormones, endocrine organs, metabolism and regulation. |
| 47 | Pulmonology | Lung structure, respiratory physiology and disease research. |
| 48 | Nephrology | Kidney function, filtration, fluid balance and renal disease. |
| 49 | Gastroenterology | Digestive tract, gut physiology, disorders and endoscopy. |
| 50 | Hepatology | Liver biology, metabolism, fibrosis and liver disease. |

### 6. Clinical specialties and care

| # | Domain | Scientific / healthcare scope |
|---:|---|---|
| 51 | Hematology | Blood cells, coagulation, marrow and blood disorders. |
| 52 | Dermatology | Skin biology, inflammatory disease and dermatopathology. |
| 53 | Rheumatology | Autoimmunity, joints, connective tissue and inflammatory disease. |
| 54 | Orthopedics | Musculoskeletal structure, injury, reconstruction and function. |
| 55 | Obstetrics | Pregnancy, maternal health, fetal development and childbirth research. |
| 56 | Gynecology | Reproductive health, pelvic medicine and gynecologic disease. |
| 57 | Pediatrics | Child health, growth, development and pediatric disease research. |
| 58 | Geriatrics | Ageing, multimorbidity, function and older-adult care research. |
| 59 | Ophthalmology | Eye anatomy, vision science, retinal and ocular disease. |
| 60 | Psychiatry | Mental health, brain–behaviour relationships and psychiatric research. |

### 7. Diagnostics and medical technology

| # | Domain | Scientific / healthcare scope |
|---:|---|---|
| 61 | Radiology | Diagnostic imaging, image interpretation research and radiological methods. |
| 62 | Medical ultrasound | Ultrasound physics, sonography and image-guided assessment. |
| 63 | Nuclear medicine | Radiotracers, molecular imaging and radionuclide therapy research. |
| 64 | Computed tomography | CT acquisition, reconstruction and cross-sectional imaging. |
| 65 | Histology | Microscopic tissue architecture and staining methods. |
| 66 | Cytology | Cell morphology, cytopathology and cellular diagnostics. |
| 67 | Laboratory medicine | Clinical laboratory workflows, assays and analytical quality. |
| 68 | Clinical chemistry | Biochemical testing, biomarkers and analytical methods. |
| 69 | Clinical genetics | Genetic evaluation, variant interpretation and inherited disease research. |
| 70 | Medical imaging engineering | Image reconstruction, sensors, acquisition and computational imaging. |

### 8. Treatment, rehabilitation and prevention

| # | Domain | Scientific / healthcare scope |
|---:|---|---|
| 71 | Surgery | Operative science, surgical systems and perioperative research. |
| 72 | Anesthesiology | Anaesthesia, perioperative physiology and pain mechanisms. |
| 73 | Emergency medicine | Time-critical assessment systems, trauma and acute-care research. |
| 74 | Critical care | Organ support, intensive care physiology and critical illness. |
| 75 | Radiation oncology | Radiation biology, planning systems and cancer treatment research. |
| 76 | Pharmaceutics | Dosage forms, formulation science and pharmaceutical delivery. |
| 77 | Drug delivery | Targeted delivery, release systems and therapeutic transport. |
| 78 | Rehabilitation medicine | Recovery, function, assistive therapy and outcome measurement. |
| 79 | Palliative care | Symptom science, supportive care and quality-of-life research. |
| 80 | Preventive medicine | Risk reduction, screening evidence and prevention strategies. |

### 9. Population, engineering and future health

| # | Domain | Scientific / healthcare scope |
|---:|---|---|
| 81 | Public health | Population health, prevention systems and health protection. |
| 82 | Epidemiology | Disease frequency, determinants, surveillance and causal inference. |
| 83 | Global health | Health systems, cross-border health challenges and equity. |
| 84 | Clinical research | Human-subject research design, monitoring and evidence generation. |
| 85 | Clinical trials | Trial design, endpoints, randomization and safety monitoring. |
| 86 | Evidence synthesis | Systematic reviews, meta-analysis and evidence grading. |
| 87 | Health economics | Cost, value, resource allocation and health technology assessment. |
| 88 | Bioethics | Research ethics, consent, governance and responsible innovation. |
| 89 | Biomedical engineering | Engineering methods for biology, medicine and healthcare. |
| 90 | Bioinformatics | Computational analysis of biological data and scientific workflows. |

### 10. Frontier and human resilience

| # | Domain | Scientific / healthcare scope |
|---:|---|---|
| 91 | Medical robotics | Surgical, rehabilitation and assistive robotics research. |
| 92 | Prosthetics | Prosthetic limbs, orthotics, interfaces and human-device integration. |
| 93 | Biomaterials | Biocompatible materials, implants and tissue interfaces. |
| 94 | Bioinstrumentation | Sensors, biosignal acquisition and biomedical measurement devices. |
| 95 | Medical devices | Medical device design, verification, usability and safety engineering. |
| 96 | Nanomedicine | Nanoscale diagnostics, delivery and therapeutic platforms. |
| 97 | Health informatics | Health data standards, interoperability and clinical information systems. |
| 98 | Digital health | Remote monitoring, telehealth and connected-care technologies. |
| 99 | Artificial intelligence in medicine | Validated AI methods for medical research and decision support. |
| 100 | Humanitarian and disaster health | Health resilience in disasters, conflict, displacement and infrastructure failure. |

Canonical source document: `docs/SCIENCE_DOMAIN_CATALOGUE_100.md`.

## Architecture

Kinetics is designed as a set of explicit layers rather than one monolithic model or database.

| Layer | Main responsibility | Key safeguards |
|---|---|---|
| Source registry | Track datasets, publications, standards and APIs | Licensing, access terms, versioning and attribution |
| Acquisition | Import permitted scientific records | Checksums, resumability and immutable raw inputs |
| Storage | Store metadata, measurements and scientific artifacts | Schema versions, integrity checks, safe formats and backups |
| Domain contracts | Represent genes, proteins, compounds, assays, structures, samples and evidence | Typed units, identifiers, context and explicit mappings |
| Analysis runtime | Run curation, feature generation, partitioning and models | Reproducible configuration, bounded resources and cancellation |
| Evidence layer | Link results to sources, methods and study context | Uncertainty, limitations, provenance and abstention |
| Service layer | Provide jobs, artifacts, identity and audit interfaces | Least privilege, tenant boundaries and integrity |
| Applications | Researcher workbench and future domain interfaces | Accessibility, usability and intended-use boundaries |
| Validation | Establish scientific and operational trust | Reference data, external replication, security and recovery tests |

### Technology map

| Technology | Role in the repository |
|---|---|
| Python | Scientific data processing, bioinformatics, chemistry, modelling, CLI and workbench |
| Rust | Infrastructure services, authentication, jobs, artifacts, audit and cloud adapters |
| C++17 | Native molecular data and scene foundation |
| SQLite | Local metadata, dataset registry and workbench state |
| PostgreSQL | Candidate durable multi-user job and audit persistence |
| AWS components | Terraform deployment candidate using ECS, RDS, S3 and KMS |
| Scientific formats | CSV/NPZ, FASTA, PDB and related formats as supported by each adapter |

Architecture and engineering decisions: Architecture (`ARCHITECTURE.md`) · Engineering stack (`ENGINEERING_STACK.md`) · Scientific architecture (`docs/SCIENTIFIC_ARCHITECTURE.md`).

## Research workflow

The current scientific workflow is organized around traceable, target-specific observations.

| Stage | Operation | Typical output |
|---:|---|---|
| 1 | Acquire a permitted source snapshot | Raw files and acquisition manifest |
| 2 | Normalize observations and units | Canonical one-target-per-row records |
| 3 | Audit identity, duplicates and metadata | Rejection tables and quality reports |
| 4 | Persist and release reviewed data | Immutable SQLite snapshot and KDB release |
| 5 | Build protein and chemical representations | ESM-2, Morgan and molecular graph feature archives |
| 6 | Create leakage-aware partitions | Protein-cluster and chemical-scaffold split manifests |
| 7 | Compare and train models | Target-specific and multimodal model artifacts |
| 8 | Evaluate and report | Metrics, uncertainty summaries and reproducibility report |

The workflow is documented in End-to-end research workflow (`docs/WORKFLOW.md`). The CatPred-DB source currently has an access gate and an upstream kcat-unit caveat; a real immutable source release and source-level audit are still required before scientific benchmark claims.

## Get started

### 1. Create an environment and install

Python 3.10 or newer is required.

~~~bash
git clone https://github.com/AssayFlux/Kinetics.git
cd Kinetics

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev,workbench]"
~~~

On Windows, activate the environment with .venv\Scripts\activate.

### 2. Start the local research workbench

~~~bash
kinetics-workbench
~~~

Open **http://127.0.0.1:8765** in your browser. The workbench binds to loopback only and is intended for local, single-user use. Do not expose it through a public address, LAN interface, reverse proxy or tunnel.

### 3. Explore the command-line interface

~~~bash
kinetics-research --help
kinetics-research audit --help
kinetics-research persist --help
~~~

Optional scientific dependencies for protein encoders, chemistry and baseline models are defined in the baseline extra:

~~~bash
python -m pip install -e ".[baseline]"
~~~

For detailed setup, supported tasks, workspace layout and security boundaries, read the Workbench guide (`docs/WORKBENCH_GUIDE.md`).

## Assets and visual identity

The repository currently tracks a small, explicit asset set. This section intentionally lists only files that exist in the Git tree; planned domain imagery is not presented as if it had already been downloaded.

<p align="center">
  <img src="Assets/Kinetics.gif" width="100%" alt="Kinetics animated scientific platform showcase">
</p>
<p align="center"><sub>Kinetics animated showcase · Assets/Kinetics.gif</sub></p>

| Asset | Repository path | Purpose | Status |
|---|---|---|---|
| Original Kinetics brand mark | Assets/Brand Logo.svg | Project identity and README branding | Tracked; preserved original artwork |
| Legacy animated GIF | Assets/Kinetics.gif | Earlier visual/animation experiment | Tracked legacy file; structural validation is unresolved, so it is not embedded as a live demo |
| 100-domain image collection | Assets/ (planned) | Future domain-specific scientific image gallery | Not yet committed; no missing image paths are referenced |

<p align="center">
  <img src="Assets/Brand%20Logo.svg" width="150" alt="Original Kinetics brand artwork">
</p>
<p align="center"><sub>Original brand artwork · stored at <strong>Assets/Brand Logo.svg</strong></sub></p>

| Asset resource | Location |
|---|---|
| Brand asset policy | docs/ASSET_PIPELINE.md (`docs/ASSET_PIPELINE.md`) |
| Legacy GIF file | Assets/Kinetics.gif (`Assets/Kinetics.gif`) |
| Asset and visual regression tests | tests/test_visual_assets.py (`tests/test_visual_assets.py`) |

**Asset integrity policy:** preserve original artwork and source attribution; verify file format, dimensions, frame metadata and license before displaying downloaded media. Do not fabricate gallery entries or commit unverified/generated substitutes for real scientific imagery. Add domain images only after their source, reuse license, attribution and checksum have been recorded.

## Repository map

| Path | Contents |
|---|---|
| src/kinetics_core/ | Python research core, curation, provenance, features, modelling and validation |
| src/kinetics_core/workbench/ | Local-first FastAPI workbench and static browser UI |
| rust/kinetics-infra/ | Rust service, identity, jobs, artifacts, audit and cloud integration |
| native/ | C++17 molecular structure and scene-data foundation |
| database/ | SQLite schema, migrations and source catalogue |
| deploy/aws/ | AWS Terraform deployment candidate |
| scripts/ | Dataset acquisition, inspection, schema validation and recovery utilities |
| tests/ | Python, workbench, structure, persistence and contract tests |
| docs/ | Scientific contracts, operating guides, validation plans and status records |
| Assets/ | Original logo and legacy GIF asset |

## Project status

The project is in an integration and acceptance phase. Passing unit tests or CI checks demonstrates only the tested software behaviour; it does not establish scientific validity, production readiness or clinical performance.

| Workstream | Current state | What is still needed |
|---|---|---|
| Steps 1–3: foundations and representations | Substantial code and fixture coverage | Real licensed data, actual ESM-2/MMseqs2 execution and reproducibility evidence |
| Steps 4–5: modelling and evaluation | Baseline and feature-fusion implementations; validation utilities | Frozen real-data benchmarks, external validation and statistical review |
| Step 6: native molecular engine | C++17 PDB/scene foundation and traceable simulation-plan schema | mmCIF, renderer, engine adapters, real execution and reference validation |
| Step 7: infrastructure and security | Rust services and AWS deployment candidate in repository | Live deployment, scientific worker handlers, per-job sandboxing, tenant tests and restore drills |
| Step 8: research workbench | Local-first workbench and fixture integration | Researcher and accessibility acceptance, real-data workflow, device and upgrade tests |
| Step 9: domain expansion | Versioned protein/structure contracts and PDB C-alpha adapter | mmCIF, source adapters, automated alignment and independent structural validation |
| Step 10: release readiness | Executable release-gate evaluator | Release manifest, SBOM, evidence archive, signed reviews and human sign-off |

### Explicit non-claims

- No reviewed, immutable real-world benchmark dataset release is currently recorded.
- No scientific performance or clinical efficacy claim is made.
- The local workbench is not a remote multi-tenant service.
- The AWS infrastructure is a deployment candidate, not evidence of a live production deployment.
- The worker's registered task handler is currently a health-check task; scientific task execution is not yet registered.
- The C++ component is not a full interactive GPU molecular viewer or molecular-dynamics engine.
- The PDB adapter is not a complete proteomics or structural-biology platform.
- The 100-domain catalogue is not evidence that 100 domain implementations exist.

See Step 10 release-readiness gates (`docs/STEP10_RELEASE_READINESS_GATES.md`) for the current NO-GO conditions and required evidence.

## Testing and quality checks

Run the Python test suite:

~~~bash
python -m pytest -q
~~~

Run focused checks:

~~~bash
python -m pytest -q tests/test_workbench.py tests/test_workbench_ui.py
python -m ruff check src tests
~~~

Native and Rust checks:

~~~bash
cmake -S native -B build/native
cmake --build build/native
ctest --test-dir build/native --output-on-failure

cd rust/kinetics-infra
cargo fmt --all -- --check
cargo clippy --all-targets -- -D warnings
cargo test --all-targets
~~~

Some tests require optional dependencies or local services. Follow the relevant workflow guide and CI configuration rather than interpreting an unavailable integration environment as a passing test.

## Documentation index

| Document | What it explains |
|---|---|
| Mission (`KINETICS_MISSION.md`) | Authoritative purpose, principles and boundaries |
| Vision (`VISION.md`) | Long-term scientific and platform direction |
| Master roadmap (`ROADMAP.md`) | Multi-stage programme and exit criteria |
| Implementation status (`docs/IMPLEMENTATION_STATUS.md`) | Implemented, pending and blocked capabilities |
| 100-domain catalogue (`docs/SCIENCE_DOMAIN_CATALOGUE_100.md`) | Canonical scientific domain register |
| Architecture (`ARCHITECTURE.md`) | Platform architecture and data/evidence model |
| Engineering stack (`ENGINEERING_STACK.md`) | Technology responsibilities and interoperability |
| Research workflow (`docs/WORKFLOW.md`) | Data-to-model workflow and scientific cautions |
| Workbench guide (`docs/WORKBENCH_GUIDE.md`) | Local setup, researcher workflow and security |
| Step 6 native engine (`docs/STEP6_IMPLEMENTATION_STATUS.md`) | Molecular parser, scene foundation and limitations |
| Step 7 production acceptance (`docs/STEP7_PRODUCTION_ACCEPTANCE.md`) | Identity, infrastructure and deployment gates |
| Step 9 structural contract (`docs/STEP9_PROTEOMICS_STRUCTURAL_CONTRACT.md`) | Protein/structure data contracts and PDB adapter |
| Step 10 release gates (`docs/STEP10_RELEASE_READINESS_GATES.md`) | Evidence manifest and release decision rules |
| Asset policy (`docs/ASSET_PIPELINE.md`) | Brand and media handling |

## Scientific integrity, privacy and safety

Kinetics must preserve source attribution, licenses, consent and access restrictions. Raw records should remain immutable; derived records must retain transformation lineage, software versions and checksums. Predictions are computational estimates, not experimental observations. Uncertainty and applicability limits must remain visible, and high-impact interpretation requires qualified human review.

Do not upload private, controlled, identifiable or sensitive health/genetic data to public services or repositories. Use only data for which the project has appropriate rights and authorization. The platform is research infrastructure and must not be used as a substitute for professional medical judgement or emergency care.

## Contributing and licensing

Contributions should preserve scientific semantics, provenance, reproducibility, test coverage and documented capability boundaries. Start with Contributing (`docs/CONTRIBUTING.md`), Publication protocol (`docs/PUBLICATION_PROTOCOL.md`) and the repository LICENSE (`LICENSE`).

---

<p align="center"><strong>KINETICS</strong><br>
<sub>Connect knowledge. Preserve evidence. Build responsibly.</sub></p>