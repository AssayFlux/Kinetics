# Kinetics

<p align="center">
  <strong>Offline-first scientific research workbench</strong><br/>
  <em>Android-native · Reproducible · Provenance-aware · Research-only</em>
</p>

Kinetics is an offline-first, modular platform for computational biology and in-silico research. Engineering tracks execute in the owner-approved order **R → S → I → P → G**, with implementation, automated regression, independent scientific validation, device verification and release acceptance recorded separately. The project remains under active development; implementation progress is not scientific validation or release readiness.

> **Current release state:** Pre-release development. Kinetics is not yet a validated scientific application or a production release. Clinical and patient-data workflows are disabled.

---

## Project at a glance

| Project card | Current position |
|---|---|
| **Product** | Offline-first Android scientific workbench |
| **Primary mode** | Research Mode only |
| **Engineering scope** | R1–R10, developed as one integrated platform |
| **Active track** | I — In-silico laboratory; I1 Android graph preview and host RDKit; I2 Vina 1.2.7 runner and private Node worker; I3 OpenMM 8.6.1 CPU runner; I4 PK/PD reference models, leakage-aware ADMET evaluation utilities and gated source catalogue; I5 synthetic cohort and additive-effect simulations |
| **User experience** | D-015 Light Classic visual direction; supplied dashboard/login references recorded; Compose redesign in progress |
| **Build channel** | GitHub Actions · unsigned arm64 debug APK/AAB |
| **Validation state** | I1-I5 combined exact-head CI passed on `026032962de7b8315cfbeaaa0e0d6c39aa0d4ef4` (9/9 jobs); Python 489 passed/9 skipped, Ruff/mypy, Vina/OpenMM/ADMET/RDKit smoke, host reference comparisons, Node worker security, SPDX, Android arm64 APK/AAB/JVM and artifact hashes passed; physical-device, secure-node, complete transitive licence review, approved force fields/data and independent scientific validation remain open |
| **Publication** | Methods-paper preparation only; results must come from reproducible evidence |

## Development dashboard

The current documentation index is [`docs/README.md`](docs/README.md). Track order and decision history are controlled by [`ROADMAP.md`](ROADMAP.md) and [`DECISIONS.md`](DECISIONS.md); superseded instructions are retained only as history.

<sub>Latest fully passing I-track exact-source checkpoint: [workflow #42967649660](https://github.com/AssayFlux/Kinetics/actions/runs/42967649660) on `026032962de7b8315cfbeaaa0e0d6c39aa0d4ef4`. All 9 jobs passed. Physical-device runtime, independent scientific validation, approved resource licensing and secure-node deployment remain open.</sub>


The cards below summarise the state recorded in the project roadmap. “In progress” means implementation or preparation exists; it does **not** mean the phase has passed its exit gate.

| Track | Focus | Progress recorded | Overall state |
|---|---|---|---|
| **R — Research platform** | Android foundation, secure data, scientific engines, genomics, quality and release hardening | Engineering implementation and host-side audit pass completed; device, external validation, licensing and signed-release gates remain open | **Audit closed; acceptance evidence open** |
| **S — Structure & discovery** | Structure analysis, unknown-sequence investigation, genome annotation and protein intelligence | S1–S10 software scope and exact-head software CI exit audit closed; external model/data, independent validation and device gates remain carry-forward | **Software scope closed; acceptance evidence open** |
| **I — In-silico laboratory** | Chemistry, docking, molecular dynamics, ADMET and simulation | I1–I5 software foundations integrated; exact-head combined CI #42967649660 passed all 9 jobs, including Python, Android APK/AAB/JVM, Vina, OpenMM, RDKit, ADMET, Node security, SPDX and scientific-reference checks. Secure node deployment, force-field/data rights, ADMET model validation, governed cohorts, device and scientific acceptance remain gated | **Software CI checkpoint passed; track exit open** |
| **P — Precision medicine** | PGx-first research pathway and future governance | P1 public-data metadata gate, synthetic reference-build/coordinate/SHA-256 contract and regression tests implemented; no acquired datasets or genotype interpretation | **Preparation in progress; P0 blocked** |
| **U — User experience** | Brand system, app shell, authentication, dashboard and research workflows | D-015 Light Classic/Dark Classic/System shell and a local biometric/device-credential app-lock screen are implemented in source; full screen system, brand integration and device verification remain open | **In progress** |
| **G — Governance** | Security, licensing, quality system, bias and publication evidence | Requirements and inventories are documented; formal reviews and evidence gates remain open | **In progress** |

## Track R · Research platform

| Phase | Workstream | Recorded implementation | Remaining acceptance focus |
|---|---|---|---|
| **R1** | Android & runtime foundation | Reproducible arm64 debug APK/AAB build lane, runtime probes and dependency inventory | Device runtime, cold-start/memory, engine decisions and complete license audit |
| **R2** | Storage & workflow | Compose/SQLite/SAF/WorkManager, encrypted chunk storage, provenance, recovery-state handling and orphan inventory | Interrupted export, migration fixtures, recovery review and device lifecycle tests |
| **R3** | Core scientific analysis | Sequence, protein and kinetics primitives; diagnostics and host-side SciPy comparison | Independent reference datasets, experimental validation, uncertainty and app integration |
| **R4** | Sequence & variant formats | FASTA/FASTQ, SAM/VCF, bounded BAM core decoding, QC and normalization primitives | Reference concordance, CRAM Android integration, broader format coverage and benchmarks |
| **R5** | Structural biology | PDB/mmCIF atom parsing, contacts, RMSD, approximate SASA and interaction-candidate screening | Full format semantics, secondary structure and fixed-reference validation |
| **R6** | Chemistry | SDF V2000/V3000 subset, streaming ingestion, graph descriptors and bounded matching/fingerprints | Stereochemistry, aromaticity, production engine and license/benchmark review |
| **R7** | Phylogenetics | Newick, UPGMA/NJ, Jukes–Cantor distances and seeded bootstrap support | ML/Bayesian methods, model selection, search and independent concordance |
| **R8** | Omics & statistics | Normalisation, correlation, growth, diversity and exploratory differential-analysis primitives | Count-model calibration, repeated measures and broader reference validation |
| **R9** | Gene & domain catalogue | NCBI Gene annotation ingestion/search and coverage reporting | Versioned domain packs, comprehensive PGx definitions and validated interpretation |
| **R10** | Quality & release hardening | Registry integrity checks, CI build lane and security/accessibility/release requirements | Transitive SBOM, threat-model review, accessibility/device/performance evidence and signed release |

## Track S · Structure, sequence & discovery

| Phase | Workstream | Recorded implementation / preparation | Remaining gate |
|---|---|---|---|
| **S1** | Offline-first structure viewer | Canvas 2D renderer, bounded PDB/mmCIF SAF import, provenance, JSON/SVG/PNG export and persisted viewer state | Exact-head CI and physical-device import/render/export, screenshots, accessibility and performance evidence |
| **S2–S5** | Geometry/torsion metrics, mapping/interface contacts, prediction evidence and session export | S2 bounded clash/torsion metrics; S3 exact/alignment mapping, inter-chain contacts, ligand-site and apo-pocket geometry candidates; S4 hash-pinned local prediction-process boundary; S5 JSON/PNG/SVG export and viewer-state persistence | S2 calibration, S3 chemical/assembly semantics and independent references, approved S4 model/weights and exact-head/device verification |
| **S6** | Unknown-sequence triage | Bounded FASTA/FASTQ and hash-verified packs; exact/Smith–Waterman search; hash-pinned BLASTP/HMMER adapters and motif evidence | Licensed/versioned reference packs, independent concordance and calibrated thresholds |
| **S7** | Genome annotation | Bounded ORF/contig QC; hash-pinned Prodigal/AUGUSTUS runners; GFF3 validation and CDS reconstruction | Approved/versioned species models, organism-diverse reference concordance and functional annotation validation |
| **S8** | Genetic-code investigation | Explicit translation across 24 supported NCBI tables plus bounded candidate-table ranking from coding-frame/internal-stop and optional complete-CDS evidence, with low-evidence/tie abstention | Taxonomic/codon-usage/homolog/transcript evidence, organism-specific truth sets, calibration and independent confirmation |
| **S9** | Protein/structure intelligence | Protein descriptors, motif scan, exact/alignment-aware mapping, interface evidence and HMMER domain-evidence parsing/ranking | Licensed profile databases, independent family/domain concordance and calibrated thresholds |
| **S10** | Constrained protein design | Typed non-generative brief validator with mandatory human-review and release gates; generation remains blocked | Approved model/data, secure compute, independent benchmarks, biosafety and wet-lab validation |

## Track I · In-silico laboratory

| Phase | Workstream | Recorded implementation / preparation | Remaining gate |
|---|---|---|---|
| **I1** | Ligand preparation & descriptors | Host RDKit descriptor adapter; Android SAF SDF/MOL graph-only preview; 16 MiB input cap and SHA-256 provenance | Exact-head CI passed; physical-device, wider chemistry-reference and Android RDKit licence/ABI/size review |
| **I2** | Docking & virtual screening | Pinned Vina 1.2.7 host runner, bounded PDBQT inputs, provenance, strict schemas and disabled-by-default authenticated Node worker | Engine smoke and Node security CI passed; secure deployment, complete transitive SBOM/licence review, redocking/cross-docking RMSD and decoy enrichment |
| **I3** | Molecular dynamics | Pinned OpenMM 8.6.1 CPU runner for trusted constructed systems, seeded replicas, bounded DCD and provenance | Synthetic harmonic smoke passed; biomolecular force-field/licence selection, secure compute, convergence and independent energy/stability validation |
| **I4** | ADMET / PK-PD / PBPK | One-compartment oral PK/Emax references with SciPy ODE comparison; scaffold split, binary metrics/calibration and Tanimoto applicability domain; metadata-only source catalogue | Exact-head smoke passed; no acquired datasets/trained ADMET model; approved source terms, external validation and PBPK remain open |
| **I5** | Variant-effect & virtual-cohort research | Seeded synthetic aggregate HWE cohort and caller-supplied additive-effect simulation; strict non-patient schemas | Exact-head tests passed; public-cohort governance, fairness/ancestry review and independent variant-effect benchmarks remain open |

## Track P · Precision medicine (PGx first)

<blockquote>
  **P0 is blocked.** Until its legal, ethics, regulatory, qualified-adviser and owner-approval requirements are satisfied, work is restricted to non-patient public-source preparation. No patient data, clinical interpretation or Clinical Mode is enabled.
</blockquote>

| Phase | Workstream | Current state |
|---|---|---|
| **P0** | Intended use, legal/ethics/regulatory review and qualified advisers | **Blocked — mandatory gate** |
| **P1** | Genotype ingestion, QC and build-aware annotation | Not started |
| **P2** | Expandable PGx star-allele/diplotype/phenotype research | Not started |
| **P3** | Guideline mapping and research reports | Not started |
| **P4** | Evidence assistant with human curator | Not started |
| **P5** | Adviser review and usability evaluation | Not started |
| **P6** | Clinical governance, audit and internal validation | Not started |
| **P7** | Regulatory planning and prospective evaluation | Not started |

Only source metadata is catalogued at this stage; no public dataset payloads have been acquired through this preparation work. A gene's presence in a catalogue must never be mistaken for a validated caller or interpretation.

## Product design & experience

| Area | Current direction | Verification still required |
|---|---|---|
| **Visual authority** | D-015 Light Classic: warm ivory, deep maroon, restrained gold and peacock teal; coherent Dark Classic and System options | Contrast measurements and full theme coverage |
| **Layout** | Spacious rounded surfaces, central workspace carousel, adjacent-card previews and stacked research cards | Complete adaptive screen implementation and screenshot review |
| **Typography** | Cormorant Garamond display, IBM Plex Sans UI, IBM Plex Mono scientific data; limited Great Vibes accent only where appropriate | Font licensing, glyph coverage, offline packaging and size review |
| **Brand assets** | Owner-supplied logo artwork must remain unchanged | Correct integration on splash, navigation, login and export surfaces |
| **Authentication** | Local biometric/device-credential app lock is distinct from a user account | Lifecycle, fallback, recovery and device testing; no cloud account is implied |
| **Accessibility** | Touch targets, dynamic type, semantics, RTL, keyboard/switch access and reduced motion are requirements | Automated contrast and accessibility checks plus device evidence |

**Superseded visual directions are discontinued for active development.** Neon, Obsidian Cyan and earlier palettes remain historical records only; D-015 is the sole active visual authority.

## Build & verification

| Evidence item | Latest recorded state |
|---|---|
| **Current source revision** | `026032962de7b8315cfbeaaa0e0d6c39aa0d4ef4` |
| **Latest passing CI** | [#42967649660 — all 9 jobs successful](https://github.com/AssayFlux/Kinetics/actions/runs/42967649660) |
| **Python suite** | 498 collected; 489 passed; 9 skipped; Ruff and strict mypy passed |
| **Android arm64 APK** | 70,388,850 bytes · SHA-256 `b767656e1d39f1954da8b4d97d7409cb854ef41ce4ded0d17b62356ba42b81a0` |
| **Android arm64 AAB** | 40,252,958 bytes · SHA-256 `1edbb63f5fc8f0969c8137f9edc7b4f9b775b5cea5c6fa8499fb04e83bd03a80` |
| **Android workflow artifact ZIP** | 80,652,760 bytes · SHA-256 `9ac654392a86fbc494c84bf2c44eed7e9f12c9301646f36c60035e3b5848f430`; [artifact 13832212511](https://github.com/AssayFlux/Kinetics/actions/runs/42967649660/artifacts/13832212511) |
| **Automated checks** | Python, Android APK/AAB/JVM, RDKit, Vina, OpenMM, ADMET, Node worker security, SPDX and pinned scientific-reference jobs all passed on the exact source revision |
| **Emulator / physical device** | Not verified; installation and runtime evidence remain outstanding |
| **Independent scientific validation** | Not established for the platform's research capabilities |
| **Release readiness** | Not ready; debug artifacts are not production-signed releases |

Every substantial implementation cycle follows D-016: implement a meaningful vertical slice, build the exact revision, run relevant automated and scientific-reference tests, inspect the artifact, exercise it on available Android targets, fix failures and record exact evidence. Missing device access, reference data or external approval is recorded as **not run / blocked**, never as a pass.

## Research integrity & publication

- Research Mode only; no patient/clinical workflows.
- Predictions are hypotheses, not experimental proof or clinical advice.
- Outputs must preserve provenance, versions, parameters, uncertainty, warnings and limitations.
- Scientific claims require independent reference validation; software tests alone do not establish scientific validity.
- The manuscript is a working methods-paper skeleton. Results, performance figures and comparative claims are reserved for reproducible evidence in the repository.

## Essential project documents

| Document | Purpose |
|---|---|
| [Roadmap](ROADMAP.md) | Canonical phases, dependencies, status and exit gates |
| [Parallel-track protocol](docs/parallel-track-execution.md) | Rules for concurrent R/S/I/P work |
| [Integrated implementation inventory](docs/research-platform-implementation.md) | Detailed implemented and unfinished engineering scope |
| [Visual design system](docs/ui/kinetics-visual-design-system.md) | Current D-015 brand and interface authority |
| [UI specification](docs/ui/ui-spec.md) | Screen, interaction, accessibility and verification requirements |
| [Research manuscript skeleton](paper/manuscript-skeleton.md) | Publication structure and evidence requirements |

## License

Kinetics project code is licensed under [Apache-2.0](LICENSE). Third-party dependencies, engines, models, fonts, renderers and datasets retain their own terms and require separate review before bundling or redistribution.
