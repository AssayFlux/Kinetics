from __future__ import annotations

import pytest

from kinetics.catalog import iter_ncbi_gene_info, validate_gene_catalog


def test_ncbi_gene_info_preserves_full_annotation_and_release() -> None:
    row = "\t".join([
        "9606", "7157", "TP53", "-", "P53|BCC7", "MIM:191170|HGNC:11998",
        "17", "17p13.1", "tumor protein p53", "protein-coding", "TP53",
        "tumor protein p53", "Official", "cellular tumor antigen p53",
        "20250101", "gene",
    ])
    gene = next(iter_ncbi_gene_info([row], source_release="NCBI-2025-01"))
    assert gene.gene_id == "7157"
    assert gene.synonyms == ("BCC7", "P53")
    assert gene.dbxrefs == ("HGNC:11998", "MIM:191170")
    assert gene.chromosome == "17"
    assert gene.nomenclature_full_name == "tumor protein p53"
    assert gene.source_release == "NCBI-2025-01"


def test_gene_catalog_rejects_truncated_rows_and_duplicate_ids() -> None:
    with pytest.raises(ValueError, match="16 NCBI columns"):
        list(iter_ncbi_gene_info(["9606\t1\tA"], source_release="release"))
    entries = list(iter_ncbi_gene_info([
        "\t".join(["9606", "1", "A", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "20250101", "gene"]),
        "\t".join(["9606", "1", "A2", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "20250101", "gene"]),
    ], source_release="release"))
    with pytest.raises(ValueError, match="Duplicate"):
        validate_gene_catalog(entries)


def test_catalog_import_cannot_mark_gene_validated() -> None:
    from dataclasses import replace

    entry = next(iter_ncbi_gene_info([
        "\t".join(["9606", "1", "A", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "20250101", "gene"])
    ], source_release="release"))
    with pytest.raises(ValueError, match="cannot confer validated"):
        validate_gene_catalog([replace(entry, evidence_status="validated")])


def test_gene_catalog_searches_synonyms_and_nomenclature_with_taxonomy_filter() -> None:
    from kinetics.catalog import search_gene_catalog

    row = "\t".join([
        "9606", "7157", "TP53", "-", "P53|BCC7", "HGNC:11998", "17",
        "17p13.1", "tumor protein p53", "protein-coding", "TP53",
        "tumor protein p53", "Official", "-", "20250101", "gene",
    ])
    entries = list(iter_ncbi_gene_info([row], source_release="NCBI-2025-01"))
    assert search_gene_catalog(entries, "p53")[0].gene_id == "7157"
    assert search_gene_catalog(entries, "7157", tax_id="10090") == []
    with pytest.raises(ValueError, match="cannot be empty"):
        search_gene_catalog(entries, " ")
