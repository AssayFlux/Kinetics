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
    """Return a Bemis-Murcko scaffold key under an explicit stereochemistry policy.

    Stereochemistry is deliberately removed from the grouping key so stereoisomers
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
        scaffold, canonical=True, isomericSmiles=False
    )
    if scaffold_smiles:
        return f"MURCKO:{scaffold_smiles}"
    canonical = Chem.MolToSmiles(
        molecule, canonical=True, isomericSmiles=False
    )
    return f"ACYCLIC:{canonical}"


def annotate_scaffolds(
    frame,
    *,
    smiles_column: str = "smiles",
    output_column: str = "scaffold_id",
):
    """Return a copy with deterministic Murcko IDs and an explicit stereo policy."""
    if smiles_column not in frame.columns:
        raise ValueError(f"Missing SMILES column: {smiles_column}")
    result = frame.copy()
    result[output_column] = result[smiles_column].map(murcko_scaffold_id)
    return result



def molecular_graph_features(smiles: str) -> dict:
    """Build a sanitized, stereochemistry-aware molecular graph as NumPy arrays.

    Atom rows are [atomic number, degree, formal charge, total H, aromatic,
    CIP stereochemistry (0 none, 1 R, 2 S), hybridization enum, isotope, mass].
    Each bond is represented by two directed edges. Bond rows are [bond type
    enum, conjugated, in ring, stereo enum]. Atom order follows the canonical
    isomeric SMILES parse, and no salt/tautomer normalization is applied.
    """
    import numpy as np

    try:
        from rdkit import Chem
    except ImportError as exc:
        raise RuntimeError("Molecular graph generation requires RDKit") from exc
    molecule = Chem.MolFromSmiles(str(smiles), sanitize=True)
    if molecule is None:
        raise ValueError(f"Invalid SMILES: {smiles!r}")
    Chem.AssignStereochemistry(molecule, cleanIt=True, force=True)

    atom_rows = []
    for atom in molecule.GetAtoms():
        cip = atom.GetProp("_CIPCode") if atom.HasProp("_CIPCode") else ""
        cip_index = {"R": 1, "S": 2}.get(cip, 0)
        atom_rows.append([
            atom.GetAtomicNum(),
            atom.GetDegree(),
            atom.GetFormalCharge(),
            atom.GetTotalNumHs(),
            int(atom.GetIsAromatic()),
            cip_index,
            int(atom.GetHybridization()),
            atom.GetIsotope(),
            atom.GetMass(),
        ])

    edge_pairs = []
    bond_rows = []
    for bond in molecule.GetBonds():
        begin, end = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        feature = [
            int(bond.GetBondType()),
            int(bond.GetIsConjugated()),
            int(bond.IsInRing()),
            int(bond.GetStereo()),
        ]
        edge_pairs.extend(((begin, end), (end, begin)))
        bond_rows.extend((feature, feature))

    edge_index = (
        np.asarray(edge_pairs, dtype=np.int64).T
        if edge_pairs else np.empty((2, 0), dtype=np.int64)
    )
    bond_features = (
        np.asarray(bond_rows, dtype=np.float32)
        if bond_rows else np.empty((0, 4), dtype=np.float32)
    )
    atom_features = np.asarray(atom_rows, dtype=np.float32)
    return {
        "canonical_smiles": Chem.MolToSmiles(
            molecule, canonical=True, isomericSmiles=True
        ),
        "atom_features": atom_features,
        "edge_index": edge_index,
        "bond_features": bond_features,
        "num_atoms": int(molecule.GetNumAtoms()),
        "num_bonds": int(molecule.GetNumBonds()),
        "schema_version": "1.0",
        "atom_feature_names": [
            "atomic_number", "degree", "formal_charge", "total_hydrogens",
            "is_aromatic", "cip_stereochemistry", "hybridization", "isotope",
            "atomic_mass",
        ],
        "bond_feature_names": [
            "bond_type", "is_conjugated", "in_ring", "bond_stereo",
        ],
    }



def annotate_scaffolds_audited(
    frame,
    *,
    smiles_column: str = "smiles",
    output_column: str = "scaffold_id",
):
    """Annotate valid structures and return row-level rejections for invalid SMILES."""
    import pandas as pd

    if smiles_column not in frame.columns:
        raise ValueError(f"Missing SMILES column: {smiles_column}")
    if output_column in frame.columns:
        raise ValueError(f"Output scaffold column already exists: {output_column}")
    if frame.empty:
        raise ValueError("At least one observation is required for scaffold annotation")
    accepted = []
    rejected = []
    for index, row in frame.iterrows():
        item = row.to_dict()
        try:
            item[output_column] = murcko_scaffold_id(row[smiles_column])
            accepted.append(item)
        except (TypeError, ValueError) as exc:
            rejected.append({
                "source_row_number": int(index) if isinstance(index, int) else str(index),
                "source_record_id": str(row.get("source_record_id", "")),
                "reason": str(exc),
            })
    return (
        pd.DataFrame(accepted, columns=list(frame.columns) + [output_column]),
        pd.DataFrame(
            rejected,
            columns=["source_row_number", "source_record_id", "reason"],
        ),
    )
