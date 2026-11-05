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
