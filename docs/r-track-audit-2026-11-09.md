# R-track audit — 2026-11-09

**Disposition: OPEN — not accepted as complete.** This audit separates implementation, automated regression, independent scientific validation and device/release evidence. Current owner-directed order is D-019: R → S → I → P → G, two steps per track.

## Exact-source baseline

- Commit: `8c4128d5e448db51f2b48fec6c38ce6022fdb053`
- CI: [run #2101](https://github.com/AssayFlux/Kinetics/actions/runs/42554027490), all five jobs successful.
- Python: 233 collected; 229 passed; 4 skipped (3 optional RDKit adapter tests, 1 optional pysam test).
- Separate pinned RDKit sanity and SciPy/Biopython reference-comparison jobs passed.
- Android: arm64 debug APK/AAB build, static package/ELF alignment and JVM unit tests passed. APK SHA-256 `059abb9e3a299b5295b8f08772b976195d7be1cd7db46dce34faa7bcf486d2d9`; AAB SHA-256 `9c8e2ca3a81c4ef2b1fb041aefee99ace5cbfb3292574b815c6a87549210044e`.

## Phase disposition

| Phase | Current implementation/evidence | Remaining exit blockers |
|---|---|---|
| R0 | Owner accepted foundation; registry and CI baseline established | None for the recorded R0 scope |
| R1 | Reproducible ARM64 debug build and static alignment; Python/NumPy/Biopython prototype | Owner Moto G54 device run; actual Python/Rust/C++ invocation; SciPy decision; sequence engine; offline viewer; SAF/background/cancellation; runtime page-size and performance; licence review; owner go/no-go |
| R2 | Encrypted import/provenance, schema-v4 result persistence, bounded imported-FASTA QC worker, digest-bound JSON export, plaintext cleanup regression; JVM/CI green | SQLite fresh/v3→v4 migration tests; WorkManager retry/process-death/re-enqueue; SAF provider failure/partial cleanup; instrumentation/UI; on-device Chaquopy; real device lifecycle |
| R3 | Sequence/protein/kinetics primitives, bootstrap helper, synthetic SciPy comparison job passed | Experimental/reference datasets; reference-calibrated uncertainty; residual diagnostics/AIC/BIC/unit and identifiability validation; external concordance; device performance; alpha owner approval |
| R4 | Sequence/genomics parsers, normalization/reference contracts, FASTA/FASTQ QC and imported FASTA workflow; host regression suite green | Device-scale streaming/Chaquopy; full durable FASTQ workflow with explicit Phred selection; external aligner/variant concordance; BAM/CRAM/large-file limits; no clinical interpretation |
| R5 | PDB/mmCIF subset, geometry/RMSD/SASA/contact code; host structure tests green | Independent reference structures and contact/RMSD/SASA concordance; edge-case/large-structure benchmarks; offline viewer/device evidence |
| R6 | SDF parsers, graph descriptors and optional host RDKit adapter; core tests and pinned descriptor sanity pass | Broad owner-approved corpus; stereochemistry/valence/tautomer concordance; Android engine decision/build; complete transitive licence and footprint review |
| R7 | Newick, UPGMA/NJ, JC69 and seeded site-bootstrap; tests now confirmed executed | Published reference matrices/trees, independent topology/branch concordance, tie/degenerate/large-tree tests and viewer/device evidence |
| R8 | Transformations, Welch tests and exploratory NB2 GLM; tests now confirmed executed | Null calibration, power/FDR/effect-size simulation, independent tool concordance, design robustness, repeated measures/outliers and performance |
| R9 | NCBI Gene catalogue ingestion/search; versioned complete-phased allele-definition and PharmVar TSV parser foundations; tests green | Licensed authoritative data intake, coverage inventory, reference concordance, phase/CNV/hybrid handling, diplotype/phenotype and independent review; P0 remains blocked and clinical mode off |
| R10 | Offline/config guardrails, Keystore/app-private storage foundations, registry, source SBOM and reproducible debug build checks | Runtime migration/crash recovery; independent security review; accessibility; transitive SBOM/licences; privacy/deletion evidence; performance/thermal/device matrix; signed release |

## Acceptance boundaries

- A passing host test is regression evidence, not independent scientific validation.
- A successful APK/AAB build is not an installed-app or physical-device test.
- The four optional-dependency skips remain skipped; separate RDKit sanity does not exercise the entire optional adapter suite, and no pysam run is claimed.
- No patient data, clinical recommendations or Clinical Mode are enabled. P0 remains blocked.
- No phase is marked validated/device-verified without matching evidence in the capability registry and dated records.
- R Step 2 is not accepted until available host-side integration gaps are fixed and remaining unavailable owner-device/external-validation gates are explicitly dispositioned by the owner. Do not start S before that review.
