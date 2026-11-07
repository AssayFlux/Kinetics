<p align="center">
  <img src="Assets/Brand%20Logo.svg" width="350" alt="Kinetics brand logo">
</p>
<p align="center">
  <img src="Assets/Kinetics.gif" width="100%" alt="Kinetics animated scientific platform showcase">
</p>

<h1 align="center">KINETICS</h1>
<p align="center"><strong>CONNECTING SCIENCE · ADVANCING HEALTH · PROTECTING HUMANITY</strong></p>
<p align="center">An evidence-centred platform for connected biomedical research.</p>

<p align="center">
  <img src="https://github.com/AssayFlux/Kinetics/actions/workflows/ci.yml/badge.svg" alt="CI status">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Rust-infrastructure-000000?logo=rust" alt="Rust">
  <img src="https://img.shields.io/badge/C%2B%2B-17-00599C?logo=cplusplus" alt="C++17">
  <img src="https://img.shields.io/badge/Research--first-not%20clinical%20software-6D28D9" alt="Research-first">
</p>

---

## What is Kinetics?

**Kinetics** is an open research-platform project bringing biological data, computational methods and scientific evidence into a coherent, reproducible environment.

The platform is being built in stages: integrate the scientific and infrastructure foundations first, develop the application on top of them, then complete real-data testing, researcher training and acceptance. The repository is an evolving engineering foundation—not a claim that every planned domain or clinical capability is complete.

| Principle | What it means |
|---|---|
| Evidence first | Results retain source, method, version and provenance |
| Reproducibility | Data transformations and model runs are traceable |
| Interoperability | Explicit schemas, identifiers, units and adapters |
| Responsible use | Uncertainty, privacy and human oversight are built into the workflow |

## Platform capabilities

| Area | Available foundation | Next validation milestone |
|---|---|---|
| Scientific data | Ingestion, normalization, provenance and quality-audit utilities | Reviewed, licensed real-world datasets and source audits |
| Bioinformatics & chemistry | Protein and molecular feature pipelines, including ESM-2 configuration and Morgan fingerprints | Reproducible execution and benchmark results on reviewed data |
| Modelling & evaluation | Baselines, feature-fusion model and leakage-aware split utilities | Frozen benchmarks, external validation and statistical review |
| Research workbench | Local-first browser interface, project workspaces, jobs and artifacts | Researcher, accessibility, installation and real-data acceptance |
| Molecular structures | C++17 PDB parsing and molecular scene-data foundation | Broader structure formats, independent validation and interactive rendering |
| Platform services | Rust foundations for identity, jobs, artifacts and audit; AWS deployment configuration | Live deployment, scientific workers, isolation, security and recovery tests |

**Scope note:** these are implementation foundations, not claims of production deployment, clinical validation or scientific performance. The 100-domain catalogue describes intended scope; it does not mean 100 finished modules.

## Scientific scope — all 100 domains

The complete domain register is listed below. These entries define the platform's intended scientific scope; inclusion does not imply that a domain-specific module is already complete or clinically validated.

| # | Domain | Scientific area |
|---:|---|---|
| 1 | Genomics | Molecular foundations |
| 2 | Genetics | Molecular foundations |
| 3 | Transcriptomics | Molecular foundations |
| 4 | Proteomics | Molecular foundations |
| 5 | Structural biology | Molecular foundations |
| 6 | Cell biology | Molecular foundations |
| 7 | Molecular biology | Molecular foundations |
| 8 | Biochemistry | Molecular foundations |
| 9 | Epigenetics | Molecular foundations |
| 10 | Systems biology | Molecular foundations |
| 11 | Metabolomics | Omics & living systems |
| 12 | Lipidomics | Omics & living systems |
| 13 | Glycomics | Omics & living systems |
| 14 | Metagenomics | Omics & living systems |
| 15 | Single-cell biology | Omics & living systems |
| 16 | Spatial omics | Omics & living systems |
| 17 | Developmental biology | Omics & living systems |
| 18 | Stem-cell biology | Omics & living systems |
| 19 | Microbiome science | Omics & living systems |
| 20 | Regenerative medicine | Omics & living systems |
| 21 | Microbiology | Microbes, immunity & disease |
| 22 | Virology | Microbes, immunity & disease |
| 23 | Immunology | Microbes, immunity & disease |
| 24 | Bacteriology | Microbes, immunity & disease |
| 25 | Mycology | Microbes, immunity & disease |
| 26 | Parasitology | Microbes, immunity & disease |
| 27 | Vaccinology | Microbes, immunity & disease |
| 28 | Antimicrobial resistance | Microbes, immunity & disease |
| 29 | Infectious diseases | Microbes, immunity & disease |
| 30 | Oncology | Microbes, immunity & disease |
| 31 | Pharmacology | Molecular design & therapeutics |
| 32 | Medicinal chemistry | Molecular design & therapeutics |
| 33 | Enzymology | Molecular design & therapeutics |
| 34 | Protein engineering | Molecular design & therapeutics |
| 35 | Biophysics | Molecular design & therapeutics |
| 36 | Molecular simulation | Molecular design & therapeutics |
| 37 | Chemical biology | Molecular design & therapeutics |
| 38 | Pharmacogenomics | Molecular design & therapeutics |
| 39 | Clinical pharmacology | Molecular design & therapeutics |
| 40 | Toxicology | Molecular design & therapeutics |
| 41 | Anatomy | Human biology & specialties |
| 42 | Physiology | Human biology & specialties |
| 43 | Pathology | Human biology & specialties |
| 44 | Cardiology | Human biology & specialties |
| 45 | Neuroscience | Human biology & specialties |
| 46 | Endocrinology | Human biology & specialties |
| 47 | Pulmonology | Human biology & specialties |
| 48 | Nephrology | Human biology & specialties |
| 49 | Gastroenterology | Human biology & specialties |
| 50 | Hepatology | Human biology & specialties |
| 51 | Hematology | Clinical specialties & care |
| 52 | Dermatology | Clinical specialties & care |
| 53 | Rheumatology | Clinical specialties & care |
| 54 | Orthopedics | Clinical specialties & care |
| 55 | Obstetrics | Clinical specialties & care |
| 56 | Gynecology | Clinical specialties & care |
| 57 | Pediatrics | Clinical specialties & care |
| 58 | Geriatrics | Clinical specialties & care |
| 59 | Ophthalmology | Clinical specialties & care |
| 60 | Psychiatry | Clinical specialties & care |
| 61 | Radiology | Diagnostics & medical technology |
| 62 | Medical ultrasound | Diagnostics & medical technology |
| 63 | Nuclear medicine | Diagnostics & medical technology |
| 64 | Computed tomography | Diagnostics & medical technology |
| 65 | Histology | Diagnostics & medical technology |
| 66 | Cytology | Diagnostics & medical technology |
| 67 | Laboratory medicine | Diagnostics & medical technology |
| 68 | Clinical chemistry | Diagnostics & medical technology |
| 69 | Clinical genetics | Diagnostics & medical technology |
| 70 | Medical imaging engineering | Diagnostics & medical technology |
| 71 | Surgery | Treatment, rehabilitation & prevention |
| 72 | Anesthesiology | Treatment, rehabilitation & prevention |
| 73 | Emergency medicine | Treatment, rehabilitation & prevention |
| 74 | Critical care | Treatment, rehabilitation & prevention |
| 75 | Radiation oncology | Treatment, rehabilitation & prevention |
| 76 | Pharmaceutics | Treatment, rehabilitation & prevention |
| 77 | Drug delivery | Treatment, rehabilitation & prevention |
| 78 | Rehabilitation medicine | Treatment, rehabilitation & prevention |
| 79 | Palliative care | Treatment, rehabilitation & prevention |
| 80 | Preventive medicine | Treatment, rehabilitation & prevention |
| 81 | Public health | Population, engineering & future health |
| 82 | Epidemiology | Population, engineering & future health |
| 83 | Global health | Population, engineering & future health |
| 84 | Clinical research | Population, engineering & future health |
| 85 | Clinical trials | Population, engineering & future health |
| 86 | Evidence synthesis | Population, engineering & future health |
| 87 | Health economics | Population, engineering & future health |
| 88 | Bioethics | Population, engineering & future health |
| 89 | Biomedical engineering | Population, engineering & future health |
| 90 | Bioinformatics | Population, engineering & future health |
| 91 | Medical robotics | Frontier & human resilience |
| 92 | Prosthetics | Frontier & human resilience |
| 93 | Biomaterials | Frontier & human resilience |
| 94 | Bioinstrumentation | Frontier & human resilience |
| 95 | Medical devices | Frontier & human resilience |
| 96 | Nanomedicine | Frontier & human resilience |
| 97 | Health informatics | Frontier & human resilience |
| 98 | Digital health | Frontier & human resilience |
| 99 | Artificial intelligence in medicine | Frontier & human resilience |
| 100 | Humanitarian and disaster health | Frontier & human resilience |

Canonical definitions and scope notes: `docs/SCIENCE_DOMAIN_CATALOGUE_100.md`.

## Architecture at a glance

| Layer | Responsibility | Main technologies |
|---|---|---|
| Scientific core | Data processing, curation, features, modelling and validation | Python |
| Infrastructure | Identity, job lifecycle, artifact handling and audit foundations | Rust |
| Native science | Molecular structure parsing and scene data | C++17 |
| Local persistence | Workbench state and scientific metadata | SQLite |
| Deployment path | Candidate cloud infrastructure and managed services | AWS / Terraform |
| Research interface | Local-first workbench and future application surfaces | FastAPI / web UI |

## Get started

**Requirements:** Python 3.10 or newer.

```bash
git clone https://github.com/AssayFlux/Kinetics.git
cd Kinetics

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev,workbench]"
```

Start the local research workbench:

```bash
kinetics-workbench
```

Then open **http://127.0.0.1:8765**.

The workbench currently binds to loopback and is intended for local, single-user use. Do not expose it to the public internet or a shared network.

Explore available commands:

```bash
kinetics-research --help
```

Optional modelling dependencies:

```bash
python -m pip install -e ".[baseline]"
```

## Project status

**Current phase: integration and acceptance preparation.** The priority is to complete and validate the foundations before building out the full application.

| Workstream | Current position | Outstanding evidence |
|---|---|---|
| Scientific pipelines | Core utilities and test fixtures exist | Licensed datasets, end-to-end real-data runs and reproducibility |
| Modelling | Baseline and feature-fusion components exist | ESM-2/MMseqs2 execution, frozen benchmarks and external validation |
| Molecular engine | PDB and scene-data foundation exists | Independent structure validation and full renderer/engine integration |
| Infrastructure | Rust service foundations and cloud configuration exist | Production deployment, scientific worker isolation, tenant security and recovery drills |
| Workbench | Local-first interface exists | Researcher and accessibility acceptance across supported devices |
| Release readiness | Release gates and evidence requirements are documented | SBOM, security review, evidence archive and signed release approval |

A passing test suite or CI run verifies only the behaviours covered by those tests. It does not establish scientific validity, production readiness or clinical performance.

## Quality checks

Run the Python tests:

```bash
python -m pytest -q
```

Run linting:

```bash
python -m ruff check src tests
```

Native and Rust checks:

```bash
cmake -S native -B build/native
cmake --build build/native
ctest --test-dir build/native --output-on-failure

cd rust/kinetics-infra
cargo fmt --all -- --check
cargo clippy --all-targets -- -D warnings
cargo test --all-targets
```

Some integration checks require optional dependencies or local services.

## Documentation

| Document | Purpose |
|---|---|
| `ARCHITECTURE.md` | System architecture and component boundaries |
| `ROADMAP.md` | Development stages and milestones |
| `docs/IMPLEMENTATION_STATUS.md` | Implemented, pending and blocked work |
| `docs/SCIENCE_DOMAIN_CATALOGUE_100.md` | Complete scientific domain catalogue |
| `docs/WORKFLOW.md` | End-to-end scientific workflow |
| `docs/WORKBENCH_GUIDE.md` | Setup, usage and workbench boundaries |
| `docs/STEP7_PRODUCTION_ACCEPTANCE.md` | Infrastructure and production acceptance criteria |
| `docs/STEP10_RELEASE_READINESS_GATES.md` | Release evidence and go/no-go requirements |

## Responsible research

Kinetics is research and engineering infrastructure—not a diagnostic device, treatment recommendation system or substitute for qualified medical judgement. Use only data with appropriate rights and authorization. Protect identifiable, genetic and other sensitive information; preserve source attribution, consent restrictions and provenance. Treat model outputs as estimates, retain uncertainty and require qualified human review for consequential interpretation.

## Contributing

Contributions should include tests, clear documentation and evidence for scientific or operational claims. Preserve data provenance, licensing, reproducibility and the explicit limits of each capability. Review `docs/CONTRIBUTING.md` and the repository `LICENSE` before contributing.

---

<p align="center"><strong>KINETICS</strong><br>
<sub>Connect knowledge. Preserve evidence. Build responsibly.</sub></p>
