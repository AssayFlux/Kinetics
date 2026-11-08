"""Optional RDKit-backed chemistry adapter.

RDKit is not currently bundled in the Android application. These functions use the
real RDKit sanitization/descriptor/fingerprint engine when it is installed on a host.
"""
from __future__ import annotations

from typing import Any


def _rdkit() -> tuple[Any, Any, Any, Any, Any]:
    try:
        from rdkit import Chem, DataStructs, rdBase  # type: ignore[import-not-found]
        from rdkit.Chem import Descriptors, rdFingerprintGenerator, rdMolDescriptors  # type: ignore[import-not-found]
    except ImportError as error:
        raise RuntimeError(
            "RDKit backend is unavailable in this runtime; install an approved, "
            "version-pinned RDKit distribution before using production chemistry"
        ) from error
    return Chem, DataStructs, rdBase, Descriptors, (rdFingerprintGenerator, rdMolDescriptors)


def rdkit_backend_info() -> dict[str, str]:
    """Return the exact active RDKit version or a clear unavailable status."""
    try:
        _, _, version, _, _ = _rdkit()
    except RuntimeError as error:
        return {"available": "false", "status": str(error)}
    return {"available": "true", "engine": "RDKit", "version": version.rdkitVersion}


def _describe(molecule: Any, *, source_format: str) -> dict[str, object]:
    Chem, _, version, descriptors, modules = _rdkit()
    fingerprint_generator, mol_descriptors = modules
    if molecule is None:
        raise ValueError("RDKit could not parse the supplied molecule")
    # MolFromSmiles/MolFromMolBlock sanitizes by default. Sanitize explicitly so
    # the recorded operation is clear and failure is surfaced.
    Chem.SanitizeMol(molecule)
    canonical = Chem.MolToSmiles(molecule, canonical=True, isomericSmiles=True)
    generator = fingerprint_generator.GetMorganGenerator(radius=2, fpSize=2048)
    fingerprint = generator.GetFingerprint(molecule)
    chiral_centres = Chem.FindMolChiralCenters(molecule, includeUnassigned=True)
    return {
        "engine": "RDKit",
        "engine_version": version.rdkitVersion,
        "source_format": source_format,
        "sanitization": "RDKit Chem.SanitizeMol",
        "canonical_isomeric_smiles": canonical,
        "formula": mol_descriptors.CalcMolFormula(molecule),
        "molecular_weight": descriptors.MolWt(molecule),
        "exact_molecular_weight": descriptors.ExactMolWt(molecule),
        "crippen_logp": descriptors.MolLogP(molecule),
        "tpsa_angstrom2": descriptors.TPSA(molecule),
        "h_bond_donors": descriptors.NumHDonors(molecule),
        "h_bond_acceptors": descriptors.NumHAcceptors(molecule),
        "rotatable_bonds": descriptors.NumRotatableBonds(molecule),
        "ring_count": descriptors.RingCount(molecule),
        "atom_count": molecule.GetNumAtoms(),
        "bond_count": molecule.GetNumBonds(),
        "chiral_centres": chiral_centres,
        "morgan_fingerprint": {
            "algorithm": "Morgan", "radius": 2, "bits": 2048,
            "on_bits": list(fingerprint.GetOnBits()),
        },
        "limitations": [
            "Descriptor values depend on the exact RDKit release and sanitization model",
            "Protonation, tautomer and conformer selection are not inferred",
            "No biological activity or clinical interpretation is provided",
        ],
    }


def analyze_smiles(smiles: str) -> dict[str, object]:
    """Parse, sanitize and describe a SMILES string using RDKit."""
    if not isinstance(smiles, str) or not smiles.strip() or len(smiles) > 1_000_000:
        raise ValueError("SMILES must be a non-empty string no longer than 1 MB")
    Chem, _, _, _, _ = _rdkit()
    molecule = Chem.MolFromSmiles(smiles, sanitize=True)
    return _describe(molecule, source_format="SMILES")


def analyze_molblock(molblock: str) -> dict[str, object]:
    """Parse and sanitize a V2000/V3000 mol block using RDKit."""
    if not isinstance(molblock, str) or not molblock.strip() or len(molblock) > 10_000_000:
        raise ValueError("Mol block must be non-empty and no larger than 10 MB")
    Chem, _, _, _, _ = _rdkit()
    molecule = Chem.MolFromMolBlock(
        molblock, sanitize=True, removeHs=False, strictParsing=True,
    )
    return _describe(molecule, source_format="molblock")


def morgan_tanimoto(first_smiles: str, second_smiles: str, *, radius: int = 2, bits: int = 2048) -> float:
    """Calculate Morgan-fingerprint Tanimoto similarity using RDKit."""
    if not 1 <= radius <= 6 or not 256 <= bits <= 16_384 or bits & (bits - 1):
        raise ValueError("Morgan radius must be 1..6 and bit count a power of two in 256..16384")
    if not first_smiles or not second_smiles:
        raise ValueError("Both SMILES inputs are required")
    Chem, DataStructs, _, _, modules = _rdkit()
    generator_module, _ = modules
    first = Chem.MolFromSmiles(first_smiles, sanitize=True)
    second = Chem.MolFromSmiles(second_smiles, sanitize=True)
    if first is None or second is None:
        raise ValueError("RDKit could not parse one or both SMILES inputs")
    generator = generator_module.GetMorganGenerator(radius=radius, fpSize=bits)
    return float(DataStructs.TanimotoSimilarity(
        generator.GetFingerprint(first), generator.GetFingerprint(second),
    ))
