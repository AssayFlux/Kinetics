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
