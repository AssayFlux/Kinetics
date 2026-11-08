# Kinetics — Roadmap
**Status:** Owner-approved baseline; R0 done; integrated R1–R10 implementation in progress; build-first / test-later owner direction recorded  
**Last updated:** 2026-11-08  
**Statuses:** not-started | in-progress | blocked | done | dropped  
**Owners:** Project owner = repository owner; Engineering = implementation contributor. Dates are review/target dates, not completion claims.

This roadmap operationalises the archived master. A phase is complete only when exit evidence exists in the repository and required owner approval is recorded.

## Current position
- Track R / R0 Foundations: owner accepted the R0 exit and authorised R1 on 2026-11-07; R0 is done.
- The owner-approved direction baseline and reconstructed historical master are present; NORTH_STAR was not changed.
- Repository skeleton, capability registry/checker/tests, reproduction stub, pre-commit configuration, CI and governance metadata are committed.
- R0 accepted by the owner when they authorised R1 on 2026-11-07. CI evidence: [R0 workflow run](https://github.com/AssayFlux/Kinetics/actions/runs/42378815901).
- On 2026-11-08 the owner directed one integrated R1–R10 implementation delivery, with the first local Android build before the later testing campaign. Engineering must not stop at R1 to request permission to begin downstream implementation. Implementation may proceed across the R track, while scientific, licensing, device, privacy and release gates remain in force. GitHub Actions must not build APK/AAB or run Android emulator/device tests. D-006 remains a target, not a verified support claim.
- D-005 is approved as a broad strategic direction: build both a comprehensive, expandable PGx gene panel and a broad cross-domain gene catalogue. Treat PGx as a specialised workstream within the wider catalogue, with separate evidence and validation gates. The earlier six-gene list is not a scope limit; exact inventories and rollout waves remain evidence-led. No exhaustive coverage or PGx implementation is claimed. D-004 is approved: defer clinical-adviser recruitment until the research platform is more mature (target review after R3); P0 and all patient/clinical work remain blocked until qualified advisers and all other prerequisites are in place. D-003 (publication strategy) is approved: multiple papers over time, beginning with an evidence-backed platform/software-methods paper after R1–R3 readiness, followed by independently validated domain papers. D-001 (project license) is approved as Apache-2.0; D-002 sets a global long-term ambition including future clinical use, subject to jurisdiction-by-jurisdiction advice and approvals. The canonical Apache-2.0 LICENSE grant file is present at the repository root; the third-party dependency audit remains open.

## Track R — Research platform
| ID | Scope | Dependencies | Exit gate | Status | Owner | Date |
|---|---|---|---|---|---|---|
| R0 | Skeleton; direction files; owner-selected license (do not choose); CI lint/type/tests/native builds/16 KB/size budgets; pre-commit; registry/checker; reproduce-all stub | Direction approval | Empty-skeleton CI green; registry checks/tests; honest blocked checks; stop | done | Engineering + owner | 2026-11-07 |
| R1 | Android arm64 feasibility: embedded Python/Biopython/NumPy/SciPy, Rust FFI, C++ JNI, real scientific engine, RDKit/alternative, offline viewer, 16 KB, local APK/AAB build, SAF/lifecycle, cold start and memory | R0 approved | Local build evidence, complete feasibility matrix and explicit owner go/no-go; GitHub Actions does not build/test APKs | in-progress | Engineering + owner | Started 2026-11-07 |
| R2 | Compose, SQLite, SAF, provenance, cancellable/resumable WorkManager, registry, pack manager, Keystore encryption | Integrated R1 architecture findings; validation remains gated | On-device import, cancellable/resumable job, provenance inspection, security review | in-progress — Compose/SQLite/SAF/WorkManager import; resumable chunks use AES-GCM with job/index AAD, transactional provenance, hash-verified private-cache materialization and SAF export; startup detects definite Keystore alias loss and marks completed encrypted records and retained encrypted partial imports recovery_required without replacing the key or deleting ciphertext; interrupted-export cleanup, orphan reconciliation, migration fixtures and Android verification remain open | Engineering | 2026-11-08 |
| R3 | v0.1 alpha: sequence tools, protein properties, enzyme kinetics and independent-reference validation | R2 integration; scientific validation remains gated | Offline end-to-end alpha, independent validation records and owner-approved v0.1 gate | in-progress — sequence/protein/kinetics primitives, finite-input guards, residual diagnostics, AIC/BIC and exploratory linearized transforms; reference validation, uncertainty and app integration open | Engineering + Validation | 2026-11-08 |
| R4 | Rust FASTA/FASTQ/SAM/BAM/VCF, QC, trimming, k-mers | R2/Rust feasibility | Reference concordance, bounded memory, device benchmarks | in-progress — wrapped FASTQ, terminal quality trimming, strict SAM/VCF text parsing, QC, sequence statistics and alignment; BAM/CRAM, adapter trimming, Rust acceleration and concordance open | Engineering + Validation | 2026-11-08 |
| R5 | PDB/mmCIF, secondary structure, RMSD, contacts, SASA, H-bonds, salt bridges, disulfides | R2/licensed reference set | Fixed PDB benchmark/tolerances | in-progress — PDB/mmCIF atom-site parsing, contacts, superposed RMSD, approximate SASA and distance-only interaction-candidate screening; secondary structure, full mmCIF semantics and reference validation open | Engineering + Validation | 2026-11-08 |
| R6 | Chemistry formats/descriptors/fingerprints/similarity/substructure; PCR/plasmid/cloning/CRISPR rules | R1 chemistry feasibility/license review | Tests, benchmarks and license approvals | in-progress — multi-record SDF V2000 parsing, graph descriptors, bounded substructure matching and exploratory fingerprints; stereochemistry, aromaticity and production engine open | Engineering + Validation | 2026-11-08 |
| R7 | Search, phylogenetics, evolution; Tier B local/Tier C node; viewers/conservation/logos | R2/engine and license approvals | Reference concordance, offline viewer and node security tests | in-progress — quoted-label Newick, UPGMA/NJ, Jukes–Cantor distances and seeded site-bootstrap split support; ML/Bayesian inference, search, viewers and node security open | Engineering + Validation | 2026-11-08 |
| R8 | Omics, microbiology, systems, multi-omics and statistics | R2/datasets/R reference CI | Reproducible reference comparisons | in-progress — finite-input-checked CPM/CLR, Pearson/cross-omics correlation, fold change, logistic growth, Shannon/Gini-Simpson diversity and exploratory Welch/BH differential expression; count-model inference and broader multi-omics open | Engineering + Validation | 2026-11-08 |
| R9 | Domain rollout in waves of 10–20; preserve supplied definitions; coverage reports | Registry and capabilities | Implemented only when a tool works and is tested | in-progress — full 16-column NCBI Gene annotation ingestion/search from plain/gzip streams; comprehensive PGx allele definitions, domain data packs and coverage reports open | Engineering | 2026-11-08 |
| R10 | Accessibility, low-end performance, crash testing, privacy/data safety, signed AAB, honest listing, owner-approved distribution channels (GitHub release assets and/or F-Droid only after channel review) | R3/G1–G4 | Publishing checklist and owner release approval; GitHub Actions must not build APK/AAB | in-progress — capability implementation-path integrity checks, manual-only CI dispatch under test-later policy, and accessibility/security/release gates retained; full hardening remains open | Engineering + owner | 2026-11-08 |

v0.1.0 = R0–R3.

## Track S — Structure excellence

**Sequencing gate (owner direction, 2026-11-08):** Track S must not begin until every R1–R10 exit criterion is evidenced, the Research Platform integration is coherent, and the owner accepts the Track R completion gate. Existing R5 structural-analysis code remains part of Track R and may be completed there; it does not authorize starting Track S early.

| ID | Scope | Dependencies | Exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| S1 | Offline Mol*/3Dmol.js, structure loading/preparation log | R1 WebView, R2, license review | Offline tests and preparation provenance | not-started | Engineering | TBD |
| S2 | Quality badges/metrics | S1, fixed PDB set | Benchmark concordance/tolerances | not-started | Engineering + Validation | TBD |
| S3 | Variant mapping, interface and pocket analysis | S2, variant evidence | Capability validation; evidence not verdict | not-started | Engineering + Validation | TBD |
| S4 | Node prediction with approved models/confidence and experimental comparison | Node security, code/weights licenses | Reproducible benchmark and limitations | not-started | Engineering + Validation | TBD |
| S5 | Rendering/export and structure benchmark | S1–S4 as applicable | Benchmark-generated figures | not-started | Engineering + Validation | TBD |

## Track I — In-silico lab
| ID | Scope | Dependencies | Exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| I1 | Ligand prep, descriptors, drug-likeness | R1 chemistry/license | Correctness, limits, provenance | not-started | Engineering + Validation | TBD |
| I2 | Node docking/virtual screening | Node, approved licenses | Redocking RMSD and decoy enrichment | not-started | Engineering + Validation | TBD |
| I3 | Node MD | Node, engine/model/license | Stability, energy conservation, reference runs | not-started | Engineering + Validation | TBD |
| I4 | ADMET and PK/PD/PBPK | Approved data/models | Held-out performance and applicability domain | not-started | Engineering + Validation | TBD |
| I5 | Variant-effect and virtual-cohort simulations, Research Mode | I4, fairness/model review | Benchmarks, ancestry portability, prediction labels | not-started | Engineering + Validation | TBD |

## Track P — Precision medicine (PGx first)
Hard gate: no patient-related feature before P0; early research uses public test data only.
| ID | Scope | Dependencies | Exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| P0 | Intended use; legal/ethics/regulatory advice; advisers identified; QMS approach | G1–G3 planning | Written gate packet and owner approval; no patient feature before pass | blocked | Owner + qualified advisers | TBD |
| P1 | Genotype ingest/QC/annotation/build handling, Research Mode, public data | P0, R4, reference/license review | Pinned builds, thresholds and concordance | not-started | Engineering + Validation | TBD |
| P2 | PGx star-allele/diplotype/phenotype across a comprehensive, expandable, adviser-reviewed and owner-approved panel; inventory and implementation staged by evidence | P1, caller/license review | Reference and established-tool concordance; indeterminate never guessed | not-started | Engineering + advisers | TBD |
| P3 | Guideline mapping/report, Research Mode | P2, guideline license review | Versioned mapping tests and wording review | not-started | Engineering + advisers | TBD |
| P4 | Variant evidence assistant with human curator | P1, evidence-source license review | Curator workflow; no autonomous final classification | not-started | Engineering + curators | TBD |
| P5 | Advisory review and clinician usability testing | P3–P4, ethics review/exemption | Documented review/study evidence | not-started | Owner + advisers | TBD |
| P6 | Clinical Mode flag, audit/RBAC/signoff and internal validation | P0–P5, legal/regulatory clearance | Evidence package and owner approval; public flag off | not-started | Engineering + advisers | TBD |
| P7 | Regulatory planning and prospective evaluation | P6, advice/ethics approvals | Documented plans, approvals and evidence | not-started | Owner + advisers | TBD |
Further disease areas only after P7 evidence, one at a time.

## Track G — Governance
| ID | Scope | Dependencies | Exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| G1 | Local-first privacy/security, encryption, consent, deletion, sensitive-log prevention, node threat model | R0 | Reviewed design/testable requirements before sensitive workflows | not-started | Engineering + owner | TBD |
| G2 | License register for dependencies/engines/models/databases; flag restrictive terms | R0, before bundling | docs/third-party.md backed by upstream license text and approvals | not-started | Engineering + owner | TBD |
| G3 | QMS/software lifecycle documentation from P0 | P0 planning | Requirements, risk, verification, change and traceability controls | not-started | Owner + advisers | TBD |
| G4 | Bias and ancestry coverage | Relevant P/I capabilities and datasets | Coverage/limitations in reports and outputs | not-started | Validation + advisers | TBD |
| G5 | Paper evidence pipeline | R/S/I/P evidence | Manuscript tables/figures generated from validation/benchmarks | not-started | Research + Validation | TBD |

## Gene strategy (D-005 — approved strategic direction)
- Build both a comprehensive, expandable PGx gene panel and a broad cross-domain gene catalogue spanning genomics and relevant Kinetics domains.
- The cross-domain catalogue is the wider inventory; PGx is a specialised workstream within it. Maintain separate domain annotations, reference datasets, caller/assay requirements, interpretation rules and validation status.
- The earlier six-gene list is not a scope limit. Do not invent a target count or claim exhaustive coverage; define versioned inventories and prioritised implementation waves from scientific relevance, evidence, reference availability, locus/caller feasibility, ancestry coverage, licensing, compute/device constraints and independent validation.
- A gene's presence in the catalogue does not imply that a caller, assay, interpretation or clinical workflow is implemented or validated.
- PGx remains research-only and gated by qualified advisers, P0, jurisdiction-specific legal/ethics/regulatory requirements and owner approval. No patient-data or clinical work is authorized.

## Clinical adviser timing (D-004)
- Defer clinical-adviser recruitment during the current R1 engineering-feasibility phase.
- Revisit after the research platform reaches a meaningful maturity milestone, with a target review after R3.
- Recruit/engage qualified clinical expertise before P0, PGx gene-set selection or any patient-related, clinical-study or clinical-scope work. P0 remains blocked until its full gate packet and owner approval are complete.
- This is a timing decision only; it does not relax safety, legal, ethics, regulatory, QMS or evidence requirements.

## Publication strategy (D-003)
- Plan multiple papers over time, not one broad paper claiming every planned domain.
- First candidate: platform/software-methods paper after R1–R3 evidence is complete enough to support reproducible methods, validation and benchmark claims.
- Later domain papers require domain-specific independent validation and reference comparisons.
- Venue fit/requirements, authorship, affiliations, funding, competing interests and all claims require owner review at the relevant milestone. No publication or acceptance is implied.

## Mandatory gates
Direction baseline; R0 exit (accepted 2026-11-07); R1 go/no-go; P0; GPL/AGPL bundling; new language; engine-tier change; restrictive license; jurisdiction-specific legal/regulatory/ethics review; real patient data/human participants; paper venue/authorship and evidence-backed claims; NORTH_STAR change; Clinical Mode. Stop at each gate.

## Session protocol
At start read NORTH_STAR, ROADMAP, DECISIONS and latest SESSION_LOG; state phase/objective in two lines. Map every task to roadmap; drift-check before tasks/commits. At end update statuses, record decisions, append session log and report evidence/gaps/risks. Never claim unverified work.


## Owner authorization D-008 — R1 through R3
- On 2026-11-07, the owner explicitly approved proceeding with R1, R2 and R3.
- Execute them in sequence. This authorization does not mark any phase complete and does not waive technical, scientific, licensing, device, security, privacy, clinical or owner exit gates.
- R1 is still in progress. R2 starts after R1 evidence is complete and its go/no-go is documented; R3 starts after R2's exit evidence and approval.


## Owner authorization — integrated R1–R10 implementation (2026-11-08)
- The owner explicitly directed Engineering to implement Research Platform R1 through R10 as one integrated delivery, rather than stopping after R1 to request permission to begin R2/R3.
- Build-first / test-later: prepare the first APK build locally before the later testing campaign. Do not add APK/AAB builds or Android emulator/device tests to GitHub Actions.
- This changes implementation sequencing only. It does not authorize false validation claims, bypass third-party license review, enable clinical/patient workflows, or waive scientific/device/security/release exit criteria.
- See docs/research-platform-implementation.md for the current implementation inventory and unfinished scope.
