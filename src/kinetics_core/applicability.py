"""Training-reference applicability-domain diagnostics.

This is a descriptive feature-space warning, not a calibrated probability that
a prediction is correct. The threshold is learned from leave-one-out distances
within the reference training set and must be reported with its configuration.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.neighbors import NearestNeighbors


@dataclass
class ApplicabilityDomain:
    """Nearest-neighbour feature-space monitor fitted on reference training rows."""

    quantile: float = 0.95
    metric: str = "euclidean"

    def fit(self, X):
        matrix = np.asarray(X, dtype=np.float64)
        if matrix.ndim != 2 or matrix.shape[0] < 3 or matrix.shape[1] < 1:
            raise ValueError("reference features must be 2D with at least three rows")
        if not np.isfinite(matrix).all():
            raise ValueError("reference features must be finite")
        if not 0.5 < self.quantile < 1.0:
            raise ValueError("quantile must be between 0.5 and 1.0")
        self.center_ = np.median(matrix, axis=0)
        q25, q75 = np.quantile(matrix, [0.25, 0.75], axis=0)
        scale = q75 - q25
        scale[scale <= np.finfo(float).eps] = 1.0
        self.scale_ = scale
        standardized = (matrix - self.center_) / self.scale_
        self.reference_ = standardized
        self.neighbors_ = NearestNeighbors(n_neighbors=2, metric=self.metric)
        self.neighbors_.fit(standardized)
        # The first neighbor is the row itself; the second is its nearest peer.
        loo_distances = self.neighbors_.kneighbors(standardized, return_distance=True)[0][:, 1]
        self.threshold_ = float(np.quantile(loo_distances, self.quantile))
        self.reference_size_ = int(matrix.shape[0])
        self.feature_dimension_ = int(matrix.shape[1])
        return self

    def score(self, X):
        """Return nearest-reference distances and an above-threshold warning."""
        if not hasattr(self, "neighbors_"):
            raise RuntimeError("ApplicabilityDomain must be fitted before score")
        matrix = np.asarray(X, dtype=np.float64)
        if matrix.ndim != 2 or matrix.shape[1] != self.feature_dimension_:
            raise ValueError("query feature dimensions do not match fitted reference")
        if not np.isfinite(matrix).all():
            raise ValueError("query features must be finite")
        standardized = (matrix - self.center_) / self.scale_
        distances = self.neighbors_.kneighbors(
            standardized, n_neighbors=1, return_distance=True
        )[0][:, 0]
        return {
            "nearest_reference_distance": distances,
            "threshold": self.threshold_,
            "quantile": self.quantile,
            "within_domain": distances <= self.threshold_,
            "method": "robust_iqr_scaled_nearest_neighbor",
            "reference_size": self.reference_size_,
            "interpretation": (
                "Feature-space similarity warning only; not a probability of correctness "
                "or a substitute for external validation."
            ),
        }
