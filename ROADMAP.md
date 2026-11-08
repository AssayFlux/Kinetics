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
- On 2026-11-08 the owner directed one integrated R1–R10 implementation delivery, with the first local Android build before the later testing campaign. Engineering must not stop at R1 to request permission to begin downstream implementation. Implementation may proceed across the R track, while scientific, licensing, device, privacy and release gates remain in force. The owner subsequently authorized GitHub Actions to build unsigned arm64 debug APK/AAB artifacts, run automated checks and Android JVM unit tests; emulator and physical-device tests remain separate. D-006 remains a target, not a verified support claim.
- D-005 is approved as a broad strategic direction: build both a comprehensive, expandable PGx gene panel and a broad cross-domain gene catalogue. Treat PGx as a specialised workstream within the wider catalogue, with separate evidence and validation gates. The earlier six-gene list is not a scope limit; exact inventories and rollout waves remain evidence-led. No exhaustive coverage or PGx implementation is claimed. D-004 is approved: defer clinical-adviser recruitment until the research platform is more mature (target review after R3); P0 and all patient/clinical work remain blocked until qualified advisers and all other prerequisites are in place. D-003 (publication strategy) is approved: multiple papers over time, beginning with an evidence-backed platform/software-methods paper after R1–R3 readiness, followed by independently validated domain papers. D-001 (project license) is approved as Apache-2.0; D-002 sets a global long-term ambition including future clinical use, subject to jurisdiction-by-jurisdiction advice and approvals. The canonical Apache-2.0 LICENSE grant file is present at the repository root; the third-party dependency audit remains open.

## Track R — Research platform
| ID | Scope | Dependencies | Exit gate | Status | Owner | Date |
|---|---|---|---|---|---|---|
| R0 | Skeleton; direction files; owner-selected license (do not choose); CI lint/type/tests/native builds/16 KB/size budgets; pre-commit; registry/checker; reproduce-all stub | Direction approval | Empty-skeleton CI green; registry checks/tests; honest blocked checks; stop | done | Engineering + owner | 2026-11-07 |
| R1 | Android arm64 feasibility: embedded Python/Biopython/NumPy/SciPy, Rust FFI, C++ JNI, real scientific engine, RDKit/alternative, offline viewer, 16 KB, local APK/AAB build, SAF/lifecycle, cold start and memory | R0 approved | Reproducible arm64 APK/AAB build evidence, complete feasibility matrix and explicit owner go/no-go; CI build is not device-runtime evidence | in-progress — reproducible arm64 debug APK (67,678,526 bytes) and AAB (38,860,218 bytes) built successfully in CI run #1904 on commit `30d19ea`; Android JVM unit tests, artifact size checks, APK ZIP alignment and native ELF alignment checks passed. This is build/package evidence only; transitive/file-level license audit, engine go/no-go decisions, cold-start/memory probes and physical-device runtime remain open | Engineering + owner | 2026-11-08 |
| R2 | Compose, SQLite, SAF, provenance, cancellable/resumable WorkManager, registry, pack manager, Keystore encryption | Integrated R1 architecture findings; validation remains gated | On-device import, cancellable/resumable job, provenance inspection, security review | in-progress — Compose/SQLite/SAF/WorkManager import; resumable AES-GCM chunks, transactional provenance, verified cache/export and Keystore-loss preservation; cancellation persists a resumable terminal state; new report-only encrypted orphan inventory scans unreferenced finalized/partial ciphertext without deleting it, with JVM tests for active, missing-job, stale-partial and symlink cases; interrupted-export provider behavior, migration fixtures and device verification remain open | Engineering | 2026-11-08 |
| R3 | v0.1 alpha: sequence tools, protein properties, enzyme kinetics and independent-reference validation | R2 integration; scientific validation remains gated | Offline end-to-end alpha, independent validation records and owner-approved v0.1 gate | in-progress — sequence/protein/kinetics primitives and diagnostics; pinned host-only SciPy comparison now runs on deterministic synthetic cases in CI; experimental reference validation, calibrated uncertainty and app integration remain open | Engineering + Validation | 2026-11-08 |
| R4 | Rust FASTA/FASTQ/SAM/BAM/VCF, QC, trimming, k-mers | R2/Rust feasibility | Reference concordance, bounded memory, device benchmarks | in-progress — wrapped FASTQ, terminal quality trimming, strict SAM/VCF text parsing, QC, sequence statistics and alignment; BAM/CRAM, adapter trimming, Rust acceleration and concordance open | Engineering + Validation | 2026-11-08 |
| R5 | PDB/mmCIF, secondary structure, RMSD, contacts, SASA, H-bonds, salt bridges, disulfides | R2/licensed reference set | Fixed PDB benchmark/tolerances | in-progress — PDB/mmCIF atom-site parsing, contacts, superposed RMSD, approximate SASA and distance-only interaction-candidate screening; secondary structure, full mmCIF semantics and reference validation open | Engineering + Validation | 2026-11-08 |
| R6 | Chemistry formats/descriptors/fingerprints/similarity/substructure; PCR/plasmid/cloning/CRISPR rules | R1 chemistry feasibility/license review | Tests, benchmarks and license approvals | in-progress — multi-record SDF V2000 parsing, graph descriptors, bounded substructure matching and exploratory fingerprints; stereochemistry, aromaticity and production engine open | Engineering + Validation | 2026-11-08 |
| R7 | Search, phylogenetics, evolution; Tier B local/Tier C node; viewers/conservation/logos | R2/engine and license approvals | Reference concordance, offline viewer and node security tests | in-progress — quoted-label Newick, UPGMA/NJ, Jukes–Cantor distances and seeded site-bootstrap split support; ML/Bayesian inference, search, viewers and node security open | Engineering + Validation | 2026-11-08 |
| R8 | Omics, microbiology, systems, multi-omics and statistics | R2/datasets/R reference CI | Reproducible reference comparisons | in-progress — finite-input-checked CPM/CLR, Pearson/cross-omics correlation, fold change, logistic growth, Shannon/Gini-Simpson diversity and exploratory Welch/BH differential expression; count-model inference and broader multi-omics open | Engineering + Validation | 2026-11-08 |
| R9 | Domain rollout in waves of 10–20; preserve supplied definitions; coverage reports | Registry and capabilities | Implemented only when a tool works and is tested | in-progress — full 16-column NCBI Gene annotation ingestion/search from plain/gzip streams; comprehensive PGx allele definitions, domain data packs and coverage reports open | Engineering | 2026-11-08 |
| R10 | Accessibility, low-end performance, crash testing, privacy/data safety, signed AAB, honest listing, owner-approved distribution channels (GitHub release assets and/or F-Droid only after channel review) | R3/G1–G4 | Publishing checklist, automated hardening, signed release evidence and owner release approval | in-progress — capability implementation-path integrity checks, authorized CI APK/AAB build lane plus accessibility/security/release gates, and accessibility/security/release gates retained; full hardening remains open | Engineering + owner | 2026-11-08 |

v0.1.0 = R0–R3.

## Track S — Structure excellence, protein intelligence and discovery

**Sequencing gate (updated by explicit owner instruction, 2026-11-08):** The owner has now explicitly authorized S-track implementation to begin in parallel with completion of R1–R10. This supersedes the earlier sequencing-only prohibition on starting S. Work may proceed only on independently safe S1 preparation that does not assume R1 WebView feasibility or unapproved third-party assets. Full offline rendering remains blocked on R1 WebView/runtime evidence and exact viewer/dependency license approval. S2–S5 retain their scientific, security, model-license and benchmark dependencies. This sequencing change does not mark any R phase complete, waive exit evidence, or authorize patient/clinical use.

| ID | Scope | Dependencies | Exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| S1 | Offline Mol*/3Dmol.js, structure loading/preparation log | R1 WebView, R2, license review | Offline tests and preparation provenance | in-progress — deterministic bounded coordinate payload + schema + tests committed; renderer, offline bundle, bridge and license review open | Engineering | 2026-11-08 |
| S2 | Quality badges/metrics | S1, fixed PDB set | Benchmark concordance/tolerances | not-started | Engineering + Validation | TBD |
| S3 | Variant mapping, interface and pocket analysis | S2, variant evidence | Capability validation; evidence not verdict | not-started | Engineering + Validation | TBD |
| S4 | Node prediction with approved models/confidence and experimental comparison | Node security, code/weights licenses | Reproducible benchmark and limitations | not-started | Engineering + Validation | TBD |
| S5 | Rendering/export and structure benchmark | S1–S4 as applicable | Benchmark-generated figures | not-started | Engineering + Validation | TBD |
| S6 | Unknown-sequence triage, protein family/domain/motif search and evidence-ranked annotation | R4; versioned local reference packs | Curated positive/negative fixtures, reference concordance, calibrated thresholds, resource bounds | in-progress — JSON evidence contract, exact full-length triage and verified local FASTA pack ingestion/search with byte-level SHA-256, strict manifest, alphabet/duplicate checks and resource caps; no similarity/homology or novelty inference; evidence_level remains none | Engineering + Validation | 2026-11-08 |
| S7 | Prokaryotic and eukaryotic genome annotation pipelines, gene discovery and provenance | R4; S6; organism-specific references | Curated genome truth sets, coordinate/strand concordance, transcript and annotation review | in-progress — bounded six-frame complete ORF candidate enumeration now uses explicit table-specific start/stop codons and maps reverse-strand coordinates; no full prokaryotic/eukaryotic gene prediction, splice model or annotation claim | Engineering + Validation | 2026-11-08 |
| S8 | Non-standard genetic-code investigation and translation-table candidate inference | S6–S7; organism-specific truth sets | Independent reference validation, confusion matrices, calibrated abstention and ambiguous-case tests | in-progress — explicit translation for NCBI tables 1, 2, 4, 5 and 11; pinned Biopython host comparison exhaustively checks all 64 codons and start/stop sets; this validates table transcription only, not genetic-code inference or organism identification | Engineering + Validation | 2026-11-08 |
| S9 | Protein sequence/domain/family intelligence and sequence-to-structure mapping | S1, S6, R5; licensed reference sets | Independent annotation comparisons, residue-mapping tests and model-vs-experiment provenance | planned | Engineering + Validation | TBD |
| S10 | Constrained de novo protein design research, candidate ranking and experimental validation workflow | Model/data license approval, secure compute/node, biosafety review, S6/S9 | Reproducible generation, held-out benchmarks, prospective wet-lab validation and owner approval | planned — model/license/compute/biosafety feasibility only until gates pass | Engineering + Validation + Owner | TBD |

## Parallel execution and publication evidence

The owner authorized R, S, I and P work to proceed simultaneously on 2026-11-08, subject to each phase dependency and hard gate. The execution protocol and paper-readiness requirements are recorded in [docs/parallel-track-execution.md](docs/parallel-track-execution.md). Manuscript preparation and claim/evidence ledger are in `paper/`; validation result contract is in `validation/RESULT-MANIFEST.md`. Paper 1 remains a candidate only after R1–R3 exit evidence and independent validation. P0 remains blocked; P-track work is restricted to non-patient public-data preparation until the formal gate passes.

## Track I — In-silico lab
| ID | Scope | Dependencies | Exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| I1 | Ligand prep, descriptors, drug-likeness | R1 chemistry/license | Correctness, limits, provenance | in-progress — optional RDKit adapter now has a pinned host-only RDKit 2025.9.4 CI fixture job and JSON artifact for ethanol/benzene descriptor sanity; no independent chemistry benchmark, Android integration, ADMET or biological-activity validation claimed | Engineering + Validation | 2026-11-08 |
| I2 | Node docking/virtual screening | Node, approved licenses | Redocking RMSD and decoy enrichment | not-started | Engineering + Validation | TBD |
| I3 | Node MD | Node, engine/model/license | Stability, energy conservation, reference runs | not-started | Engineering + Validation | TBD |
| I4 | ADMET and PK/PD/PBPK | Approved data/models | Held-out performance and applicability domain | not-started | Engineering + Validation | TBD |
| I5 | Variant-effect and virtual-cohort simulations, Research Mode | I4, fairness/model review | Benchmarks, ancestry portability, prediction labels | not-started | Engineering + Validation | TBD |

## Track P — Precision medicine (PGx first)
Hard gate: no patient-related feature before P0; early research uses public test data only.

Public-data preparation increment: `data/public-dataset-catalog.yaml` is an intentionally empty, metadata-only inventory with a strict schema at `api/public-dataset-catalog.schema.json`. Entries require explicit license-review status and `patient_data: false`; this does not authorize data intake or lift P0.
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
- Build-first / test-later: after the initial local-build preference, the owner explicitly authorized GitHub Actions to build unsigned arm64 debug APK/AAB artifacts and run automated source/JVM checks. Emulator and physical-device tests remain separate and are not run in CI.
- This changes implementation sequencing only. It does not authorize false validation claims, bypass third-party license review, enable clinical/patient workflows, or waive scientific/device/security/release exit criteria.
- See docs/research-platform-implementation.md for the current implementation inventory and unfinished scope.

## Track U — User interface (owner specification 2026-11-08)
| ID | Scope | Dependency | Exit gate | Status |
|---|---|---|---|---|
| U0 | Tokens, brand contract/placeholders, generator, design-system skeleton/gallery, lint and screenshot harness | R0 | Three directions shown from a working gallery; owner selects; placeholders flagged; tokens compile to Compose/CSS | in-progress |
| U1 | Adaptive shell, search, Research Mode/status/tier chips, onboarding, schema settings | R2 | Full device/window matrix passed | not-started |
| U2 | App/vault lock, FLAG_SECURE, Recents, encrypted settings, consent, inventory, threat model | R2 | Security tests pass; threat model owner-reviewed | not-started |
| U3 | Tool runner, sequence viewer, kinetics lab, results/provenance and branded export | R3 | TalkBack and 200% font-scale pass | not-started |
| U4 | Mol*/3Dmol.js bridge, alignment/tree/chart/chemistry viewers | S1–S3 | Low-end-device performance budgets met | not-started |
| U5 | Genomics, PGx Research Mode and in-silico screens | P1–P3, I2–I4 | Clinical wording adviser-reviewed before release | not-started |
| U6 | Settings, themes, localisation/RTL, motion/haptics, usability and quality report | U1–U5 | All quality bars measured and recorded | not-started |

U0 visual direction: owner authorized best-judgement completion; Obsidian Cyan is selected as the dark-first default, with Light and Neon alternatives. Thirteen palette combinations and 26 font candidates are catalogued. Owner-supplied astronaut background is integrated in the Home hero and organization SVG master copied unchanged. Token generation, font licence review, gallery screenshots across compact/medium/expanded and light/dark, and full matrix validation remain open. App-logo placeholders still block release.


### U1 responsive shell progress (2026-11-08)
- Implemented live Compose window-based bottom navigation, rail and permanent drawer, including compact-height landscape rail and 840dp content width cap.
- Added pure JVM boundary tests for navigation classification. Check CI against latest main SHA.
- U1 remains open: NavigationSuiteScaffold/WindowManager posture support, universal search, Research Mode/connectivity chips, onboarding, full screen map and device matrix are not complete.


### Owner authorization D-009 — begin Track S in parallel (2026-11-08)
- The owner explicitly instructed Engineering to complete R1–R10 and start Track S without waiting for another per-track approval.
- This supersedes the previous sequencing prohibition only for independently implementable Track S preparation and implementation. S1 preparation has started; full rendering remains gated on R1 WebView/runtime evidence and exact third-party license approval.
- S2–S5 remain dependent on their scientific reference sets, model/license decisions, node security and benchmark evidence. No scientific, device, production, clinical or release gate is waived.
