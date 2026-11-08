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



def test_pgx_definition_pack_requires_pinned_source_and_matches_only_complete_phase() -> None:
    import json

    from kinetics.pgx import VariantKey, match_phased_haplotype, parse_star_allele_definitions

    pack = {
        "schema_version": 1, "genome_build": "GRCh38",
        "source": {"name": "Reviewed PGx source fixture", "release": "fixture-1",
                   "url": "https://example.org/fixture", "sha256": "a" * 64, "license": "CC-BY-4.0"},
        "definitions": [{
            "id": "CYP2C19-17-def-1", "gene": "CYP2C19", "star_allele": "*17",
            "required_variants": [{"chromosome": "10", "position": 94781859, "ref": "C", "alt": "T"}],
            "excluded_variants": [],
        }],
    }
    definitions = parse_star_allele_definitions(json.dumps(pack), expected_source_release="fixture-1")
    variant = VariantKey("GRCh38", "10", 94781859, "C", "T")
    incomplete = match_phased_haplotype(
        "CYP2C19", [variant], definitions, genome_build="GRCh38", phase_confirmed=True,
    )
    assert incomplete.status == "no_call_incomplete"
    matched = match_phased_haplotype(
        "CYP2C19", [variant], definitions, genome_build="GRCh38",
        phase_confirmed=True, call_complete=True,
    )
    assert matched.status == "matched"
    assert matched.star_allele == "*17"


def test_pgx_definition_pack_rejects_release_mismatch_and_unphased_call() -> None:
    import json

    from kinetics.pgx import match_phased_haplotype, parse_star_allele_definitions

    pack = {
        "schema_version": 1, "genome_build": "GRCh38",
        "source": {"name": "fixture", "release": "v1", "url": "https://example.org", "sha256": "b" * 64, "license": "MIT"},
        "definitions": [{"id": "d1", "gene": "GENE1", "star_allele": "*1",
                         "required_variants": [], "excluded_variants": []}],
    }
    with pytest.raises(ValueError, match="pinned release"):
        parse_star_allele_definitions(json.dumps(pack), expected_source_release="v2")
    definitions = parse_star_allele_definitions(json.dumps(pack), expected_source_release="v1")
    result = match_phased_haplotype(
        "GENE1", [], definitions, genome_build="GRCh38", phase_confirmed=False,
        call_complete=True,
    )
    assert result.status == "no_call_unphased"
