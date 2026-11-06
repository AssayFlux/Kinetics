"""Canonical observation contracts for enzyme kinetic measurements.

Km and kcat are represented as independent observations. A source record is never
paired with another target unless the source explicitly establishes that link.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Literal

Target = Literal["km", "kcat"]
MeasurementKind = Literal["individual_measurement", "source_aggregated"]

_KM_TO_M = {"M": 1.0, "mM": 1e-3, "uM": 1e-6, "µM": 1e-6, "nM": 1e-9}
_KCAT_TO_S = {"s^-1": 1.0, "s-1": 1.0, "min^-1": 1.0 / 60.0, "h^-1": 1.0 / 3600.0}


@dataclass(frozen=True, slots=True)
class KineticObservation:
    """One measured kinetic parameter with source and assay context."""

    target: Target
    value: float
    unit: str
    source: str
    source_record_id: str
    sequence: str | None = None
    smiles: str | None = None
    protein_accession: str | None = None
    organism: str | None = None
    ph: float | None = None
    temperature_k: float | None = None
    assay_id: str | None = None
    publication_doi: str | None = None
    source_version: str | None = None
    license_id: str | None = None
    measurement_kind: MeasurementKind = "individual_measurement"
    aggregation_method: str | None = None

    def __post_init__(self) -> None:
        if self.target not in ("km", "kcat"):
            raise ValueError("target must be 'km' or 'kcat'")
        if self.measurement_kind not in ("individual_measurement", "source_aggregated"):
            raise ValueError("unsupported measurement_kind")
        if self.measurement_kind == "source_aggregated" and not self.aggregation_method:
            raise ValueError("source_aggregated observations require aggregation_method")
        if self.measurement_kind == "individual_measurement" and self.aggregation_method:
            raise ValueError("individual measurements cannot declare an aggregation_method")
        if not math.isfinite(float(self.value)) or float(self.value) <= 0:
            raise ValueError("kinetic measurement must be finite and strictly positive")
        if not self.source.strip() or not self.source_record_id.strip():
            raise ValueError("source and source_record_id are required")
        if self.ph is not None and not math.isfinite(float(self.ph)):
            raise ValueError("pH must be finite when provided")
        if self.temperature_k is not None and (
            not math.isfinite(float(self.temperature_k)) or float(self.temperature_k) <= 0
        ):
            raise ValueError("temperature_k must be finite and positive when provided")

    def canonical_value(self) -> float:
        """Return Km in molar (M) or kcat in reciprocal seconds (s^-1)."""
        factors = _KM_TO_M if self.target == "km" else _KCAT_TO_S
        if self.unit not in factors:
            raise ValueError(
                f"Unsupported unit {self.unit!r} for {self.target}; "
                f"supported units: {sorted(factors)}"
            )
        return float(self.value) * factors[self.unit]

    def as_dict(self) -> dict:
        row = asdict(self)
        row["canonical_value"] = self.canonical_value()
        row["canonical_unit"] = "M" if self.target == "km" else "s^-1"
        return row


def canonicalize_measurement(target: Target, value: float, unit: str) -> tuple[float, str]:
    """Validate and convert a single measurement to its canonical SI-compatible unit."""
    if target not in ("km", "kcat"):
        raise ValueError("target must be 'km' or 'kcat'")
    factors = _KM_TO_M if target == "km" else _KCAT_TO_S
    if unit not in factors:
        raise ValueError(f"Unsupported unit {unit!r} for {target}; choose {sorted(factors)}")
    numeric = float(value)
    if not math.isfinite(numeric) or numeric <= 0:
        raise ValueError("measurement must be finite and strictly positive")
    return numeric * factors[unit], ("M" if target == "km" else "s^-1")
