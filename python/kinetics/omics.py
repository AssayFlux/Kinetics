"""Transparent exploratory count-table normalisation and omics statistics."""
from __future__ import annotations

from math import exp, isfinite, log, log2, sqrt


def _finite(values: list[float], label: str) -> None:
    if not all(isfinite(value) for value in values):
        raise ValueError(f"{label} must contain only finite values")


def cpm(counts: list[list[float]]) -> list[list[float]]:
    if not counts or not counts[0] or any(len(row) != len(counts[0]) for row in counts):
        raise ValueError("Counts must be a non-empty rectangular matrix")
    flattened = [value for row in counts for value in row]
    _finite(flattened, "Counts")
    if any(value < 0 for value in flattened):
        raise ValueError("Counts cannot be negative")
    columns = len(counts[0])
    totals = [sum(row[j] for row in counts) for j in range(columns)]
    if any(total == 0 for total in totals):
        raise ValueError("Cannot normalise a zero-library column")
    return [[row[j] * 1_000_000 / totals[j] for j in range(columns)] for row in counts]


def pearson(x: list[float], y: list[float]) -> float:
    if len(x) != len(y) or len(x) < 3:
        raise ValueError("Need >=3 paired values")
    _finite(x + y, "Correlation inputs")
    mx, my = sum(x) / len(x), sum(y) / len(y)
    dx, dy = [value - mx for value in x], [value - my for value in y]
    denom = sqrt(sum(value * value for value in dx) * sum(value * value for value in dy))
    if denom == 0:
        raise ValueError("Correlation undefined for constant input")
    return sum(a * b for a, b in zip(dx, dy)) / denom


def log2_fold_change(
    group_a: list[float], group_b: list[float], *, pseudocount: float = 0.5,
) -> float:
    if not group_a or not group_b or not isfinite(pseudocount) or pseudocount <= 0:
        raise ValueError("Groups must be non-empty and pseudocount finite and positive")
    _finite(group_a + group_b, "Counts")
    if any(value < 0 for value in group_a + group_b):
        raise ValueError("Counts cannot be negative")
    mean_a = sum(group_a) / len(group_a)
    mean_b = sum(group_b) / len(group_b)
    return log2((mean_a + pseudocount) / (mean_b + pseudocount))


def shannon_diversity(counts: list[float]) -> float:
    if not counts:
        raise ValueError("Counts must be a non-empty non-negative vector")
    _finite(counts, "Counts")
    if any(value < 0 for value in counts):
        raise ValueError("Counts must be non-negative")
    total = sum(counts)
    if total <= 0:
        raise ValueError("Total abundance must be positive")
    return -sum((value / total) * log(value / total) for value in counts if value > 0)


def simpson_diversity(counts: list[float]) -> float:
    """Return Gini-Simpson diversity (1 - sum of squared relative abundances)."""
    if not counts:
        raise ValueError("Counts must be a non-empty non-negative vector")
    _finite(counts, "Counts")
    if any(value < 0 for value in counts):
        raise ValueError("Counts must be non-negative")
    total = sum(counts)
    if total <= 0:
        raise ValueError("Total abundance must be positive")
    return 1.0 - sum((value / total) ** 2 for value in counts)


def clr_transform(
    matrix: list[list[float]], *, pseudocount: float = 0.5,
) -> list[list[float]]:
    if not matrix or not matrix[0] or not isfinite(pseudocount) or pseudocount <= 0:
        raise ValueError("Require a non-empty matrix and finite positive pseudocount")
    width = len(matrix[0])
    flattened = [value for row in matrix for value in row]
    if any(len(row) != width for row in matrix):
        raise ValueError("Matrix must be rectangular")
    _finite(flattened, "Matrix")
    if any(value < 0 for value in flattened):
        raise ValueError("Matrix must be non-negative")
    output: list[list[float]] = []
    for column in range(width):
        logs = [log(matrix[row][column] + pseudocount) for row in range(len(matrix))]
        center = sum(logs) / len(logs)
        output.append([value - center for value in logs])
    return [list(row) for row in zip(*output)]


def logistic_growth(
    timepoints: list[float], counts: list[float], *,
    carrying_capacity: float, growth_rate: float, initial: float,
) -> list[float]:
    if len(timepoints) != len(counts) or not timepoints:
        raise ValueError("Timepoints and counts must have equal non-zero lengths")
    _finite(timepoints + counts + [carrying_capacity, growth_rate, initial], "Model inputs")
    if carrying_capacity <= 0 or growth_rate <= 0 or initial <= 0:
        raise ValueError("Model parameters must be positive")
    if any(time < 0 for time in timepoints) or any(value < 0 for value in counts):
        raise ValueError("Timepoints and counts must be non-negative")
    return [
        carrying_capacity
        / (1 + ((carrying_capacity - initial) / initial) * exp(-growth_rate * time))
        for time in timepoints
    ]


def cross_omics_correlation(
    first: list[list[float]], second: list[list[float]],
) -> list[list[float]]:
    """Pairwise feature correlations; rows are features, columns are matched samples."""
    if not first or not second or not first[0] or not second[0]:
        raise ValueError("Both omics matrices must be non-empty")
    sample_count = len(first[0])
    if any(len(row) != sample_count for row in first + second):
        raise ValueError("All features must share the same sample order and count")
    return [[pearson(left, right) for right in second] for left in first]
