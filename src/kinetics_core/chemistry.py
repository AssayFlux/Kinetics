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


def murcko_scaffold_id(smiles: str) -> str:
    """Return a Bemis-Murcko scaffold key; keep acyclic compounds distinct.

    This is a reproducible grouping convention, not a claim that scaffold identity
    captures all chemical similarity. Record RDKit version with benchmark metadata.
    """
    try:
        from rdkit import Chem
        from rdkit.Chem.Scaffolds import MurckoScaffold
    except ImportError as exc:
        raise RuntimeError("Scaffold generation requires RDKit") from exc
    molecule = Chem.MolFromSmiles(str(smiles))
    if molecule is None:
        raise ValueError(f"Invalid SMILES: {smiles!r}")
    canonical = Chem.MolToSmiles(molecule, canonical=True, isomericSmiles=True)
    scaffold = MurckoScaffold.GetScaffoldForMol(molecule)
    scaffold_smiles = Chem.MolToSmiles(scaffold, canonical=True, isomericSmiles=True)
    return f"MURCKO:{scaffold_smiles}" if scaffold_smiles else f"ACYCLIC:{canonical}"
