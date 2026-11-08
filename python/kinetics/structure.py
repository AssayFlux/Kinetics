"""Conservative PDB parsing and geometry, including optional rigid-body RMSD fitting."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Iterable


@dataclass(frozen=True)
class Atom:
    serial: int
    name: str
    residue: str
    chain: str
    residue_number: int
    x: float
    y: float
    z: float
    element: str


def parse_pdb(text: str, *, include_hetero: bool = False) -> list[Atom]:
    atoms = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if not (line.startswith("ATOM  ") or (include_hetero and line.startswith("HETATM"))):
            continue
        if len(line) < 54:
            raise ValueError(f"PDB line {line_no}: truncated coordinate record")
        if line[16:17] not in (" ", "A"):
            continue
        try:
            atoms.append(
                Atom(
                    int(line[6:11]), line[12:16].strip(), line[17:20].strip(),
                    line[21:22].strip(), int(line[22:26]), float(line[30:38]),
                    float(line[38:46]), float(line[46:54]),
                    line[76:78].strip().upper() if len(line) >= 78 else "",
                )
            )
        except ValueError as exc:
            raise ValueError(f"PDB line {line_no}: invalid atom field") from exc
        if not all(isfinite(value) for value in (atoms[-1].x, atoms[-1].y, atoms[-1].z)):
            raise ValueError(f"PDB line {line_no}: coordinates must be finite")
    if not atoms:
        raise ValueError("No supported PDB coordinate records")
    return atoms


def _largest_symmetric_eigenvector(matrix: list[list[float]]) -> list[float]:
    """Jacobi eigensolver for a real symmetric 4x4 matrix."""
    size = 4
    values = [row[:] for row in matrix]
    vectors = [[1.0 if row == col else 0.0 for col in range(size)] for row in range(size)]
    for _ in range(100):
        p, q = max(
            ((i, j) for i in range(size) for j in range(i + 1, size)),
            key=lambda pair: abs(values[pair[0]][pair[1]]),
        )
        if abs(values[p][q]) < 1e-14:
            break
        app, aqq, apq = values[p][p], values[q][q], values[p][q]
        tau = (aqq - app) / (2.0 * apq)
        sign = 1.0 if tau >= 0 else -1.0
        tangent = sign / (abs(tau) + sqrt(1.0 + tau * tau))
        cosine = 1.0 / sqrt(1.0 + tangent * tangent)
        sine = tangent * cosine

        values[p][p] = app - tangent * apq
        values[q][q] = aqq + tangent * apq
        values[p][q] = values[q][p] = 0.0
        for k in range(size):
            if k in (p, q):
                continue
            vkp, vkq = values[k][p], values[k][q]
            values[k][p] = values[p][k] = cosine * vkp - sine * vkq
            values[k][q] = values[q][k] = sine * vkp + cosine * vkq
            vkp, vkq = vectors[k][p], vectors[k][q]
            vectors[k][p] = cosine * vkp - sine * vkq
            vectors[k][q] = sine * vkp + cosine * vkq

    index = max(range(size), key=lambda item: values[item][item])
    vector = [vectors[row][index] for row in range(size)]
    norm = sqrt(sum(value * value for value in vector))
    if norm == 0:
        raise ValueError("Rigid-body fit failed to determine a rotation")
    return [value / norm for value in vector]


def _optimal_rotation(mobile: list[tuple[float, float, float]],
                      reference: list[tuple[float, float, float]]) -> list[list[float]]:
    covariance = [[0.0] * 3 for _ in range(3)]
    for moving, target in zip(mobile, reference):
        for row in range(3):
            for col in range(3):
                covariance[row][col] += moving[row] * target[col]
    sxx, sxy, sxz = covariance[0]
    syx, syy, syz = covariance[1]
    szx, szy, szz = covariance[2]
    trace = sxx + syy + szz
    horn = [
        [trace, syz - szy, szx - sxz, sxy - syx],
        [syz - szy, sxx - syy - szz, sxy + syx, szx + sxz],
        [szx - sxz, sxy + syx, -sxx + syy - szz, syz + szy],
        [sxy - syx, szx + sxz, syz + szy, -sxx - syy + szz],
    ]
    w, x, y, z = _largest_symmetric_eigenvector(horn)
    return [
        [w*w + x*x - y*y - z*z, 2*(x*y - w*z), 2*(x*z + w*y)],
        [2*(x*y + w*z), w*w - x*x + y*y - z*z, 2*(y*z - w*x)],
        [2*(x*z - w*y), 2*(y*z + w*x), w*w - x*x - y*y + z*z],
    ]


def rmsd(reference: Iterable[Atom], mobile: Iterable[Atom], *, superpose: bool = False) -> float:
    """RMSD in angstroms; optional Horn quaternion rigid-body least-squares fit."""
    first, second = list(reference), list(mobile)
    if len(first) != len(second) or not first:
        raise ValueError("Coordinate sets must have equal non-zero length")
    target = [(atom.x, atom.y, atom.z) for atom in first]
    moving = [(atom.x, atom.y, atom.z) for atom in second]
    if not all(isfinite(value) for point in target + moving for value in point):
        raise ValueError("Coordinate sets must contain only finite values")
    if not superpose:
        return sqrt(sum(sum((a - b) ** 2 for a, b in zip(p, q))
                        for p, q in zip(target, moving)) / len(first))

    target_center = tuple(sum(point[i] for point in target) / len(target) for i in range(3))
    moving_center = tuple(sum(point[i] for point in moving) / len(moving) for i in range(3))
    target_centered = [tuple(point[i] - target_center[i] for i in range(3)) for point in target]
    moving_centered = [tuple(point[i] - moving_center[i] for i in range(3)) for point in moving]
    rotation = _optimal_rotation(moving_centered, target_centered)
    squared = 0.0
    for point, expected in zip(moving_centered, target_centered):
        rotated = tuple(sum(rotation[i][j] * point[j] for j in range(3)) for i in range(3))
        squared += sum((rotated[i] - expected[i]) ** 2 for i in range(3))
    return sqrt(squared / len(first))


def contact_pairs(atoms: Iterable[Atom], cutoff_angstrom: float = 8.0) -> list[tuple[int, int, float]]:
    points = list(atoms)
    if not isfinite(cutoff_angstrom) or cutoff_angstrom <= 0:
        raise ValueError("cutoff must be finite and positive")
    result = []
    for i, first in enumerate(points):
        for j in range(i + 1, len(points)):
            second = points[j]
            if first.chain == second.chain and first.residue_number == second.residue_number:
                continue
            distance = sqrt(
                (first.x - second.x) ** 2 + (first.y - second.y) ** 2 + (first.z - second.z) ** 2
            )
            if distance <= cutoff_angstrom:
                result.append((i, j, distance))
    return result
