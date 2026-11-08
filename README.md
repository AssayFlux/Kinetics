# Kinetics

<p align="center">
  <strong>Offline-first scientific research workbench</strong><br/>
  <em>Android-native · Reproducible · Provenance-aware · Research-only</em>
</p>

Kinetics is an ambitious, modular platform for computational biology and in-silico research. Its engineering work is organised into four parallel research tracks—**R, S, I and P**—with a dedicated governance and user-experience layer. The project is under active development; implementation progress is not the same as scientific validation or release readiness.

> **Current release state:** Pre-release development. Kinetics is not yet a validated scientific application or a production release. Clinical and patient-data workflows are disabled.

---

## Project at a glance

| Project card | Current position |
|---|---|
| **Product** | Offline-first Android scientific workbench |
| **Primary mode** | Research Mode only |
| **Engineering scope** | R1–R10, developed as one integrated platform |
| **Parallel research** | S — Structure & discovery · I — In-silico laboratory · P — Precision medicine preparation |
| **User experience** | D-015 Light Classic visual direction; native Compose implementation in progress |
| **Build channel** | GitHub Actions · unsigned arm64 debug APK/AAB |
| **Validation state** | Source tests and CI evidence are distinct from device and independent scientific validation |
| **Publication** | Methods-paper preparation only; results must come from reproducible evidence |

## Development dashboard

The cards below summarise the state recorded in the project roadmap. “In progress” means implementation or preparation exists; it does **not** mean the phase has passed its exit gate.

| Track | Focus | Progress recorded | Overall state |
|---|---|---|---|
| **R — Research platform** | Android foundation, secure data, scientific engines, genomics, quality and release hardening | R1–R10 have implementation work recorded; every phase still has outstanding exit evidence | **In progress** |
| **S — Structure & discovery** | Structure analysis, unknown-sequence investigation, genome annotation and protein intelligence | S1 and S6–S9 have bounded preparation/implementation; S2–S5 are not started; S10 remains gated | **In progress** |
| **I — In-silico laboratory** | Chemistry, docking, molecular dynamics, ADMET and simulation | I1 has host-side descriptor/reference-fixture work; I4 is source-inventory preparation; I2, I3 and I5 are not started | **In progress** |
| **P — Precision medicine** | PGx-first research pathway and future governance | Public-source metadata preparation only; P0 is blocked and P1–P7 have not started | **Gated / blocked** |
| **U — User experience** | Brand system, app shell, authentication, dashboard and research workflows | D-015 design authority is active; Compose shell and selected settings/security work exist; complete screen and device verification remain open | **In progress** |
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
| **S1** | Offline structure viewer foundation | Bounded deterministic coordinate payload and schema | Renderer, offline bundle, bridge, R1 feasibility and license review |
| **S2–S5** | Structure quality, variant/pocket analysis, prediction and export | Not started | Reference structures, approved models, security and independent benchmarks |
| **S6** | Unknown-sequence triage | Bounded exact full-length local reference matching and evidence contract | Licensed/versioned packs, curated fixtures and calibrated similarity methods |
| **S7** | Genome annotation | Bounded six-frame complete-ORF candidate enumeration | Organism-specific truth sets, splice-aware models and annotation validation |
| **S8** | Genetic-code investigation | Explicit translation tables with exhaustive codon transcription comparison | Independent inference validation, abstention and organism-specific truth sets |
| **S9** | Protein/structure mapping | Conservative exact unique chain mapping with bounded inputs | Alignment, insertion-code handling, domain references and validation |
| **S10** | De novo protein design | Feasibility planning only | Model/data licensing, secure compute, biosafety, held-out benchmarks and wet-lab validation |

## Track I · In-silico laboratory

| Phase | Workstream | Recorded implementation / preparation | Remaining gate |
|---|---|---|---|
| **I1** | Ligand preparation & descriptors | Bounded SDF foundation; optional host RDKit adapter and pinned descriptor sanity fixture | Independent chemistry benchmarks, Android integration and applicability-domain validation |
| **I2** | Docking & virtual screening | Not started | Secure compute node, engine/model licensing, redocking and decoy benchmarks |
| **I3** | Molecular dynamics | Not started | Approved engine, reproducibility, stability and energy-conservation references |
| **I4** | ADMET / PK-PD / PBPK | Metadata-only candidate source inventory | Data/model licensing, approved datasets and held-out external validation |
| **I5** | Variant-effect & virtual-cohort research | Not started | Research-only schemas, bias/ancestry review and benchmark evidence |

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
| **Current source revision** | `244dddb682af37d14fe9228add9b51b8ae44a8ae` |
| **Latest CI run** | [#2020 — pending](https://github.com/AssayFlux/Kinetics/actions/runs/42477665109) |
| **Current-revision APK/AAB** | Not yet confirmed; do not treat an older artifact as containing the latest UI/security changes |
| **Automated checks** | Awaiting the current workflow result |
| **Android emulator / physical device** | Not verified by CI; installation and runtime evidence remain outstanding |
| **Independent scientific validation** | Not yet established for the platform's research capabilities |
| **Release readiness** | Not ready; unsigned debug builds are development artifacts, not production releases |

Every substantial implementation cycle follows the same loop:

1. Implement a meaningful, roadmap-aligned slice.
2. Build APK/AAB from the exact source revision.
3. Run relevant automated regression, security, schema and scientific tests.
4. Install and inspect the exact build on supported Android environments.
5. Record failures, fix them and repeat the build-and-test cycle.
6. Publish evidence with commit, workflow, artifact hash, environment and limitations.

A missing device, reference dataset or external approval is recorded as **not run / blocked**, never as a pass.

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
