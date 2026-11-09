#!/usr/bin/env python3
"""Compare the structural parser and geometry primitives with Biopython/NumPy.

Synthetic fixtures validate software concordance only; they are not an
experimental structural benchmark or a biological-assembly validation.
"""
from __future__ import annotations

from io import StringIO
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

try:
    import Bio
    import numpy as np
    from Bio.PDB import PDBParser
except ImportError as error:
    raise SystemExit(
        "Install validation/requirements-biopython.txt and validation/requirements-scipy.txt"
    ) from error

from kinetics.structure import contact_pairs, parse_pdb, rmsd


def atom_line(
    serial: int,
    name: str,
    residue_number: int,
    xyz: tuple[float, float, float],
    element: str,
) -> str:
    x, y, z = xyz
    return (
        f"ATOM  {serial:5d} {name:<4s} GLY A{residue_number:4d}    "
        f"{x:8.3f}{y:8.3f}{z:8.3f}{1.0:6.2f}{20.0:6.2f}"
        f"          {element:>2s}\n"
    )


def pdb_text(coordinates: list[tuple[float, float, float]]) -> str:
    atoms = [(1, "N", "N"), (2, "CA", "C"), (3, "C", "C"), (4, "O", "O")]
    return "".join(
        atom_line(serial, name, serial, coordinates[serial - 1], element)
        for serial, name, element in atoms
    ) + "END\n"


def parse_biopython(text: str):
    return list(PDBParser(QUIET=True).get_structure("reference", StringIO(text)).get_atoms())


def numpy_superposed_rmsd(reference: np.ndarray, mobile: np.ndarray) -> float:
    """Independent row-vector Kabsch fit using NumPy's SVD."""
    reference_center = reference.mean(axis=0)
    mobile_center = mobile.mean(axis=0)
    target = reference - reference_center
    moving = mobile - mobile_center
    left, _, right = np.linalg.svd(moving.T @ target)
    correction = np.eye(3)
    correction[2, 2] = np.linalg.det(left @ right)
    rotation = left @ correction @ right
    aligned = moving @ rotation + reference_center
    return float(np.sqrt(np.mean(np.sum((aligned - reference) ** 2, axis=1))))


def run() -> dict[str, object]:
    reference_xyz = [
        (0.0, 0.0, 0.0), (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0), (0.0, 0.0, 1.0),
    ]
    mobile_xyz = [
        (5.0, -2.0, 3.0), (5.0, -1.0, 3.0),
        (4.0, -2.0, 3.0), (5.15, -2.0, 4.0),
    ]
    reference_text = pdb_text(reference_xyz)
    mobile_text = pdb_text(mobile_xyz)
    local_reference = parse_pdb(reference_text)
    local_mobile = parse_pdb(mobile_text)
    bio_reference = parse_biopython(reference_text)
    bio_mobile = parse_biopython(mobile_text)

    metadata_match = len(local_reference) == len(bio_reference)
    max_coordinate_delta = 0.0
    if metadata_match:
        for local, reference in zip(local_reference, bio_reference):
            metadata_match = metadata_match and (
                local.serial == reference.get_serial_number()
                and local.name == reference.get_name().strip()
                and local.residue == reference.get_parent().get_resname()
                and local.chain == reference.get_parent().get_parent().id
                and local.residue_number == reference.get_parent().id[1]
                and local.element == reference.element.upper()
            )
            max_coordinate_delta = max(
                max_coordinate_delta,
                float(np.max(np.abs(
                    np.asarray((local.x, local.y, local.z), dtype=float)
                    - reference.coord.astype(float)
                ))),
            )
    parser_pass = metadata_match and max_coordinate_delta <= 1e-5

    cutoff = 1.1
    expected_contacts = []
    bio_coordinates = np.asarray([atom.coord for atom in bio_reference], dtype=float)
    for first in range(len(bio_reference)):
        for second in range(first + 1, len(bio_reference)):
            first_residue = bio_reference[first].get_parent()
            second_residue = bio_reference[second].get_parent()
            if (
                first_residue.get_parent().id == second_residue.get_parent().id
                and first_residue.id[1] == second_residue.id[1]
            ):
                continue
            distance = float(np.linalg.norm(bio_coordinates[first] - bio_coordinates[second]))
            if distance <= cutoff:
                expected_contacts.append((first, second, distance))
    observed_contacts = contact_pairs(local_reference, cutoff_angstrom=cutoff)
    contacts_pass = (
        len(expected_contacts) == len(observed_contacts)
        and all(
            expected[:2] == observed[:2]
            and abs(expected[2] - observed[2]) <= 1e-6
            for expected, observed in zip(expected_contacts, observed_contacts)
        )
    )

    reference_coordinates = np.asarray([atom.coord for atom in bio_reference], dtype=float)
    mobile_coordinates = np.asarray([atom.coord for atom in bio_mobile], dtype=float)
    expected_rmsd = numpy_superposed_rmsd(reference_coordinates, mobile_coordinates)
    observed_rmsd = rmsd(local_reference, local_mobile, superpose=True)
    rmsd_pass = expected_rmsd > 0.0 and abs(expected_rmsd - observed_rmsd) <= 1e-5

    comparisons = [
        {
            "check": "PDB atom metadata and coordinates",
            "pass": parser_pass,
            "metadata_match": metadata_match,
            "max_coordinate_delta_angstrom": max_coordinate_delta,
            "tolerance_angstrom": 1e-5,
        },
        {
            "check": "heavy-atom contact pairs",
            "pass": contacts_pass,
            "expected_pairs": len(expected_contacts),
            "observed_pairs": len(observed_contacts),
            "cutoff_angstrom": cutoff,
            "distance_tolerance_angstrom": 1e-6,
        },
        {
            "check": "rigid-body superposed RMSD",
            "pass": rmsd_pass,
            "numpy_kabsch_rmsd_angstrom": expected_rmsd,
            "kinetics_horn_rmsd_angstrom": observed_rmsd,
            "tolerance_angstrom": 1e-5,
        },
    ]
    return {
        "validation_id": "kinetics-structure-biopython-numpy-reference-2026-11-09",
        "references": {
            "parser": "Bio.PDB.PDBParser",
            "geometry": "NumPy pairwise Euclidean distances and SVD Kabsch fit",
            "biopython_version": Bio.__version__,
            "numpy_version": np.__version__,
        },
        "method": "synthetic PDB fixture; independent parser and geometry implementation comparison",
        "comparisons": comparisons,
        "overall_pass": all(item["pass"] for item in comparisons),
        "limitations": [
            "Synthetic coordinates only; no experimental PDB/mmCIF reference structure is included.",
            "Checks basic PDB atom parsing, pairwise contacts and rigid-body RMSD only.",
            "Does not validate full mmCIF semantics, biological assemblies, alternate-location policies, SASA, interaction chemistry or large-structure performance.",
            "This host-only comparison does not establish Android runtime or device performance.",
        ],
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["overall_pass"]:
        raise SystemExit(1)
