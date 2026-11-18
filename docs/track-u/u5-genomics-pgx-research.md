# U5 — Genomics, PGx and in-silico research surfaces

**Disposition:** PARTIAL — a bounded aggregate-only VCF research QC surface is integrated; PGx and in-silico launchers remain deliberately gated.
**Scope:** synthetic or authorized public non-patient data only. P0 remains BLOCKED / NOT APPROVED.

## Implemented in this work package

### P1 — aggregate VCF research QC

- Explore now exposes a VCF record-structure QC card when the repository's genomics.sam_vcf source capability is present.
- Android SAF accepts uncompressed .vcf files only, with strict UTF-8 decoding, NUL rejection and a 5 MiB input ceiling.
- The user must explicitly attest that the selected file contains synthetic or authorized public non-patient data before analysis is enabled. This is an operator declaration, not automated data-origin verification.
- The Python parser applies hard ceilings of 10,000 variant records and 32 sample columns.
- The result contains aggregate record, contig, filter, missing-QUAL, SNV and multiallelic counts plus source SHA-256 and tool metadata.
- Sample names and genotype strings are never returned in the result. The UI does not persist the VCF or result in ResearchStore and does not offer an export from this screen.
- The output explicitly states that this is basic record-structure and aggregate QC only: no reference build or REF concordance, normalization, phasing, variant effect, pathogenicity, PGx or clinical interpretation is performed.

### Explicit gate presentation

- Explore states that PGx parsing/matching source is not an approved clinical caller. Licensed release-pinned allele packs, independent biological concordance and qualified review are not established.
- Individual genotype interpretation, star-allele/diplotype/phenotype assignment and guideline recommendations are not exposed.
- Docking and OpenMM remain host-side adapters; no secured compute node is deployed. No validated force-field pack or ADMET model/dataset is approved. Android does not present these engines as runnable.
- No new clinical, patient, human-subject, remote inference or telemetry path is added.

## Current dependencies and non-claims

- P0-E01–E12 remain draft/pending; formal P0 is NOT APPROVED. No patient/clinical records, human-subject data, patient-specific risk, diagnosis, treatment, dosing or clinical decision support.
- P1 still needs exact-source terms review, acquired/licensed public resources, authoritative reference concordance, fuzz/resource audit and device workflow verification.
- P2 still needs licensed release-pinned definitions, broader gene coverage, independent biological concordance and complex-allele/CNV/SV support. The Android screen does not invoke PGx allele matching.
- P3 has a research evidence schema only; no licensed guideline corpus or executable recommendation mapping.
- I2 docking remains host-only and lacks independent redocking/cross-docking and decoy-enrichment validation.
- I3 OpenMM remains CPU host-only; no approved force field or independent biomolecular validation.
- I4 has no selected/acquired ADMET dataset or prediction model and no external calibration/validation.
- No patient data or clinical interpretation is permitted by this work package.

## Verification added

- tests/test_genomics.py verifies aggregate VCF counts, bounds, missing records and that sample names/genotype strings do not appear in the returned report.
- tests/test_android_scientific_viewers.py verifies the consent-gated Android surface, input ceiling, no persistence/export path and explicit PGx/in-silico gates.
- Exact-head CI, embedded Android Python runtime fixture tests, device validation, legal/source-rights review and independent scientific review remain required.

**Decision:** U5 is not closed. The Android genomics QC surface is implemented; PGx and in-silico capabilities remain visibly unavailable until their independent and P0 gates are satisfied.
