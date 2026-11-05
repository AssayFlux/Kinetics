# Nested double-cold partition workflow

Use `kinetics_core.partition.prepare_target_partitions` to create a final test
set that is cold on both protein cluster and substrate scaffold, then reserve a
separate double-cold calibration set from the remaining development pool.

```python
from kinetics_core.partition import prepare_target_partitions

result = prepare_target_partitions(
    "data/processed/km_observations_with_groups.csv",
    "data/partitions/km",
    target="km",
    protein_group_column="protein_cluster_id",
    substrate_group_column="scaffold_id",
    test_fraction=0.2,
    calibration_fraction=0.2,
    random_state=42,
)
print(result["manifest_path"])
```

The function writes separate train, calibration, test, and excluded
cross-quadrant CSVs plus a provenance manifest. It refuses to partition when
duplicate source record IDs remain, because replicate/conflict handling must be
decided explicitly before splitting. It checks that protein and scaffold groups
are disjoint across all three retained partitions.

Double-cold intersections can be small or empty for sparse datasets. In that
case, the workflow stops rather than silently weakening the evaluation design.
Adjust the holdout fraction or report that the source dataset cannot support the
requested cold-start benchmark.
