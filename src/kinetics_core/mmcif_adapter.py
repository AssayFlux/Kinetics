"""Provenance-checked mmCIF coordinate ingestion.

The adapter reads deposited atom-site coordinates only. It does not infer
sequence alignment, biological assemblies, missing atoms, or structure quality.
Author residue numbering is retained so explicit ResidueMapping records can be
used with the same evidence-linked C-alpha distance routine as the PDB adapter.
"""
from __future__ import annotations

import hashlib

from .pdb_adapter import PdbAtom, ParsedPdb
from .proteomics import StructureRecord


def _column(data: dict[str, list[str]], name: str, index: int, default: str = "") -> str:
    values = data.get(name)
    if values is None or index >= len(values):
        return default
    value = str(values[index]).strip()
    return default if value in {"", ".", "?"} else value


def parse_mmcif_coordinates(content: bytes, structure: StructureRecord) -> ParsedPdb:
    """Parse mmCIF atom_site rows after verifying the exact source-file SHA-256."""
    if structure.coordinate_format != "mmcif":
        raise ValueError("mmCIF parser requires a structure record with mmcif format")
    digest = hashlib.sha256(content).hexdigest()
    if digest != structure.coordinate_sha256.lower():
        raise ValueError("mmCIF coordinate digest does not match structure provenance")
    try:
        from Bio.PDB.MMCIF2Dict import MMCIF2Dict
    except ImportError as exc:
        raise RuntimeError(
            "mmCIF parsing requires the optional Biopython dependency; install the baseline extra"
        ) from exc
    try:
        data = MMCIF2Dict(content.decode("utf-8"))
    except (UnicodeDecodeError, ValueError, OSError) as exc:
        raise ValueError("invalid UTF-8 mmCIF coordinate document") from exc

    required = (
        "_atom_site.Cartn_x", "_atom_site.Cartn_y", "_atom_site.Cartn_z",
        "_atom_site.auth_atom_id", "_atom_site.auth_comp_id",
        "_atom_site.auth_asym_id", "_atom_site.auth_seq_id",
    )
    if any(key not in data for key in required):
        raise ValueError("mmCIF atom_site is missing required author-coordinate columns")

    count = len(data["_atom_site.Cartn_x"])
    atoms: list[PdbAtom] = []
    for i in range(count):
        try:
            chain = _column(data, "_atom_site.auth_asym_id", i)
            if not chain:
                # Do not silently substitute label numbering for missing author IDs.
                raise ValueError("mmCIF atom_site row has no author chain identifier")
            if chain not in structure.chain_ids:
                raise ValueError(f"atom chain {chain!r} is absent from structure metadata")
            atom_name = _column(data, "_atom_site.auth_atom_id", i).upper()
            residue_name = _column(data, "_atom_site.auth_comp_id", i).upper()
            if not atom_name or not residue_name:
                raise ValueError("mmCIF atom_site row has missing atom or residue identity")
            raw_number = _column(data, "_atom_site.auth_seq_id", i)
            if not raw_number:
                raise ValueError("mmCIF atom_site row has no author residue number")
            model_raw = _column(data, "_atom_site.pdbx_PDB_model_num", i, "1")
            atom = PdbAtom(
                model=int(model_raw),
                serial=int(_column(data, "_atom_site.id", i, str(i + 1))),
                atom_name=atom_name,
                alternate_location=_column(data, "_atom_site.label_alt_id", i),
                residue_name=residue_name,
                chain_id=chain,
                residue_number=int(raw_number),
                insertion_code=_column(data, "_atom_site.pdbx_PDB_ins_code", i),
                x=float(_column(data, "_atom_site.Cartn_x", i)),
                y=float(_column(data, "_atom_site.Cartn_y", i)),
                z=float(_column(data, "_atom_site.Cartn_z", i)),
                occupancy=float(_column(data, "_atom_site.occupancy", i, "1")),
                b_factor=float(_column(data, "_atom_site.B_iso_or_equiv", i, "0")),
                element=_column(data, "_atom_site.type_symbol", i).upper(),
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid mmCIF atom_site row {i + 1}: {exc}") from exc
        import math

        if atom.model < 1 or not all(
            math.isfinite(value)
            for value in (atom.x, atom.y, atom.z, atom.occupancy, atom.b_factor)
        ):
            raise ValueError(f"non-finite or invalid coordinates in mmCIF atom_site row {i + 1}")
        atoms.append(atom)

    if not atoms:
        raise ValueError("mmCIF file contains no atom_site coordinate records")
    return ParsedPdb(structure, digest, tuple(atoms))
