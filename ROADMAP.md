# Kinetics — Roadmap
**Status:** Proposed baseline; owner approval pending  
**Last updated:** 2026-11-07  
**Statuses:** not-started | in-progress | blocked | done | dropped  
**Owners:** Project owner = repository owner; Engineering = implementation contributor. Dates are review/target dates, not completion claims.

This roadmap operationalises the archived master. A phase is complete only when exit evidence exists in the repository and required owner approval is recorded.

## Current position
- Track R / R0 Foundations: in-progress. Direction documents exist; master archive and R0 phase plan are prepared. Skeleton, registry, checker, reproduce-all, pre-commit and CI remain unimplemented.
- The owner supplied the complete master in conversation; it is reconstructed at docs/origin/KINETICS_MASTER.md as read-only history. No root master file existed to Git-move.
- Direction baseline remains proposed pending explicit owner approval. NORTH_STAR was not changed.
- No scientific implementation, validation, Android feasibility or device verification is claimed.
- Six decisions remain open: license, target jurisdictions, paper framing/venue, clinical advisers, first PGx gene set and target Android devices.

## Track R — Research platform
| ID | Scope | Dependencies | Exit gate | Status | Owner | Date |
|---|---|---|---|---|---|---|
| R0 | Skeleton; direction files; owner-selected license (do not choose); CI lint/type/tests/native builds/16 KB/size budgets; pre-commit; registry/checker; reproduce-all stub | Direction approval | Empty-skeleton CI green; registry checks/tests; honest blocked checks; stop | in-progress | Engineering + owner | Owner review |
| R1 | Real arm64 + emulator: embedded Python/Biopython, Rust app call, C++ JNI, cross-compiled engine, RDKit/alternative, offline Mol* WebView, 16 KB, APK/AAB size, cold start, memory | R0 approved | docs/android-feasibility.md and go/no-go matrix; owner decision | not-started | Engineering | TBD |
| R2 | Compose, SQLite, SAF, provenance, cancellable/resumable WorkManager, registry, pack manager, Keystore encryption | R1 go | On-device import, cancellable job, provenance inspection | not-started | Engineering | TBD |
| R3 | v0.1 alpha: sequence tools, protein properties, enzyme kinetics and independent-reference validation | R2 | Offline real-device install and validation records; v0.1 gate | not-started | Engineering + Validation | TBD |
| R4 | Rust FASTA/FASTQ/SAM/BAM/VCF, QC, trimming, k-mers | R2/Rust feasibility | Reference concordance, bounded memory, device benchmarks | not-started | Engineering + Validation | TBD |
| R5 | PDB/mmCIF, secondary structure, RMSD, contacts, SASA, H-bonds, salt bridges, disulfides | R2/licensed reference set | Fixed PDB benchmark/tolerances | not-started | Engineering + Validation | TBD |
| R6 | Chemistry formats/descriptors/fingerprints/similarity/substructure; PCR/plasmid/cloning/CRISPR rules | R1 chemistry feasibility/license review | Tests, benchmarks and license approvals | not-started | Engineering + Validation | TBD |
| R7 | Search, phylogenetics, evolution; Tier B local/Tier C node; viewers/conservation/logos | R2/engine and license approvals | Reference concordance, offline viewer and node security tests | not-started | Engineering + Validation | TBD |
| R8 | Omics, microbiology, systems, multi-omics and statistics | R2/datasets/R reference CI | Reproducible reference comparisons | not-started | Engineering + Validation | TBD |
| R9 | Domain rollout in waves of 10–20; preserve supplied definitions; coverage reports | Registry and capabilities | Implemented only when a tool works and is tested | not-started | Engineering | TBD |
| R10 | Accessibility, low-end performance, crash testing, privacy/data safety, signed AAB, honest listing, GitHub APK, optional F-Droid | R3/G1–G4 | Publishing checklist and owner release approval | not-started | Engineering + owner | TBD |

v0.1.0 = R0–R3.

## Track S — Structure excellence
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
| P2 | PGx star-allele/diplotype/phenotype for owner-approved small gene set | P1, caller/license review | Reference and established-tool concordance; indeterminate never guessed | not-started | Engineering + advisers | TBD |
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

## Mandatory gates
Direction baseline; R0 exit; R1 go/no-go; owner-selected LICENSE; P0; GPL/AGPL bundling; new language; engine-tier change; restrictive license; target jurisdiction; real patient data/human participants; paper framing/venue/authorship; NORTH_STAR change; Clinical Mode. Stop at each gate.

## Session protocol
At start read NORTH_STAR, ROADMAP, DECISIONS and latest SESSION_LOG; state phase/objective in two lines. Map every task to roadmap; drift-check before tasks/commits. At end update statuses, record decisions, append session log and report evidence/gaps/risks. Never claim unverified work.
