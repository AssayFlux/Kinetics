# Kinetics — Roadmap

**Status:** Proposed baseline; requires owner approval  
**Last updated:** 2026-11-07  
**Status vocabulary:** `not-started | in-progress | blocked | done | dropped`  
**Owner convention:** `Project owner` means the repository owner; `Engineering` means the implementation contributor. Assign named owners before execution where needed. Dates are target/review dates, not claims of completion.

This roadmap is derived from the Kinetics master specification. A phase is not complete until its exit evidence is in the repository and the owner has approved its gate. Never infer completion from code presence alone.

## Current position

- **Track R / R0 Foundations — in-progress (documentation setup only).**
- No scientific implementation or validation is claimed.
- The current repository default branch contains the `Assets/` directory; the requested four direction files are being established.
- The supplied master specification was present in the session, but no root `KINETICS_MASTER.md` was found in the current repository tree. Archival under `docs/origin/` is therefore blocked pending restoration/creation of the exact source text.

## Track R — Research platform

| ID | Phase / scope | Dependencies | Exit gate / evidence | Status | Owner | Target / review |
|---|---|---|---|---|---|---|
| R0 | Foundations: repo skeleton; direction files; owner-selected LICENSE placeholder (do not choose license); CI for lint/type-check/tests/native builds/16 KB alignment/size budgets; pre-commit; capability registry; registry checker; reproduce-all stub. | Direction-file approval | CI green on empty skeleton; registry checks run; no license chosen without owner decision. Stop for owner approval. | in-progress | Engineering + Project owner | 2026-11-07 review |
| R1 | Feasibility spikes on real arm64 device and emulator: embedded Python + Biopython; Rust app call; C++ JNI kernel; one cross-compiled engine; RDKit or alternative; offline Mol* WebView; 16 KB alignment, APK/AAB size, cold start, memory. | R0 approved | `docs/android-feasibility.md` with reproducible evidence and go/no-go matrix. **Owner go/no-go gate.** | not-started | Engineering | TBD |
| R2 | App core: Compose shell, SQLite project store, SAF import/export, provenance, cancellable/resumable WorkManager jobs, registry loader, pack manager, Keystore encryption. | R1 go decision | On device: import file, run trivial cancellable job, inspect provenance. | not-started | Engineering | TBD |
| R3 | v0.1 alpha: sequence tools, protein properties, enzyme kinetics; published/textbook and independent-reference validation. | R2 | Real-device offline install; validation records and reproducibility evidence for every shipped capability. **v0.1 gate.** | not-started | Engineering + Validation | TBD |
| R4 | Rust fast layer: FASTA/FASTQ/SAM/BAM/VCF parsing, QC, trimming, k-mers. | R2; R1 Rust feasibility | Concordance to reference tools; bounded-memory and on-device benchmarks. | not-started | Engineering + Validation | TBD |
| R5 | Structure basics: PDB/mmCIF, secondary structure, RMSD, contacts, SASA, H-bonds, salt bridges, disulfides. | R2; structure test data/license review | Fixed reference PDB benchmark and documented tolerances. | not-started | Engineering + Validation | TBD |
| R6 | Chemistry and molecular biology: SMILES/SDF/MOL, descriptors, fingerprints, similarity, substructure, drug-likeness; PCR, plasmid/cloning checks, CRISPR guide enumeration with documented rules. | R1 chemistry feasibility; license review | Per-capability tests, benchmark evidence and license approvals. | not-started | Engineering + Validation | TBD |
| R7 | Search, phylogenetics, evolution: Tier-B local and Tier-C node engines; alignment/tree viewers; conservation and logos. | R2; engine tier and license decisions | Independent-reference concordance and offline viewer tests; remote-node security tests. | not-started | Engineering + Validation | TBD |
| R8 | Omics, microbiology, systems, multi-omics and statistics: count matrices, normalisation, differential expression, enrichment, diversity, flux balance, networks, ODEs, PCA/clustering and plots. | R2; validation datasets and R reference CI | Reproducible reference comparisons (including R/DESeq2 where applicable). | not-started | Engineering + Validation | TBD |
| R9 | Domain rollout in waves of 10–20, preserving supplied domain names/descriptions; publish coverage report each wave. | Registry and relevant R capabilities | A domain is implemented only when at least one tool works and is tested; generated coverage report per wave. | not-started | Engineering | TBD |
| R10 | Release hardening: accessibility, low-end performance, crash-free testing, privacy/data-safety documents, signed AAB, honest store listing, GitHub APK, optional F-Droid assessment. | R3 and selected shipped scope; G1–G4 | Publishing checklist in master specification satisfied; release review and owner approval. | not-started | Engineering + Project owner | TBD |

**v0.1.0 scope:** R0–R3 only. R1 is a mandatory go/no-go gate. R0 exit gate is CI green on the empty skeleton.

## Track S — Structure excellence

| ID | Phase / scope | Dependencies | Exit gate / evidence | Status | Owner | Target / review |
|---|---|---|---|---|---|---|
| S1 | Offline Mol*/3Dmol.js viewers, structure loading and preparation log. | R1 WebView feasibility; R2; license review | Offline loading tests and provenance of preparation operations. | not-started | Engineering | TBD |
| S2 | Structure quality metrics and badges. | S1; fixed reference PDB set | Benchmark concordance and documented metric tolerances. | not-started | Engineering + Validation | TBD |
| S3 | Variant-on-structure mapping, interface and pocket analysis. | S2; variant annotation evidence | Capability-level validation; output explicitly evidence, not verdict. | not-started | Engineering + Validation | TBD |
| S4 | Node-based prediction using approved open models; confidence display; predicted-vs-experimental comparison. | Remote-node security; model/code/weights license approval | Reproducible benchmark report and confidence limitations. | not-started | Engineering + Validation | TBD |
| S5 | High-quality rendering/export and structure benchmark report for paper. | S1–S4 as applicable | Reproducible renders and figures generated from benchmark data. | not-started | Engineering + Validation | TBD |

## Track I — In-silico lab

| ID | Phase / scope | Dependencies | Exit gate / evidence | Status | Owner | Target / review |
|---|---|---|---|---|---|---|
| I1 | Ligand preparation, descriptors and drug-likeness; on-device only where feasible. | R1 chemistry feasibility; license review | Per-capability correctness tests, limits and provenance. | not-started | Engineering + Validation | TBD |
| I2 | Node docking/virtual screening. | Remote node; approved engine/data licenses | Redocking pose accuracy at stated RMSD thresholds and decoy enrichment benchmark. | not-started | Engineering + Validation | TBD |
| I3 | Node molecular dynamics. | Remote node; engine/model/license approval | Stability, energy-conservation checks and reproduced reference runs where possible. | not-started | Engineering + Validation | TBD |
| I4 | ADMET and PK/PD/PBPK-style models. | Approved datasets/models; validation design | Held-out performance, assumptions, applicability domain and uncertainty documented. | not-started | Engineering + Validation | TBD |
| I5 | Variant-effect and virtual-cohort simulations (Research Mode). | I4; fairness review; model approvals | Benchmark evidence, ancestry portability and explicit prediction labels. | not-started | Engineering + Validation | TBD |

## Track P — Precision medicine (PGx first)

**Hard gate:** no patient-related feature is built before P0 passes. Early research work uses public test/reference data only. No clinical decision support is enabled by implication.

| ID | Phase / scope | Dependencies | Exit gate / evidence | Status | Owner | Target / review |
|---|---|---|---|---|---|---|
| P0 | Intended-use statement; jurisdiction-specific legal, ethics and regulatory advice recorded in DECISIONS; clinical advisers identified; QMS/lifecycle approach initiated. | G1–G3 planning | Written gate packet and explicit owner approval. **No patient-related feature before this gate.** | blocked | Project owner + qualified advisers | TBD |
| P1 | Genotype ingestion, QC, annotation and genome-build handling in Research Mode using public test data. | P0; R4; reference data/license review | Version-pinned build handling, QC thresholds and reference concordance. | not-started | Engineering + Validation | TBD |
| P2 | PGx star-allele/diplotype/phenotype calls for a small, owner-approved well-guidelined gene set. | P1; specialist caller and data license review | Reference-material and established-tool concordance; indeterminate calls never guessed. | not-started | Engineering + Clinical advisers | TBD |
| P3 | Guideline mapping and Research Mode report with provenance, uncertainty and indeterminate handling. | P2; CPIC/DPWG/ClinPGx license/attribution review | Versioned guideline/evidence mapping tests and research-only wording review. | not-started | Engineering + Clinical advisers | TBD |
| P4 | Variant-interpretation evidence assistant; human curator makes final classification. | P1; evidence source/license review | Curator workflow tests; no autonomous final pathogenicity classification. | not-started | Engineering + qualified curators | TBD |
| P5 | Clinical advisory review of wording/workflows and clinician usability testing. | P3–P4; ethics review/exemption as applicable | Documented advisory review and approved study evidence. | not-started | Project owner + Clinical advisers | TBD |
| P6 | Clinical Decision Support Mode behind feature flag, with audit logs, RBAC and clinician sign-off; internal validation. | P0–P5; regulatory/legal clearance | Evidence package and explicit owner approval; flag remains off in public builds until authorised. | not-started | Engineering + Clinical advisers | TBD |
| P7 | Regulatory submission planning and prospective evaluation, executed outside repo as appropriate. | P6; jurisdiction-specific advice and ethics approvals | Documented plans, approvals and evidence; no claims beyond standing. | not-started | Project owner + qualified advisers | TBD |

Further disease areas require a separate decision after P7 evidence, one area at a time.

## Track G — Governance

| ID | Phase / scope | Dependencies | Exit gate / evidence | Status | Owner | Target / review |
|---|---|---|---|---|---|---|
| G1 | Privacy/security architecture: local-first storage, encryption, consent, deletion, no sensitive logs, remote-node threat model. | R0 | Reviewed design and testable requirements before sensitive-data workflows. | not-started | Engineering + Project owner | TBD |
| G2 | License register for every dependency, engine, model and database; restrictive licenses flagged for owner decision. | R0; before each dependency is bundled | `docs/third-party.md` entries backed by upstream license text; approval recorded where required. | not-started | Engineering + Project owner | TBD |
| G3 | Quality-management and software lifecycle documentation, starting at P0 and progressively applied to clinical track. | P0 planning | Controlled requirements, risk, verification, change and traceability records appropriate to intended use. | not-started | Project owner + qualified advisers | TBD |
| G4 | Bias and ancestry-coverage reporting. | Relevant P/I capabilities and datasets | Coverage and limitations included in validation reports and user-facing output. | not-started | Validation + Clinical advisers | TBD |
| G5 | Paper evidence pipeline: correctness, performance, reproducibility, coverage, fairness and optional ethical usability evidence. | R/S/I/P evidence as relevant | Manuscript figures/tables generated from validation/benchmarks; every claim traceable to registry evidence. | not-started | Research + Validation | TBD |

## Mandatory approval gates

- **Direction documents:** owner approval before they become the authoritative baseline.
- **R0:** CI green on empty skeleton; stop and report.
- **R1:** explicit owner go/no-go before R2.
- **LICENSE:** owner chooses; do not commit a project license before approval.
- **P0:** no patient-related feature before approval.
- Any GPL/AGPL bundling, new language, engine tier change, restrictive license, real patient data, human-participant work, paper framing/venue/authorship, target jurisdiction or NORTH_STAR change.
- Clinical Decision Support Mode: separate evidence, legal/regulatory and owner approval gate.

## Session protocol

At session start, read NORTH_STAR, ROADMAP, DECISIONS and the last SESSION_LOG entry; report current phase and session objective in two lines. Every task maps to a roadmap item. Before each task and commit, check whether it advances that item's exit gate and respects guardrails. At session end, update statuses honestly, record decisions, append SESSION_LOG and report evidence, gaps and risks. Stop at every gate and wait for explicit owner approval.

## Current session notes

The repository tree inspected on 2026-11-07 contained `Assets/Brand Logo.svg` and `Assets/Kinetics.gif`, but no root `KINETICS_MASTER.md` and no existing direction files. The source-spec archival step is therefore not marked complete. Do not replace or overwrite assets.
