# Kinetics

**Open-source baseline for enzyme kinetic parameter prediction from protein sequence and substrate SMILES.**

Predicts `log10(Km)` (Km in mM) and `log10(kcat)` (kcat in s⁻¹) using ESM-2 embeddings, 2048-bit radius-2 Morgan fingerprints, and two XGBoost regressors.

> Research-use software. Predictions are computational estimates, not experimental measurements. Generalization depends on dataset quality, assay conditions, and leakage-resistant evaluation.

## Project layout

```text
Kinetics/
├── data/                       # User CSVs, features and cache (git-ignored)
├── src/
│   ├── data_preprocessing.py   # Validation, unit conversion, log targets, split
│   ├── feature_extraction.py   # ESM-2 + RDKit fingerprints and disk cache
│   ├── train_model.py          # 5-fold CV, holdout metrics, XGBoost
│   ├── optimize_mobile.py      # ONNX export, optional INT8 / FP16
│   └── predict.py              # CLI and Python inference API
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
