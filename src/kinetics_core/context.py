"""Leakage-aware preprocessing for optional enzyme assay context.

Only explicitly selected columns are encoded. Fit this transformer on training
rows only, then reuse the fitted instance for validation/test/inference data.
Do not include record IDs, publication IDs, or other target-leaking identifiers.
"""

from __future__ import annotations

from typing import Sequence

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils.validation import check_is_fitted
from sklearn.base import BaseEstimator, TransformerMixin


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
                    ("imputer", SimpleImputer(strategy="median", add_indicator=True)),
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



def augment_feature_archive(
    feature_archive: str,
    context_csv: str,
    output_archive: str,
    *,
    numeric_columns: Sequence[str] = ("ph", "temperature_k"),
    categorical_columns: Sequence[str] = ("organism", "assay_method", "cofactor"),
    encoder_path: str | None = None,
    fit_encoder: bool = False,
    id_column: str = "source_record_id",
) -> str:
    """Append assay-context features to an NPZ while enforcing row identity.

    Fit mode is intended for the training archive only and persists the fitted
    encoder. Transform mode loads that exact encoder for calibration/test data.
    The CSV must contain one row per feature row in identical order, keyed by
    the source record ID. No join/reordering is performed implicitly.
    """
    from pathlib import Path

    import joblib
    import numpy as np

    archive_path = Path(feature_archive)
    csv_path = Path(context_csv)
    output_path = Path(output_archive)
    if not archive_path.is_file() or not csv_path.is_file():
        raise FileNotFoundError("feature archive and context CSV must both exist")
    if not encoder_path:
        raise ValueError("encoder_path is required to persist or load the context encoder")
    with np.load(archive_path, allow_pickle=False) as data:
        arrays = {key: data[key] for key in data.files}
    if "source_record_ids" not in arrays:
        raise ValueError("feature archive must contain source_record_ids for alignment")
    context_frame = pd.read_csv(csv_path)
    if id_column not in context_frame:
        raise ValueError(f"context CSV is missing identity column {id_column!r}")
    archive_ids = arrays["source_record_ids"].astype(str).reshape(-1)
    context_ids = context_frame[id_column].astype(str).to_numpy()
    if len(archive_ids) != len(context_ids) or not np.array_equal(archive_ids, context_ids):
        raise ValueError(
            "context CSV record IDs must exactly match feature archive IDs and row order"
        )
    encoder_file = Path(encoder_path)
    if fit_encoder:
        if encoder_file.exists():
            raise FileExistsError(
                f"Refusing to overwrite fitted encoder: {encoder_file}; choose a new path"
            )
        encoder = AssayContextEncoder(
            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
        )
        encoded = encoder.fit_transform(context_frame)
        encoder_file.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(encoder, encoder_file, compress=3)
    else:
        if not encoder_file.is_file():
            raise FileNotFoundError(encoder_file)
        encoder = joblib.load(encoder_file)
        if tuple(encoder.numeric_columns) != tuple(numeric_columns):
            raise ValueError("loaded encoder numeric columns differ from requested columns")
        if tuple(encoder.categorical_columns) != tuple(categorical_columns):
            raise ValueError("loaded encoder categorical columns differ from requested columns")
        encoded = encoder.transform(context_frame)
    encoded = np.asarray(encoded, dtype=np.float32)
    base = np.asarray(arrays["X"], dtype=np.float32)
    if encoded.ndim != 2 or encoded.shape[0] != base.shape[0]:
        raise ValueError("encoded context rows do not align with base feature matrix")
    arrays["X"] = np.concatenate([base, encoded], axis=1).astype(np.float32)
    arrays["context_feature_names"] = encoder.get_feature_names_out().astype(str)
    arrays["context_encoder_path"] = np.asarray([str(encoder_file)])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(output_path, **arrays)
    return str(output_path)
