from __future__ import annotations

import pytest

from kinetics.phylo import leaf_names, parse_newick, upgma


def test_newick_supports_quoted_labels_with_delimiters_and_escaped_quotes() -> None:
    tree = parse_newick("('A, B':1,'C''D':2);")
    assert leaf_names(tree) == ["A, B", "C'D"]


@pytest.mark.parametrize("source", ["(A:NaN,B:1);", "(A:inf,B:1);", "(A:-1,B:1);", "('A,B:1);"])
def test_newick_rejects_non_finite_negative_and_unterminated_values(source: str) -> None:
    with pytest.raises(ValueError):
        parse_newick(source)


def test_upgma_rejects_non_finite_distance_values() -> None:
    with pytest.raises(ValueError, match="finite"):
        upgma([[0.0, float("nan")], [float("nan"), 0.0]], ["a", "b"])
