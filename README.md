<!-- Kinetics | concise project README -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:800020,55:D4AF37,100:1F2A6B&height=155&section=header&text=KINETICS&fontSize=46&fontColor=FFF8E7&font=Marcellus%20SC&fontAlignY=43" alt="Kinetics — maroon, antique gold and indigo header">
</p>

<p align="center">
  <img src="assets/ornaments/toran-banner.svg" alt="Kinetics Indian-heritage toran ornament" width="100%">
</p>

<p align="center">
  <img src="assets/brand/organization-logo.gif" alt="AssayFlux organization logo" width="104" height="104">
  &nbsp;&nbsp;
  <img src="assets/brand/brand-logo.svg" alt="AssayFlux vector brand mark" width="104" height="104">
  &nbsp;&nbsp;
  <img src="assets/brand/kinetics-logo.gif" alt="Kinetics project logo" width="104" height="104">
</p>

<h1 align="center">Kinetics</h1>
<p align="center">
  <strong>Offline-first scientific research workbench</strong><br>
  Android · Python · C++ · Rust
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/AssayFlux/Kinetics?style=flat-square&color=800020" alt="Apache-2.0 license"></a>
  <a href="https://github.com/AssayFlux/Kinetics/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/AssayFlux/Kinetics/ci.yml?branch=main&style=flat-square&label=CI" alt="GitHub Actions CI status"></a>
  <a href="https://github.com/AssayFlux/Kinetics/issues"><img src="https://img.shields.io/github/issues/AssayFlux/Kinetics?style=flat-square" alt="Open issues"></a>
  <a href="https://github.com/AssayFlux/Kinetics/commits/main"><img src="https://img.shields.io/github/last-commit/AssayFlux/Kinetics?style=flat-square" alt="Latest commit"></a>
</p>

<p align="center"><strong>PRE-RELEASE · RESEARCH USE ONLY · NOT CLINICALLY VALIDATED</strong></p>

---

## Overview

Kinetics is an AssayFlux research workbench combining an Android application foundation with a modular Python scientific package and selected native components. The project is designed around local-first workflows, reproducibility, explicit capability boundaries and traceable research outputs.

## What is in the repository

| Area | Implemented foundations |
|---|---|
| Sequence & genomics | FASTA/FASTQ, sequence statistics, alignment, k-mers, SAM/BAM/VCF utilities |
| Structure | PDB/mmCIF parsing, contacts, RMSD and structure-analysis utilities |
| Chemistry & simulation | Molecular graph utilities; optional RDKit, AutoDock Vina and OpenMM integrations |
| Kinetics & omics | Michaelis–Menten, PK/PD, statistical and exploratory omics utilities |
| Pharmacogenomics | Research-only allele/variant parsing and matching foundations |
| Application & native stack | Kotlin/Jetpack Compose, Python integration, C++/JNI and Rust components |
| Governance | Versioned contracts, capability registry, provenance and validation tooling |

These are repository implementation areas, not a claim that every workflow is complete, enabled in the Android app or independently scientifically validated.

## Current track order

The owner-approved sequence is **R → S → I → P → G → U** (Decision [D-023](DECISIONS.md)).

| Track | Current position |
|---|---|
| R — Research platform | Software/host audit recorded closed; device, scientific, licensing and release evidence remain open |
| S — Structure, sequence & discovery | Software scope recorded closed; independent validation and device/licensing evidence remain open |
| I — In-silico laboratory | Software implementation/integration audit recorded closed; scientific, licensing, secure-node and device gates remain open |
| P — Precision-medicine preparation | In progress; exact-head verification is required before software audit closure. **P0 remains NOT APPROVED** |
| G — Governance & assurance | In progress; exact-head audit, owner acceptance, independent reviews and operating exercises remain open |
| U — User experience | Follows G; partial U0–U3 work is retained as baseline |

The [roadmap](ROADMAP.md) is the status authority. Software completion does not imply scientific, clinical, regulatory or release acceptance.

## Quick start

Python package development requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pip install -e .
pytest
```

Example:

```python
from kinetics import parse_fasta

records = parse_fasta(">example\nACGT")
print(records[0])
```

Optional integrations are declared in `pyproject.toml`:

```bash
python -m pip install -e ".[docking]"
python -m pip install -e ".[md]"
```

For Android build prerequisites and the supported local build procedure, see [the Android build guide](docs/local-android-build.md) and `scripts/build_android_local.sh`.

## Project documentation

- [North Star](NORTH_STAR.md) — purpose, scope and permanent guardrails
- [Roadmap](ROADMAP.md) — current track plan and exit criteria
- [Decision log](DECISIONS.md) — owner-approved decisions
- [Documentation index](docs/README.md) — architecture, implementation, validation and governance documents
- [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Privacy](PRIVACY.md)

## Research boundary

Kinetics is a pre-release research project. It is not a medical device or clinical decision-support system. Do not use it for diagnosis, treatment, dosing or patient-care decisions. P0 remains not approved; patient/clinical workflows remain gated. Computational outputs require method-specific validation and must not be presented as established biological or clinical facts.

## License

Project code is licensed under [Apache-2.0](LICENSE). Third-party engines, dependencies, datasets, models and assets may have separate terms; review their licenses before use or redistribution.

<p align="center">
  <img src="assets/brand/My%20Signature.svg" alt="Project owner's original signature artwork" height="76">
  <br>
  <sub><strong>BUILD CAREFULLY · MEASURE HONESTLY · SHARE REPRODUCIBLY</strong></sub>
</p>
