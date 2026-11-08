"""Newick parsing and distance-based phylogenetic tree utilities."""
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from math import isfinite


@dataclass
class Node:
    name: str = ""
    length: float = 0.0
    children: list["Node"] = field(default_factory=list)


class _Parser:
    def __init__(self, source: str) -> None:
        self.tokens: list[str] = []
        token: list[str] = []
        quoted = False
        text = source.strip()
        index = 0
        while index < len(text):
            char = text[index]
            if char == "'":
                if quoted and index + 1 < len(text) and text[index + 1] == "'":
                    token.append("'")
                    index += 2
                    continue
                quoted = not quoted
                index += 1
                continue
            if not quoted and char in "(),:;":
                if token:
                    value = "".join(token).strip()
                    if value:
                        self.tokens.append(value)
                    token = []
                self.tokens.append(char)
            else:
                token.append(char)
            index += 1
        if quoted:
            raise ValueError("Unterminated quoted Newick label")
        if token:
            value = "".join(token).strip()
            if value:
                self.tokens.append(value)
        self.index = 0

    def peek(self) -> str | None:
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def pop(self) -> str:
        token = self.peek()
        if token is None:
            raise ValueError("Unexpected end of Newick tree")
        self.index += 1
        return token

    def subtree(self) -> Node:
        node = Node()
        if self.peek() == "(":
            self.pop()
            node.children.append(self.subtree())
            while self.peek() == ",":
                self.pop()
                node.children.append(self.subtree())
            if self.pop() != ")":
                raise ValueError("Unbalanced Newick parentheses")
        label = self.peek()
        if label is not None and label not in {",", ")", ":", ";"}:
            node.name = self.pop()
        if self.peek() == ":":
            self.pop()
            raw_length = self.pop()
            try:
                node.length = float(raw_length)
            except ValueError as exc:
                raise ValueError(f"Invalid branch length: {raw_length}") from exc
            if not isfinite(node.length) or node.length < 0:
                raise ValueError("Branch lengths must be finite and non-negative")
        return node


def parse_newick(source: str) -> Node:
    if not source.strip():
        raise ValueError("Newick tree cannot be empty")
    parser = _Parser(source)
    root = parser.subtree()
    if parser.pop() != ";" or parser.peek() is not None:
        raise ValueError("Newick must contain one tree terminated by semicolon")
    return root


def leaf_names(root: Node) -> list[str]:
    return [node.name for node in _walk(root) if not node.children]


def patristic_distance(root: Node, first: str, second: str) -> float:
    paths: dict[str, list[tuple[Node, float]]] = {}

    def visit(node: Node, ancestors: list[tuple[Node, float]], distance: float) -> None:
        current = ancestors + [(node, distance)]
        if not node.children:
            if node.name in paths:
                raise ValueError(f"Duplicate leaf name: {node.name}")
            paths[node.name] = current
        for child in node.children:
            visit(child, current, distance + child.length)

    visit(root, [], 0.0)
    if first not in paths or second not in paths:
        raise ValueError("Requested leaf is absent")
    a, b = paths[first], paths[second]
    common = 0
    while common < min(len(a), len(b)) and a[common][0] is b[common][0]:
        common += 1
    return a[-1][1] + b[-1][1] - 2 * (a[common - 1][1] if common else 0.0)


def _walk(node: Node) -> Iterator[Node]:
    yield node
    for child in node.children:
        yield from _walk(child)


def upgma(distance_matrix: list[list[float]], labels: list[str]) -> Node:
    """Construct a rooted UPGMA tree from a finite symmetric distance matrix."""
    size = len(labels)
    if size < 2 or len(distance_matrix) != size or len(set(labels)) != size:
        raise ValueError("Need at least two unique labels and a square matrix")
    if any(len(row) != size for row in distance_matrix):
        raise ValueError("Distance matrix must be square")
    for i in range(size):
        if not isfinite(distance_matrix[i][i]) or abs(distance_matrix[i][i]) > 1e-12:
            raise ValueError("Distance matrix diagonal must be finite and zero")
        for j in range(size):
            value = distance_matrix[i][j]
            if not isfinite(value) or value < 0 or abs(value - distance_matrix[j][i]) > 1e-9:
                raise ValueError("Distances must be finite, non-negative and symmetric")
    clusters: dict[int, tuple[Node, list[int], float]] = {
        i: (Node(name=labels[i]), [i], 0.0) for i in range(size)
    }
    distances = {(i, j): distance_matrix[i][j] for i in range(size) for j in range(i + 1, size)}
    next_id = size
    while len(clusters) > 1:
        pair = min(distances, key=lambda key: distances[key])
        first, second = pair
        distance = distances[pair]
        height = distance / 2.0
        left, left_members, left_height = clusters.pop(first)
        right, right_members, right_height = clusters.pop(second)
        left.length = max(0.0, height - left_height)
        right.length = max(0.0, height - right_height)
        merged = Node(children=[left, right])
        members = left_members + right_members
        old_ids = list(clusters)
        distances = {
            key: value for key, value in distances.items()
            if first not in key and second not in key
        }
        for other in old_ids:
            other_members = clusters[other][1]
            numerator = sum(distance_matrix[a][b] for a in members for b in other_members)
            distances[(min(next_id, other), max(next_id, other))] = numerator / (
                len(members) * len(other_members)
            )
        clusters[next_id] = (merged, members, height)
        next_id += 1
    return next(iter(clusters.values()))[0]


def neighbor_joining(distance_matrix: list[list[float]], labels: list[str]) -> Node:
    """Build a neighbour-joining tree; rejects negative inferred limbs rather than clipping.

    The distance matrix must contain finite, non-negative, symmetric distances with a
    zero diagonal. Non-additive/noisy matrices can imply negative limbs; those inputs
    are rejected and must not be silently altered.
    """
    size = len(labels)
    if size < 2 or len(distance_matrix) != size or len(set(labels)) != size:
        raise ValueError("Need at least two unique labels and a square matrix")
    if any(len(row) != size for row in distance_matrix):
        raise ValueError("Distance matrix must be square")
    for i in range(size):
        if not isfinite(distance_matrix[i][i]) or abs(distance_matrix[i][i]) > 1e-12:
            raise ValueError("Distance matrix diagonal must be finite and zero")
        for j in range(size):
            value = distance_matrix[i][j]
            if not isfinite(value) or value < 0 or abs(value - distance_matrix[j][i]) > 1e-9:
                raise ValueError("Distances must be finite, non-negative and symmetric")
    clusters: dict[int, Node] = {i: Node(name=labels[i]) for i in range(size)}
    distances = {
        (i, j): float(distance_matrix[i][j])
        for i in range(size) for j in range(i + 1, size)
    }
    next_id = size
    while len(clusters) > 2:
        active = sorted(clusters)
        count = len(active)
        totals = {
            i: sum(distances[tuple(sorted((i, j)))] for j in active if j != i)
            for i in active
        }
        pair = min(
            ((i, j) for pos, i in enumerate(active) for j in active[pos + 1:]),
            key=lambda ij: ((count - 2) * distances[ij] - totals[ij[0]] - totals[ij[1]], ij),
        )
        first, second = pair
        distance = distances[pair]
        limb_first = 0.5 * distance + (totals[first] - totals[second]) / (2 * (count - 2))
        limb_second = distance - limb_first
        tolerance = 1e-10 * max(1.0, distance)
        if limb_first < -tolerance or limb_second < -tolerance:
            raise ValueError("Neighbour joining inferred a negative branch length")
        parent = Node(children=[
            Node(length=max(0.0, limb_first), children=[clusters[first]]),
            Node(length=max(0.0, limb_second), children=[clusters[second]]),
        ])
        others = [item for item in active if item not in pair]
        for item in others:
            left = distances[tuple(sorted((first, item)))]
            right = distances[tuple(sorted((second, item)))]
            new_distance = 0.5 * (left + right - distance)
            if not isfinite(new_distance) or new_distance < -tolerance:
                raise ValueError("Neighbour joining inferred an invalid cluster distance")
            distances[tuple(sorted((next_id, item)))] = max(0.0, new_distance)
        for key in list(distances):
            if first in key or second in key:
                del distances[key]
        del clusters[first]
        del clusters[second]
        clusters[next_id] = parent
        next_id += 1

    first, second = sorted(clusters)
    final_distance = distances[tuple(sorted((first, second)))]
    root = Node(children=[
        Node(length=final_distance / 2.0, children=[clusters[first]]),
        Node(length=final_distance / 2.0, children=[clusters[second]]),
    ])
    return root

def to_newick(root: Node) -> str:
    """Serialize a tree to deterministic Newick with safe quoting and branch lengths."""
    active: set[int] = set()

    def label_text(label: str) -> str:
        if not label:
            return ""
        if any(character.isspace() or character in "(),:;[]'" for character in label):
            return "'" + label.replace("'", "''") + "'"
        return label

    def render(node: Node) -> str:
        identity = id(node)
        if identity in active:
            raise ValueError("Tree contains a cycle")
        if not isfinite(node.length) or node.length < 0:
            raise ValueError("Branch lengths must be finite and non-negative")
        active.add(identity)
        try:
            children = ""
            if node.children:
                children = "(" + ",".join(render(child) for child in node.children) + ")"
            result = children + label_text(node.name)
            if node.length != 0:
                result += ":" + format(node.length, ".17g")
            elif node is not root:
                result += ":0"
            return result
        finally:
            active.remove(identity)

    return render(root) + ";"

