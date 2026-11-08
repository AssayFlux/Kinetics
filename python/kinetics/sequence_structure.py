"""Conservative exact sequence-to-structure residue mapping.

Only unique, contiguous exact matches to standard amino-acid residues are reported.
This does not perform alignment, mutation interpretation, numbering-scheme conversion,
or infer missing/disordered residues.
"""
from __future__ import annotations

from typing import Iterable

from .structure import Atom

THREE_TO_ONE = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
}


def map_exact_chain_sequence(
    query_sequence: str,
    atoms: Iterable[Atom],
    *,
    chain_id: str,
    max_query_residues: int = 1_000_000,
    max_structure_residues: int = 100_000,
) -> dict[str, object]:
    """Map a uniquely occurring exact chain sequence to a query protein sequence.

    Residues are keyed by chain and residue number. The current Atom
    representation does not retain insertion codes, so insertion-code-aware mapping
    is explicitly unsupported rather than guessed.
    """
    if not isinstance(query_sequence, str) or not query_sequence:
        raise ValueError("query_sequence must be non-empty text")
    query = "".join(query_sequence.split()).upper()
    if not query or set(query) - set(THREE_TO_ONE.values()):
        raise ValueError("query_sequence must contain only the 20 canonical amino acids")
    if max_query_residues < 1 or len(query) > max_query_residues:
        raise ValueError("query sequence exceeds the configured residue limit")
    if max_structure_residues < 1:
        raise ValueError("max_structure_residues must be positive")
    if not isinstance(chain_id, str) or not chain_id:
        raise ValueError("chain_id must be non-empty text")

    selected_atoms = [atom for atom in atoms if atom.chain == chain_id]
    residues: dict[int, str] = {}
    residue_names: dict[int, str] = {}
    for atom in selected_atoms:
        if atom.residue_number not in residues and len(residues) >= max_structure_residues:
            raise ValueError("structure chain exceeds the configured residue limit")
        residue_name = atom.residue.upper()
        amino_acid = THREE_TO_ONE.get(residue_name)
        if amino_acid is None:
            raise ValueError(
                f"Unsupported/non-standard residue {residue_name} in chain {chain_id}; mapping abstained"
            )
        previous = residues.setdefault(atom.residue_number, amino_acid)
        previous_name = residue_names.setdefault(atom.residue_number, residue_name)
        if previous != amino_acid or previous_name != residue_name:
            raise ValueError("Conflicting residue identity at one chain position")
    ordered = sorted(residues.items())
    if not ordered:
        raise ValueError(f"No canonical residues found for chain {chain_id}")
    if any(
        current_number != previous_number + 1
        for (previous_number, _), (current_number, _) in zip(ordered, ordered[1:])
    ):
        return {
            "status": "noncontiguous_structure_numbering",
            "chain_id": chain_id,
            "observed_chain_sequence": "".join(amino_acid for _, amino_acid in ordered),
            "query_length": len(query),
            "mapped_residues": [],
            "limitations": [
                "Residue numbering gaps are not repaired or assumed to be contiguous.",
                "No alignment, missing-residue reconstruction or insertion-code conversion is performed.",
            ],
        }

    observed = "".join(amino_acid for _, amino_acid in ordered)
    positions = [
        index for index in range(len(query) - len(observed) + 1)
        if query[index:index + len(observed)] == observed
    ]
    if not positions:
        return {
            "status": "no_exact_match",
            "chain_id": chain_id,
            "observed_chain_sequence": observed,
            "query_length": len(query),
            "mapped_residues": [],
            "limitations": [
                "Exact contiguous matching only; no alignment or gap handling.",
                "Missing/disordered residues can prevent a match.",
                "Insertion codes are not retained by the current atom model.",
            ],
        }
    if len(positions) != 1:
        return {
            "status": "ambiguous_exact_match",
            "chain_id": chain_id,
            "observed_chain_sequence": observed,
            "query_length": len(query),
            "candidate_query_starts_1based": [position + 1 for position in positions],
            "mapped_residues": [],
            "limitations": [
                "Repeated exact occurrences are ambiguous and are not arbitrarily selected.",
                "No alignment, gap handling or insertion-code conversion is performed.",
            ],
        }

    start = positions[0]
    mapped = [
        {
            "query_position_1based": start + index + 1,
            "chain_id": chain_id,
            "structure_residue_number": residue_number,
            "residue_name": residue_names[residue_number],
            "amino_acid": amino_acid,
        }
        for index, (residue_number, amino_acid) in enumerate(ordered)
    ]
    return {
        "status": "exact_unique_match",
        "chain_id": chain_id,
        "observed_chain_sequence": observed,
        "query_length": len(query),
        "query_start_1based": start + 1,
        "query_end_1based": start + len(observed),
        "mapped_residues": mapped,
        "limitations": [
            "Exact contiguous matching only; no alignment or gap handling.",
            "Missing/disordered residues can prevent a match.",
            "Insertion codes are not retained by the current atom model.",
            "This mapping is not evidence of variant effect or protein function.",
        ],
    }
