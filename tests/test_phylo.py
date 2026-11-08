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


def test_neighbor_joining_recovers_additive_three_taxon_distances() -> None:
    from kinetics.phylo import neighbor_joining, patristic_distance

    tree = neighbor_joining(
        [[0.0, 2.0, 4.0], [2.0, 0.0, 4.0], [4.0, 4.0, 0.0]],
        ["A", "B", "C"],
    )
    assert patristic_distance(tree, "A", "B") == pytest.approx(2.0)
    assert patristic_distance(tree, "A", "C") == pytest.approx(4.0)
    assert patristic_distance(tree, "B", "C") == pytest.approx(4.0)


def test_neighbor_joining_rejects_negative_inferred_limb() -> None:
    from kinetics.phylo import neighbor_joining

    with pytest.raises(ValueError, match="negative branch"):
        neighbor_joining(
            [[0.0, 1.0, 10.0], [1.0, 0.0, 1.0], [10.0, 1.0, 0.0]],
            ["A", "B", "C"],
        )



def test_newick_serializer_round_trips_quoted_labels_and_branch_lengths() -> None:
    from kinetics.phylo import parse_newick, patristic_distance, to_newick

    original = parse_newick("((A:0.1,'B B':0.2)clade:0.3,C:0);")
    serialized = to_newick(original)
    restored = parse_newick(serialized)
    assert leaf_names(restored) == ["A", "B B", "C"]
    assert patristic_distance(original, "A", "B B") == pytest.approx(
        patristic_distance(restored, "A", "B B")
    )
