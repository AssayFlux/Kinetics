"""Transparent exploratory count-table normalisation and omics statistics."""
from __future__ import annotations

from math import exp, isfinite, log, log1p, log2, sqrt


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


def _beta_continued_fraction(a: float, b: float, x: float) -> float:
    """Modified Lentz continued fraction for the incomplete beta function."""
    max_iterations, epsilon, tiny = 300, 3e-14, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, max_iterations + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < epsilon:
            return h
    raise ArithmeticError("Incomplete beta continued fraction did not converge")


def _regularized_beta(x: float, a: float, b: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    from math import lgamma

    front = exp(lgamma(a + b) - lgamma(a) - lgamma(b) + a * log(x) + b * log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _beta_continued_fraction(a, b, x) / a
    return 1.0 - front * _beta_continued_fraction(b, a, 1.0 - x) / b


def _student_two_sided_p(statistic: float, degrees_freedom: float) -> float:
    if degrees_freedom <= 0 or not isfinite(degrees_freedom):
        raise ValueError("Welch degrees of freedom must be finite and positive")
    x = degrees_freedom / (degrees_freedom + statistic * statistic)
    return min(1.0, max(0.0, _regularized_beta(x, degrees_freedom / 2.0, 0.5)))


def welch_differential_expression(
    values: list[list[float]], group_a: list[int], group_b: list[int], *,
    feature_ids: list[str] | None = None,
) -> list[dict[str, float | str]]:
    """Exploratory two-group Welch tests on pre-normalized/log-scale feature values.

    Rows are features and columns are independent biological samples. This function
    does not normalize counts, model covariates/batches, or correct for study design.
    Benjamini-Hochberg q-values are returned across the supplied feature family.
    """
    if not values or not values[0] or not group_a or not group_b:
        raise ValueError("Feature matrix and both sample groups must be non-empty")
    width = len(values[0])
    if any(len(row) != width for row in values):
        raise ValueError("Feature matrix must be rectangular")
    if len(group_a) < 2 or len(group_b) < 2:
        raise ValueError("Welch testing requires at least two samples per group")
    indices = group_a + group_b
    if len(set(indices)) != len(indices) or any(index < 0 or index >= width for index in indices):
        raise ValueError("Sample indices must be unique, disjoint and within matrix bounds")
    if feature_ids is None:
        feature_ids = [str(index) for index in range(len(values))]
    if len(feature_ids) != len(values) or len(set(feature_ids)) != len(feature_ids):
        raise ValueError("Feature identifiers must be unique and match matrix rows")
    _finite([value for row in values for value in row], "Differential-expression values")

    raw: list[dict[str, float | str]] = []
    for index, row in enumerate(values):
        left = [row[i] for i in group_a]
        right = [row[i] for i in group_b]
        mean_a, mean_b = sum(left) / len(left), sum(right) / len(right)
        var_a = sum((x - mean_a) ** 2 for x in left) / (len(left) - 1)
        var_b = sum((x - mean_b) ** 2 for x in right) / (len(right) - 1)
        term_a, term_b = var_a / len(left), var_b / len(right)
        standard_error = sqrt(term_a + term_b)
        difference = mean_a - mean_b
        if standard_error == 0:
            statistic, p_value = (0.0, 1.0) if difference == 0 else (float("inf"), 0.0)
        else:
            statistic = difference / standard_error
            denominator = term_a * term_a / (len(left) - 1) + term_b * term_b / (len(right) - 1)
            degrees = (term_a + term_b) ** 2 / denominator
            p_value = _student_two_sided_p(abs(statistic), degrees)
        raw.append({
            "feature_id": feature_ids[index], "mean_group_a": mean_a,
            "mean_group_b": mean_b, "difference": difference,
            "welch_t": statistic, "p_value": p_value, "q_value": 1.0,
        })

    order = sorted(range(len(raw)), key=lambda i: float(raw[i]["p_value"]))
    running = 1.0
    count = len(raw)
    for rank_index in range(count - 1, -1, -1):
        position = order[rank_index]
        adjusted = min(1.0, float(raw[position]["p_value"]) * count / (rank_index + 1))
        running = min(running, adjusted)
        raw[position]["q_value"] = running
    return raw
