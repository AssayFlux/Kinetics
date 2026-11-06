# Model-family comparison and held-out uncertainty

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

The held-out report includes deterministic paired-row percentile-bootstrap
95% intervals for log10 MAE and RMSE (2,000 resamples by default). When
`holdout_group_arrays` are supplied, it also reports paired cluster-bootstrap
intervals for each declared held-out axis, resampling unique groups while retaining
all rows within each sampled group. Cluster intervals are unstable with few
independent groups and do not address dataset shift, model-selection bias, or
establish calibrated predictive uncertainty. External-source replication remains
necessary for broader generalization claims.

This is a fixed baseline comparison, not an exhaustive hyperparameter search.
Do not tune candidates against the final test set. Repeat independently for Km
and kcat; they are distinct targets and datasets. Row-random CV is marked
diagnostic-only and cannot support protein/chemical cold-start claims.
