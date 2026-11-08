# Research Platform integrated implementation delivery

**Owner direction (2026-11-08):** implement Research Platform R1–R10 as one integrated delivery; prepare the first local Android build before the later testing campaign. Do not stop at R1 to request permission to begin R2.

## Implemented source layer

- R1: Android arm64/Python/Rust/C++ feasibility probes and local build script remain in place. Local APK build and Android runtime results are outstanding.
- R2: Compose research shell, SQLite job/provenance tables, SAF document picker and WorkManager streaming-import/hash worker. Import records file provenance only; it is not a scientific pipeline.
- R3: initial sequence, protein and enzyme-kinetics primitives.
- R4: FASTA/FASTQ, sequence statistics, reverse complement, transcription, k-mers, global pairwise alignment, SAM/VCF text parsing and FASTQ quality summaries.
- R5: PDB coordinate parsing, geometric contacts and coordinate RMSD without superposition.
- R6: SDF V2000 parsing, formula/molecular weight and exploratory graph fingerprints/Tanimoto similarity.
- R7: Newick parsing, leaf listing, patristic distance and UPGMA clustering.
- R8: CPM/CLR normalization, Pearson correlation, log2 fold change, cross-omics correlation, logistic growth and Shannon/Simpson diversity.
- R9: streaming NCBI Gene gene_info importer preserving taxonomy, GeneID, symbols, synonyms, source and release metadata. The catalogue is expandable and not represented as exhaustive.
- R10: release/security/privacy principles and release gates remain documented; operational hardening remains required.

The capability registry distinguishes source-implemented from validated. Current entries are implemented with no validation evidence; none is marked validated or device-verified.

## Known unfinished scope

This is an integrated implementation increment, not a claim that every R1–R10 exit criterion is satisfied. Outstanding work includes BAM/CRAM, robust VCF normalization, mmCIF, rigid-body structure superposition, secondary-structure/SASA/H-bond/salt-bridge/disulfide analysis, production-grade chemistry and stereochemistry, full phylogenetic inference/search, statistically sound differential-expression inference, richer omics/multi-omics workflows, catalogue data-pack management and comprehensive gene-domain annotations, and full R10 accessibility/performance/crash/security/release automation. R1 SciPy and production scientific-engine decisions also remain open.

Simple alignment, graph fingerprints, protein pI estimates and kinetic grid fitting are exploratory implementations. They must not be presented as independently validated scientific results. Clinical mode remains disabled; no patient workflow or patient data is included.

## Build-first / test-later policy

- First APK build is local, not in GitHub Actions.
- No Android emulator/device testing is scheduled in GitHub Actions.
- Host checks may run automatically on commits; they are not a substitute for the owner's requested build-first workflow or later device-validation campaign.
- Do not publish an AAB or claim release readiness until R10 and the owner release gate are complete.
