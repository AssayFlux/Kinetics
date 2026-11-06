# Kinetics

**An open-source molecular research platform for understanding biological differences and advancing personalized, genetics-informed medicine.**

Kinetics brings together bioinformatics, structural biology, protein engineering, enzyme kinetics, cheminformatics, and machine learning. Its long-term purpose is to help researchers investigate how each person's genetic and molecular characteristics may influence disease biology, drug response, and treatment outcomes.

> **Research software — not a clinical system.** Kinetics does not diagnose, prescribe, or produce validated treatment plans. All predictions are computational hypotheses and require appropriate scientific and clinical validation.

## Vision

People are biologically different. Genetic variants and other molecular, physiological, and environmental factors can influence how diseases develop and how individuals respond to medicines.

Kinetics aims to support research into these differences and, over time, help organize evidence for **person-specific, genetics-informed treatment research**.

The long-term research direction includes:

- **Genomics and pharmacogenomics** — variant interpretation and evidence about gene–drug relationships.
- **Protein and structural biology** — sequence, structure, mutations, function, stability, and molecular interactions.
- **Enzyme and molecular kinetics** — enzyme activity, substrate relationships, Km, kcat, and catalytic efficiency.
- **Cheminformatics and drug research** — molecular representations, compound properties, and target interactions.
- **Multi-omics integration** — genomic, transcriptomic, proteomic, and metabolomic evidence where available.
- **Personalized evidence research** — combining molecular findings with relevant clinical context to produce transparent, source-supported research summaries for qualified professional review.

Genes alone do not determine treatment. Any future person-level workflow must account for clinical context, evidence quality, uncertainty, population applicability, contraindications, and patient preferences. It must not autonomously diagnose, prescribe, or recommend medication changes. Clinical decisions remain with qualified healthcare professionals and the patient.

## Current foundation

The repository currently includes an enzyme-kinetics baseline that estimates:

- `log10(Km)` — Michaelis constant, expressed in mM.
- `log10(kcat)` — catalytic turnover, expressed in s⁻¹.

The baseline uses ESM-2 protein embeddings, RDKit Morgan fingerprints, and XGBoost regressors. The repository also contains research infrastructure for data curation, provenance, assay context, experiment records, leakage-aware data partitioning, uncertainty and reporting workflows.

These capabilities are a foundation—not a completed personalized-medicine platform. The broader genomics, pharmacogenomics, multi-omics, and person-specific research capabilities are future development goals.

## Scientific technology

- **BioPython:** sequence handling, translation, annotation, alignments, motifs, database retrieval, and structural-biology workflows.
- **RDKit:** chemical parsing, molecular descriptors, fingerprints, and similarity analysis.
- **PyTorch and protein language models:** representation learning and future task-specific molecular models.
- **Structural and molecular tools:** planned integrations may include BLAST+, MMseqs2, MAFFT, HMMER, DSSP, Foldseek, PyMOL, and molecular-simulation software.
- **Research assistant:** a future offline integration with the separate Astronaut project, when that project is ready.

Only tools relevant to a defined research task will be integrated; deprecated APIs and unnecessary dependencies will be avoided.

## Data and storage

Kinetics uses a hybrid research-data architecture:

| Data | Storage |
|---|---|
| Metadata, assays, measurements, provenance, experiments | SQLite |
| Large tabular datasets | Parquet / Arrow |
| Numeric arrays and embeddings | NumPy / memory mapping |
| Chunked scientific data | HDF5 / Zarr |
| Model checkpoints | Safetensors or framework-native formats |
| Sequences and structures | FASTA, GenBank, PDB, mmCIF |

SQLite is intended for structured records and metadata, not large tensors or unrestricted concurrent writes. Large scientific files and model artifacts remain in appropriate file formats, with their metadata, hashes, and provenance recorded in the database.

## Research principles

- Reproducible methods, versioned data, and traceable sources.
- Transparent curation, units, assay conditions, and exclusion records.
- Leakage-resistant evaluation and independent validation.
- Calibrated uncertainty and explicit applicability limits.
- Population-aware assessment and responsible interpretation.
- Informed consent, data minimization, privacy, and secure handling of genetic and health data.
- Clear separation of implemented capabilities, research hypotheses, and future plans.

Identifiable patient data and private genomic information must never be committed to this repository. Any future person-level research must follow applicable legal, ethical, institutional, and consent requirements.

## Development status

The immediate objective is to complete the software architecture, data models, scientific integrations, ingestion pipelines, storage, provenance, and interfaces first. Model training, testing, benchmarking, and scientific validation are reserved for the final verification stage.

Clinical or treatment-related use would require additional evidence, specialist collaboration, prospective evaluation, independent clinical validation, and any applicable regulatory and ethics approvals. No clinical readiness is claimed.

## Installation

Python 3.10–3.12 is recommended.

```bash
git clone https://github.com/AssayFlux/Kinetics.git
cd Kinetics
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Repository guide

- `src/` — baseline models and Kinetics research package.
- `src/kinetics_core/` — modular research infrastructure and storage.
- `docs/` — architecture, data model, BioPython integration, database design, research protocols, and roadmap.
- `data/` and `models/` — local datasets and model artifacts; keep private or restricted data out of version control.

## Research status

Kinetics is an evolving research project. Predictions are not experimental findings, and software implementation is not evidence of biological or clinical validity. Contributions should preserve scientific transparency, reproducibility, privacy, and responsible use.
