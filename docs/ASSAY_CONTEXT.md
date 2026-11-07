# Assay-context feature pipeline

> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

`kinetics_core.context.attach_context_archive` attaches raw assay metadata to feature archives with exact source-record ID alignment. The model-fitting pipeline then performs fold-local preprocessing. `AssayContextEncoder` remains available as a standalone utility for non-CV exploratory workflows.

## Supported behavior

- Numeric context (default: `ph`, `temperature_k`): training-set median
  imputation, standardization, and explicit missingness indicators.
- Categorical context (default: `organism`, `assay_method`, `cofactor`):
  explicit missing token and one-hot encoding.
- Unknown categories at inference time are ignored safely.
- Only configured allowlisted columns are selected; IDs and target columns are
  not passed through.

## Example

```python
from kinetics_core.context import AssayContextEncoder

encoder = AssayContextEncoder(
    numeric_columns=("ph", "temperature_k"),
    categorical_columns=("organism", "assay_method"),
)
X_train_context = encoder.fit_transform(train_frame)
X_test_context = encoder.transform(test_frame)
feature_names = encoder.get_feature_names_out()
```

Fit the encoder on training rows only. Never fit it on the combined train/test
table. Convert temperature to Kelvin before encoding and retain the original
reported value/unit in the canonical observation/provenance records.

This transformer is a feature utility; it has not yet been connected to the
model-fitting orchestrator or scientifically evaluated. Compare context-aware
and context-free models using identical, leakage-resistant split manifests.


## Cross-validation integration

For model fitting, prefer `attach_context_archive` from `kinetics_core.context`. It attaches raw metadata arrays after exact source-record alignment. The model workflow builds a scikit-learn preprocessing pipeline, so imputation, scaling, and one-hot vocabularies are fitted separately inside each cross-validation training fold. This avoids the subtle leakage that occurs when preprocessing is fitted once on the full training partition before CV. The standalone `AssayContextEncoder` remains available for exploratory use, but pre-encoded context archives are rejected by the publication-oriented fitting workflow.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
