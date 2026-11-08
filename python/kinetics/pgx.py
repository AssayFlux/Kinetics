"""Provenance-first PGx allele-definition foundations; no clinical interpretation.

Definitions must be imported from reviewed, versioned sources. This module only
matches fully phased small-variant sets to explicitly supplied allele definitions.
It does not infer phase, copy number, structural alleles, phenotype or treatment.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, order=True)
class VariantKey:
    genome_build: str
    chromosome: str
    position: int
    reference: str
    alternate: str

    def __post_init__(self) -> None:
        if not self.genome_build.strip() or not self.chromosome.strip():
            raise ValueError("Variant requires genome build and chromosome")
        if self.position < 1:
            raise ValueError("Variant position must be 1-based and positive")
        if not self.reference or not self.alternate or self.reference == self.alternate:
            raise ValueError("Variant requires distinct non-empty REF and ALT alleles")
        if any(base not in "ACGT" for base in (self.reference + self.alternate).upper()):
            raise ValueError("Only normalized literal A/C/G/T variants are supported")


@dataclass(frozen=True)
class StarAlleleDefinition:
    gene_symbol: str
    star_allele: str
    required_variants: frozenset[VariantKey]
    excluded_variants: frozenset[VariantKey]
    source_name: str
    source_release: str
    source_url: str
    license_id: str
    genome_build: str
    definition_id: str


@dataclass(frozen=True)
class AlleleMatch:
    gene_symbol: str
    star_allele: str | None
    status: str
    matched_definition_ids: tuple[str, ...]
    observed_variant_count: int


def parse_star_allele_definitions(
    document: str, *, expected_source_release: str | None = None,
) -> list[StarAlleleDefinition]:
    """Load a JSON definition pack with mandatory source, build and license metadata."""
    try:
        value = json.loads(document)
    except json.JSONDecodeError as error:
        raise ValueError("PGx definition pack must be valid JSON") from error
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValueError("Unsupported PGx definition schema version")
    source = value.get("source")
    if not isinstance(source, dict):
        raise ValueError("PGx definition source metadata is mandatory")
    source_name = source.get("name")
    source_release = source.get("release")
    source_url = source.get("url")
    license_id = source.get("license")
    genome_build = value.get("genome_build")
    if not all(isinstance(item, str) and item.strip() for item in
               (source_name, source_release, source_url, license_id, genome_build)):
        raise ValueError("PGx source, release, URL, license and genome build are mandatory")
    if not source_url.startswith("https://"):
        raise ValueError("PGx source URL must use HTTPS")
    if expected_source_release is not None and source_release != expected_source_release:
        raise ValueError("PGx source release does not match the pinned release")
    raw_definitions = value.get("definitions")
    if not isinstance(raw_definitions, list) or not raw_definitions:
        raise ValueError("PGx definition pack must contain allele definitions")

    definitions: list[StarAlleleDefinition] = []
    seen: set[tuple[str, str, str]] = set()

    def variants(raw: object) -> frozenset[VariantKey]:
        if not isinstance(raw, list):
            raise ValueError("Allele variants must be arrays")
        result: set[VariantKey] = set()
        for item in raw:
            if not isinstance(item, dict):
                raise ValueError("Variant definition must be an object")
            variant = VariantKey(
                genome_build=genome_build,
                chromosome=str(item.get("chromosome", "")),
                position=item.get("position") if isinstance(item.get("position"), int) else 0,
                reference=str(item.get("ref", "")).upper(),
                alternate=str(item.get("alt", "")).upper(),
            )
            if variant in result:
                raise ValueError("Duplicate variant in allele definition")
            result.add(variant)
        return frozenset(result)

    for raw in raw_definitions:
        if not isinstance(raw, dict):
            raise ValueError("Allele definition must be an object")
        gene, star, definition_id = raw.get("gene"), raw.get("star_allele"), raw.get("id")
        if not all(isinstance(item, str) and item.strip() for item in (gene, star, definition_id)):
            raise ValueError("Allele definition requires gene, star_allele and id")
        if not star.startswith("*"):
            raise ValueError("Star allele names must begin with '*'")
        key = (gene, star, definition_id)
        if key in seen:
            raise ValueError("Duplicate PGx allele definition identifier")
        seen.add(key)
        required = variants(raw.get("required_variants", []))
        excluded = variants(raw.get("excluded_variants", []))
        if required & excluded:
            raise ValueError("A variant cannot be both required and excluded")
        definitions.append(StarAlleleDefinition(
            gene, star, required, excluded, source_name, source_release,
            source_url, license_id, genome_build, definition_id,
        ))
    return definitions


def match_phased_haplotype(
    gene_symbol: str, observed_variants: Iterable[VariantKey],
    definitions: Iterable[StarAlleleDefinition], *, genome_build: str,
    phase_confirmed: bool, call_complete: bool = False,
) -> AlleleMatch:
    """Match one completely called, already phased haplotype; never infer missing calls."""
    if not phase_confirmed:
        return AlleleMatch(gene_symbol, None, "no_call_unphased", (), 0)
    if not call_complete:
        return AlleleMatch(gene_symbol, None, "no_call_incomplete", (), 0)
    observed = frozenset(observed_variants)
    if any(variant.genome_build != genome_build for variant in observed):
        raise ValueError("Observed variants do not match requested genome build")
    candidates = [
        definition for definition in definitions
        if definition.gene_symbol == gene_symbol and definition.genome_build == genome_build
        and definition.required_variants.issubset(observed)
        and not (definition.excluded_variants & observed)
    ]
    if not candidates:
        return AlleleMatch(gene_symbol, None, "no_matching_definition", (), len(observed))
    # A definition with more required variants is more specific, but tied best
    # definitions remain ambiguous rather than being resolved by file order.
    specificity = max(len(item.required_variants) for item in candidates)
    best = [item for item in candidates if len(item.required_variants) == specificity]
    names = sorted({item.star_allele for item in best})
    if len(names) != 1:
        return AlleleMatch(
            gene_symbol, None, "ambiguous", tuple(sorted(item.definition_id for item in best)),
            len(observed),
        )
    return AlleleMatch(
        gene_symbol, names[0], "matched", tuple(sorted(item.definition_id for item in best)),
        len(observed),
    )
