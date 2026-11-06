"""Chemical identity and scaffold utilities based on RDKit."""
from __future__ import annotations


def canonicalize_smiles(smiles: str) -> str:
    """Return RDKit canonical isomeric SMILES; do not silently repair invalid input."""
    try:
        from rdkit import Chem
    except ImportError as exc:
        raise RuntimeError("SMILES standardization requires RDKit") from exc
    molecule = Chem.MolFromSmiles(str(smiles))
    if molecule is None:
        raise ValueError(f"Invalid SMILES: {smiles!r}")
    return Chem.MolToSmiles(molecule, canonical=True, isomericSmiles=True)


def murcko_scaffold_id(
    smiles: str,
    *,
    include_chirality: bool = False,
) -> str:
    """Return a Bemis-Murcko scaffold key under an explicit stereochemistry policy.

    By default stereochemistry is removed from the grouping key so stereoisomers
    remain in the same scaffold partition. This does not remove stereochemistry
    from the molecular representation used for feature generation. Acyclic
    molecules use their canonical molecular graph as a fallback because their
    Bemis-Murcko scaffold is empty. Salt and tautomer normalization are not applied.
    """
    try:
        from rdkit import Chem
        from rdkit.Chem.Scaffolds import MurckoScaffold
    except ImportError as exc:
        raise RuntimeError("Scaffold generation requires RDKit") from exc
    molecule = Chem.MolFromSmiles(str(smiles))
    if molecule is None:
        raise ValueError(f"Invalid SMILES: {smiles!r}")
    scaffold = MurckoScaffold.GetScaffoldForMol(molecule)
    scaffold_smiles = Chem.MolToSmiles(
        scaffold, canonical=True, isomericSmiles=include_chirality
    )
    if scaffold_smiles:
        return f"MURCKO:{scaffold_smiles}"
    canonical = Chem.MolToSmiles(
        molecule, canonical=True, isomericSmiles=include_chirality
    )
    return f"ACYCLIC:{canonical}"


def annotate_scaffolds(
    frame,
    *,
    smiles_column: str = "smiles",
    output_column: str = "scaffold_id",
    include_chirality: bool = False,
):
    """Return a copy with deterministic Murcko IDs and an explicit stereo policy."""
    if smiles_column not in frame.columns:
        raise ValueError(f"Missing SMILES column: {smiles_column}")
    result = frame.copy()
    result[output_column] = result[smiles_column].map(
        lambda value: murcko_scaffold_id(
            value, include_chirality=include_chirality
        )
    )
    return result
