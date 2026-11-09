# R-track audit — 2026-11-09

**Disposition: ENGINEERING AUDIT CLOSED; R ACCEPTANCE EVIDENCE REMAINS OPEN.** The implementation and host-side regression review for R0–R10 has been completed to the extent supported by repository code and CI. This is not a claim that every R phase is scientifically validated, device-verified, licensed for redistribution or release-ready. Per D-019 the next engineering track is S; unresolved R evidence is retained as carry-forward work and cannot be represented as passed.

## Exact-source baseline

- Repository: [AssayFlux/Kinetics](https://github.com/AssayFlux/Kinetics)
- Commit: `888e49bc7108a2609db97d76193a60d5eec175e0`
- CI: [run #2126 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42560038764); all five jobs completed successfully.
- Python: 242 collected; **238 passed, 4 skipped**.
- Pinned scientific-reference comparisons, pinned RDKit descriptor sanity fixtures, and direct declared-source SPDX inventory passed.
- Android arm64 debug APK/AAB build, APK/package alignment and Android JVM unit-test task passed. The Android log reports `BUILD SUCCESSFUL` and `:app:testDebugUnitTest` successful.
- APK: 69,891,771 bytes; SHA-256 `73e66bacb3d1e45e8928c52c10b3fed14e29aa71c8e09a8df73945ffef24aa06`.
- AAB: 39,953,771 bytes; SHA-256 `a851cdeaf921e8b8b40dd82184fb2ef8200bc7b660ab32c80da448cd22d5aadf`.
- Uploaded Android artifact ZIP: [artifact 13649560656](https://github.com/AssayFlux/Kinetics/actions/runs/42560038764/artifacts/13649560656), 80,049,058 bytes; ZIP SHA-256 `3c4b135979a4b1920a7afae3fc500c2aa7ebb35a3ef0af357fa867de9be60488`. ZIP digest is not the APK/AAB digest.
- Python/registry job confirms 238 passed and 4 skipped. Skips remain explicit; separate RDKit sanity does not mean all optional adapter tests ran.

## Phase disposition

| Phase | Implementation and automated evidence | Carry-forward acceptance evidence |
|---|---|---|
| R0 | Owner-accepted foundation; registry/checker, reproduction stub, CI and governance baseline. R0 acceptance remains valid for its recorded scope. | None for the defined R0 foundation scope. |
| R1 | Reproducible arm64 debug APK/AAB CI build; JVM suite; static package/ELF alignment; host scientific-stack probes. | Owner Moto G54 physical-device run; actual embedded Python, Rust FFI and C++ JNI invocation; SciPy Android packaging decision; approved sequence/chemistry engines and offline viewer; SAF/background/cancellation runtime; performance/page-size evidence; full dependency license review. |
| R2 | Encrypted SAF import foundations, SQLite schema v4, fresh/v1/v2/v3 migration fixtures, authenticated chunk storage, FASTA analysis worker, digest-bound result/export checks, private plaintext cleanup tests, report-only encrypted orphan scan. Worker now closes SQLite helper in `finally`; staging setup and preflight cleanup are guarded. Exact-source #2126 Android build/JVM tests passed. | WorkManager process-death/retry/re-enqueue/resume and cancellation integration; SAF provider permission revocation/partial-write behavior; instrumentation/UI tests; real Chaquopy and Keystore behavior on device; end-to-end import/run/export and recovery on owner device. |
| R3 | Sequence/protein/kinetics primitives and deterministic synthetic SciPy reference comparison. | Independent experimental/reference datasets; uncertainty calibration; residual, AIC/BIC, units and identifiability validation; external concordance; device performance and owner alpha gate. |
| R4 | FASTA/FASTQ and selected SAM/VCF/BAM parsing/QC/normalization foundations; imported FASTA Android workflow; host regressions. | Durable FASTQ workflow with explicit Phred policy; external aligner/variant concordance; CRAM and large-file limits; device-scale streaming/Chaquopy and benchmarks. |
| R5 | PDB/mmCIF subset, contacts and superposed RMSD; synthetic Biopython/NumPy comparison fixtures passed. | Independent structures and contact/RMSD/SASA concordance; full mmCIF semantics, edge cases, large structures, viewer/device validation. |
| R6 | SDF V2000/V3000 subset, graph descriptors and bounded matching/fingerprint primitives; pinned RDKit descriptor sanity fixtures passed. | Approved reference corpus; stereochemistry, valence, aromaticity and tautomer concordance; production engine decision/build; transitive license and footprint review. |
| R7 | Newick, UPGMA/NJ, JC69 and seeded site bootstrap; synthetic Biopython NJ patristic-distance comparison passed. | Published reference matrices/trees, independent biological topology/branch concordance, degenerate/large-tree cases, viewer/device evidence. |
| R8 | CPM/CLR, correlation, Welch and exploratory NB2 GLM; synthetic SciPy NB2 MLE concordance passed. | Null calibration, power/FDR/effect-size simulation, independent tool concordance, repeated-measure/outlier robustness and performance. |
| R9 | NCBI Gene exact-16-column parser and real-calendar-date validation; PharmVar TSV parser hardening; conservative versioned complete/phased allele-definition infrastructure. | Licensed authoritative PGx content, comprehensive coverage inventory, reference build/coordinate normalization, phase/CNV/hybrid handling, diplotype/phenotype translation and independent review. No clinical interpretation. |
| R10 | Offline/config guardrails, Keystore/app-private storage foundations, registry integrity, reproducible CI, direct declared-dependency SPDX inventory and security/release documentation. | Full transitive SBOM/license resolution, independent security/privacy review, accessibility audit, crash/device/performance evidence, deletion lifecycle verification and signed release. |

## Audit closure and sequencing decision

- The R implementation/host regression audit step is closed against exact-source commit `888e49b` and CI #2126.
- R0 remains accepted. R1–R10 remain **implemented to varying degrees**, not uniformly complete or scientifically validated.
- The owner has directed the project to proceed to S after this audit and documentation consolidation. This authorizes the next engineering track; it does not waive, erase or relabel the R carry-forward acceptance evidence above.
- Track S work must not claim downstream R dependencies are validated until the relevant evidence is supplied.
- No patient data, clinical recommendations or Clinical Mode are enabled. P0 remains blocked.
- No physical-device runtime, independent experimental validation, complete transitive license audit or signed production release is claimed.

## Required carry-forward controls

Keep these items visible in the master roadmap and revisit them when their dependencies are needed:
1. Owner-device installation and runtime test on the named Moto G54 5G; capture Android/API, SoC, RAM, ABI, page size, logs and reproducible steps.
2. WorkManager/SAF/Keystore end-to-end lifecycle and recovery instrumentation.
3. Independent biological/experimental reference datasets and prespecified tolerances for R3–R9.
4. Licensed PGx source intake and qualified review; P0 remains blocked.
5. Transitive SBOM/license/security/accessibility/performance review and signed release evidence.

