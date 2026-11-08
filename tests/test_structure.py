from __future__ import annotations

import pytest

from kinetics.structure import Atom, rmsd


def atom(serial: int, x: float, y: float, z: float) -> Atom:
    return Atom(serial, "CA", "GLY", "A", serial, x, y, z, "C")


def test_rmsd_without_superposition_measures_raw_coordinates() -> None:
    reference = [atom(1, 0, 0, 0), atom(2, 1, 0, 0), atom(3, 0, 1, 0)]
    translated = [atom(1, 5, 2, 0), atom(2, 6, 2, 0), atom(3, 5, 3, 0)]
    assert rmsd(reference, translated) > 1


def test_rmsd_superposition_removes_rigid_rotation_and_translation() -> None:
    reference = [
        atom(1, 0, 0, 0), atom(2, 1, 0, 0),
        atom(3, 0, 1, 0), atom(4, 0, 0, 1),
    ]
    # Mobile coordinates are rotated +90 degrees around Z and translated.
    mobile = [
        atom(1, 5, -2, 3), atom(2, 5, -1, 3),
        atom(3, 4, -2, 3), atom(4, 5, -2, 4),
    ]
    assert rmsd(reference, mobile, superpose=True) == pytest.approx(0, abs=1e-8)


def test_rmsd_requires_equal_non_empty_coordinate_sets() -> None:
    with pytest.raises(ValueError):
        rmsd([atom(1, 0, 0, 0)], [])
