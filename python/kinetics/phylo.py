"""Small recursive-descent Newick parser and tree utilities."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    name: str = ""
    length: float = 0.0
    children: list["Node"] = field(default_factory=list)


class _Parser:
    def __init__(self, source: str) -> None:
        self.tokens: list[str] = []
        token = ""
        for char in source.strip():
            if char in "(),:;":
                if token.strip():
                    self.tokens.append(token.strip())
                self.tokens.append(char)
                token = ""
            else:
                token += char
        if token.strip():
            self.tokens.append(token.strip())
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
            if node.length < 0:
                raise ValueError("Negative branch lengths are not supported")
        return node


def parse_newick(source: str) -> Node:
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


def _walk(node: Node):
    yield node
    for child in node.children:
        yield from _walk(child)



def upgma(distance_matrix: list[list[float]], labels: list[str]) -> Node:
    """Construct a rooted UPGMA tree from a symmetric distance matrix."""
    size = len(labels)
    if size < 2 or len(distance_matrix) != size or len(set(labels)) != size:
        raise ValueError("Need at least two unique labels and a square matrix")
    if any(len(row) != size for row in distance_matrix):
        raise ValueError("Distance matrix must be square")
    for i in range(size):
        if abs(distance_matrix[i][i]) > 1e-12:
            raise ValueError("Distance matrix diagonal must be zero")
        for j in range(size):
            value = distance_matrix[i][j]
            if value < 0 or abs(value - distance_matrix[j][i]) > 1e-9:
                raise ValueError("Distances must be non-negative and symmetric")
    clusters: dict[int, tuple[Node, list[int], float]] = {
        i: (Node(name=labels[i]), [i], 0.0) for i in range(size)
    }
    distances = {(i, j): distance_matrix[i][j] for i in range(size) for j in range(i+1, size)}
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
