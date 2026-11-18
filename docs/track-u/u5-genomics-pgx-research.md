# U5 — Genomics, PGx and in-silico research surfaces

**Disposition:** PARTIAL — a bounded aggregate-only VCF research QC surface is integrated; PGx and in-silico launchers remain deliberately gated.
**Scope:** synthetic/public datasets and patient-derived research data within the institutional approval scope declared by the owner under D-025. The approval reference and protocol copy remain pending attachment; clinical deployment remains separate.

## Implemented in this work package

### P1 — aggregate VCF research QC

- Home now exposes a VCF record-structure QC card when the repository's genomics.sam_vcf source capability is present.
- Android SAF accepts uncompressed .vcf and bounded .vcf.gz files, with strict UTF-8 decoding, NUL rejection and a 5 MiB input ceiling.
- The user must confirm institutional authorization for the selected dataset before analysis is enabled. This is an operator declaration, not automated data-origin verification.
- The Python parser applies hard ceilings of 10,000 variant records and 32 sample columns.
- The result contains aggregate record, contig, filter, missing-QUAL, SNV and multiallelic counts plus source SHA-256 and tool metadata.
- Sample names and genotype strings are never returned in the result. The UI does not persist the VCF or result in ResearchStore and does not offer an export from this screen.
- The output explicitly states that this is basic record-structure and aggregate QC only: no reference build or REF concordance, normalization, phasing, variant effect, pathogenicity, PGx or clinical interpretation is performed.

### Explicit gate presentation

- The Home research notice states that PGx parsing/matching source is not an approved clinical caller. Licensed release-pinned allele packs, independent biological concordance and qualified review are not established.
- Individual genotype interpretation, star-allele/diplotype/phenotype assignment and guideline recommendations are not exposed.
- Docking and OpenMM remain host-side adapters; no secured compute node is deployed. No validated force-field pack or ADMET model/dataset is approved. Android does not present these engines as runnable.
- No patient-care, diagnosis, treatment, human-subject recruitment or remote-inference workflow is added. Patient-data research testing is limited to the declared institutional approval scope.

## Current dependencies and non-claims

- The D-025 research-testing scope is owner-authorized. The approval record remains pending attachment; independent privacy/security and scientific review are still open. No patient-specific risk, diagnosis, treatment, dosing or clinical decision support is provided.
- P1 still needs exact-source terms review, acquired/licensed public resources, authoritative reference concordance, fuzz/resource audit and device workflow verification.
- P2 still needs licensed release-pinned definitions, broader gene coverage, independent biological concordance and complex-allele/CNV/SV support. The Android screen does not invoke PGx allele matching.
- P3 has a research evidence schema only; no licensed guideline corpus or executable recommendation mapping.
- I2 docking remains host-only and lacks independent redocking/cross-docking and decoy-enrichment validation.
- I3 OpenMM remains CPU host-only; no approved force field or independent biomolecular validation.
- I4 has no selected/acquired ADMET dataset or prediction model and no external calibration/validation.
- Patient-derived data may be used for the bounded aggregate QC workflow only when covered by the institutional approval. No clinical interpretation is performed.

## Verification added

- tests/test_genomics.py verifies aggregate VCF counts, bounds, missing records and that sample names/genotype strings do not appear in the returned report.
- tests/test_android_scientific_viewers.py verifies the consent-gated Android surface, input ceiling, no persistence/export path and explicit PGx/in-silico gates.
- Exact-head CI, embedded Android Python runtime fixture tests, device validation, legal/source-rights review and independent scientific review remain required.

**Decision:** U5 is not closed. The Android genomics QC surface is implemented; PGx and in-silico capabilities remain visibly unavailable until their independent and the relevant independent evidence gates are satisfied.
