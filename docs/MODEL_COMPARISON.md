# Model-family comparison

`kinetics_core.benchmark.compare_regressors` compares fixed classical baselines:
Ridge, Random Forest, Extra Trees, and HistGradientBoosting. Candidate selection
uses only training-set cross-validation; the held-out archive is evaluated once
after selection and is not used to rank candidates.

Use a protein-cluster grouping array for grouped CV and provide all relevant
holdout axes for leakage checks:

```python
from kinetics_core.benchmark import compare_regressors

report = compare_regressors(
    "data/features/km_train.npz",
    "data/features/km_test.npz",
    target="km",
    output_dir="artifacts/km/baselines",
    group_array="protein_cluster_id",
    holdout_group_arrays=("protein_cluster_id", "scaffold_id"),
)
```

This is a fixed baseline comparison, not an exhaustive hyperparameter search.
Do not tune candidates against the final test set. Repeat independently for Km
and kcat; they are distinct targets and datasets. Row-random CV is marked
diagnostic-only and cannot support protein/chemical cold-start claims.
