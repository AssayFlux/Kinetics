"""Biopython-backed structural analysis with explicit provenance.

These utilities operate on local PDB/mmCIF files. They do not predict structures,
infer missing residues, or equate experimental and predicted evidence.
"""
from __future__ import annotations

import hashlib
import io
import math
from pathlib import Path
from typing import Any


def _biopython():
    try:
        from Bio import Align, PDB
        from Bio.PDB import NeighborSearch, ShrakeRupley, Superimposer
    except ImportError as exc:
        raise RuntimeError(
            "Structural analysis requires Biopython; install kinetics[baseline]"
        ) from exc
    return Align, PDB, NeighborSearch, ShrakeRupley, Superimposer


def _parse_structure(source: str | Path | bytes, file_format: str):
    _, PDB, _, _, _ = _biopython()
    if file_format not in {"pdb", "mmcif"}:
        raise ValueError("file_format must be pdb or mmcif")
    if isinstance(source, bytes):
        handle = io.StringIO(source.decode("ascii" if file_format == "pdb" else "utf-8"))
        name = "kinetics-input"
    else:
        path = Path(source)
        handle = str(path)
        name = path.name
    parser = PDB.PDBParser(QUIET=True) if file_format == "pdb" else PDB.MMCIFParser(
        QUIET=True, auth_chains=True, auth_residues=True
    )
    try:
        structure = parser.get_structure(name, handle)
    except Exception as exc:
        raise ValueError(f"Unable to parse {file_format} structure: {exc}") from exc
    models = list(structure.get_models())
    if not models:
        raise ValueError("Structure contains no models")
    return structure


def _source_digest(source: str | Path | bytes) -> str:
    if isinstance(source, bytes):
        payload = source
    else:
        payload = Path(source).read_bytes()
    return hashlib.sha256(payload).hexdigest()


def structure_summary(
    source: str | Path | bytes, *, file_format: str
) -> dict[str, Any]:
    """Summarize models, chains, polymer residues and atom counts."""
    structure = _parse_structure(source, file_format)
    models = []
    for model in structure:
        chains = []
        for chain in model:
            residues = [
                residue for residue in chain
                if residue.id[0] == " " and residue.has_id("CA")
            ]
            chains.append({
                "chain_id": str(chain.id),
                "polymer_residue_count": len(residues),
                "residue_ids": [
                    {"number": int(residue.id[1]), "insertion_code": str(residue.id[2]).strip(),
                     "resname": str(residue.resname)}
                    for residue in residues
                ],
            })
        models.append({
            "model_id": int(model.id) + 1,
            "atom_count": sum(1 for atom in model.get_atoms()),
            "chains": chains,
        })
    return {
        "file_format": file_format,
        "source_sha256": _source_digest(source),
        "model_count": len(models),
        "models": models,
    }


def calculate_residue_sasa(
    source: str | Path | bytes, *, file_format: str, model_index: int = 0
) -> dict[str, Any]:
    """Compute residue solvent-accessible surface area using Shrake-Rupley."""
    _, _, _, ShrakeRupley, _ = _biopython()
    structure = _parse_structure(source, file_format)
    models = list(structure.get_models())
    if not 0 <= model_index < len(models):
        raise ValueError("model_index is outside the structure model range")
    model = models[model_index]
    calculator = ShrakeRupley(n_points=100)
    calculator.compute(model, level="R")
    residues = []
    for chain in model:
        for residue in chain:
            if residue.id[0] != " ":
                continue
            value = float(residue.sasa)
            if not math.isfinite(value):
                raise ValueError("Biopython returned a non-finite SASA value")
            residues.append({
                "chain_id": str(chain.id),
                "residue_number": int(residue.id[1]),
                "insertion_code": str(residue.id[2]).strip(),
                "residue_name": str(residue.resname),
                "sasa_angstrom2": value,
            })
    return {
        "feature": "residue_sasa",
        "method": "Biopython ShrakeRupley",
        "biopython_version": _biopython_version(),
        "source_sha256": _source_digest(source),
        "model_index": model_index,
        "n_points": 100,
        "unit": "angstrom^2",
        "residues": residues,
    }


def _biopython_version() -> str:
    import Bio
    return str(Bio.__version__)


def calculate_residue_contacts(
    source: str | Path | bytes, *, file_format: str, cutoff_angstrom: float = 8.0,
    model_index: int = 0
) -> dict[str, Any]:
    """Find unique polymer-residue contacts by minimum heavy-atom distance."""
    _, _, NeighborSearch, _, _ = _biopython()
    if not math.isfinite(cutoff_angstrom) or not 0 < cutoff_angstrom <= 30:
        raise ValueError("cutoff_angstrom must be finite and in (0, 30]")
    structure = _parse_structure(source, file_format)
    models = list(structure.get_models())
    if not 0 <= model_index < len(models):
        raise ValueError("model_index is outside the structure model range")
    model = models[model_index]
    atoms = [
        atom for atom in model.get_atoms()
        if atom.element.strip().upper() not in {"H", "D"}
        and atom.get_parent().id[0] == " "
    ]
    search = NeighborSearch(atoms)
    pairs: dict[tuple[tuple[str, int, str], tuple[str, int, str]], float] = {}
    for atom in atoms:
        left_residue = atom.get_parent()
        left_key = (str(left_residue.get_parent().id), int(left_residue.id[1]),
                    str(left_residue.id[2]).strip())
        for other in search.search(atom.coord, cutoff_angstrom, level="A"):
            right_residue = other.get_parent()
            if right_residue is left_residue:
                continue
            right_key = (str(right_residue.get_parent().id), int(right_residue.id[1]),
                         str(right_residue.id[2]).strip())
            key = tuple(sorted((left_key, right_key)))
            distance = float(atom - other)
            if key not in pairs or distance < pairs[key]:
                pairs[key] = distance
    contacts = [
        {
            "first": {"chain_id": key[0][0], "residue_number": key[0][1],
                      "insertion_code": key[0][2]},
            "second": {"chain_id": key[1][0], "residue_number": key[1][1],
                       "insertion_code": key[1][2]},
            "minimum_heavy_atom_distance_angstrom": distance,
        }
        for key, distance in sorted(pairs.items())
    ]
    return {
        "feature": "residue_contacts",
        "method": "Biopython NeighborSearch",
        "biopython_version": _biopython_version(),
        "source_sha256": _source_digest(source),
        "model_index": model_index,
        "cutoff_angstrom": cutoff_angstrom,
        "contacts": contacts,
    }


def superimpose_ca_atoms(
    reference: str | Path | bytes,
    mobile: str | Path | bytes,
    *,
    reference_format: str,
    mobile_format: str,
    chain_id: str,
    residue_pairs: list[tuple[int, int]],
    reference_model_index: int = 0,
    mobile_model_index: int = 0,
) -> dict[str, Any]:
    """Superimpose explicit author-numbered C-alpha residue pairs.

    residue_pairs contains (reference_author_residue_number, mobile_author_residue_number).
    At least three non-collinear pairs are needed for a meaningful rigid-body fit.
    """
    _, _, _, _, Superimposer = _biopython()
    if len(residue_pairs) < 3:
        raise ValueError("At least three explicit residue pairs are required")
    if len(set(residue_pairs)) != len(residue_pairs):
        raise ValueError("Residue pairs must be unique")
    ref_models = list(_parse_structure(reference, reference_format).get_models())
    mob_models = list(_parse_structure(mobile, mobile_format).get_models())
    if not 0 <= reference_model_index < len(ref_models):
        raise ValueError("reference_model_index is outside the model range")
    if not 0 <= mobile_model_index < len(mob_models):
        raise ValueError("mobile_model_index is outside the model range")
    try:
        ref_chain = ref_models[reference_model_index][chain_id]
        mob_chain = mob_models[mobile_model_index][chain_id]
    except KeyError as exc:
        raise ValueError(f"Requested chain {chain_id!r} is absent") from exc
    fixed, moving = [], []
    for ref_number, mob_number in residue_pairs:
        try:
            ref_residue = ref_chain[(" ", int(ref_number), " ")]
            mob_residue = mob_chain[(" ", int(mob_number), " ")]
            fixed.append(ref_residue["CA"])
            moving.append(mob_residue["CA"])
        except KeyError as exc:
            raise ValueError(f"Explicit residue pair {ref_number}:{mob_number} lacks C-alpha") from exc
    if any(a.get_parent().resname != b.get_parent().resname for a, b in zip(fixed, moving)):
        raise ValueError("Explicit residue pairs contain mismatched amino-acid identities")
    superimposer = Superimposer()
    superimposer.set_atoms(fixed, moving)
    rotation, translation = superimposer.rotran
    return {
        "feature": "ca_superposition",
        "method": "Biopython Superimposer",
        "biopython_version": _biopython_version(),
        "reference_sha256": _source_digest(reference),
        "mobile_sha256": _source_digest(mobile),
        "chain_id": chain_id,
        "residue_pairs": [list(pair) for pair in residue_pairs],
        "atom_count": len(fixed),
        "rmsd_angstrom": float(superimposer.rms),
        "rotation": [[float(value) for value in row] for row in rotation],
        "translation_angstrom": [float(value) for value in translation],
        "coordinate_transform": "mobile_to_reference",
    }


def align_protein_sequences(
    reference_sequence: str, query_sequence: str, *, mode: str = "global"
) -> dict[str, Any]:
    """Align protein sequences with Bio.Align.PairwiseAligner (BLOSUM62)."""
    Align, _, _, _, _ = _biopython()
    if mode not in {"global", "local"}:
        raise ValueError("mode must be global or local")
    if not reference_sequence or not query_sequence:
        raise ValueError("Both sequences are required")
    from Bio.Align import substitution_matrices
    aligner = Align.PairwiseAligner()
    aligner.mode = mode
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    alignments = aligner.align(reference_sequence.upper(), query_sequence.upper())
    if len(alignments) == 0:
        raise ValueError("No sequence alignment was produced")
    best = alignments[0]
    return {
        "method": "Biopython PairwiseAligner",
        "biopython_version": _biopython_version(),
        "mode": mode,
        "score": float(best.score),
        "alignment": str(best),
        "reference_length": len(reference_sequence),
        "query_length": len(query_sequence),
    }
