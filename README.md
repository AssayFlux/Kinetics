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
| **Next track** | S — Structure, sequence & discovery (after R engineering audit closure) |
| **User experience** | D-015 Light Classic visual direction; supplied dashboard/login references recorded; Compose redesign in progress |
| **Build channel** | GitHub Actions · unsigned arm64 debug APK/AAB |
| **Validation state** | Source tests and CI evidence are distinct from device and independent scientific validation |
| **Publication** | Methods-paper preparation only; results must come from reproducible evidence |

## Development dashboard

The current documentation index is [`docs/README.md`](docs/README.md). Track order and decision history are controlled by [`ROADMAP.md`](ROADMAP.md) and [`DECISIONS.md`](DECISIONS.md); superseded instructions are retained only as history.

<sub>Latest exact-source verification: [CI #2126](https://github.com/AssayFlux/Kinetics/actions/runs/42560038764) on `888e49b` — all five jobs passed. Python: 238 passed, 4 skipped; Android arm64 APK/AAB, JVM tests, package alignment, scientific reference fixtures, RDKit sanity and direct SPDX inventory passed. Physical-device runtime and independent experimental validation remain open.</sub>


The cards below summarise the state recorded in the project roadmap. “In progress” means implementation or preparation exists; it does **not** mean the phase has passed its exit gate.

| Track | Focus | Progress recorded | Overall state |
|---|---|---|---|
| **R — Research platform** | Android foundation, secure data, scientific engines, genomics, quality and release hardening | Engineering implementation and host-side audit pass completed; device, external validation, licensing and signed-release gates remain open | **Audit closed; acceptance evidence open** |
| **S — Structure & discovery** | Structure analysis, unknown-sequence investigation, genome annotation and protein intelligence | Next sequential track; prior preparation is not treated as phase acceptance | **Next** |
| **I — In-silico laboratory** | Chemistry, docking, molecular dynamics, ADMET and simulation | I1 has host-side descriptor/reference-fixture work; I4 is source-inventory preparation; I2, I3 and I5 are not started | **In progress** |
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
| **Current source revision** | `79a24eb00ec7beea30674a591361c2351beaa13d` |
| **Latest CI run** | [#2039 — all five jobs successful](https://github.com/AssayFlux/Kinetics/actions/runs/42493028735) |
| **Current build result** | ARM64 debug APK/AAB, package alignment, artifact hash verification and Android JVM unit-test task passed; Python/registry, pinned host reference, RDKit and SPDX jobs passed |
| **APK / AAB** | APK 69,792,811 bytes · SHA-256 `7029555e9640fd920f22a67890fe921473582affd2538e8aaddd61a261c9e44e`; AAB 39,926,363 bytes · SHA-256 `dd6eb3cc6ddc97c9ed3036b4d6e0747c2e91ef2a6ee57f80eaa4e11e28b8cfa9` |
| **Workflow artifact ZIP** | 79,991,103 bytes · SHA-256 `4b6211b80b9a50a773bdb38c20ee6f7026e327255844f1eeffeb696bc613d8cd` |
| **Automated checks** | All five CI jobs passed on exact source commit `79a24eb`; Android build log reports `BUILD SUCCESSFUL` |
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
