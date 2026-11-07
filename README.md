<p align="center">
  <img src="Assets/Brand%20Logo.svg" width="190" alt="Kinetics original brand mark">
</p>
<h1 align="center">KINETICS</h1>
<p align="center"><strong>CONNECTING SCIENCE · ADVANCING HEALTH · PROTECTING HUMANITY</strong><br>
An evidence-centred scientific infrastructure for connected biomedical research.</p>
<p align="center">
  <a href="https://github.com/AssayFlux/Kinetics/actions/workflows/ci.yml"><img src="https://github.com/AssayFlux/Kinetics/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Rust-infrastructure-000000?logo=rust" alt="Rust infrastructure">
  <img src="https://img.shields.io/badge/C%2B%2B-17-00599C?logo=cplusplus" alt="C++17">
  <img src="https://img.shields.io/badge/Research--first-not%20clinical%20software-6D28D9" alt="Research-first">
</p>
<p align="center">
  <a href="#overview">Overview</a> · <a href="#capabilities">Capabilities</a> ·
  <a href="#science-domain-universe">100 domains</a> · <a href="#architecture">Architecture</a> ·
  <a href="#get-started">Get started</a> · <a href="#assets-and-visual-identity">Assets</a> ·
  <a href="#project-status">Status</a>
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

See [Implementation status](docs/IMPLEMENTATION_STATUS.md) for the detailed capability register and limitations.

## Science domain universe

Kinetics uses a 100-domain catalogue as its long-term coverage map. The table below groups that catalogue into ten connected research families; the canonical catalogue contains all domain names and descriptions.

| Domain family | Catalogue range | Included research areas |
|---|---:|---|
| Molecular foundations | 01–10 | Genomics, genetics, transcriptomics, proteomics, structural biology, cell and molecular biology, biochemistry, epigenetics, systems biology |
| Omics and living systems | 11–20 | Metabolomics, lipidomics, glycomics, metagenomics, single-cell and spatial omics, development, stem cells, microbiome, regenerative medicine |
| Microbes, immunity and disease | 21–30 | Microbiology, virology, immunology, bacteriology, mycology, parasitology, vaccinology, antimicrobial resistance, infectious disease, oncology |
| Molecular design and therapeutics | 31–40 | Pharmacology, medicinal chemistry, enzymology, protein engineering, biophysics, molecular simulation, chemical biology, pharmacogenomics, clinical pharmacology, toxicology |
| Human biology and specialties | 41–50 | Anatomy, physiology, pathology, cardiology, neuroscience, endocrinology, pulmonology, nephrology, gastroenterology, hepatology |
| Clinical specialties and care | 51–60 | Hematology, dermatology, rheumatology, orthopedics, obstetrics, gynecology, pediatrics, geriatrics, ophthalmology, psychiatry |
| Diagnostics and medical technology | 61–70 | Radiology, ultrasound, nuclear medicine, CT, histology, cytology, laboratory medicine, clinical chemistry, clinical genetics, imaging engineering |
| Treatment, rehabilitation and prevention | 71–80 | Surgery, anesthesiology, emergency and critical care, radiation oncology, pharmaceutics, drug delivery, rehabilitation, palliative and preventive medicine |
| Population, engineering and future health | 81–90 | Public and global health, epidemiology, clinical research, trials, evidence synthesis, health economics, bioethics, biomedical engineering, bioinformatics |
| Frontier and human resilience | 91–100 | Medical robotics, prosthetics, biomaterials, bioinstrumentation, medical devices, nanomedicine, health informatics, digital health, medical AI, humanitarian and disaster health |

**Full register:** [100-domain scientific catalogue](docs/SCIENCE_DOMAIN_CATALOGUE_100.md).

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

Architecture and engineering decisions: [Architecture](ARCHITECTURE.md) · [Engineering stack](ENGINEERING_STACK.md) · [Scientific architecture](docs/SCIENTIFIC_ARCHITECTURE.md).

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

The workflow is documented in [End-to-end research workflow](docs/WORKFLOW.md). The CatPred-DB source currently has an access gate and an upstream kcat-unit caveat; a real immutable source release and source-level audit are still required before scientific benchmark claims.

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

For detailed setup, supported tasks, workspace layout and security boundaries, read the [Workbench guide](docs/WORKBENCH_GUIDE.md).

## Assets and visual identity

The repository currently tracks a small, explicit asset set. This section intentionally lists only files that exist in the Git tree; planned domain imagery is not presented as if it had already been downloaded.

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
| Brand asset policy | [docs/ASSET_PIPELINE.md](docs/ASSET_PIPELINE.md) |
| Legacy GIF file | [Assets/Kinetics.gif](Assets/Kinetics.gif) |
| Asset and visual regression tests | [tests/test_visual_assets.py](tests/test_visual_assets.py) |

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

See [Step 10 release-readiness gates](docs/STEP10_RELEASE_READINESS_GATES.md) for the current NO-GO conditions and required evidence.

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
| [Mission](KINETICS_MISSION.md) | Authoritative purpose, principles and boundaries |
| [Vision](VISION.md) | Long-term scientific and platform direction |
| [Master roadmap](ROADMAP.md) | Multi-stage programme and exit criteria |
| [Implementation status](docs/IMPLEMENTATION_STATUS.md) | Implemented, pending and blocked capabilities |
| [100-domain catalogue](docs/SCIENCE_DOMAIN_CATALOGUE_100.md) | Canonical scientific domain register |
| [Architecture](ARCHITECTURE.md) | Platform architecture and data/evidence model |
| [Engineering stack](ENGINEERING_STACK.md) | Technology responsibilities and interoperability |
| [Research workflow](docs/WORKFLOW.md) | Data-to-model workflow and scientific cautions |
| [Workbench guide](docs/WORKBENCH_GUIDE.md) | Local setup, researcher workflow and security |
| [Step 6 native engine](docs/STEP6_IMPLEMENTATION_STATUS.md) | Molecular parser, scene foundation and limitations |
| [Step 7 production acceptance](docs/STEP7_PRODUCTION_ACCEPTANCE.md) | Identity, infrastructure and deployment gates |
| [Step 9 structural contract](docs/STEP9_PROTEOMICS_STRUCTURAL_CONTRACT.md) | Protein/structure data contracts and PDB adapter |
| [Step 10 release gates](docs/STEP10_RELEASE_READINESS_GATES.md) | Evidence manifest and release decision rules |
| [Asset policy](docs/ASSET_PIPELINE.md) | Brand and media handling |

## Scientific integrity, privacy and safety

Kinetics must preserve source attribution, licenses, consent and access restrictions. Raw records should remain immutable; derived records must retain transformation lineage, software versions and checksums. Predictions are computational estimates, not experimental observations. Uncertainty and applicability limits must remain visible, and high-impact interpretation requires qualified human review.

Do not upload private, controlled, identifiable or sensitive health/genetic data to public services or repositories. Use only data for which the project has appropriate rights and authorization. The platform is research infrastructure and must not be used as a substitute for professional medical judgement or emergency care.

## Contributing and licensing

Contributions should preserve scientific semantics, provenance, reproducibility, test coverage and documented capability boundaries. Start with [Contributing](docs/CONTRIBUTING.md), [Publication protocol](docs/PUBLICATION_PROTOCOL.md) and the repository [LICENSE](LICENSE).

---

<p align="center"><strong>KINETICS</strong><br>
<sub>Connect knowledge. Preserve evidence. Build responsibly.</sub></p>