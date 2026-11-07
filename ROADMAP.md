# KINETICS — ROADMAP
**Status vocabulary:** `not-started | in-progress | blocked | done | dropped`  
**Owner convention:** Owner = project owner; contributors/AI assistant may execute only explicitly approved roadmap tasks.  
**Date convention:** target dates are `TBD` until owner approves a schedule. Statuses reflect repository evidence, not intention.

## Current phase
**Track R — Phase 0: Foundations (not-started).** This documentation baseline must be reviewed/approved before Phase 0 implementation begins. No code task is authorized by this initial document-creation step.

## Track R — Research platform

| ID | Phase / scope | Status | Owner | Date / target | Dependencies | Exit gate / evidence |
|---|---|---|---|---|---|---|
| R0 | Foundations: skeleton, CI, linters, registry, registry checker, reproduce-all stub | not-started | Project owner | TBD | Approval of direction documents | CI green on empty skeleton; logs and workflow evidence |
| R1 | Feasibility: embedded Python/Biopython, Rust FFI, C++ JNI, one engine, RDKit alternative, 16 KB alignment, size/startup/memory | not-started | Project owner | TBD | R0 approved; real arm64 device + emulator | Feasibility matrix; explicit owner go/no-go |
| R2 | App core: Compose, SQLite, SAF, provenance, cancellable/resumable jobs, registry and pack manager | not-started | Project owner | TBD | R1 go decision | Import file, run cancellable job, inspect provenance |
| R3 | v0.1 alpha: sequence, protein properties, enzyme kinetics | not-started | Project owner | TBD | R2 | Real-device offline install; independent validation records |
| R4 | Rust fast layer: FASTA/FASTQ/SAM/BAM/VCF, QC, trimming, k-mers | not-started | Project owner | TBD | R1, R2, Rust feasibility | Reference concordance and device benchmarks |
| R5 | Structure: PDB/mmCIF, viewer, secondary structure, RMSD, contacts, SASA, bonds and quality | not-started | Project owner | TBD | R2; Track S dependencies | Fixed-PDB benchmark comparison |
| R6 | Chemistry/molecular biology: formats, descriptors, fingerprints, similarity, PCR/plasmid/CRISPR checks | not-started | Project owner | TBD | R1 feasibility; license approval | Tool-specific tests and license record |
| R7 | Search/phylogenetics/evolution: Tier B local, Tier C node, viewers and conservation | not-started | Project owner | TBD | R2, node security, tier approvals | Reproducible search/tree benchmarks |
| R8 | Omics/microbiology/systems/multi-omics/statistics | not-started | Project owner | TBD | R2, data governance, reference workflows | Independent reference comparisons |
| R9 | Domain rollout in waves of 10–20 | not-started | Project owner | TBD | R3–R8 capabilities and registry | Each domain has ≥1 working tested tool; coverage report |
| R10 | Release hardening: accessibility, performance, crash, privacy, signed AAB, store/GitHub release | not-started | Project owner | TBD | Relevant R gates and G controls | Release checklist and owner approval |

## Track S — Structure excellence

| ID | Scope | Status | Owner | Date / target | Dependencies | Exit gate / evidence |
|---|---|---|---|---|---|---|
| S1 | Offline Mol*/3Dmol.js WebView viewers, structure loading and preparation log | not-started | Project owner | TBD | R2; viewer feasibility; license review | Offline load tests and provenance logs |
| S2 | Quality badges and benchmark-validated structural metrics | not-started | Project owner | TBD | S1; fixed benchmark PDB set | Metric comparison meets predeclared tolerances |
| S3 | Variant-on-structure mapping, interfaces and pockets | not-started | Project owner | TBD | S2; validated residue mapping | Reference cases and mapping tests |
| S4 | Node prediction, confidence display, predicted-vs-experimental comparison | not-started | Project owner | TBD | Secure node; model/weights license approval | Confidence and comparison benchmark report |
| S5 | High-quality rendering/export and structure paper benchmark | not-started | Project owner | TBD | S1–S4 | Reproducible render/export and benchmark report |

## Track I — In-silico lab

| ID | Scope | Status | Owner | Date / target | Dependencies | Exit gate / evidence |
|---|---|---|---|---|---|---|
| I1 | Ligand preparation, descriptors and drug-likeness | not-started | Project owner | TBD | R1/R2; RDKit/Open Babel license/feasibility | Chemistry tests and documented limits |
| I2 | Node docking/virtual screening | not-started | Project owner | TBD | Secure node; engine license approval | Redocking RMSD success + decoy enrichment report |
| I3 | Node MD workflows | not-started | Project owner | TBD | Secure node; force-field/data licenses | Stability/energy checks and reproduced reference run |
| I4 | ADMET and PK/PD/PBPK models | not-started | Project owner | TBD | Published data and model license review | Held-out metrics, applicability-domain warnings |
| I5 | Variant-effect and virtual-cohort simulations (Research Mode) | not-started | Project owner | TBD | S/R structural and data foundations | Reproducible benchmark; predictions clearly labelled |

## Track P — Precision medicine (PGx first)

| ID | Scope | Status | Owner | Date / target | Dependencies | Exit gate / evidence |
|---|---|---|---|---|---|---|
| P0 | **Hard gate:** intended use, legal/ethics/regulatory advice, clinical advisers; no patient feature before pass | not-started | Project owner | TBD | G1–G3 preparation; adviser/legal access | Approved intended-use statement, advice logged, advisers identified |
| P1 | Genotype ingestion, QC, annotation, genome-build handling; Research Mode/public test data only | blocked | Project owner | TBD | P0 pass; R4; public test data and license review | QC/concordance records, build pinned, no patient data |
| P2 | PGx star-allele/diplotype/phenotype calling for small guideline-supported gene set | blocked | Project owner | TBD | P1; gene set decision; reference materials | Per-gene validation vs references/established tools |
| P3 | Guideline mapping and Research Mode report generator | blocked | Project owner | TBD | P2; CPIC/DPWG license/version review | Provenance, uncertainty, indeterminate and guideline-version tests |
| P4 | Variant interpretation evidence assistant with human curator | blocked | Project owner | TBD | P1; evidence-source license review; curator workflow | Human classification workflow; no autonomous final pathogenic label |
| P5 | Clinical advisory review and clinician usability testing | blocked | Project owner | TBD | P0–P4; advisers; ethics review if required | Signed review and documented usability evidence |
| P6 | Clinical mode behind flag; audit, RBAC, sign-off and internal validation | blocked | Project owner | TBD | P5; all applicable Part G evidence | Flag-off public build tests; internal validation and audit evidence |
| P7 | Regulatory submission planning and prospective evaluation | blocked | Project owner | TBD | P6; jurisdictional advice, ethics and clinical partners | Documented regulatory plan and prospective evidence; outside-repo tasks tracked |

## Track G — Governance (continuous)

| ID | Scope | Status | Owner | Date / target | Dependencies | Exit gate / evidence |
|---|---|---|---|---|---|---|
| G1 | Local-first privacy/security, encryption, consent, threat model and data lifecycle | not-started | Project owner | TBD | Direction approval | Architecture, threat model and tests |
| G2 | Third-party software/model/data license register | not-started | Project owner | TBD | Source-text review | Versioned license evidence; restrictive items escalated |
| G3 | QMS and software lifecycle documentation from P0 | not-started | Project owner | TBD | P0 preparation; legal/regulatory advice | Approved lifecycle/risk documentation |
| G4 | Bias and ancestry coverage reporting | not-started | Project owner | TBD | Source/model inventory | Coverage documented in registry, UI and validation |
| G5 | Paper evidence automation and claim-to-registry mapping | not-started | Project owner | TBD | R/S/I/P validation outputs | Reproducible manuscript evidence; venue chosen by owner |

## Phase gates and approval holds
- **Gate D0 — Direction baseline:** owner reviews NORTH_STAR, ROADMAP, DECISIONS and SESSION_LOG. No Phase 0 code until explicit approval.
- **Gate R0 — Phase 0 exit:** CI green on empty skeleton. Stop and obtain explicit approval before R1.
- **Gate R1 — Feasibility go/no-go:** owner decision required before Phase 2.
- **Gate P0 — Precision-medicine safety gate:** no patient-related feature before pass.
- **Gate P6/P7 — Clinical release:** public clinical mode stays disabled until all applicable Part G criteria, validation and jurisdictional authorization are satisfied.
- **Other gates:** stop at each phase exit and obtain explicit approval before starting the next phase.

## Status policy
- `done` requires repository evidence and gate approval where applicable.
- `validated` is an evidence claim, not a plan status; attach machine-generated report and references.
- `blocked` requires a stated blocker and resolution condition.
- `dropped` requires owner approval and a DECISIONS.md entry.
- Update owner and date fields as assignments/schedule are approved. Never infer completion from code presence alone.
