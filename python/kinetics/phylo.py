"""Small Newick parser and patristic-distance utilities."""
from __future__ import annotations
from dataclasses import dataclass,field

@dataclass
class Node:
    name:str=""
    length:float=0.0
    children:list["Node"]=field(default_factory=list)

def parse_newick(source: str) -> Node:
    text=source.strip()
    if not text.endswith(";"): raise ValueError("Newick must end with semicolon")
    tokens=[]; buf=""
    for char in text[:-1]:
        if char in "(),:": 
            if buf.strip(): tokens.append(buf.strip())
            tokens.append(char); buf=""
        else: buf+=char
    if buf.strip(): tokens.append(buf.strip())
    stack=[]; root=None; current=None; expect_length=False
    for token in tokens:
        if token=="(":
            node=Node()
            if current is not None: current.children.append(node)
            stack.append(node); current=node
        elif token==",":
            continue
        elif token==")":
            if not stack: raise ValueError("Unbalanced Newick")
            current=stack.pop()
            if not stack: root=current
        elif token==":":
            expect_length=True
        else:
            if expect_length:
                try: current.length=float(token)
                except (ValueError,AttributeError) as exc: raise ValueError("Invalid branch length") from exc
                expect_length=False
            elif current is None:
                current=Node(name=token); root=current
            elif current.children or not current.name:
                current.name=token
            else:
                parent=stack[-1] if stack else None
                if parent is None: raise ValueError("Unexpected Newick label")
                parent.children.append(Node(name=token))
    if root is None or stack: raise ValueError("Invalid Newick tree")
    return root

def leaf_names(root: Node) -> list[str]:
    return [n.name for n in _walk(root) if not n.children]
def _walk(node:Node):
    yield node
    for child in node.children: yield from _walk(child)
