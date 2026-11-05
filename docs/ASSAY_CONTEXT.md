# Assay-context feature pipeline

`kinetics_core.context.AssayContextEncoder` provides an optional, leakage-aware
preprocessor for assay metadata.

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
