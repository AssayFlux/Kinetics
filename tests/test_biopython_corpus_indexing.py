from pathlib import Path

from scripts.tokenize_corpus import extract_text


def test_fasta_is_parsed_with_biopython_and_split_into_searchable_kmers(tmp_path: Path):
    fasta = tmp_path / "sample.fasta"
    fasta.write_text(">seq1 enzyme sequence\nATGAAACCCGGG\n", encoding="utf-8")
    text = extract_text(fasta)
    assert ">seq1" in text
    assert "ATG AAA CCC GGG" in text
