# R9 — Gene catalogue and precision-medicine research foundations

**Status:** In progress. Clinical/PGx decision support remains disabled.

## Scope
- Broad, expandable cross-domain gene catalogue with source/release metadata.
- Streaming ingestion of all 16 NCBI Gene gene_info columns from plain and gzip-compressed files.
- Search by GeneID, official symbol, synonyms, description, nomenclature and cross-references.
- Future: domain-specific annotation packs, comprehensive PGx gene/allele inventories, star-allele definitions, haplotype/diplotype translation, phenotype evidence, ancestry portability and guideline-version tracking.

## Current source
Implemented in `python/kinetics/catalog.py`. Catalogue ingestion does not elevate evidence status to validated.

## Limitations and gates
- NCBI Gene gene_info is not a PGx allele-definition source.
- No validated star-allele caller, diplotype translator or guideline implementation.
- No patient data or clinical recommendations.
- D-004 adviser checkpoint, P0 legal/ethics/regulatory requirements and qualified clinical review remain mandatory before any patient workflow.

## Exit evidence
Versioned source packs, checksums/licenses, taxonomy and nomenclature coverage reports, allele-definition concordance against approved reference datasets, ancestry/fairness analysis, independent review and provenance.


### R9 PGx foundation increment

Added a versioned JSON star-allele definition schema with mandatory source name/release/HTTPS URL/license/genome build, normalized literal small-variant keys, required/excluded variant sets and duplicate-definition checks. Added conservative matching for a caller-supplied, fully phased and explicitly complete haplotype; incomplete or unphased calls produce no-call statuses, and tied best definitions remain ambiguous. This is infrastructure only: no PharmVar/CPIC/PharmGKB source data has been imported or licensed, no gene inventory is claimed comprehensive, and there is no diplotype/phenotype translation or clinical recommendation.
