"""Transparent count-table normalisation and correlation primitives."""
from __future__ import annotations
from math import sqrt

def cpm(counts: list[list[float]]) -> list[list[float]]:
    if not counts or not counts[0] or any(len(row)!=len(counts[0]) for row in counts):
        raise ValueError("Counts must be a non-empty rectangular matrix")
    if any(v<0 for row in counts for v in row): raise ValueError("Counts cannot be negative")
    columns=len(counts[0]); totals=[sum(row[j] for row in counts) for j in range(columns)]
    if any(total==0 for total in totals): raise ValueError("Cannot normalise a zero-library column")
    return [[row[j]*1_000_000/totals[j] for j in range(columns)] for row in counts]

def pearson(x:list[float],y:list[float]) -> float:
    if len(x)!=len(y) or len(x)<3: raise ValueError("Need >=3 paired values")
    mx,my=sum(x)/len(x),sum(y)/len(y)
    dx,dy=[v-mx for v in x],[v-my for v in y]
    denom=sqrt(sum(v*v for v in dx)*sum(v*v for v in dy))
    if denom==0: raise ValueError("Correlation undefined for constant input")
    return sum(a*b for a,b in zip(dx,dy))/denom

def log2_fold_change(group_a:list[float],group_b:list[float], *, pseudocount:float=0.5) -> float:
    if not group_a or not group_b or pseudocount<=0: raise ValueError("Groups must be non-empty and pseudocount positive")
    if any(v<0 for v in group_a+group_b): raise ValueError("Counts cannot be negative")
    mean_a=sum(group_a)/len(group_a); mean_b=sum(group_b)/len(group_b)
    import math
    return math.log2((mean_a+pseudocount)/(mean_b+pseudocount))


def shannon_diversity(counts: list[float]) -> float:
    from math import log

    if not counts or any(value < 0 for value in counts):
        raise ValueError("Counts must be a non-empty non-negative vector")
    total = sum(counts)
    if total == 0:
        raise ValueError("Total abundance must be positive")
    return -sum((value / total) * log(value / total) for value in counts if value > 0)


def simpson_diversity(counts: list[float]) -> float:
    if not counts or any(value < 0 for value in counts):
        raise ValueError("Counts must be a non-empty non-negative vector")
    total = sum(counts)
    if total <= 1:
        raise ValueError("At least two observations are required")
    return 1 - sum(value * (value - 1) for value in counts) / (total * (total - 1))


def clr_transform(matrix: list[list[float]], *, pseudocount: float = 0.5) -> list[list[float]]:
    from math import log

    if not matrix or not matrix[0] or pseudocount <= 0:
        raise ValueError("Require a non-empty matrix and positive pseudocount")
    width = len(matrix[0])
    if any(len(row) != width for row in matrix) or any(
        value < 0 for row in matrix for value in row
    ):
        raise ValueError("Matrix must be rectangular and non-negative")
    output: list[list[float]] = []
    for column in range(width):
        logs = [log(matrix[row][column] + pseudocount) for row in range(len(matrix))]
        center = sum(logs) / len(logs)
        output.append([value - center for value in logs])
    return [list(row) for row in zip(*output)]
