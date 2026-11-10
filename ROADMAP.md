# Kinetics — Roadmap
**Status:** R implementation/host audit closed; Track S implementation active under owner decision D-021; external biological-validation, licensed-resource/model and physical-device gates are approved deferred deliverables, while missing S software implementation remains open; Track I remains blocked
**Last updated:** 2026-11-09  
**Statuses:** not-started | in-progress | blocked | done | dropped  
**Owners:** Project owner = repository owner; Engineering = implementation contributor. Dates are review/target dates, not completion claims.

This roadmap operationalises the archived master. A phase is complete only when exit evidence exists in the repository and required owner approval is recorded.

## Current position
- Track R / R0 Foundations: owner accepted the R0 exit and authorised R1 on 2026-11-07; R0 is done.
- The owner-approved direction baseline and reconstructed historical master are present; NORTH_STAR was not changed.
- Repository skeleton, capability registry/checker/tests, reproduction stub, pre-commit configuration, CI and governance metadata are committed.
- R0 accepted by the owner when they authorised R1 on 2026-11-07. CI evidence: [R0 workflow run](https://github.com/AssayFlux/Kinetics/actions/runs/42378815901).
- D-019 controls sequential execution: R → S → I → P → G. On 2026-11-09 the owner confirmed R complete for sequencing purposes and explicitly directed Engineering to complete S1–S10 before proceeding to I. Track I is blocked until the implementable S software scope is delivered and audited. Owner decision D-021 (2026-11-10) explicitly defers external biological-validation, licensed-resource/model and physical-device requirements as carry-forward deliverables, but does not waive missing software implementation. R device/scientific/licensing/release evidence remains a carry-forward obligation. D-016 requires exact-source build/test evidence for every substantial increment; build success does not replace runtime, scientific or device validation.
- D-005 is approved as a broad strategic direction: build both a comprehensive, expandable PGx gene panel and a broad cross-domain gene catalogue. Treat PGx as a specialised workstream within the wider catalogue, with separate evidence and validation gates. The earlier six-gene list is not a scope limit; exact inventories and rollout waves remain evidence-led. No exhaustive coverage or PGx implementation is claimed. D-004 is approved: defer clinical-adviser recruitment until the research platform is more mature (target review after R3); P0 and all patient/clinical work remain blocked until qualified advisers and all other prerequisites are in place. D-003 (publication strategy) is approved: multiple papers over time, beginning with an evidence-backed platform/software-methods paper after R1–R3 readiness, followed by independently validated domain papers. D-001 (project license) is approved as Apache-2.0; D-002 sets a global long-term ambition including future clinical use, subject to jurisdiction-by-jurisdiction advice and approvals. The canonical Apache-2.0 LICENSE grant file is present at the repository root; the third-party dependency audit remains open.

## Track R — Research platform
| ID | Scope | Dependencies | Exit gate | Status | Owner | Date |
|---|---|---|---|---|---|---|
| R0 | Skeleton; direction files; owner-selected license (do not choose); CI lint/type/tests/native builds/16 KB/size budgets; pre-commit; registry/checker; reproduce-all stub | Direction approval | Empty-skeleton CI green; registry checks/tests; honest blocked checks; stop | done | Engineering + owner | 2026-11-07 |
| R1 | Android arm64 feasibility: embedded Python/Biopython/NumPy/SciPy, Rust FFI, C++ JNI, real scientific engine, RDKit/alternative, offline viewer, 16 KB, local APK/AAB build, SAF/lifecycle, cold start and memory | R0 approved | Reproducible arm64 APK/AAB build evidence, complete feasibility matrix and explicit owner go/no-go; CI build is not device-runtime evidence | implementation and host audit step closed; exact-source CI #2126 on `888e49b` passed all five jobs. APK 69,891,771 bytes (SHA-256 `73e66bacb3d1e45e8928c52c10b3fed14e29aa71c8e09a8df73945ffef24aa06`), AAB 39,953,771 bytes (SHA-256 `a851cdeaf921e8b8b40dd82184fb2ef8200bc7b660ab32c80da448cd22d5aadf`); JVM tests and static alignment passed. Physical-device runtime, embedded Python/Rust/JNI invocation, SciPy/device packaging decision, engine/viewer selection, performance and transitive license review remain open | Engineering + owner | 2026-11-08 |
| R2 | Compose, SQLite, SAF, provenance, cancellable/resumable WorkManager, registry, pack manager, Keystore encryption | Integrated R1 architecture findings; validation remains gated | On-device import, cancellable/resumable job, provenance inspection, security review | in-progress — Compose/SQLite/SAF/WorkManager import; resumable AES-GCM chunks, transactional import provenance, verified cache/export and Keystore-loss preservation; R Step 1 adds a bounded authenticated imported-FASTA WorkManager analysis path with transactional result/provenance storage and job-card inspection; analysis-result SAF JSON export is implemented; Robolectric fresh-install and v1→v4, v2→v4 and v3→v4 migration cases passed exact-source CI #2104; added WorkManager worker fail-closed tests for malformed/missing IDs, unknown jobs, over-limit imports and FASTQ gating (guard tests now seed committed-row metadata to exercise the intended preflight branches without Keystore/decryption; corrected tests passed exact-source CI #2126; Android device/runtime and process-recovery tests remain open; cancellation persists a resumable terminal state; new report-only encrypted orphan inventory scans unreferenced finalized/partial ciphertext without deleting it, with JVM tests for active, missing-job, stale-partial and symlink cases; interrupted-export provider behavior, migration fixtures and device verification remain open | Engineering | 2026-11-08 |
| R3 | v0.1 alpha: sequence tools, protein properties, enzyme kinetics and independent-reference validation | R2 integration; scientific validation remains gated | Offline end-to-end alpha, independent validation records and owner-approved v0.1 gate | in-progress — sequence/protein/kinetics primitives and diagnostics; pinned host-only SciPy comparison now runs on deterministic synthetic cases in CI; experimental reference validation, calibrated uncertainty and app integration remain open | Engineering + Validation | 2026-11-08 |
| R4 | Rust FASTA/FASTQ/SAM/BAM/VCF, QC, trimming, k-mers | R2/Rust feasibility | Reference concordance, bounded memory, device benchmarks | in-progress — wrapped FASTA/FASTQ parsing, FASTA QC and explicit-Phred FASTQ read-quality cards are connected to Android Explore through Chaquopy; R Step 1 adds bounded authenticated imported-FASTA analysis with durable SHA-256-linked result records, job-card inspection and SAF JSON export; Step 2 audit adds export-time source-digest revalidation and bounded result/preview guards (latest audit CI #2126 passed); exact-source ARM64 APK/AAB, JVM tests and host regression suite passed CI #2101; Robolectric SQLite fresh-install and v1→v4/v2→v4/v3→v4 migration tests passed CI #2104; imported FASTA result/export integrity and private plaintext cleanup tests are present; strict SAM/VCF end-to-end workflows, core BAM limits, CRAM Android, adapter trimming, Rust acceleration and on-device Chaquopy execution remain open | Engineering + Validation | 2026-11-08 |
| R5 | PDB/mmCIF, secondary structure, RMSD, contacts, SASA, H-bonds, salt bridges, disulfides | R2/licensed reference set | Fixed PDB benchmark/tolerances | in-progress — PDB/mmCIF atom-site parsing, contacts, superposed RMSD, approximate SASA and distance-only interaction-candidate screening; synthetic Biopython/NumPy PDB/contact/RMSD software comparison passed CI #2105; experimental structures, full mmCIF semantics, SASA/interaction concordance, viewer and device evidence remain open | Engineering + Validation | 2026-11-08 |
| R6 | Chemistry formats/descriptors/fingerprints/similarity/substructure; PCR/plasmid/cloning/CRISPR rules | R1 chemistry feasibility/license review | Tests, benchmarks and license approvals | in-progress — multi-record SDF V2000/V3000 subset parsing, new incremental SDF stream ingestion with positive-integer record/record-size/aggregate-size budgets, graph descriptors, bounded substructure matching and exploratory fingerprints; stereochemistry, aromaticity and production engine open | Engineering + Validation | 2026-11-08 |
| R7 | Search, phylogenetics, evolution; Tier B local/Tier C node; viewers/conservation/logos | R2/engine and license approvals | Reference concordance, offline viewer and node security tests | in-progress — quoted-label Newick, UPGMA/NJ, Jukes–Cantor distances and seeded site-bootstrap split support; ML/Bayesian inference, search, viewers and node security open | Engineering + Validation | 2026-11-08 |
| R8 | Omics, microbiology, systems, multi-omics and statistics | R2/datasets/R reference CI | Reproducible reference comparisons | in-progress — finite-input-checked CPM/CLR, Pearson/cross-omics correlation, fold change, logistic growth, Shannon/Gini-Simpson diversity and exploratory Welch/BH differential expression; count-model inference and broader multi-omics open | Engineering + Validation | 2026-11-08 |
| R9 | Domain rollout in waves of 10–20; preserve supplied definitions; coverage reports | Registry and capabilities | Implemented only when a tool works and is tested | in-progress — full 16-column NCBI Gene annotation ingestion/search from plain/gzip streams; new snapshot-scoped coverage/composition report with no invented completeness denominator; comprehensive PGx allele definitions and domain data packs remain open | Engineering | 2026-11-08 |
| R10 | Accessibility, low-end performance, crash testing, privacy/data safety, signed AAB, honest listing, owner-approved distribution channels (GitHub release assets and/or F-Droid only after channel review) | R3/G1–G4 | Publishing checklist, automated hardening, signed release evidence and owner release approval | in-progress — capability implementation-path integrity checks, authorized CI APK/AAB build lane plus accessibility/security/release gates, and accessibility/security/release gates retained; full hardening remains open | Engineering + owner | 2026-11-08 |

v0.1.0 = R0–R3.

## Track S — Structure excellence, protein intelligence and discovery

**Sequencing gate — CURRENT (D-019/D-020, 2026-11-09):** Execute tracks strictly **R → S → I → P → G**, with exactly two steps per track: (1) build the documented base; (2) audit, test and fix the remaining base gaps. R's implementation/host-audit step has been assessed and reported in `docs/r-track-audit-2026-11-09.md`; D-020 authorizes S as the next engineering track while retaining R device/scientific/licensing/release evidence as carry-forward obligations. The 2026-11-08 parallel S authorization below is historical and superseded by D-019. No phase exit evidence or clinical gate is waived.

| ID | Scope | Dependencies | Exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| S1 | Offline-first Canvas 2D structure viewer, bounded PDB/mmCIF SAF import, provenance and JSON session export | R1 WebView, R2 | Offline asset parity/security tests, import/export build and preparation provenance; device verification remains separate | in-progress — dependency-free Canvas renderer, exact Android/web asset parity, hardened local-only WebView, bounded SAF import (16 MiB), strict UTF-8, Python parser/provenance handoff and SAF JSON session export; physical-device import/export, screenshots, accessibility and performance remain open | Engineering | 2026-11-09 |
| S2 | Geometry/torsion metrics; quality badge only after calibration | S1, fixed experimental structures | Independent geometry concordance, calibrated thresholds and explicit abstention | in-progress — bounded clash screening and phi/psi angles implemented; ambiguous residue identity at one chain/number now rejects; no calibrated grade or Ramachandran classifier | Engineering + Validation | 2026-11-09 |
| S3 | Variant mapping, interface contacts and pocket candidates | S2, variant evidence | Capability validation; evidence not verdict | in-progress — exact and bounded alignment-aware coordinate mapping with tie abstention plus heavy-atom inter-chain contact report; pocket analysis and independent biological validation remain open | Engineering + Validation | 2026-11-09 |
| S4 | Approved model prediction, confidence provenance and experimental comparison | Node security, code/weights licenses | Reproducible benchmark and calibrated confidence | blocked — strict external prediction-envelope validation and experimental CA comparison primitives exist; no prediction engine, approved weights, secure node or calibration benchmark is available | Engineering + Validation | 2026-11-09 |
| S5 | Viewer session export and structure benchmark | S1–S4 as applicable | Deterministic export, benchmark-generated figures and device verification | in-progress — bounded provenance-bearing JSON session export and bounded Android SAF PNG snapshot export; SVG rendering, persisted interactive state and experimental benchmark figures remain open/deferred | Engineering + Validation | 2026-11-09 |
| S6 | Unknown-sequence triage, protein family/domain/motif search and evidence-ranked annotation | R4; versioned local reference packs | Curated positive/negative fixtures, reference concordance, calibrated thresholds, resource bounds | in-progress — bounded streaming FASTA/FASTQ, verified local packs, exact-only DNA/RNA/protein triage and fixed-width motif scanning; no local similarity/profile-HMM/novelty inference and no licensed reference pack is present | Engineering + Validation | 2026-11-09 |
| S7 | Prokaryotic and eukaryotic genome annotation pipelines, gene discovery and provenance | R4; S6; organism-specific references | Curated genome truth sets, coordinate/strand concordance, transcript and annotation review | in-progress — bounded contig QC (N50/L50, GC/ambiguity) and six-frame ORF candidate enumeration; no full prokaryotic/eukaryotic gene prediction, splice/transcript model or functional annotation claim | Engineering + Validation | 2026-11-09 |
| S8 | Non-standard genetic-code investigation and translation-table candidate inference | S6–S7; organism-specific truth sets | Independent reference validation, confusion matrices, calibrated abstention and ambiguous-case tests | in-progress — explicit translation for 24 supported NCBI tables; pinned Biopython 1.88 comparison exhaustively checks all 64 codons and start/stop sets; context-dependent dual-stop tables are excluded; no genetic-code inference | Engineering + Validation | 2026-11-09 |
| S9 | Protein sequence/domain/family intelligence and sequence-to-structure mapping | S1, S6, R5; licensed reference sets | Independent annotation comparisons, residue-mapping tests and model-vs-experiment provenance | in-progress — protein descriptors, fixed-width motif scanning, exact/alignment-aware mapping, geometry and interface primitives; profile-HMM/domain/family references and independent annotation validation remain open | Engineering + Validation | 2026-11-09 |
| S10 | Constrained de novo protein design research, candidate ranking and experimental validation workflow | Model/data license approval, secure compute/node, biosafety review, S6/S9 | Reproducible generation, held-out benchmarks, prospective wet-lab validation and owner approval | blocked — deterministic non-generative design-brief validation with mandatory human review exists; generation is disabled pending approved model/data licenses, secure compute, benchmarks, biosafety and wet-lab plan | Engineering + Validation + Owner | 2026-11-09 |

## Parallel execution and publication evidence

The owner briefly authorized parallel R/S/I/P work on 2026-11-08; that sequencing permission was explicitly superseded by D-019 on 2026-11-09. The historical protocol is retained at [docs/parallel-track-execution.md](docs/parallel-track-execution.md) for audit only. Current work must follow R → S → I → P → G. Manuscript and claim/evidence records remain subject to their publication gates. P0 remains blocked; only non-patient public-data preparation is permitted before its formal gate.

## Track I — In-silico lab
| ID | Scope | Dependencies | Exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| I1 | Ligand prep, descriptors, drug-likeness | R1 chemistry/license | Correctness, limits, provenance | blocked — prior exploratory source work is preserved; do not proceed with I implementation until S exits | Engineering + Validation | 2026-11-09 |
| I2 | Node docking/virtual screening | Node, approved licenses | Redocking RMSD and decoy enrichment | blocked — D-019 sequencing gate; do not start until S exits | Engineering + Validation | 2026-11-09 |
| I3 | Node MD | Node, engine/model/license | Stability, energy conservation, reference runs | blocked — D-019 sequencing gate; do not start until S exits | Engineering + Validation | 2026-11-09 |
| I4 | ADMET and PK/PD/PBPK | Approved data/models | Held-out performance and applicability domain | blocked — prior metadata-only source inventory is preserved; do not proceed with I implementation until S exits | Engineering + Validation | 2026-11-09 |
| I5 | Variant-effect and virtual-cohort simulations, Research Mode | I4, fairness/model review | Benchmarks, ancestry portability, prediction labels | blocked — D-019 sequencing gate; do not start until S exits | Engineering + Validation | 2026-11-09 |

## Track P — Precision medicine (PGx first)
Hard gate: no patient-related feature before P0; early research uses public test data only.

Public-data preparation increment: `data/public-dataset-catalog.yaml` separates candidate source discovery (NCBI Gene, PharmVar, ClinVar, CPIC; all `verify_before_intake`) from acquired dataset entries (`entries: []`). A strict schema plus `scripts/check_public_dataset_catalog.py` enforce non-patient metadata, pinned hashes/timestamps, licence-review evidence and non-clinical intended-use boundaries; synthetic tests run in CI. No data payloads are present; this does not authorize intake or lift P0.
| ID | Scope | Dependencies | Exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| P0 | Intended use; legal/ethics/regulatory advice; advisers identified; QMS approach | G1–G3 planning | Written gate packet and owner approval; no patient feature before pass | blocked | Owner + qualified advisers | TBD |
| P1 | Genotype ingest/QC/annotation/build handling, Research Mode, public data | Public-data-only preparation may proceed now; patient/human data and clinical interpretation require P0, R4, reference/license review | Pinned builds, thresholds and concordance; no patient data | in-progress — metadata-only public-source catalogue and automated gate; synthetic reference-build/contig/coordinate/SHA-256 contract and reference-checked variant normalization implemented with tests; acquired entries remain empty and no genotype interpretation is claimed | Engineering + Validation | 2026-11-09 |
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
- D-016 integrated cycle: implement a substantial vertical slice, build the exact revision, run relevant automated and scientific-reference tests, inspect the artifact, exercise the app on available emulator/device targets, fix defects, and record what was and was not verified. Do not defer all testing to a later campaign.
- This changes implementation sequencing only. It does not authorize false validation claims, bypass third-party license review, enable clinical/patient workflows, or waive scientific/device/security/release exit criteria.
- See docs/research-platform-implementation.md for the current implementation inventory and unfinished scope.

## Track U — User interface (owner specification 2026-11-08)
| ID | Scope | Dependency | Exit gate | Status |
|---|---|---|---|---|
| U0 | D-015 Light Classic/Dark Classic semantic tokens, owner-brand asset contract, generator, Compose primitives/gallery and screenshot harness | R0 | Tokens compile deterministically; owner assets preserved; screenshot, contrast and accessibility evidence reviewed | in-progress — D-015 is the sole active visual direction; Light/Dark/System theme plumbing and local biometric lock screen are implemented in source and CI #2039 passed; reference-image comparison, original logo integration, full screen system and quality evidence remain open |
| U1 | Adaptive shell, search, Research Mode/status/tier chips, onboarding, schema settings | R2 | Full device/window matrix passed | in-progress — four-destination shell and responsive navigation source exist; D-015 local lock screen is compiled in CI #2039; search, onboarding, full destination map and device/window matrix remain open |
| U2 | App/vault lock, FLAG_SECURE, Recents, encrypted settings, consent, inventory, threat model | R2 | Security tests pass; threat model owner-reviewed | in-progress — opt-in AndroidX biometric/device-credential local app-lock source is present and CI #2039 passed; FLAG_SECURE, key lifecycle/recovery review, encrypted settings, consent/inventory and owner-reviewed threat model remain open |
| U3 | Tool runner, sequence viewer, kinetics lab, results/provenance and branded export | R3 | TalkBack and 200% font-scale pass | in-progress — bounded FASTA/FASTQ QC cards launch from Explore; durable job/provenance/result/export integration and remaining viewers are open |
| U4 | Mol*/3Dmol.js bridge, alignment/tree/chart/chemistry viewers | S1–S3 | Low-end-device performance budgets met | not-started |
| U5 | Genomics, PGx Research Mode and in-silico screens | P1–P3, I2–I4 | Clinical wording adviser-reviewed before release | not-started |
| U6 | Settings, themes, localisation/RTL, motion/haptics, usability and quality report | U1–U5 | All quality bars measured and recorded | not-started |

U0 visual direction: D-015 Light Classic is the default and sole active visual authority, with Dark Classic and System appearance. Earlier Obsidian Cyan/neon and pre-D-015 palette proposals are historical only. The owner-supplied dashboard/login JPGs and original brand/organization assets remain the design references; preserve their bytes. Existing carousel/theme work is partial. Full reference-image analysis against running-app screenshots, original brand integration, font licence/glyph review, compact/medium/expanded screenshots, contrast, accessibility and device matrix validation remain open. Do not use the old astronaut/neon direction in active screens.


### U1 responsive shell progress (2026-11-08)
- Implemented live Compose window-based bottom navigation, rail and permanent drawer, including compact-height landscape rail and 840dp content width cap.
- Added pure JVM boundary tests for navigation classification. Check CI against latest main SHA.
- U1 remains open: NavigationSuiteScaffold/WindowManager posture support, universal search, Research Mode/connectivity chips, onboarding, full screen map and device matrix are not complete.


### Historical owner authorization D-009 — begin Track S in parallel (2026-11-08; SUPERSEDED BY D-019)
- The owner explicitly instructed Engineering to complete R1–R10 and start Track S without waiting for another per-track approval.
- This supersedes the previous sequencing prohibition only for independently implementable Track S preparation and implementation. S1 preparation has started; full rendering remains gated on R1 WebView/runtime evidence and exact third-party license approval.
- S2–S5 remain dependent on their scientific reference sets, model/license decisions, node security and benchmark evidence. No scientific, device, production, clinical or release gate is waived.

## Integrated implementation and verification cycle — owner direction (2026-11-08)

The owner required substantial implementation and verification as one continuous cycle. Its parallel-track sequencing clause was superseded by D-019 on 2026-11-09. The build/test/fix/evidence cycle remains active, but tracks must now be executed strictly in sequence.

### Mandatory cycle
1. Plan and inspect: read NORTH_STAR, ROADMAP, DECISIONS and the latest SESSION_LOG; inspect source, assets, registry, dependencies and tests. Map changes to roadmap items.
2. Implement a substantial vertical slice: include UI, domain/orchestration, persistence/security, capability registry and real user actions as applicable. No dead buttons, fake results, placeholder success or controls that merely change appearance without applying state.
3. Build: run reproducible arm64 debug APK/AAB pipeline. Preserve exact source commit, toolchain, artifact hashes and logs. Compilation is only a build result.
4. Test the affected system: Python/Rust/C++/Kotlin tests; Android JVM and instrumentation/UI tests; registry/schema/licence/security checks; migration/recovery/import/export; navigation/action coverage; accessibility/contrast/responsive screenshot checks; runtime probes and resource checks. Emulator and physical-device tests are separate. Unavailable tests are BLOCKED or NOT RUN, never PASS.
5. Inspect the exact artifact: install and exercise the APK from that cycle; verify authentication/biometric flows, visible controls, navigation, persistence, offline behavior and crash-free paths. Record device/API/ABI, steps, expected/actual results, screenshots/logs and APK SHA-256. CI compilation is not an installed-app test.
6. Fix and repeat: any failure returns to implementation; rerun affected tests and required regression suite. Do not accept a failing baseline.
7. Record honestly: update roadmap, registry, validation manifests, UI quality report and session log. Distinguish implemented, automated-test-passed, reference-validated, emulator-verified and physical-device-verified.

### Required UI and authentication scope
- D-015 Light Classic is the sole active visual authority, with Dark Classic and System. Previous neon/Obsidian Cyan and earlier palettes are discontinued for active UI work and retained only as historical records.
- Implement actual splash/onboarding, authentication, dashboard, navigation, profile/security and appearance flows in native Compose, using original owner-provided brand assets without destructive alteration.
- No fictitious remote account service. Clearly distinguish local app-lock from account authentication.
- Biometric unlock must use AndroidX BiometricPrompt, runtime capability/enrollment checks, explicit opt-in, secure credential fallback, lockout/error handling and Keystore-backed cryptographic protection where appropriate. Never store biometric templates or passwords.
- Every visible option must perform a real action, open a real screen, or be explicitly disabled with a reason.
- Research tools are runnable only with a real registry entry, input contract, dispatcher, result model/viewer and tests. Research Mode and non-clinical restrictions remain mandatory.

### Tested-build acceptance
A build may be called tested only when its exact artifact has a recorded successful build, applicable automated regression results and required install/runtime UI evidence. Device checks that cannot be performed remain explicit blockers. A debug APK is not a production release.


## Engineering integration standard — owner direction (2026-11-09)
- Adopted `docs/ENGINEERING_INTEGRATION_STANDARD.md` and `api/engine-envelope-v1.schema.json` under D-018.
- All future implementation increments must state component ownership, call direction, transport, contract/version, boundary risks and matching caller/callee changes before coding. JSON Schema is the semantic source of truth for cross-component engine envelopes.
- Target ownership is Python (science), C++ (performance core), Rust (security), Kotlin (Android), Swift (iPhone), TypeScript/Three.js (offline 3D), Bash (build/test/deploy).
- This is a target standard, not an implementation claim. Current Kotlin/Python/C++/Rust reality and absent Swift/TypeScript sources are explicitly documented. Team size, iOS minimum version and WebView/device matrix remain TBD.
- Follow the owner's strict R → S → I → P → G, two-step-per-track sequence. No parallel track work until the owner changes that instruction.


### R-track exact-source audit CI update — 2026-11-09
- Commit `2ea102719fc37354f18def85bb329a60a885ee2a`, CI run #2094: all five jobs passed, including ARM64 APK/AAB, JVM tests, scientific reference fixtures, RDKit sanity fixtures and declared-source SPDX inventory.
- The imported FASTA integration slice and its Step 2 code audit now have successful exact-source CI evidence. This is not a declaration that all R1–R10 exit criteria are met. Device/runtime, migration/recovery, broader workflow coverage, independent scientific validation and full licence/security gates remain.


### Track execution order — D-019 (2026-11-09)
D-019 supersedes D-009's parallel-track sequencing. Current execution is strictly R → S → I → P → G, with a two-step base-build and audit gate for each track. Do not start S until R's two-step gate is assessed and reported; do not start I until S is assessed, and so on.


## R-track evidence refresh — 2026-11-09 (CI #2101)

The exact-source revision `8c4128d5e448db51f2b48fec6c38ce6022fdb053` passed all five CI jobs. The Python suite collected 233 tests (229 passed, 4 skipped for optional RDKit/pysam dependencies); the separate pinned RDKit sanity job and pinned SciPy/Biopython reference-comparison job passed. Android ARM64 debug APK/AAB packaging, static alignment checks and JVM unit tests passed. See `docs/ci-build-evidence.md` and the R3/R4/R7/R8 phase plans.

This corrects stale records that the R3 bootstrap, R7 phylogenetics and R8 NB2 regression tests had not run: those modules execute in the passing Python suite. It does **not** close R. R1 device/runtime feasibility; R2 database migration, WorkManager and SAF lifecycle instrumentation; R3 independent experimental/reference uncertainty and residual/model-selection validation; R4 device-scale workflows; R5 independent structure concordance/viewer; R6 approved-engine chemistry concordance; R7 published tree concordance; R8 null/power/FDR calibration; R9 authoritative licensed PGx content and clinical gates; and R10 security, accessibility, transitive licensing, signed release and device benchmarks remain open. Current execution remains D-019 strict R → S → I → P → G; S has not started under this sequence.


### S implementation step 1 — started 2026-11-09
- R implementation/host-audit step was closed on exact-source CI #2126 and recorded in D-020; S is now the next sequential engineering track.
- Initial S6 increment hardens local FASTA reference-pack resource limits: all byte/manifest/record/residue limits must be positive integers (booleans and floats are rejected). Exact bytes remain hash-verified before parsing and after ingestion.
- S1 renderer/bridge remains blocked on R1 WebView/device feasibility and exact viewer/transitive-license review. Existing S6–S9 code remains bounded research foundations, not validated biological inference.


### Owner decision D-021 — Track S external gates (2026-11-10)
The owner approved deferring independent biological validation, licensed reference/model acquisition and secure inference infrastructure, and physical-device verification as explicit carry-forward obligations. Unvalidated capabilities remain disabled. This does not close missing software: S4 prediction-engine integration, S6 homology/profile-HMM, S7 full prokaryotic/eukaryotic annotation, and S9 family/domain workflows remain open. S10 generation remains disabled. Track I stays blocked until the remaining implementable S software scope is delivered and audited. See `docs/track-s/audit-2026-11-09.md`.
