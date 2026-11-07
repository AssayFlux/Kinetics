# KINETICS — Master Prompt (Android-first)

Read this file completely and follow it. Begin work at Part 3 (repository situation protocol). This file governs repository work unless the project owner gives a later explicit instruction. Work directly on main when explicitly requested; do not create branches without permission.

## Part 1 — Mission

Kinetics is an Android-first scientific toolbox for biologists, biochemists and bioinformaticians. It consists of working tools, computational engines, curated data packs, a domain registry and a clean Android application. It is not a library of books, papers, tutorials, literature archives or bulk documents.

Science logic belongs in Python (Biopython), Rust and C++. Android uses only a thin Kotlin + Jetpack Compose shell for UI, permissions, file picking and background work. The shell must contain no scientific logic.

Every capability has status planned → implemented → validated and a runs_on_device boolean. A passing test or working button is not scientific validation. Never advertise beyond real status; never fake functionality. Preserve the 160+ domain definitions. Ask the owner before changing LICENSE, deleting anything that may be original owner-authored work, changing the project name, changing scientific-claim wording, rewriting Git history, bundling GPL/AGPL components, or changing engine placement. Use small commits, one logical change each.

## Part 2 — Android reality: verify, do not assume

Treat all platform choices as feasibility hypotheses:
- Test Chaquopy or equivalent package-by-package on arm64 for Python, Biopython, NumPy, SciPy, pandas and dependencies.
- Test Rust cross-compilation with cargo-ndk for arm64-v8a and x86_64; expose via UniFFI or JNI.
- Test C++ through NDK/CMake/JNI. Investigate RDKit and OpenMM; do not assume they are practical.
- External executable engines (BLAST+, MAFFT, HMMER, MMseqs2, GROMACS, aligners, tree builders) must be bundled with the app/feature module or run on a Remote Compute Node. Runtime downloads are data packs only. Verify current Play policy.
- Verify current 16 KB page-size requirements and enforce native alignment in CI.
- Baseline: 4 GB RAM mid-range arm64 device. Use streaming parsers, bounded memory, cancellable jobs, battery/thermal awareness and resumable background work.
- Use scoped storage and Storage Access Framework; no all-files permission; stream large files.

Engine tiers (exactly one per engine):
- Tier A: always on-device (light Biopython operations, kinetics fitting, QC/k-mers, RMSD/contact maps, restriction/primer tools, light statistics).
- Tier B: on-device only if feasibility passes and size/time limits are enforced (small alignments/searches, small tree building, light chemistry).
- Tier C: Remote Compute Node only (molecular dynamics, large docking/search, assembly, structure prediction, deep learning).

Remote Compute Node is optional, authenticated HTTPS, may run on user's PC/lab/cloud. Never send user data unless the user explicitly configures it. Tier A must work without it.

## Part 3 — Repository situation protocol (first)

### 3.1 Safety
Inspect git status. Preserve uncommitted work before restructuring. Archive the pre-change HEAD and use a restructuring branch only when the owner has authorized it. If the owner explicitly directs work directly on main, obey that and do not create a branch. Never touch .git or change LICENSE without permission.

### 3.2 Discovery: read-only, then AUDIT.md
Record languages, build tools, entry points, build/test status, folder sizes, large binaries/datasets, bulk documents/books/papers/PDFs/scraped text, duplicate notes, secrets (flag without printing values), all 160+ domains (count, structure, duplicates/near-duplicates/gaps), and existing scientific code. Enzyme kinetics (Michaelis–Menten, Lineweaver–Burk, regression and inhibition) is a foundation to preserve.

### 3.3 Classification
- KEEP: working source, tests, domain definitions and small valuable data.
- MIGRATE: useful code in the wrong place/format; use git mv and convert domains to registry format.
- ARCHIVE: historical value only; preserve on archive tag and remove from working branch.
- DELETE: books, papers, PDF/document corpora, bulk prose, scraped text, superseded roadmaps/plans, duplicate plans, generated output, build artifacts, node_modules, large binaries/datasets (replace with data-pack manifests), notebook outputs and unused configs.
The 160+ domain definitions are KEEP/MIGRATE only. If domain files contain long prose, extract structured facts and ask before archiving original prose. If unsure, KEEP or ARCHIVE, never DELETE. If existing code is in another language, propose keep/wrap/port with trade-offs before deciding.

### 3.4 Approval gate
Before destructive changes, report repository identity, domain count/structure, DELETE and ARCHIVE lists with sizes/reasons, MIGRATE map, secrets found and open decisions. Delete nothing until the owner approves. History rewriting requires separate explicit approval.

### 3.5 Execute
After approval, migrate/delete, create the target skeleton, and rewrite README honestly. Existing passing builds/tests must continue to pass or exact changes must be reported.

## Part 4 — Scope and capability model

Keep these 16 tool groups: Genomics, Transcriptomics, Proteomics, Structural biology, Sequence bioinformatics, Phylogenetics, Molecular biology, Chemoinformatics, Enzyme kinetics, Systems biology, Multi-omics, Microbiology, Immunoinformatics, Biostatistics, Visualisation and Scientific infrastructure.

Remove books, papers, literature search, citation/reference managers, long-form user-guide corpora, role-based access control and enterprise audit logs. Keep per-result provenance (input hash, parameters, tool/engine versions and timestamp).

Replace Data & Knowledge with Data Packs: curated, versioned, license-checked datasets. Replace the 16-lab sidebar with mobile navigation. Each capability is Tool → Engine → Data pack (if needed), linked to domains in the registry.

## Part 5 — Target repository layout

Root: README.md, LICENSE, CHANGELOG.md, CITATION.cff, SECURITY.md, PRIVACY.md, KINETICS_MASTER_PROMPT.md.
- android/: thin Kotlin + Compose shell, Chaquopy config, no science logic.
- python/kinetics/: core, io, sequence, protein, structure, chemistry, enzyme_kinetics, genomics, transcriptomics, evolution, systems, multiomics, stats, viz, runners.
- rust/: workspace with kinetics_core and kinetics_ffi.
- cpp/: numerical kernels, JNI and CMake.
- engines/: one folder per engine with engine.yaml, build recipe and test vectors; no binaries committed.
- datapacks/: one folder per pack with pack.yaml manifest only; data not committed.
- domains/: one small YAML per domain.
- capabilities/registry.yaml: tool → engine → pack → domain mapping and status.
- remote-node/: optional authenticated server for Tier C.
- tests/: unit, integration, validation and device.
- scripts/: registry checker, pack builder and size-budget checker.
- docs/: architecture, Android feasibility, third-party inventory and generated registry report.
Docs should be generated from registry where possible. Any document over ~300 lines needs a reason.

Domain YAML fields: id, name, category, short description, tools, engines, data_packs, status (planned/implemented/validated), owner. Engine manifests pin version, tier A/B/C, license, ABIs, build recipe, input/output contracts, resource limits and test vectors. Data-pack manifests include name/version/source/license/size/SHA-256/schema/delivery. Check licenses from source text; flag restrictive licenses for owner decision. Data packs under 20 MB may be bundled; optional downloads should be versioned and checksum-verified.

Registry CI must fail on missing tool/engine/pack references; validated items require validation records and benchmark tests; README/store claims must not exceed registry. Generate domain coverage reports.

## Part 6 — Roadmap and exit gates

Stop and report at the end of every phase; wait for owner go-ahead.

0. Audit, backup/archive safety, cleanup and skeleton. Populate all 160+ domains (planned unless working), CI skeleton and registry checker. Exit: CI green, domain count matches audit, no bulk docs remain.
1. Android feasibility spikes: embedded Python/Biopython; Rust FFI; C++ JNI; one external engine; RDKit/alternative; 16 KB alignment, APK/AAB size, cold start and memory on 4 GB device. Record results in docs/android-feasibility.md. Exit: go/no-go matrix and engine tiers. Owner decides before continuing.
2. App core: Compose shell, SQLite project storage, SAF import, provenance, cancellable/resumable jobs, engine registry and data-pack manager. Exit: import, run, inspect provenance.
3. v0.1.0 alpha: sequence tools; protein properties; enzyme kinetics (Michaelis–Menten, Lineweaver–Burk, Eadie–Hofstee, Hanes–Woolf, nonlinear regression, Km/Vmax/kcat, four inhibition types, uncertainty, AIC/BIC and curves). Validate against published/textbook reference data. Exit: real-device offline use and validation records.
4. Rust fast layer: FASTA/FASTQ, QC, trimming, k-mers, SAM/BAM/VCF, composition; compare with references and benchmark on device.
5. Structure: PDB/mmCIF, offline 3Dmol.js viewer, secondary structure, RMSD, contacts, SASA, H-bonds, salt bridges and quality checks; compare with references.
6. Chemistry/molecular biology: SMILES/SDF/MOL, descriptors, fingerprints, similarity, substructure, drug-likeness, PCR/plasmid/cloning/CRISPR enumeration; compare known values.
7. Search/phylogenetics/evolution: BLAST/MMseqs2/MAFFT/HMMER/tree builders, Tier B where feasible, Tier C via node; reproduce homology/tree benchmarks.
8. Transcriptomics, microbiology, systems biology, multi-omics and statistics; reproduce reference datasets within tolerance.
9. Roll out domains in waves of 10–20. Never mark implemented without at least one working, tested tool on-device or on configured node.
10. Release hardening: privacy, accessibility, low-end performance, crash testing, signed AAB, honest listing and optional F-Droid.

v0.1.0 comprises Phases 0–3 only. Never claim beyond validated and device-verified capabilities.

## Part 7 — Engineering and safety

Python 3.10+, typed, ruff/black/mypy; Rust stable/clippy; C++17+, clang-format and sanitizers; thin linted Kotlin. Runners use argument arrays (never shell=True), timeouts, memory caps, cancellation, captured output, exit checks and version logging. Parsers reject malformed inputs specifically and use bounded memory. Offline-first; no telemetry by default; no network except user-triggered pack downloads or configured remote node. Minimal permissions; authenticated encrypted node traffic. No secrets, large binaries or datasets in git. Pin dependencies and engines, read licenses from source text and record in docs/third-party.md. Explain GPL/AGPL distribution implications before bundling. Never download executable code at runtime.

## Part 8 — Android UX

Use Home (recent projects/quick tools), Domains (searchable 160+ grouped by category), Tools (search/favourites), Data (packs/imports) and Jobs (running/finished/failed). Each tool shows status and on-device/node requirement. Results export CSV/FASTA/PDB/PNG/SVG with provenance. Paginate/stream large outputs. Long work is a job. Tier A works in airplane mode.

## Part 9 — Working protocol

For each phase, write docs/phase-N-plan.md. Deliver vertical slices (code, tests, types, docstrings, registry update), run tests and linters, update statuses honestly. Stop after each phase and report done, validated, device-verified, not done and risks. Mandatory owner gates: destructive deletion list, Phase 1 feasibility go/no-go, LICENSE, GPL/AGPL bundling, history rewrite and engine placement changes. Ask when ambiguous; report blockers; never fake.

## Part 10 — Publishing checklist

- Owner-selected LICENSE compatible with bundled engines and packs.
- README honest status table generated from registry; coverage report for 160+ domains.
- PRIVACY.md and store data-safety answers match real behavior.
- Scientific-use disclaimer in app and store listing.
- 16 KB alignment verified; target SDK per current Play requirements; signed AAB.
- Size budgets met; low-end device tested.
- No bulk documents/books/papers in repo.
- CITATION.cff placeholders flagged; CHANGELOG; v0.1.0 tag and GitHub release.
