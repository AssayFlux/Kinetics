# KINETICS — GRAND MASTER PLAN
**Fresh repository · Android-first · publication-grade**

This plan is the governing technical and research plan. Read it together with `KINETICS_DIRECTION_ADDENDUM.md`. Where they conflict, the addendum wins. The permanent direction is recorded in `NORTH_STAR.md`; execution state is recorded in `ROADMAP.md`; approved changes are recorded in `DECISIONS.md`.

## PART 1 — Vision and thesis

**Kinetics** is an offline-first, Android-native scientific workbench that puts validated bioinformatics, structural biology, chemistry, enzyme-kinetics and omics tools, engines and data packs in a scientist's pocket, with a heavy-compute escape hatch through an optional Remote Compute Node.

**Research thesis (must be proven by measurement):**
1. Core analyses can run correctly and usefully on commodity Android devices.
2. A capability-registry architecture (tool → engine → data pack → domain; status `planned | implemented | validated | device-verified`) makes mobile scientific software auditable and reproducible.
3. Every result carries machine-readable provenance so analyses can be re-run and compared.
4. A hybrid on-device / remote-node design gives scientists a practical path from phone to cluster.

**Scope:** tools, engines, data packs and domain registry. Not a library of books, papers, tutorials or scraped documents.

**Honesty:** papers, app screens and store listings may claim only what validation and benchmarks demonstrate. Never invent numbers.

## PART 2 — Language plan

| Language | Role | Rationale |
|---|---|---|
| Kotlin (Jetpack Compose) | Android shell, UI, navigation, SAF, WorkManager, permissions | Native Android integration; no science logic |
| Python | Scientific orchestration and sequence, structure, protein, kinetics and statistics logic | Scientific ecosystem; embedded and desktop/remote |
| Rust | Parsers, QC, k-mers, contact maps, distance matrices, hashing, pack verification | Memory safety and measured performance |
| C++17+ | Numeric kernels and justified engine/library wrappers | Performance only where benchmark or capability requires |
| C | Only when required by an upstream C engine | Compatibility |
| TypeScript/JavaScript | Offline WebView viewers and charts | Mature visualisation ecosystem |
| SQL / SQLite | Projects, provenance, registry cache and data-pack metadata | Local durable storage |
| R | Desktop CI reference implementations only | Independent validation |
| Bash, YAML, CMake, Gradle | Build, CI and manifests | Infrastructure |

Do not add a language without an entry here and explicit owner approval. Rust and C++ require a measured benchmark or documented capability reason.

## PART 3 — System architecture

```
Android app
  Kotlin / Compose UI (thin shell; no science logic)
       │ jobs, files, permissions
  Python orchestrator (embedded)
       ├── Python scientific tools
       ├── Rust core (parsers, QC, k-mers, hashing)
       ├── C++ kernels (only justified components)
       ├── Tier-B engines (arm64, if feasibility passes)
       └── Data-pack manager (verify and mount)
  SQLite (projects, provenance, registry)
       │ optional, user-configured, authenticated HTTPS
Remote Compute Node (Linux; Tier-C workloads)
```

**Engine tiers**
- **Tier A:** on-device always: Biopython operations, kinetics fitting, QC/k-mers, RMSD, contacts, primers/restriction and light statistics.
- **Tier B:** on-device only if feasibility passes and size/time limits are met: small MSA/search, small tree builds and light chemistry.
- **Tier C:** Remote Compute Node only: MD, docking at scale, assembly, large search and ML.

**Android constraints to verify, never assume:** embedded Python on arm64; native library execution and packaging; 16 KB page-size alignment; APK/AAB size; cold start and memory; 4 GB RAM mid-range arm64 baseline; scoped storage via Storage Access Framework; background-job limits. Only data packs may be downloaded at runtime; no executable-code downloads.

## PART 4 — Repository layout

```
kinetics/
├── README.md LICENSE CITATION.cff CHANGELOG.md SECURITY.md PRIVACY.md CONTRIBUTING.md
├── KINETICS_GRAND_MASTERPLAN.md KINETICS_DIRECTION_ADDENDUM.md
├── NORTH_STAR.md ROADMAP.md DECISIONS.md SESSION_LOG.md
├── android/                       # Kotlin/Compose shell
├── python/kinetics/               # core, io, sequence, protein, structure, chemistry,
│                                  # enzyme_kinetics, genomics, transcriptomics, evolution,
│                                  # systems, multiomics, stats, viz, runners
├── rust/                          # kinetics_core, kinetics_ffi
├── cpp/                           # kernels, JNI, CMake
├── web/                           # offline viewers
├── engines/                       # engine manifests and build recipes; no binaries
├── datapacks/                     # pack manifests only
├── domains/                       # domain YAML
├── capabilities/registry.yaml
├── remote-node/
├── validation/                    # reference datasets, expected values and reports
├── benchmarks/                    # reproducible harness and JSON results
├── paper/                          # manuscript source; generated figures only
├── tests/                          # unit, integration, device
├── scripts/                        # registry, pack, size and reproduce checks
├── docs/                           # architecture, feasibility, third-party register
└── .github/workflows/
```

Docs should be generated from the registry wherever practical. Documents over ~300 lines need a stated reason.

## PART 5 — Capability registry

Every capability is a **Tool → Engine → Data pack** triple linked to one or more domains. Example:

```yaml
- id: kinetics.michaelis_menten_fit
  name: Michaelis–Menten fitting
  domains: [enzymology_kinetics, biochemistry]
  engine: python.scipy_fit
  data_packs: [pack.kinetics_benchmarks]
  tier: A
  status: planned
  device_verified: false
  validation: validation/kinetics/michaelis_menten.md
  phase: 3
  track: R
  mode: research
  evidence_level: none
  ancestry_coverage: not_applicable
  data_licenses: []
```

The addendum's extended fields are mandatory: `track`, `mode: research|clinical`, `evidence_level`, `ancestry_coverage` where relevant, and `data_licenses`.

`scripts/check_registry.py` must fail CI when:
- a validated capability lacks a validation record and benchmark test;
- `device_verified` is true without a device test log;
- a domain references a missing tool, engine or pack;
- public-facing claims lack registry/benchmark support;
- a clinical capability lacks completed clinical evidence gates or is exposed outside the clinical feature flag.

Engine manifests record name, pinned version, tier, source license text, ABIs, build recipe, I/O contracts, limits and test vectors. Data-pack manifests record source, version, verified license, size, SHA-256, schema and delivery mode (`bundled <20 MB | optional-download | remote-only`). Flag restrictive terms for owner decision. Domain files record identity, category, description, tools, engines, packs and status.

## PART 6 — Tool inventory and flagship

Domains: genomics, transcriptomics, proteomics, structural biology, sequence bioinformatics, phylogenetics/evolution, molecular biology/primers, cheminformatics, **enzyme kinetics (flagship)**, systems biology, multi-omics, microbiology/metagenomics, immunoinformatics, biostatistics, scientific visualisation and infrastructure.

The enzyme-kinetics flagship includes Michaelis–Menten, Lineweaver–Burk, Eadie–Hofstee, Hanes–Woolf, nonlinear regression, Km/Vmax/kcat, competitive/noncompetitive/uncompetitive/mixed inhibition, uncertainty and AIC/BIC model comparison. It is a candidate first rigorous validation slice, not a claim of implementation.

Prediction, docking and molecular dynamics are separate capabilities, each validated independently. A working viewer does not validate a scientific engine.

## PART 7 — Track R phases and gates

All Track R phase details below are preserved as the research-platform backbone. Initial statuses are set in `ROADMAP.md`.

### Phase 0 — Foundations
Repository skeleton; LICENSE placeholder (owner decides); CI for lint, type-check, tests, native builds, 16 KB alignment and size budgets; pre-commit (ruff, black, mypy, clippy, rustfmt, clang-format, ktlint); capability registry; `check_registry.py`; `reproduce-all` stub.
**Exit gate:** CI green on the empty skeleton. Stop and report; do not proceed without explicit approval.

### Phase 1 — Feasibility spikes (go/no-go)
On a real arm64 device and emulator prove: (1) embedded Python imports Biopython; (2) Rust callable from app; (3) C++ kernel via JNI; (4) one real engine cross-compiled and executed; (5) RDKit or alternative feasibility; (6) 16 KB alignment, APK/AAB size, cold start and memory. Record `docs/android-feasibility.md`.
**Exit gate:** go/no-go matrix; owner decides before continuation.

### Phase 2 — App core
Compose shell, SQLite project store, SAF import/export, provenance recorder (input hashes, parameters, tool/engine/pack versions, timestamp, device), cancellable/resumable WorkManager job runner, registry loader and data-pack manager.
**Exit gate:** import a file, run a trivial cancellable job and view provenance.

### Phase 3 — v0.1.0 alpha
Sequence tools, protein properties and enzyme kinetics; validate against published/textbook data and independent references.
**Exit gate:** installs on real devices, works offline, validation records exist.

### Phase 4 — Rust fast layer
FASTA/FASTQ/SAM/BAM/VCF parsing, QC, trimming and k-mers; outputs agree with reference tools; on-device benchmarks.

### Phase 5 — Structure
PDB/mmCIF, offline viewer, secondary structure, RMSD, contact maps, SASA, H-bonds, salt bridges, disulfides and quality checks; compare with reference tools on fixed PDB IDs.

### Phase 6 — Chemistry and molecular biology
If feasibility allows: SMILES/SDF/MOL, descriptors, fingerprints, similarity, substructure and drug-likeness; in-silico PCR, plasmid/cloning checks and CRISPR guide enumeration with documented rules.

### Phase 7 — Search, phylogenetics and evolution
Tier-B engines on-device; Tier-C via Remote Compute Node; tree/alignment viewers, conservation and logos.

### Phase 8 — Omics, microbiology, systems, multi-omics and statistics
Count matrices, normalisation, differential expression cross-checked against R references in CI, enrichment, diversity, flux balance, network metrics, ODE models, PCA/clustering and publication plots.

### Phase 9 — Domain rollout
Waves of 10–20 domains. A domain is implemented only if at least one tool works and is tested. Publish a coverage report each wave.

### Phase 10 — Release hardening
Accessibility, low-end performance budgets, crash testing, privacy/data-safety docs, signed AAB, research-use disclaimer, GitHub release APK and optional F-Droid.
**Gate:** release checklist and owner approval.

**v0.1.0 = Phases 0–3.** The first paper evidence set may draw on Phases 1–5.

## PART 8 — Research-paper track

Goal: a reproducible, honest manuscript. Candidate framings to decide with owner: software/application note or methods paper on mobile scientific computing. Candidate venues to evaluate: Bioinformatics (Application Note), BMC Bioinformatics, Journal of Open Source Software, PLOS Computational Biology (Software). Verify current scope and requirements before choosing.

Repo-generated evidence:
1. Correctness: `validation/` compares each validated capability to reference values/tools with tolerances, versions and cited datasets; reports generated by machine.
2. Performance: `benchmarks/` records runtime, peak memory and, where practical, battery/thermal on defined devices, with desktop baselines; raw JSON retained.
3. Reproducibility: provenance round-trip reproduces outputs within tolerance; `scripts/reproduce-all` rebuilds every table and figure from raw data.
4. Coverage/auditability: registry-generated coverage for domains, tools, engines, packs and statuses.
5. Usability only with ethics approval/exemption, consent and pre-defined tasks; never imply a study not run.

Paper rules: figures generated only from validation/benchmark data; every claim maps to a registry entry or benchmark; limitations explicit; release artifacts include tagged release, Zenodo DOI, CITATION.cff, data/benchmark archive and license table. Preprint only after evidence exists. Author, affiliation, funding and competing-interest details remain owner-supplied placeholders.

## PART 9 — Engineering, safety and licensing

- Python 3.10+ typed; stable Rust/clippy; C++17+ with sanitizers; Kotlin lint; strict TypeScript.
- Runners use argument arrays, never `shell=True`; enforce timeout, memory cap, cancellation, output capture, exit-code checks and version logging.
- Parsers reject malformed input with specific errors; no silent coercion; bounded memory and streaming for large files.
- Offline-first; no telemetry by default; network only for user-triggered pack downloads or configured node; minimal permissions; authenticated encrypted node traffic.
- No secrets, large binaries or datasets in git; enforce size budgets.
- No executable-code downloads at runtime.
- Pin every dependency/engine/pack; read upstream license text and record it in `docs/third-party.md`. Flag GPL/AGPL and distribution implications before bundling. Owner chooses project LICENSE.
- Research-use disclaimer; no clinical claims absent evidence and regulatory standing.
- No dangerous pathogen/toxin design or enhancement capabilities.

## PART 10 — Working protocol

For every phase create `docs/phase-N-plan.md`; build vertical slices (code, tests, types, docs, registry); run tests/linters; update statuses honestly. Stop at every phase gate and report done, validated, device-verified, not done, risks and paper evidence. Mandatory owner approval: Phase 1 go/no-go, LICENSE, GPL/AGPL bundling, new language, tier changes, paper framing/venue/authors, and human-participant work. If ambiguous, ask; if blocked, report. Never fake functionality, results or citations.

## PART 11 — Publishing checklist

- [ ] LICENSE chosen by owner and compatible with bundled engines/packs
- [ ] README has honest status and registry-generated domain coverage
- [ ] PRIVACY.md and store data-safety answers match real behaviour
- [ ] 16 KB alignment verified; target SDK meets current Play requirements; signed AAB and size budgets
- [ ] Validation and benchmark reports generated and archived
- [ ] `reproduce-all` succeeds from clean checkout
- [ ] Zenodo DOI, CITATION.cff, CHANGELOG and tagged release
- [ ] Manuscript claims checked against registry and benchmark files
- [ ] No bulk books, papers or documents in repo
