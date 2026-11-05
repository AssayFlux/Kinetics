"""Leakage-aware preprocessing for optional enzyme assay context.

Only explicitly selected columns are encoded. Fit this transformer on training
rows only, then reuse the fitted instance for validation/test/inference data.
Do not include record IDs, publication IDs, or other target-leaking identifiers.
"""

from __future__ import annotations

from typing import Sequence

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils.validation import check_is_fitted


class AssayContextEncoder(BaseEstimator, TransformerMixin):
    """Encode numeric and categorical assay metadata with missingness preserved.

    Numeric fields use training-set median imputation, standardization, and
    missingness indicators. Categorical fields use an explicit missing token
    and one-hot encoding with unknown categories ignored at transform time.

    The selected feature lists are allowlists: unselected columns (including
    IDs and labels) are never passed to the estimator.
    """

    def __init__(
        self,
        numeric_columns: Sequence[str] = ("ph", "temperature_k"),
        categorical_columns: Sequence[str] = ("organism", "assay_method", "cofactor"),
    ) -> None:
        self.numeric_columns = numeric_columns
        self.categorical_columns = categorical_columns

    def _selected_columns(self) -> list[str]:
        selected = [*self.numeric_columns, *self.categorical_columns]
        if len(selected) != len(set(selected)):
            raise ValueError("context columns must be unique across feature groups")
        return selected

    def _validate_frame(self, X: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(X, pd.DataFrame):
            raise TypeError("assay context input must be a pandas DataFrame")
        selected = self._selected_columns()
        if not selected:
            raise ValueError("at least one numeric or categorical context column is required")
        missing = [column for column in selected if column not in X.columns]
        if missing:
            raise ValueError(f"missing configured assay context columns: {missing}")
        frame = X.loc[:, selected].copy()
        for column in self.numeric_columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
        for column in self.categorical_columns:
            frame[column] = frame[column].where(frame[column].notna(), None)
        return frame

    def fit(self, X: pd.DataFrame, y: object = None) -> "AssayContextEncoder":
        """Learn imputers, scaling statistics, and categories from training data."""
        frame = self._validate_frame(X)
        transformers: list[tuple[str, Pipeline, list[str]]] = []

        if self.numeric_columns:
            numeric_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
                    ("scaler", StandardScaler()),
                ]
            )
            transformers.append(("numeric", numeric_pipeline, list(self.numeric_columns)))

        if self.categorical_columns:
            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="constant", fill_value="__MISSING__")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                ]
            )
            transformers.append(
                ("categorical", categorical_pipeline, list(self.categorical_columns))
            )

        self.transformer_ = ColumnTransformer(
            transformers=transformers,
            remainder="drop",
            verbose_feature_names_out=True,
        )
        self.transformer_.fit(frame)
        self.feature_names_in_ = list(frame.columns)
        self.n_features_out_ = len(self.transformer_.get_feature_names_out())
        return self

    def transform(self, X: pd.DataFrame):
        """Transform rows using training-fitted statistics and categories."""
        check_is_fitted(self, attributes=["transformer_", "feature_names_in_"])
        frame = self._validate_frame(X)
        return self.transformer_.transform(frame)

    def get_feature_names_out(self, input_features=None):
        """Return stable names for encoded assay-context dimensions."""
        check_is_fitted(self, attributes=["transformer_"])
        return self.transformer_.get_feature_names_out(input_features)



def attach_context_archive(
    feature_archive: str,
    context_csv: str,
    output_archive: str,
    *,
    numeric_columns: Sequence[str] = ("ph", "temperature_k"),
    categorical_columns: Sequence[str] = ("organism", "assay_method", "cofactor"),
    id_column: str = "source_record_id",
) -> str:
    """Attach raw assay context for fold-local preprocessing during CV.

    Unlike pre-encoding, this stores raw context arrays. The modeling pipeline
    fits imputation, scaling, and category vocabularies independently inside
    each cross-validation fold, preventing validation-fold preprocessing
    leakage. Source record IDs and row order must match exactly.
    """
    from pathlib import Path

    import numpy as np

    archive_path = Path(feature_archive)
    csv_path = Path(context_csv)
    output_path = Path(output_archive)
    if not archive_path.is_file() or not csv_path.is_file():
        raise FileNotFoundError("feature archive and context CSV must both exist")
    selected = [*numeric_columns, *categorical_columns]
    if not selected or len(selected) != len(set(selected)):
        raise ValueError("context feature columns must be non-empty and unique")
    if id_column in selected:
        raise ValueError("the record ID column cannot also be a context feature")
    context_frame = pd.read_csv(csv_path)
    required = [id_column, *selected]
    missing = [column for column in required if column not in context_frame.columns]
    if missing:
        raise ValueError(f"context CSV is missing columns: {missing}")
    with np.load(archive_path, allow_pickle=False) as data:
        arrays = {key: data[key] for key in data.files}
    if "source_record_ids" not in arrays or "X" not in arrays:
        raise ValueError("feature archive requires X and source_record_ids arrays")
    archive_ids = arrays["source_record_ids"].astype(str).reshape(-1)
    context_ids = context_frame[id_column].astype(str).to_numpy()
    if len(archive_ids) != len(context_ids) or not np.array_equal(archive_ids, context_ids):
        raise ValueError("context IDs must exactly match feature archive IDs and row order")
    base = np.asarray(arrays["X"], dtype=np.float32)
    if base.ndim != 2 or len(base) != len(context_frame):
        raise ValueError("base feature rows do not align with context metadata")
    base_names = {f"base_{index}" for index in range(base.shape[1])}
    if base_names.intersection(selected):
        raise ValueError("context column names cannot collide with generated base feature names")
    arrays["X_base"] = base.copy()
    arrays["context_numeric_columns"] = np.asarray(tuple(numeric_columns), dtype=str)
    arrays["context_categorical_columns"] = np.asarray(tuple(categorical_columns), dtype=str)
    for column in numeric_columns:
        numeric_values = pd.to_numeric(
            context_frame[column], errors="coerce"
        ).to_numpy(dtype=np.float64)
        numeric_values[~np.isfinite(numeric_values)] = np.nan
        arrays[f"context_raw__{column}"] = numeric_values
    for column in categorical_columns:
        values = context_frame[column].where(context_frame[column].notna(), "__MISSING__")
        arrays[f"context_raw__{column}"] = values.astype(str).to_numpy()
    # X remains the base representation; fold-local pipeline handles raw context.
    arrays["X"] = base
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(output_path, **arrays)
    return str(output_path)


def context_design_matrix(payload: dict[str, np.ndarray]) -> pd.DataFrame:
    """Build a named mixed-type matrix from an archive with attached raw context."""
    import numpy as np

    base = np.asarray(payload.get("X_base", payload["X"]), dtype=np.float32)
    frame = pd.DataFrame(
        base, columns=[f"base_{index}" for index in range(base.shape[1])]
    )
    numeric = payload.get("context_numeric_columns", np.asarray([], dtype=str)).astype(str)
    categorical = payload.get(
        "context_categorical_columns", np.asarray([], dtype=str)
    ).astype(str)
    for column in numeric:
        key = f"context_raw__{column}"
        if key not in payload:
            raise ValueError(f"Missing raw context array: {column}")
        frame[column] = np.asarray(payload[key], dtype=float)
    for column in categorical:
        key = f"context_raw__{column}"
        if key not in payload:
            raise ValueError(f"Missing raw context array: {column}")
        frame[column] = np.asarray(payload[key]).astype(str)
    return frame


def make_context_pipeline(estimator, *, numeric_columns, categorical_columns, base_dimension):
    """Create a fold-local preprocessing/model pipeline for assay context."""
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    base_columns = [f"base_{index}" for index in range(base_dimension)]
    transformers = [("base", "passthrough", base_columns)]
    if numeric_columns:
        transformers.append((
            "numeric",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
                ("scaler", StandardScaler()),
            ]),
            list(numeric_columns),
        ))
    if categorical_columns:
        transformers.append((
            "categorical",
            Pipeline([
                ("imputer", SimpleImputer(strategy="constant", fill_value="__MISSING__")),
                ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
            ]),
            list(categorical_columns),
        ))
    preprocessing = ColumnTransformer(
        transformers=transformers, remainder="drop", verbose_feature_names_out=True
    )
    return Pipeline([("preprocessing", preprocessing), ("estimator", estimator)])
