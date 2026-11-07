# Assay context, calibration and applicability workflow

> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

## Fit assay context without leakage

Attach raw assay metadata after verifying exact source-record ID order. The modeling pipeline fits imputation, scaling, and categorical vocabularies independently inside each cross-validation fold, then refits on the full training partition.

```python
from kinetics_core.context import attach_context_archive

attach_context_archive(
    "data/features/km_train.npz",
    "data/metadata/km_train.csv",
    "data/features/km_train_context.npz"
)
attach_context_archive(
    "data/features/km_calibration.npz",
    "data/metadata/km_calibration.csv",
    "data/features/km_calibration_context.npz",
)
attach_context_archive(
    "data/features/km_test.npz",
    "data/metadata/km_test.csv",
    "data/features/km_test_context.npz",
)
```

Each metadata CSV must contain `source_record_id` and the configured assay
columns. Rows must be in exactly the same order as its feature archive. The
fold-local pipeline learns preprocessing only from each CV training fold, then
refits on the full training partition before calibration and final test.

## Independent calibration and model fitting

Reserve a calibration partition before model selection. It must not be used for
fitting, feature selection, hyperparameter tuning, or early stopping. For
grouped generalization claims, provide group arrays and require disjoint groups
across train, calibration, and final test:

```python
from kinetics_core.modeling import fit_target_model

fit_target_model(
    "data/features/km_train_context.npz",
    "data/features/km_test_context.npz",
    target="km",
    output_dir="artifacts/km",
    group_array="protein_cluster_id",
    holdout_group_arrays=("protein_cluster_id", "scaffold_id"),
    calibration_archive="data/features/km_calibration_context.npz",
    conformal_alpha=0.10,
)
```

When no independent calibration archive is supplied, the model is explicitly
marked uncalibrated. Test-set empirical coverage is descriptive and must not be
used to tune the interval.

## Prediction

```python
from kinetics_core.prediction import predict_one

prediction = predict_one(
    "PROTEIN_SEQUENCE",
    "SUBSTRATE_SMILES",
    model_path="artifacts/km/km_model.joblib",
    target="km",
    assay_context={
        "ph": 7.0,
        "temperature_k": 298.15,
        "organism": "source organism",
        "assay_method": "source assay method",
        "cofactor": "source cofactor",
    },
)
```

For context-trained models, pass all configured assay fields. The fitted
conformal quantile is attached automatically when present. The returned
applicability warning compares the query feature vector with the training
reference distribution.

## Interpretation limits

- Split conformal relies on exchangeability between calibration and future
  observations; biological datasets often violate this through publication,
  protein-family, substrate-scaffold, and assay shifts.
- A marginal coverage target is not a per-subgroup guarantee.
- The nearest-neighbour applicability monitor is a feature-space warning, not
  a probability of correctness or calibrated confidence.
- Do not compare intervals across targets as if their units were identical.
- Report the exact split manifest, calibration size, alpha, feature pipeline,
  and any distribution shift limitations.
