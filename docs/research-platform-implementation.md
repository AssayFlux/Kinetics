# Research Platform integrated implementation delivery

**Owner direction (2026-11-08):** implement Research Platform R1–R10 as one integrated delivery; prepare the first local Android build before the later testing campaign. Do not stop at R1 to request permission to begin R2.

## Implemented source layer

- R1: Android arm64/Python/Rust/C++ feasibility probes and local build script remain in place. The Gradle Android NDK version is now pinned to match the local build script. Local APK build and Android runtime results are outstanding.
- R2: Compose research shell, SQLite job/provenance tables, SAF document picker and WorkManager streaming-import/hash worker. The store now has a v1-to-v2 migration and completed imports are encrypted with Android Keystore AES-256-GCM in app-private no-backup storage; provenance and encrypted storage location are committed transactionally. Partial/resumable staging is now stored as independently authenticated AES-GCM chunks; resume verifies the source prefix by decrypting chunks in memory, and torn final records are truncated before retry. A caller-facing decrypted export/analysis pipeline, key-loss recovery and device verification remain incomplete. Full export/recovery, key-loss, process-death, cleanup and device verification remain incomplete.
- R3: initial sequence, protein and enzyme-kinetics primitives. The kinetic fit now rejects non-finite inputs and reports residual mean/dispersion, R-squared and assumption-qualified Gaussian least-squares AIC/BIC; confidence intervals and identifiability analysis remain absent. Regression tests cover input validation and diagnostics, but these are software tests, not independent scientific validation. Reference datasets, unit-aware analysis, external concordance and device benchmarks remain open.
- R4: FASTA/FASTQ, sequence statistics, reverse complement, transcription, k-mers, global pairwise alignment, stricter SAM/VCF text parsing and FASTQ quality summaries. BAM/CRAM and normalization remain open.
- R5: PDB coordinate parsing, geometric contacts and coordinate RMSD with an optional Horn-quaternion rigid-body superposition implementation. mmCIF, secondary structure, SASA, hydrogen bonds and other structural chemistry remain open.
- R6: SDF V2000 parsing with coordinate/bond validation, graph descriptors, bounded exact element/bond-order substructure matching, graph descriptors, and resource-capped exploratory path fingerprints/Tanimoto similarity. Stereochemistry, aromaticity sanitization, protonation/tautomer handling and production RDKit-equivalent behavior remain open.
- R7: Newick parsing with quoted labels and finite branch-length checks, leaf listing, patristic distance and UPGMA clustering with finite distance validation.
- R8: CPM/CLR normalization, finite-input-checked Pearson correlation, log2 fold change, cross-omics correlation, logistic growth and Shannon/Gini-Simpson diversity. Statistically sound differential-expression and multi-omics inference remain open.
- R9: streaming NCBI Gene gene_info importer now preserves the complete 16-column annotation record, including taxonomy, GeneID, symbols, synonyms, cross-references, chromosome, map location, gene type, nomenclature, designations, source and release metadata. The catalogue is expandable and not represented as exhaustive.
- R10: capability registry validation now checks that implementation paths exist inside the repository. Automated CI execution has been changed to manual dispatch to honor the build-first/test-later instruction; release/security/privacy hardening remains incomplete.

The capability registry distinguishes source-implemented from validated. Current entries are implemented with no validation evidence; none is marked validated or device-verified.

## Known unfinished scope

This is an integrated implementation increment, not a claim that every R1–R10 exit criterion is satisfied. Outstanding work includes BAM/CRAM, robust VCF normalization, mmCIF, rigid-body structure superposition, secondary-structure/SASA/H-bond/salt-bridge/disulfide analysis, production-grade chemistry and stereochemistry, full phylogenetic inference/search, statistically sound differential-expression inference, richer omics/multi-omics workflows, catalogue data-pack management and comprehensive gene-domain annotations, and full R10 accessibility/performance/crash/security/release automation. R1 SciPy and production scientific-engine decisions also remain open.

Simple alignment, graph fingerprints, protein pI estimates and kinetic grid fitting are exploratory implementations. They must not be presented as independently validated scientific results. Clinical mode remains disabled; no patient workflow or patient data is included.

## Build-first / test-later policy

- First APK build is local, not in GitHub Actions.
- No Android emulator/device testing is scheduled in GitHub Actions.
- Host checks may run automatically on commits; they are not a substitute for the owner's requested build-first workflow or later device-validation campaign.
- Do not publish an AAB or claim release readiness until R10 and the owner release gate are complete.
