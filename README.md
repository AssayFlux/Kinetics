# Kinetics

**Open-source research platform for enzyme kinetics, molecular intelligence, and a long-term vision of evidence-based precision molecular medicine.**

The current baseline predicts `log10(Km)` (Km in mM) and `log10(kcat)` (kcat in s⁻¹) from protein sequence and substrate SMILES using ESM-2 embeddings, 2048-bit radius-2 Morgan fingerprints, and two XGBoost regressors.

> **Research-use software.** Kinetics is being developed as a scientific research and decision-support platform. Computational predictions are hypotheses, not experimental measurements or clinical conclusions. The current enzyme-kinetics baseline does not diagnose disease, select medication, or generate validated patient treatment plans.

## Grand vision: molecularly informed, person-specific medicine

The long-term ambition is to investigate how an individual's molecular biology can inform more precise therapeutic research. People differ in their genomes and in other biological and clinical factors; the same intervention may therefore have different benefits, risks, metabolism, or response across individuals.

Kinetics aims to grow toward a platform that can help researchers study these differences and organize evidence for **personalized, genetics-informed treatment research**. The goal is not to assume that genes alone determine a person's treatment. Any future patient-specific research workflow must consider the broader biological and clinical context, including:

- **Genomics and variant interpretation:** quality-controlled variants, gene annotations, variant effects, inheritance where relevant, and well-supported gene–drug or gene–disease evidence.
- **Pharmacogenomics:** genetic variation that may influence drug metabolism, transport, targets, efficacy, or adverse-effect risk.
- **Protein and molecular function:** sequence variation, protein structure, stability, expression, enzyme activity, binding, and molecular mechanisms.
- **Chemical and drug properties:** molecular structures, target interactions, metabolism-related evidence, and compound-level predictions.
- **Multi-omics, where available:** transcriptomic, proteomic, metabolomic, and other molecular measurements to complement genomic information.
- **Clinical context:** confirmed diagnosis, age, relevant history, current medicines, allergies, organ function, laboratory findings, contraindications, and patient preferences—only where lawful, consented, and clinically appropriate.
- **Evidence and uncertainty:** source traceability, evidence strength, population applicability, conflicting findings, model uncertainty, and explicit reasons why a result may not generalize.

A future research workflow could organize evidence and generate **clinician-reviewable research summaries or candidate options**, with explanations, supporting sources, limitations, and uncertainty. It must not autonomously prescribe, diagnose, recommend a dose, or tell a person to start, stop, or change treatment. Clinical decisions belong to qualified healthcare professionals and the patient, using validated evidence and applicable standards of care.

### Important scientific and clinical boundary

This is a long-term research direction, not a capability of the current release. Enzyme Km/kcat prediction is a focused molecular-engineering task; it is not, by itself, a pharmacogenomics system or a clinical treatment recommender. Reaching the broader vision will require separate validated components, suitable consented datasets, clinical and domain-expert collaboration, prospective evaluation, regulatory and ethics review where applicable, and independent clinical validation before any clinical use is considered.

Kinetics must not infer a person's treatment from a single variant or model score. Genetic associations can be population-dependent, incompletely penetrant, uncertain, or contradicted by other clinical factors. A lack of evidence must be reported as a lack of evidence—not converted into a confident recommendation.

## Research domains and planned capabilities

The platform is intended to bring together complementary disciplines:

1. **Bioinformatics and sequence analysis** — DNA/RNA/protein sequence parsing, translation, annotation, motif analysis, sequence similarity, alignment, and quality checks.
2. **Structural bioinformatics** — PDB/mmCIF parsing, residue-level features, contacts, solvent accessibility, secondary structure, structural comparison, and structure-derived descriptors.
3. **Protein engineering** — mutation analysis, sequence/property prediction, stability and function hypotheses, enzyme–substrate relationships, and candidate sequence research.
4. **Enzyme kinetics** — Km, kcat, catalytic efficiency, assay-context normalization, and enzyme–substrate evidence.
5. **Cheminformatics** — molecular parsing, descriptors, fingerprints, similarity, compound curation, and ligand-related feature generation.
6. **Molecular interaction research** — protein–ligand and protein–protein interaction hypotheses, binding-related features, and affinity prediction where suitable data supports it.
7. **Genomics and pharmacogenomics (future research expansion)** — variant annotation, gene–drug evidence, genotype-to-phenotype interpretation, and population-aware uncertainty.
8. **Personalized molecular research (future research expansion)** — carefully governed integration of molecular and clinical context into traceable, clinician-reviewable evidence summaries.
9. **Machine learning and research reporting** — task-specific models, calibrated uncertainty, applicability-domain checks, leakage-resistant evaluation, model cards, and reproducible experiment records.
10. **Offline research assistance** — a future local assistant integration through the separate Astronaut project, subject to explicit integration and safety boundaries.

## BioPython integration

Kinetics will use the relevant BioPython ecosystem broadly across sequence, alignment, structural biology, annotation, and biological data workflows. The aim is to integrate the modules that serve the research tasks—not to import every BioPython module indiscriminately or rely on deprecated APIs.

The planned integration inventory is documented in [BioPython integration](docs/BIOPYTHON_INTEGRATION.md). Core areas include:

- `Bio.Seq`, `Bio.SeqRecord`, `Bio.SeqIO`, `Bio.SeqUtils`, `Bio.SeqUtils.ProtParam`, `Bio.SeqUtils.IsoelectricPoint`, and `Bio.Data` for sequence handling, translation, parsing, and protein descriptors.
- `Bio.Align`, `Bio.AlignIO`, substitution matrices, `Bio.motifs`, `Bio.SearchIO`, and `Bio.Blast` for alignment, motifs, and search-result workflows.
- `Bio.PDB` and its relevant parsers, writers, residue utilities, SASA, DSSP integration, neighbor search, superposition, and internal-coordinate tools for structural analysis.
- `Bio.Entrez` for controlled NCBI retrieval, with caching, rate-limit compliance, and provenance.
- `Bio.SeqFeature`, `Bio.Phylo`, `Bio.Cluster`, `Bio.Restriction`, `Bio.SVDSuperimposer`, and optional `Bio.Graphics` for appropriate annotation, evolutionary, clustering, construct, structural, and visualization tasks.

External programs such as BLAST+, MMseqs2, MAFFT, HMMER, DSSP, Foldseek, PyMOL, and molecular-simulation tools will be optional integrations, not assumed to be Python modules supplied by BioPython. Deprecated interfaces will be avoided in favor of supported modern APIs. See [the integration guide](docs/BIOPYTHON_INTEGRATION.md).

## Data and storage architecture

Kinetics includes a SQLite research store for structured records, metadata, provenance, and experiment bookkeeping. It is designed for reliable local research workflows, not as a claim that SQLite can store or accelerate every training tensor.

The planned hybrid storage design is:

| Data type | Preferred storage |
|---|---|
| Dataset catalogues, entities, compounds, assays, measurements, provenance, features metadata, predictions, experiment manifests | SQLite |
| Large normalized tabular datasets | Parquet / Arrow |
| Dense numeric arrays and reusable embeddings | NumPy with memory mapping |
| Chunked scientific arrays and larger feature collections | HDF5 or Zarr |
| Model weights and checkpoints | Safetensors or framework-native checkpoint formats |
| Raw sequences and structures | Versioned FASTA, GenBank, PDB, and mmCIF files |

SQLite uses WAL mode, foreign-key enforcement, bounded cache settings, batch writes, short transactions, and explicit maintenance/checkpoint operations. WAL supports concurrent readers while a writer is active, but SQLite still has a single-writer model. A write queue and batched transactions are preferred for ingestion. Large binary arrays, model weights, and raw scientific files remain outside the database; SQLite stores their metadata, paths, hashes, and provenance.

See [database architecture](docs/DATABASE_ARCHITECTURE.md) and the storage implementation under `src/kinetics_core/storage/`.

## Research principles, privacy, and governance

- **Traceability:** retain source accession/identifier, dataset version, retrieval date, license, checksum, transformation history, and citations.
- **Reproducibility:** record code and package versions, model identifiers, random seeds, data splits, configuration, and experiment manifests.
- **Data quality:** preserve raw observations, audit exclusions, distinguish unmatched measurements, document units and assay conditions, and never silently overwrite conflicting evidence.
- **Leakage control:** use sequence-cluster, scaffold, temporal, external, and other task-appropriate splits; do not rely on random splits alone for publication claims.
- **Uncertainty:** report calibration, applicability limits, missingness, and out-of-distribution warnings. A model score is not proof of a mechanism or clinical effect.
- **Fairness and generalizability:** assess performance across relevant populations and ancestry groups where ethically and scientifically appropriate; do not assume one cohort represents everyone.
- **Privacy and consent:** genetic and health data are highly sensitive. Future person-level workflows require informed consent, data minimization, secure access controls, encryption where appropriate, de-identification/pseudonymization, retention policies, and compliance with applicable law and institutional ethics requirements. Do not commit identifiable patient data or private genomic files to this repository.
- **Human oversight:** future clinical-facing research outputs must be explainable, source-linked, reviewable by qualified professionals, and explicitly non-autonomous.
- **Publication integrity:** distinguish implemented software from planned features, computational results from experimental findings, and retrospective evaluation from prospective clinical validation.

## Project layout

```text
Kinetics/
├── data/                       # User CSVs, features and cache (git-ignored)
├── src/
│   ├── data_preprocessing.py   # Validation, unit conversion, log targets, split
│   ├── feature_extraction.py   # ESM-2 + RDKit fingerprints and disk cache
│   ├── train_model.py          # 5-fold CV, holdout metrics, XGBoost
│   ├── optimize_mobile.py      # ONNX export, optional INT8 / FP16
│   ├── predict.py              # CLI and Python inference API
│   └── kinetics_core/          # Modular research, provenance, storage and assistant layer
├── docs/                       # Architecture, protocols, roadmap and research notes
├── models/                     # Local model artifacts (git-ignored)
├── requirements.txt
└── README.md
```

## Installation

Python 3.10–3.12 is recommended. Dependency wheels vary across operating systems and CPU architectures.

```bash
git clone https://github.com/AssayFlux/Kinetics.git
cd Kinetics
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Android / Termux

The ESM-2/PyTorch/Transformers stack and ONNX Runtime may not provide wheels for every Android ABI. Treat Android as an inference target, not the default training environment. For a constrained device, precompute/carry cached ESM embeddings or deploy a distilled encoder; unseen sequences still require ESM inference in this version. Validate RDKit and ONNX Runtime availability on the target device before deployment.

## Input data and units

Raw CSV must contain `sequence,smiles,km,kcat`. Sequences must contain only the 20 standard amino acids. Invalid SMILES, non-positive targets, and non-finite values are discarded. Inputs must use one consistent unit per column:

| Field | Default | Supported input units |
|---|---|---|
| km | mM | M, mM, uM / µM, nM |
| kcat | s⁻¹ | s^-1, min^-1, h^-1 |

The preprocessing stage converts Km to mM and kcat to s⁻¹ before applying log10. Keep assay metadata (pH, temperature, organism, construct, cofactors) in the source data; these factors can materially change measured kinetics.

## End-to-end workflow

Run all commands from the repository root.

### 1. Clean and split

```bash
python -m src.data_preprocessing --input data/raw.csv --output-dir data --km-unit mM --kcat-unit s^-1
```

Writes `data/train.csv`, `data/test.csv`, and `data/preprocessing_report.csv`. The default is a shuffled random 80/20 split (seed 42).

### 2. Extract features

```bash
python -m src.feature_extraction --input data/train.csv --output data/train_features.npz
python -m src.feature_extraction --input data/test.csv --output data/test_features.npz
```

The first run downloads `facebook/esm2_t6_8M_UR50D` from Hugging Face. Use `--device cpu` for CPU-only hosts. Individual combined feature vectors are cached in `data/cache/`; cache keys include model and fingerprint settings. ESM-2 input length is limited to 1022 residues in this baseline.

### 3. Train and evaluate

```bash
python -m src.train_model --train data/train_features.npz --test data/test_features.npz --model-dir models
```

Uses 5-fold shuffled CV on the training split and reports fold RMSE, mean/std CV RMSE, and holdout R², RMSE and MAE for each target. Saves `models/kinetics_model.joblib`, XGBoost JSON files, and `models/metrics.json`. At least five training rows are required.

### 4. Export for mobile

```bash
python -m src.optimize_mobile --model models/kinetics_model.joblib --output-dir models/onnx
# Optional FP16 graph conversion:
python -m src.optimize_mobile --fp16
```

ONNX export uses onnxmltools. Dynamic INT8 quantization is best-effort because tree-ensemble operators may not be quantizable; the exporter keeps FP32 if quantization fails or does not reduce file size. FP16 conversion is also optional and does not guarantee faster CPU execution. Benchmark on the actual Android/ARM device. Original joblib artifacts remain the fallback.

### 5. Predict

```bash
python -m src.predict --sequence MKT... --smiles 'CC(=O)O'
```

The CLI prefers available ONNX artifacts and falls back to joblib. Output includes `log10_km`, `km_mM`, `log10_kcat`, and `kcat_s-1`.

Python API:

```python
from src.predict import predict
result = predict(sequence="M...", smiles="CCO", model_dir="models")
print(result)
```

## Scientific validation notes

- Random splitting can leak homologous proteins or related chemical scaffolds across train/test. For credible external claims, add sequence-cluster, scaffold, temporal, and external test sets.
- Km and kcat depend on assay conditions; this baseline does not model pH, temperature, organism, or enzyme construct.
- Audit duplicate/conflicting measurements and replicate handling before training.
- Metrics are calculated on log10 targets; supplement with raw-unit metrics and calibration analysis.
- Predictions outside the training distribution should not be treated as reliable.

## Reproducibility and licensing

Seeds default to 42. Preserve raw data provenance, assay metadata, package versions, model identifiers and metrics. Data and model artifacts are git-ignored; publish only artifacts you are permitted to redistribute.

No license is selected yet. Add an OSI-approved license before accepting contributions or redistributing model/data artifacts.

## Public datasets

Kinetics uses public enzyme-kinetics resources. Start with the CatPred-DB processed Km and kcat tables and published sequence-cluster test splits:

```bash
python scripts/download_public_datasets.py --source catpred-db
python scripts/inspect_public_datasets.py --input-dir data/public/catpred-db
```

Downloaded data stays local and is excluded from Git. Review [DATASETS.md](DATASETS.md) for source links, attribution/license notes, curation rules, and the planned BRENDA/SABIO-RK extensions. The CatPred-DB Km and kcat tables are separate datasets and must not be merged as if their rows were matched measurements. Inspect source schemas and units before normalizing or training. No data is bundled and no model has yet been trained on these downloads.

## Research infrastructure layer

The repository also contains a modular research layer under `src/kinetics_core/`. It introduces a canonical one-observation-per-target schema, explicit Km/kcat unit conversion, source-table normalization with rejection audits, SHA-256 provenance, experiment manifests, target-specific metrics, and grouped/double-cold split helpers.

Install the research package and its core dependencies:

```bash
python -m pip install -e .
```

Normalize one target-specific public table after inspecting its source columns. Km and kcat must be processed separately; do not join them unless the source explicitly establishes a matched experiment:

```bash
python -m kinetics_core.catpred --help
```

The adapter requires explicit source column names and units. It writes normalized observations, rejected rows, and a curation manifest. See [the scientific architecture](docs/SCIENTIFIC_ARCHITECTURE.md), [the canonical data model](docs/DATA_MODEL.md), [the publication protocol](docs/PUBLICATION_PROTOCOL.md), and [implementation status](docs/IMPLEMENTATION_STATUS.md).

The new research utilities are implementation work, not a claim of completed model training or scientific validation. Training, testing, benchmarking, and validation remain scheduled for the final verification stage.

See [the implementation roadmap](docs/ROADMAP.md) for the staged build and final verification sequence.

Additional implementation references: [sequence and chemical splits](docs/SEQUENCE_AND_CHEMICAL_SPLITS.md), [modeling and uncertainty](docs/MODELING_AND_UNCERTAINTY.md), [research paper outline](docs/RESEARCH_PAPER_OUTLINE.md), and [contribution guide](docs/CONTRIBUTING.md).

The new research package also includes model-card and experiment-report generators, publication-oriented parity/residual plots, fold-local assay-context preprocessing, independent split-conformal calibration, and training-reference applicability warnings. See [assay-context features](docs/ASSAY_CONTEXT.md), [calibration workflow](docs/CALIBRATION_AND_CONTEXT_WORKFLOW.md), and [applicability diagnostics](docs/APPLICABILITY_DOMAIN.md). Install plotting support with `python -m pip install -e ".[plots]"`; see [reporting and figures](docs/REPORTING_AND_FIGURES.md).

For a documented end-to-end workflow from public dataset acquisition through target-specific curation, grouping, feature generation, and the deferred final model execution stage, see [docs/WORKFLOW.md](docs/WORKFLOW.md).

## Offline research assistant

Kinetics includes a dependency-free assistant adapter contract in `src/kinetics_core/assistant.py`. It is designed for a future local integration with [AssayFlux/Astronaut](https://github.com/AssayFlux/Astronaut), which remains a separate project under development. No hosted model, network fallback, model download, or autonomous tool execution is enabled. See [the Astronaut integration plan](docs/ASTRONAUT_INTEGRATION.md). The assistant is not operational until an Astronaut adapter is implemented and verified.

## Research CLI

Install the package with `python -m pip install -e ".[baseline]"` and run `kinetics-research --help`. Use `kinetics-research compare` for fixed classical baselines selected by training-only cross-validation, or `kinetics-research fit` for a target-specific XGBoost model. Supply grouped CV and all relevant holdout grouping arrays for leakage-aware evaluation. Model fitting and benchmarking are final-stage execution tasks and have not been run during implementation.

See [model comparison](docs/MODEL_COMPARISON.md) and [calibration/context workflow](docs/CALIBRATION_AND_CONTEXT_WORKFLOW.md).

Normalized tables can be audited without deleting or averaging observations: `kinetics-research audit --input data/processed/observations.csv --output-dir data/quality`. See [the observation quality policy](docs/OBSERVATION_QUALITY.md).

Prepare a leakage-resistant train/calibration/test design with `kinetics-research partition --observations data/processed/km_observations_with_groups.csv --output-dir data/partitions/km --target km`. This uses nested double-cold protein-cluster/scaffold splits and retains cross-quadrant exclusions. See [the partition workflow](docs/PARTITION_WORKFLOW.md).

## Development sequence

The current priority is to complete the software architecture, data models, ingestion adapters, storage, provenance, and interfaces first. Training, testing, benchmarking, and scientific validation are reserved for the final verification stage in accordance with the project plan. The broader genomics and personalized molecular research direction will be developed as a separate, carefully governed expansion rather than being represented as an existing feature.
