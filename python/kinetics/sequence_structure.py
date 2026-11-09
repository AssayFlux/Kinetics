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
    max_atoms: int = 2_000_000,
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
    for name, limit in (
        ("max_query_residues", max_query_residues),
        ("max_structure_residues", max_structure_residues),
        ("max_atoms", max_atoms),
    ):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError(f"{name} must be a positive integer")
    if len(query) > max_query_residues:
        raise ValueError("query sequence exceeds the configured residue limit")
    if not isinstance(chain_id, str) or not chain_id:
        raise ValueError("chain_id must be non-empty text")

    residues: dict[int, str] = {}
    residue_names: dict[int, str] = {}
    atom_count = 0
    for atom in atoms:
        atom_count += 1
        if atom_count > max_atoms:
            raise ValueError("structure atom stream exceeds the configured atom limit")
        if atom.chain != chain_id:
            continue
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
    positions: list[int] = []
    search_from = 0
    while True:
        position = query.find(observed, search_from)
        if position < 0:
            break
        positions.append(position)
        # Advance one residue so every overlapping exact occurrence is reported.
        search_from = position + 1
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



def map_variant_to_structure(
    query_sequence: str,
    atoms: Iterable[Atom],
    *,
    chain_id: str,
    variant_position_1based: int,
    reference_amino_acid: str,
    alternate_amino_acid: str,
    max_query_residues: int = 1_000_000,
    max_structure_residues: int = 100_000,
    max_atoms: int = 2_000_000,
) -> dict[str, object]:
    """Map one protein substitution to a structure only through a unique exact chain match.

    This reports coordinate correspondence only. It does not predict structural,
    functional, pathogenic or clinical effect.
    """
    if (
        isinstance(variant_position_1based, bool)
        or not isinstance(variant_position_1based, int)
        or variant_position_1based < 1
    ):
        raise ValueError("variant_position_1based must be a positive integer")
    if (
        not isinstance(reference_amino_acid, str)
        or len(reference_amino_acid) != 1
        or reference_amino_acid not in THREE_TO_ONE.values()
    ):
        raise ValueError("reference_amino_acid must be one canonical amino-acid letter")
    if (
        not isinstance(alternate_amino_acid, str)
        or len(alternate_amino_acid) != 1
        or alternate_amino_acid not in THREE_TO_ONE.values()
    ):
        raise ValueError("alternate_amino_acid must be one canonical amino-acid letter")
    if alternate_amino_acid == reference_amino_acid:
        raise ValueError("Reference and alternate amino acids must differ")
    query = "".join(query_sequence.split()).upper() if isinstance(query_sequence, str) else ""
    if not query or variant_position_1based > len(query):
        raise ValueError("Variant position is outside the query protein sequence")
    observed_reference = query[variant_position_1based - 1]
    if observed_reference != reference_amino_acid:
        raise ValueError(
            f"Variant reference amino acid {reference_amino_acid} does not match query "
            f"residue {observed_reference} at position {variant_position_1based}"
        )

    mapping = map_exact_chain_sequence(
        query,
        atoms,
        chain_id=chain_id,
        max_query_residues=max_query_residues,
        max_structure_residues=max_structure_residues,
        max_atoms=max_atoms,
    )
    if mapping["status"] != "exact_unique_match":
        return {
            "schema": "kinetics.structure-variant-map.v1",
            "status": "abstained",
            "mapping_status": mapping["status"],
            "variant": {
                "position_1based": variant_position_1based,
                "reference": reference_amino_acid,
                "alternate": alternate_amino_acid,
            },
            "mapped_residue": None,
            "limitations": [
                "Variant-to-structure mapping requires a unique contiguous exact chain match.",
                "No structural, functional, pathogenic or clinical effect is inferred.",
            ],
        }

    mapped = next(
        (
            item for item in mapping["mapped_residues"]
            if item["query_position_1based"] == variant_position_1based
        ),
        None,
    )
    if mapped is None:
        return {
            "schema": "kinetics.structure-variant-map.v1",
            "status": "not_covered_by_structure",
            "mapping_status": mapping["status"],
            "variant": {
                "position_1based": variant_position_1based,
                "reference": reference_amino_acid,
                "alternate": alternate_amino_acid,
            },
            "mapped_residue": None,
            "limitations": [
                "The exact structure chain does not cover the requested query position.",
                "No structural, functional, pathogenic or clinical effect is inferred.",
            ],
        }
    return {
        "schema": "kinetics.structure-variant-map.v1",
        "status": "mapped_coordinate_only",
        "mapping_status": mapping["status"],
        "mapping_quality": "unique_contiguous_exact_sequence",
        "variant": {
            "position_1based": variant_position_1based,
            "reference": reference_amino_acid,
            "alternate": alternate_amino_acid,
        },
        "mapped_residue": mapped,
        "limitations": [
            "This is coordinate correspondence only, not a mutation model.",
            "No side-chain rebuilding, energy calculation, stability prediction or interface effect is performed.",
            "No pathogenicity, clinical significance or biological function is inferred.",
            "Insertion codes are not retained by the current atom model.",
        ],
    }
