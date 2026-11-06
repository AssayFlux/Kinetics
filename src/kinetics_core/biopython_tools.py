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
        from Bio import PDB, Align
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
    if not atoms:
        return {
            "feature": "residue_contacts",
            "method": "Biopython NeighborSearch",
            "biopython_version": _biopython_version(),
            "source_sha256": _source_digest(source),
            "model_index": model_index,
            "cutoff_angstrom": cutoff_angstrom,
            "contacts": [],
        }
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
            raise ValueError(
                f"Explicit residue pair {ref_number}:{mob_number} lacks C-alpha"
            ) from exc
    if any(
        a.get_parent().resname != b.get_parent().resname
        for a, b in zip(fixed, moving, strict=True)
    ):
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


def align_sequence_to_structure_chain(
    reference_sequence: str,
    source: str | Path | bytes,
    *,
    file_format: str,
    chain_id: str,
) -> dict[str, Any]:
    """Align a reference protein sequence to a structure chain and report explicit residue mapping.

    The mapping is an alignment-derived hypothesis. Ambiguous alignments and
    mismatches are reported rather than silently promoted to validated identity.
    """
    Align, PDB, _, _, _ = _biopython()
    from Bio.Align import substitution_matrices
    from Bio.PDB.Polypeptide import protein_letters_3to1_extended

    reference = "".join(reference_sequence.split()).upper()
    if not reference:
        raise ValueError("reference_sequence cannot be empty")
    if any(symbol not in "ACDEFGHIKLMNPQRSTVWYBXZJUO" for symbol in reference):
        raise ValueError("reference_sequence contains unsupported amino-acid symbols")
    structure = _parse_structure(source, file_format)
    models = list(structure.get_models())
    if not models or chain_id not in models[0]:
        raise ValueError(f"Requested chain {chain_id!r} is absent from the first model")
    residues = [
        residue for residue in models[0][chain_id]
        if residue.id[0] == " " and residue.has_id("CA")
    ]
    if not residues:
        raise ValueError("Selected chain contains no mapped polymer residues with C-alpha atoms")
    chain_sequence = "".join(
        protein_letters_3to1_extended.get(residue.resname, "X")
        for residue in residues
    )
    aligner = Align.PairwiseAligner()
    aligner.mode = "global"
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    aligner.open_gap_score = -10.0
    aligner.extend_gap_score = -0.5
    alignments = aligner.align(reference, chain_sequence)
    if len(alignments) == 0:
        raise ValueError("No sequence-to-structure alignment was produced")
    best = alignments[0]
    indices = best.indices
    mapped = []
    mapped_reference = set()
    mapped_structure = set()
    for reference_index, structure_index in zip(indices[0], indices[1], strict=True):
        if reference_index < 0 or structure_index < 0:
            continue
        residue = residues[int(structure_index)]
        ref_aa = reference[int(reference_index)]
        chain_aa = chain_sequence[int(structure_index)]
        mapped_reference.add(int(reference_index))
        mapped_structure.add(int(structure_index))
        mapped.append({
            "sequence_position": int(reference_index) + 1,
            "sequence_residue": ref_aa,
            "chain_id": chain_id,
            "structure_residue_number": int(residue.id[1]),
            "insertion_code": str(residue.id[2]).strip(),
            "structure_residue_name": str(residue.resname),
            "structure_residue": chain_aa,
            "identity_match": ref_aa == chain_aa or ref_aa == "X" or chain_aa == "X",
        })
    return {
        "method": "Biopython PairwiseAligner",
        "biopython_version": _biopython_version(),
        "file_format": file_format,
        "source_sha256": _source_digest(source),
        "chain_id": chain_id,
        "alignment_score": float(best.score),
        "alignment_is_unique": len(alignments) == 1,
        "alignment": str(best),
        "reference_sequence_length": len(reference),
        "structure_chain_sequence_length": len(chain_sequence),
        "mapped_residue_count": len(mapped),
        "mismatch_count": sum(not item["identity_match"] for item in mapped),
        "unmapped_reference_positions": [
            index + 1 for index in range(len(reference)) if index not in mapped_reference
        ],
        "unmapped_structure_residue_ids": [
            {
                "residue_number": int(residue.id[1]),
                "insertion_code": str(residue.id[2]).strip(),
                "residue_name": str(residue.resname),
            }
            for index, residue in enumerate(residues) if index not in mapped_structure
        ],
        "mapping": mapped,
    }


def calculate_ligand_contacts(
    source: str | Path | bytes, *, file_format: str, cutoff_angstrom: float = 4.0,
    model_index: int = 0
) -> dict[str, Any]:
    """Report geometric contacts between non-water non-polymer residues and protein residues."""
    _, _, NeighborSearch, _, _ = _biopython()
    if not math.isfinite(cutoff_angstrom) or not 0 < cutoff_angstrom <= 15:
        raise ValueError("cutoff_angstrom must be finite and in (0, 15]")
    structure = _parse_structure(source, file_format)
    models = list(structure.get_models())
    if not 0 <= model_index < len(models):
        raise ValueError("model_index is outside the structure model range")
    model = models[model_index]
    protein_atoms = [
        atom for atom in model.get_atoms()
        if atom.get_parent().id[0] == " "
        and atom.element.strip().upper() not in {"H", "D"}
    ]
    if not protein_atoms:
        return {
            "feature": "ligand_residue_contacts",
            "method": "Biopython NeighborSearch",
            "biopython_version": _biopython_version(),
            "source_sha256": _source_digest(source),
            "model_index": model_index,
            "cutoff_angstrom": cutoff_angstrom,
            "status": "no_polymer_atoms",
            "contacts": [],
        }
    search = NeighborSearch(protein_atoms)
    grouped: dict[tuple[str, str, int, str, int, str], float] = {}
    for ligand_residue in model.get_residues():
        if ligand_residue.id[0] == " " or ligand_residue.resname in {"HOH", "WAT", "DOD"}:
            continue
        ligand_chain = str(ligand_residue.get_parent().id)
        for ligand_atom in ligand_residue:
            if ligand_atom.element.strip().upper() in {"H", "D"}:
                continue
            for protein_atom in search.search(ligand_atom.coord, cutoff_angstrom, level="A"):
                protein_residue = protein_atom.get_parent()
                key = (
                    ligand_chain,
                    str(ligand_residue.resname),
                    int(ligand_residue.id[1]),
                    str(protein_residue.get_parent().id),
                    int(protein_residue.id[1]),
                    str(protein_residue.id[2]).strip(),
                )
                distance = float(ligand_atom - protein_atom)
                if key not in grouped or distance < grouped[key]:
                    grouped[key] = distance
    contacts = [
        {
            "ligand": {"chain_id": key[0], "residue_name": key[1], "residue_number": key[2]},
            "protein_residue": {
                "chain_id": key[3], "residue_number": key[4], "insertion_code": key[5]
            },
            "minimum_heavy_atom_distance_angstrom": distance,
        }
        for key, distance in sorted(grouped.items())
    ]
    return {
        "feature": "ligand_residue_contacts",
        "method": "Biopython NeighborSearch",
        "biopython_version": _biopython_version(),
        "source_sha256": _source_digest(source),
        "model_index": model_index,
        "cutoff_angstrom": cutoff_angstrom,
        "status": "computed" if contacts else "no_ligand_contacts_within_cutoff",
        "contacts": contacts,
    }


def calculate_hydrogen_bonds(
    source: str | Path | bytes, *, file_format: str, donor_acceptor_cutoff_angstrom: float = 3.5,
    minimum_dha_angle_degrees: float = 120.0, model_index: int = 0
) -> dict[str, Any]:
    """Detect geometrical N-H...O hydrogen bonds only when explicit hydrogens exist.

    This conservative detector does not add hydrogens, assign protonation states,
    or infer bonds from donor/acceptor distance alone.
    """
    _, _, NeighborSearch, _, _ = _biopython()
    if (
        not math.isfinite(donor_acceptor_cutoff_angstrom)
        or not 2 < donor_acceptor_cutoff_angstrom <= 5
    ):
        raise ValueError("donor_acceptor_cutoff_angstrom must be in (2, 5]")
    if (
        not math.isfinite(minimum_dha_angle_degrees)
        or not 90 <= minimum_dha_angle_degrees <= 180
    ):
        raise ValueError("minimum_dha_angle_degrees must be in [90, 180]")
    structure = _parse_structure(source, file_format)
    models = list(structure.get_models())
    if not 0 <= model_index < len(models):
        raise ValueError("model_index is outside the structure model range")
    model = models[model_index]
    atoms = list(model.get_atoms())
    hydrogens = [atom for atom in atoms if atom.element.strip().upper() in {"H", "D"}]
    if not hydrogens:
        return {
            "feature": "hydrogen_bonds",
            "method": "explicit N-H...O distance and angle geometry",
            "biopython_version": _biopython_version(),
            "source_sha256": _source_digest(source),
            "model_index": model_index,
            "status": "not_computed_no_explicit_hydrogens",
            "hydrogen_bonds": [],
        }
    donors = [atom for atom in atoms if atom.element.strip().upper() == "N"]
    acceptors = [
        atom for atom in atoms
        if atom.element.strip().upper() == "O"
        and atom.get_parent().resname not in {"HOH", "WAT", "DOD"}
    ]
    if not donors or not acceptors:
        return {
            "feature": "hydrogen_bonds",
            "method": "explicit N-H...O distance and angle geometry",
            "biopython_version": _biopython_version(),
            "source_sha256": _source_digest(source),
            "model_index": model_index,
            "status": "no_donors_or_acceptors",
            "hydrogen_bonds": [],
        }
    acceptor_search = NeighborSearch(acceptors)
    found: dict[tuple[str, int, str, str, str, int, str, str], dict[str, Any]] = {}
    for donor in donors:
        attached = [
            hydrogen for hydrogen in hydrogens
            if float(donor - hydrogen) <= 1.25
        ]
        if not attached:
            continue
        donor_residue = donor.get_parent()
        donor_key = (
            str(donor_residue.get_parent().id), int(donor_residue.id[1]),
            str(donor_residue.id[2]).strip(), str(donor.name),
        )
        for acceptor in acceptor_search.search(
            donor.coord, donor_acceptor_cutoff_angstrom, level="A"
        ):
            acceptor_residue = acceptor.get_parent()
            if acceptor_residue is donor_residue:
                continue
            distance = float(donor - acceptor)
            if distance > donor_acceptor_cutoff_angstrom:
                continue
            for hydrogen in attached:
                donor_vector = donor.coord - hydrogen.coord
                acceptor_vector = acceptor.coord - hydrogen.coord
                donor_norm = float(sum(value * value for value in donor_vector)) ** 0.5
                acceptor_norm = float(sum(value * value for value in acceptor_vector)) ** 0.5
                if donor_norm == 0 or acceptor_norm == 0:
                    continue
                cosine = float(
                    sum(a * b for a, b in zip(donor_vector, acceptor_vector, strict=True))
                    / (donor_norm * acceptor_norm)
                )
                angle = math.degrees(math.acos(max(-1.0, min(1.0, cosine))))
                if angle < minimum_dha_angle_degrees:
                    continue
                acceptor_key = (
                    str(acceptor_residue.get_parent().id), int(acceptor_residue.id[1]),
                    str(acceptor_residue.id[2]).strip(), str(acceptor.name),
                )
                key = (*donor_key, *acceptor_key)
                found[key] = {
                    "donor": {
                        "chain_id": donor_key[0], "residue_number": donor_key[1],
                        "insertion_code": donor_key[2], "atom_name": donor_key[3],
                        "xyz_angstrom": [float(value) for value in donor.coord],
                    },
                    "hydrogen": {
                        "atom_name": str(hydrogen.name),
                        "xyz_angstrom": [float(value) for value in hydrogen.coord],
                    },
                    "acceptor": {
                        "chain_id": acceptor_key[0], "residue_number": acceptor_key[1],
                        "insertion_code": acceptor_key[2], "atom_name": acceptor_key[3],
                        "xyz_angstrom": [float(value) for value in acceptor.coord],
                    },
                    "donor_acceptor_distance_angstrom": distance,
                    "donor_hydrogen_acceptor_angle_degrees": angle,
                }
    bonds = list(found.values())
    return {
        "feature": "hydrogen_bonds",
        "method": "explicit N-H...O distance and angle geometry",
        "biopython_version": _biopython_version(),
        "source_sha256": _source_digest(source),
        "model_index": model_index,
        "donor_acceptor_cutoff_angstrom": donor_acceptor_cutoff_angstrom,
        "minimum_dha_angle_degrees": minimum_dha_angle_degrees,
        "status": "computed" if bonds else "no_geometric_hydrogen_bonds_found",
        "hydrogen_bonds": bonds,
    }
