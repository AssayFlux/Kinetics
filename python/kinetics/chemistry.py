"""SDF V2000 parsing and bounded graph-only chemistry utilities.

These descriptors are exploratory and do not replace a validated cheminformatics engine.
"""
from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
from math import isfinite

ATOMIC_MASS = {
    "H": 1.008, "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998,
    "P": 30.974, "S": 32.06, "CL": 35.45, "BR": 79.904, "I": 126.90,
    "B": 10.81, "SI": 28.085,
}


def parse_sdf_record(text: str) -> dict[str, object]:
    lines = text.splitlines()
    if len(lines) < 4 or "V2000" not in lines[3]:
        raise ValueError("Only molfile V2000 is supported")
    try:
        atom_count, bond_count = int(lines[3][0:3]), int(lines[3][3:6])
    except ValueError as exc:
        raise ValueError("Invalid V2000 counts line") from exc
    if not 1 <= atom_count <= 100_000 or not 0 <= bond_count <= 200_000:
        raise ValueError("V2000 atom/bond count outside supported limits")
    if len(lines) < 4 + atom_count + bond_count:
        raise ValueError("Truncated SDF record")

    atoms = []
    elements: Counter[str] = Counter()
    for index, line in enumerate(lines[4:4 + atom_count], 1):
        if len(line) < 34:
            raise ValueError(f"Atom record {index}: truncated coordinate/element fields")
        symbol = line[31:34].strip().upper()
        if symbol not in ATOMIC_MASS:
            raise ValueError(f"Unsupported element: {symbol}")
        try:
            x, y, z = float(line[0:10]), float(line[10:20]), float(line[20:30])
        except ValueError as exc:
            raise ValueError(f"Atom record {index}: invalid coordinates") from exc
        if not all(isfinite(value) for value in (x, y, z)):
            raise ValueError(f"Atom record {index}: coordinates must be finite")
        atoms.append({"x": x, "y": y, "z": z, "element": symbol})
        elements[symbol] += 1

    bonds = []
    seen_bonds: set[tuple[int, int]] = set()
    for index, line in enumerate(lines[4 + atom_count:4 + atom_count + bond_count], 1):
        if len(line) < 9:
            raise ValueError(f"Bond record {index}: truncated bond fields")
        try:
            first, second, order = int(line[0:3]), int(line[3:6]), int(line[6:9])
        except ValueError as exc:
            raise ValueError(f"Bond record {index}: invalid numeric field") from exc
        if not (1 <= first <= atom_count and 1 <= second <= atom_count
                and first != second and order in (1, 2, 3, 4)):
            raise ValueError(f"Bond record {index}: invalid atom index or bond order")
        pair = (min(first - 1, second - 1), max(first - 1, second - 1))
        if pair in seen_bonds:
            raise ValueError(f"Bond record {index}: duplicate atom pair")
        seen_bonds.add(pair)
        bonds.append((first - 1, second - 1, order))

    return {
        "atoms": atoms, "bonds": bonds, "atom_count": atom_count, "bond_count": bond_count,
        "formula": formula(elements),
        "molecular_weight": sum(ATOMIC_MASS[element] * count for element, count in elements.items()),
        "limitations": [
            "V2000 only", "No stereochemical interpretation",
            "No protonation/tautomer normalization", "Implicit hydrogens are not inferred",
        ],
    }


def formula(elements: Counter[str]) -> str:
    keys = []
    if "C" in elements:
        keys.append("C")
    if "H" in elements:
        keys.append("H")
    keys.extend(sorted(key for key in elements if key not in ("C", "H")))
    return "".join(key + (str(elements[key]) if elements[key] != 1 else "") for key in keys)


def _graph(molecule: dict[str, object]) -> tuple[list[dict[str, object]], dict[int, list[tuple[int, int]]]]:
    atoms, bonds = molecule.get("atoms"), molecule.get("bonds")
    if not isinstance(atoms, list) or not atoms or not isinstance(bonds, list):
        raise ValueError("Expected a molecule returned by parse_sdf_record")
    adjacency: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for bond in bonds:
        if not isinstance(bond, (tuple, list)) or len(bond) != 3:
            raise ValueError("Malformed bond tuple")
        first, second, order = bond
        if (not isinstance(first, int) or not isinstance(second, int)
                or not isinstance(order, int) or not (0 <= first < len(atoms))
                or not (0 <= second < len(atoms)) or first == second
                or order not in (1, 2, 3, 4)):
            raise ValueError("Invalid graph bond")
        adjacency[first].append((second, order))
        adjacency[second].append((first, order))
    return atoms, adjacency


def graph_descriptors(molecule: dict[str, object]) -> dict[str, object]:
    atoms, adjacency = _graph(molecule)
    visited: set[int] = set()
    components = 0
    for start in range(len(atoms)):
        if start in visited:
            continue
        components += 1
        stack = [start]
        visited.add(start)
        while stack:
            current = stack.pop()
            for neighbour, _ in adjacency[current]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    stack.append(neighbour)
    edge_count = sum(len(neighbours) for neighbours in adjacency.values()) // 2
    degree_counts = Counter(len(adjacency[index]) for index in range(len(atoms)))
    return {
        "atom_count": len(atoms),
        "bond_count": edge_count,
        "connected_components": components,
        "cycle_rank": edge_count - len(atoms) + components,
        "heteroatom_count": sum(atom["element"] not in {"C", "H"} for atom in atoms),
        "degree_histogram": dict(sorted(degree_counts.items())),
        "limitations": ["Graph-only descriptors; no aromaticity, valence or stereochemical sanitization"],
    }


def path_fingerprint(
    molecule: dict[str, object], *, max_path: int = 3,
    max_features: int = 1_000_000, max_walk_states: int = 2_000_000,
) -> frozenset[str]:
    """Hash atom/bond paths with explicit memory and traversal ceilings."""
    if max_path < 1 or max_path > 6:
        raise ValueError("max_path must be between 1 and 6")
    if max_features < 1 or max_walk_states < 1:
        raise ValueError("Fingerprint resource limits must be positive")
    atoms, adjacency = _graph(molecule)
    features: set[str] = set()
    walk_states = 0

    def add_feature(value: str) -> None:
        feature = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
        if feature not in features and len(features) >= max_features:
            raise ValueError("Fingerprint exceeded max_features")
        features.add(feature)

    for index, atom in enumerate(atoms):
        start = str(atom["element"])
        add_feature(start)

        def walk(node: int, previous: int, path: tuple[str, ...], depth: int) -> None:
            nonlocal walk_states
            walk_states += 1
            if walk_states > max_walk_states:
                raise ValueError("Fingerprint exceeded max_walk_states")
            if depth >= max_path:
                return
            for neighbour, order in adjacency[node]:
                if neighbour == previous:
                    continue
                feature = path + (f"-{order}-{atoms[neighbour]['element']}",)
                add_feature("|".join(feature))
                walk(neighbour, node, feature, depth + 1)

        walk(index, -1, (start,), 0)
    return frozenset(features)


def substructure_match(
    target: dict[str, object], query: dict[str, object], *, max_search_states: int = 100_000,
) -> bool:
    """Exact element/bond-order subgraph match; ignores stereochemistry and aromaticity."""
    if max_search_states < 1:
        raise ValueError("max_search_states must be positive")
    target_atoms, target_graph = _graph(target)
    query_atoms, query_graph = _graph(query)
    if len(query_atoms) > len(target_atoms):
        return False
    candidates = {
        index: [
            target_index for target_index, target_atom in enumerate(target_atoms)
            if target_atom["element"] == atom["element"]
            and len(target_graph[target_index]) >= len(query_graph[index])
        ]
        for index, atom in enumerate(query_atoms)
    }
    if any(not values for values in candidates.values()):
        return False
    order = sorted(
        range(len(query_atoms)),
        key=lambda index: (len(candidates[index]), -len(query_graph[index]), index),
    )
    mapping: dict[int, int] = {}
    used: set[int] = set()
    states = 0

    def search(depth: int) -> bool:
        nonlocal states
        states += 1
        if states > max_search_states:
            raise ValueError("Substructure search exceeded max_search_states")
        if depth == len(order):
            return True
        query_index = order[depth]
        for target_index in candidates[query_index]:
            if target_index in used:
                continue
            compatible = True
            for query_neighbour, query_bond in query_graph[query_index]:
                if query_neighbour not in mapping:
                    continue
                target_neighbour = mapping[query_neighbour]
                if (target_neighbour, query_bond) not in target_graph[target_index]:
                    compatible = False
                    break
            if not compatible:
                continue
            mapping[query_index] = target_index
            used.add(target_index)
            if search(depth + 1):
                return True
            used.remove(target_index)
            del mapping[query_index]
        return False

    return search(0)


def tanimoto(first: frozenset[str], second: frozenset[str]) -> float:
    union = first | second
    return len(first & second) / len(union) if union else 1.0


def iter_sdf_records(text: str):
    """Yield non-empty SDF records from a multi-record V2000 file."""
    for record_number, block in enumerate(text.split("$$$$"), 1):
        if not block.strip():
            continue
        try:
            yield parse_sdf_record(block)
        except ValueError as exc:
            raise ValueError(f"SDF record {record_number}: {exc}") from exc
