"""Strict PDB coordinate ingestion and evidence-linked C-alpha distances.

Only fixed-column PDB ATOM/HETATM records are supported. mmCIF, biological
assembly expansion, missing-residue reconstruction and structural alignment
are deliberately not inferred by this adapter.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass

from .proteomics import ProteinSequenceRecord, ResidueMapping, StructureFeature, StructureRecord

_AA3_TO_1 = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
    "MSE": "U", "SEC": "U", "PYL": "O", "ASX": "B", "GLX": "Z",
}


@dataclass(frozen=True, slots=True)
class PdbAtom:
    model: int
    serial: int
    atom_name: str
    alternate_location: str
    residue_name: str
    chain_id: str
    residue_number: int
    insertion_code: str
    x: float
    y: float
    z: float
    occupancy: float
    b_factor: float
    element: str


@dataclass(frozen=True, slots=True)
class ParsedPdb:
    structure: StructureRecord
    coordinate_sha256: str
    atoms: tuple[PdbAtom, ...]


def parse_pdb_coordinates(content: bytes, structure: StructureRecord) -> ParsedPdb:
    """Parse fixed-column PDB atoms after verifying the exact source-file digest."""
    if structure.coordinate_format != "pdb":
        raise ValueError("PDB parser requires a structure record with pdb format")
    digest = hashlib.sha256(content).hexdigest()
    if digest != structure.coordinate_sha256.lower():
        raise ValueError("PDB coordinate digest does not match structure provenance")
    try:
        text = content.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ValueError("PDB coordinate content must be ASCII") from exc

    atoms: list[PdbAtom] = []
    model = 1
    for line_number, line in enumerate(text.splitlines(), start=1):
        record = line[0:6].strip().upper()
        if record == "MODEL":
            raw_model = line[10:14].strip() or line[6:].strip()
            try:
                model = int(raw_model)
            except ValueError as exc:
                raise ValueError(f"invalid MODEL number on line {line_number}") from exc
            if model < 1:
                raise ValueError(f"invalid MODEL number on line {line_number}")
            continue
        if record not in {"ATOM", "HETATM"}:
            continue
        if len(line) < 54:
            raise ValueError(f"truncated atom record on line {line_number}")
        try:
            atom = PdbAtom(
                model=model,
                serial=int(line[6:11].strip()),
                atom_name=line[12:16].strip().upper(),
                alternate_location=line[16:17].strip(),
                residue_name=line[17:20].strip().upper(),
                chain_id=line[21:22].strip() or "_",
                residue_number=int(line[22:26].strip()),
                insertion_code=line[26:27].strip(),
                x=float(line[30:38]),
                y=float(line[38:46]),
                z=float(line[46:54]),
                occupancy=float(line[54:60].strip() or "1"),
                b_factor=float(line[60:66].strip() or "0"),
                element=line[76:78].strip().upper() if len(line) >= 78 else "",
            )
        except ValueError as exc:
            raise ValueError(f"invalid atom fields on line {line_number}") from exc
        if not all(math.isfinite(v) for v in (
            atom.x, atom.y, atom.z, atom.occupancy, atom.b_factor
        )):
            raise ValueError(f"non-finite atom values on line {line_number}")
        if atom.chain_id not in structure.chain_ids:
            raise ValueError(
                f"atom chain {atom.chain_id!r} is absent from structure metadata"
            )
        if not atom.atom_name or not atom.residue_name:
            raise ValueError(f"missing atom or residue name on line {line_number}")
        atoms.append(atom)

    if not atoms:
        raise ValueError("PDB file contains no ATOM or HETATM coordinate records")
    return ParsedPdb(structure, digest, tuple(atoms))


def _mapped_ca(
    parsed: ParsedPdb,
    mapping: ResidueMapping,
    sequence: ProteinSequenceRecord,
    model: int,
) -> PdbAtom:
    mapping.validate_against(sequence, parsed.structure)
    if mapping.numbering_scheme != "author":
        raise ValueError("PDB fixed-column parser supports author residue numbering only")
    residue_code = _AA3_TO_1.get(mapping.residue_name.upper())
    if residue_code and sequence.sequence[mapping.sequence_position - 1] not in {
        residue_code, "X"
    }:
        raise ValueError("mapped residue identity does not match the protein sequence")
    candidates = [
        atom for atom in parsed.atoms
        if atom.model == model
        and atom.chain_id == mapping.chain_id
        and atom.residue_number == mapping.residue_number
        and atom.insertion_code == (mapping.insertion_code or "")
        and atom.atom_name == "CA"
        and atom.residue_name == mapping.residue_name.upper()
    ]
    if not candidates:
        raise ValueError("mapped residue has no C-alpha coordinate in the requested model")
    candidates.sort(key=lambda atom: (
        -atom.occupancy,
        0 if not atom.alternate_location else 1,
        atom.alternate_location,
        atom.serial,
    ))
    return candidates[0]


def calculate_ca_distance(
    parsed: ParsedPdb,
    sequence: ProteinSequenceRecord,
    first: ResidueMapping,
    second: ResidueMapping,
    *,
    model: int = 1,
) -> StructureFeature:
    """Calculate a C-alpha distance only for two explicit, validated residue mappings."""
    if model < 1:
        raise ValueError("model must be a positive model number")
    left = _mapped_ca(parsed, first, sequence, model)
    right = _mapped_ca(parsed, second, sequence, model)
    distance = math.dist((left.x, left.y, left.z), (right.x, right.y, right.z))
    parameters = {
        "atom": "CA",
        "model": model,
        "coordinate_sha256": parsed.coordinate_sha256,
        "first_mapping": first.as_dict(),
        "second_mapping": second.as_dict(),
    }
    parameter_digest = hashlib.sha256(
        json.dumps(parameters, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    feature_id = hashlib.sha256(
        f"{parameter_digest}:ca_distance".encode("ascii")
    ).hexdigest()
    return StructureFeature(
        feature_id=feature_id,
        structure_id=parsed.structure.structure_id,
        feature_name="ca_distance",
        value=distance,
        unit="angstrom",
        tool_name=f"kinetics-{parsed.structure.coordinate_format}",
        tool_version="0.1.0",
        parameter_sha256=parameter_digest,
        coordinate_frame=f"{parsed.structure.coordinate_format}-model:{model}",
        mapping_evidence_ids=(first.evidence_id, second.evidence_id),
    )
