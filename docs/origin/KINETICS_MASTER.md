# KINETICS — MASTER FILE
Historical source specification reconstructed from the project owner's complete 18-part instruction supplied in conversation on 2026-11-07. This is read-only history. After owner approval, NORTH_STAR.md, ROADMAP.md and DECISIONS.md are the operational source of truth.

This master replaces KINETICS_GRAND_MASTERPLAN.md and KINETICS_DIRECTION_AND_PRECISION_MEDICINE_ADDENDUM.md. Follow Parts 1–18 in order and stop at every approval gate.

## Contents
1 Direction system and session protocol; 2 Vision and thesis; 3 Modes and safe precision-medicine goal; 4 Languages; 5 Architecture; 6 Repository layout; 7 Capability registry; 8 Tool inventory; 9 PGx pipeline; 10 In-silico lab; 11 Structure analysis; 12 Governance, ethics and regulation; 13 Five-track roadmap; 14 Research-paper track; 15 Engineering rules; 16 Guardrails; 17 Working protocol and publishing checklist; 18 First session.

## PART 1 — DIRECTION SYSTEM
Create four root files before code:
- NORTH_STAR.md: permanent mission, tracks, users, measurable goals, non-goals, guardrails and definitions of done for v0.1, v1.0 and clinical-grade release. Changes only with explicit owner approval.
- ROADMAP.md: every phase, gate, dependency, status (not-started, in-progress, blocked, done, dropped), owner and date.
- DECISIONS.md: dated decision log with context, options, choice, consequences and approver. Direction, scope, language, engine tier, license, data source and regulatory-posture changes require entries.
- SESSION_LOG.md: one short entry per session recording done, validated, not done, risks and next step.
Then place this master in docs/origin as read-only history. Thereafter NORTH_STAR, ROADMAP and DECISIONS are operational source of truth.
Every session: read those three files and last SESSION_LOG entry; state phase and objective in two lines. Every task maps to a roadmap item; otherwise ask whether to add/drop. Drift-check before each task and commit. End by updating statuses honestly, recording decisions, appending session log and reporting. Stop at every gate for explicit approval. Never claim done/validated without repository evidence.

## PART 2 — VISION AND THESIS
Kinetics is an offline-first, Android-native scientific workbench for validated bioinformatics, structural biology, chemistry, enzyme kinetics, omics and precision-medicine tools, engines and data packs, with optional Remote Compute Node.
Prove by measurement: core analyses work on commodity Android; capability registry (tool → engine → data pack → domain; planned/implemented/validated/device-verified) is auditable; results carry machine-readable provenance; hybrid local/remote compute is practical.
Scope is tools, engines, data packs and domain registry, not books, papers, tutorials, scraped documents or bulk documentation. README, paper and store claims must be supported by validation/benchmarks. Never invent metrics, results or references.

## PART 3 — MODES AND TREATMENT GOAL
Research Mode is default and only mode in public builds: analysis, exploration, education and publication with provenance and uncertainty; show “Research use only. Not for diagnosis or treatment decisions.”
Clinical Decision Support Mode is future, feature-flagged off in every public build until Part 12 is satisfied. It is for evidence-linked decision support for licensed clinicians, with guideline/evidence citations, caveats, clinician review and sign-off.
Never autonomously prescribe, dose, diagnose or make emergency decisions. Patient-facing views are educational and direct users to a clinician; never give dosing or start/stop instructions. Start with pharmacogenomics (PGx). Broader disease-treatment claims come much later, if ever, and only with clinical evidence.

## PART 4 — LANGUAGE PLAN
Kotlin/Jetpack Compose: thin Android shell, navigation, SAF, WorkManager, permissions and Keystore; no science logic.
Python 3.10+ with Biopython/numpy/scipy: scientific orchestration and logic, embedded on-device and desktop/remote.
Rust stable: parsers, QC, k-mers, contact maps, distance matrices, hashing; FFI via UniFFI/JNI; only with benchmark/capability reason.
C++17+: numeric kernels and engine/library wrappers, JNI; RDKit/OpenMM only if feasible; justify with benchmark/capability reason.
C only to cross-compile upstream C engines.
JavaScript/TypeScript: offline WebView viewers (Mol*, 3Dmol.js, sequence/alignment/tree viewers, charts).
SQLite: projects, provenance, registry cache, indexed packs.
R: desktop CI reference validation only, never on-device.
Java: optional Remote Compute Node only.
Bash/YAML/CMake/Gradle: infrastructure.
No new language without this list and owner approval.

## PART 5 — ARCHITECTURE
Android: Kotlin/Compose UI → embedded Python orchestrator → Biopython/numpy/scipy, Rust core, C++ kernels, bundled Tier-B arm64 engines, offline WebView viewers, data-pack manager. SQLite stores projects/provenance/registry. Optional user-configured Remote Compute Node is authenticated and encrypted.
Tier A always on-device: basic Biopython, kinetics fitting, QC/k-mers, RMSD/contacts, primers/restriction, light statistics and viewers.
Tier B on-device only if feasibility passes and size/time limits are met: small searches/MSA/trees and light chemistry.
Tier C remote only: variant calling, PGx callers, MD, docking at scale, assembly, structure prediction, ML and large searches.
Verify Android constraints rather than assume: embedded Python/arm64 package availability; executable bundling and Play policy (never download executable code at runtime); 16 KB page alignment; SAF/scoped storage; background-job limits; 4 GB RAM arm64 baseline; WebGL.

## PART 6 — REPOSITORY LAYOUT
Root: README.md, LICENSE, CITATION.cff, CHANGELOG.md, SECURITY.md, PRIVACY.md, CONTRIBUTING.md, four direction files.
Directories: android/; python/kinetics/{core,io,sequence,protein,structure,chemistry,insilico,enzyme_kinetics,genomics,pgx,transcriptomics,evolution,systems,multiomics,stats,viz,runners}; rust/ (kinetics_core, kinetics_ffi); cpp/ (kernels, JNI, CMake); web/ (offline TypeScript viewers); engines/ (manifests, recipes, test vectors; no binaries); datapacks/ (manifests only); domains/ (small YAML per domain); capabilities/registry.yaml; remote-node/; validation/; benchmarks/; paper/; governance/; tests/{unit,integration,device}; scripts/; docs/{origin,architecture.md,android-feasibility.md,third-party.md,generated reports}; .github/workflows/.
Generate docs from registry where possible. No bulk hand-written docs; any doc over ~300 lines needs a reason.

## PART 7 — CAPABILITY REGISTRY
Each capability is Tool → Engine → Data pack, linked to domains and one track. Record id, name, track, domains, engine, packs, tier, mode (research/clinical), status (planned/implemented/validated), device_verified, evidence_level (none/benchmark/reference-concordance/clinical-study), ancestry coverage, data licenses, validation path and phase.
Checker scripts/check_registry.py must fail CI for validated without validation record and benchmark test; device_verified without device log; missing tool/engine/pack/domain references; README/store/paper claims unsupported by registry; clinical capability without Part 12 evidence or exposed without clinical flag.
Engine manifest: pinned version, tier, source-read license, ABIs, build recipe, input/output contracts, timeout/memory limits and test vectors.
Pack manifest: name/version/source URL/verified license/size/SHA-256/schema/delivery (bundled under 20 MB, optional-download or remote-only). Small, versioned, checksum/license-verified; Wi-Fi default; restrictive terms flagged for owner.
Domain YAML: id/name/category/short description/tools/engines/packs/status. If owner supplies 160+ domains, import unchanged and produce coverage report.

## PART 8 — TOOL INVENTORY
Genomics, transcriptomics, proteomics, structural biology, sequence bioinformatics, phylogenetics/evolution, molecular biology/CRISPR/primers, chemoinformatics, enzyme kinetics, systems biology, multi-omics, microbiology/metagenomics, immunoinformatics, biostatistics, PGx/precision medicine, in-silico drug discovery, scientific visualisation and infrastructure (import/export, provenance, jobs, packs, remote node).
First validation flagship: enzyme kinetics—Michaelis–Menten, Lineweaver–Burk, Eadie–Hofstee, Hanes–Woolf, nonlinear regression, Km/Vmax/kcat, competitive/noncompetitive/uncompetitive/mixed inhibition, uncertainty, AIC/BIC. Prediction, docking, MD and clinical-adjacent functions are separate capabilities validated independently. A viewer proves nothing about an engine.

## PART 9 — PGx PIPELINE
Inputs: VCF, BAM/CRAM, FASTQ, array raw data, targeted panels and consented structured context (age, sex, weight, renal/hepatic function, medicines, allergies, ancestry if consented), always with consent metadata.
Stages, each independently registered: (1) ingest/QC, strict format/sample/coverage/call-quality checks; (2) variant calling/normalisation, Tier C, pinned reference genome/build; (3) annotation with population frequency, consequence, clinical significance and gene/drug links; (4) star-allele/diplotype/phenotype calling, specialised callers for difficult genes such as CYP2D6 structural variation, validate each gene, indeterminate never guessed; (5) CPIC/DPWG/equivalent guideline mapping preserving version/evidence/strength; (6) ACMG/AMP-style evidence collection only, qualified human curator classifies; (7) PRS Research Mode only with ancestry-portability warnings; (8) provenance-rich reports with uncertainty, indeterminate calls, limitations and clinician sign-off block; (9) versioned re-analysis.
Candidates requiring source-license verification: htslib/bcftools/samtools, Rust noodles, pysam; GATK/DeepVariant-class pipelines, minimap2/BWA; Ensembl VEP, SnpEff, ANNOVAR restrictive terms; PharmCAT and specialised callers; CPIC, PharmGKB/ClinPGx, DPWG; ClinVar, gnomAD, dbSNP, ClinGen; restrictive OMIM/DrugBank flagged for owner; AlphaMissense/ESM/REVEL-class predictors supporting evidence only. Reference validation may use CDC genetic reference materials, Genome in a Bottle, 1000 Genomes and PharmCAT concordance; record versions/tolerances.
Fairness: disclose ancestry coverage of each database/model, warn when reliability is lower, never imply equal validity, and include fairness in validation.

## PART 10 — IN-SILICO LAB
Purpose: hypothesis generation/prioritisation, not proof of efficacy or safety. Every output is labelled computational prediction with method/version/parameters/benchmarks.
Candidates/tiers (verify licenses): RDKit/Open Babel ligand prep/descriptors (A/B); AutoDock Vina/smina/GNINA docking (C); fpocket (B/C); OpenMM/GROMACS MD (C); advanced free energy on GPU node (C); ADMET models (B/C); Python/scipy PK/PD/PBPK ODEs (A/B); variant effect (B/C); virtual cohorts (B/C, Research Mode).
Automated reproducible validation: docking redocking RMSD success and decoy enrichment; MD stability/energy conservation/reference runs; ADMET/PK held-out performance and applicability domain. Report failures and measured accuracy honestly.

## PART 11 — STRUCTURE ANALYSIS
Obtain experimental PDB/PDBe/mmCIF, predicted AlphaFold DB or approved node models (verify code/weights licenses), or uploads. Prepare missing residues/atoms, alternate conformations, protonation, ligands, waters, metals and assemblies; log every change. Quality: Ramachandran, clashes, rotamers, geometry, resolution/R-free, pLDDT/PAE; visible quality badge. Analyse secondary structure, contacts, interfaces, SASA, H-bonds, salt bridges, disulfides, pockets, flexibility, alignment, RMSD/TM-score and experimental/predicted comparisons. Map variants to residues, conservation, confidence, interfaces and active sites as evidence, not verdict. Offline WebView: Mol* primary, 3Dmol.js lightweight, level of detail, touch, saved views/annotations, PNG/SVG/session export; node publication renders. Validate RMSD/SASA/contacts/secondary structure against fixed PDB reference set and tolerances with generated reports.

## PART 12 — GOVERNANCE, PRIVACY, ETHICS, REGULATION
Local-first: genomic data stays on device by default; no upload without explicit node configuration and consent. Encrypt at rest (Android Keystore) and in transit; no sensitive data in logs; secure deletion; opt-in backups. Purpose-specific revocable consent, separately for research, secondary findings and sharing. De-identify where possible; no re-identifying joins without consent. Clinical mode requires audit logs and role-based access (optional Research Mode). Identify laws for every jurisdiction (e.g. India's DPDP Act, GDPR, HIPAA as applicable), record in DECISIONS and get legal review before real patient data. Human data/participants require ethics review or documented exemption. Decide incidental-findings policy with advisers. Fairness reporting mandatory. No dangerous pathogen/toxin design or enhancement.
Before Clinical Mode: written intended-use/classification; QMS/software lifecycle practices appropriate to standards such as ISO 13485, IEC 62304, ISO 14971, IEC 62366; analytical validity, clinical validity and clinical utility evidence; accredited/validated genotype sources; advisory board (clinical pharmacologist/pharmacist, clinical geneticist, physician); prospective evaluation with ethics approval before clinical-benefit claims; post-release surveillance, incident reporting and guideline updates. Until then Clinical Mode disabled in public builds, Research use only on every screen, no clinical-use claims.

## PART 13 — FIVE-TRACK ROADMAP
Track R:
R0 Foundations: skeleton; direction files; owner-selected LICENSE placeholder (do not choose); CI lint/type/tests/native builds/16 KB/size budgets; pre-commit ruff/black/mypy/clippy/rustfmt/clang-format/ktlint; registry/checker; reproduce-all stub. Exit: CI green on empty skeleton.
R1 Feasibility: real arm64 + emulator prove embedded Python/Biopython, Rust app call, C++ JNI, one cross-compiled engine, RDKit or alternative, offline Mol* WebView, 16 KB, APK/AAB size, cold start, memory. Record docs/android-feasibility.md; owner go/no-go.
R2 App core: Compose, SQLite, SAF, provenance (input hashes, parameters, tool/engine/pack versions, timestamp/device), WorkManager progress/cancel/resume, registry, pack manager, Keystore encryption. Exit: import file, cancellable job, inspect provenance.
R3 v0.1 alpha: sequence tools, protein properties, enzyme kinetics; textbook/published and independent reference validation; offline real-device install and records. v0.1 = R0–R3.
R4 Rust parsers/QC/trimming/k-mers; reference concordance/device benchmarks.
R5 PDB/mmCIF, secondary structure, RMSD, contacts, SASA, H-bonds, salt bridges, disulfides.
R6 chemistry formats/descriptors/fingerprints/similarity/substructure/drug-likeness; in-silico PCR, plasmid/cloning and documented CRISPR guide rules.
R7 search/phylogenetics/evolution; Tier B local, Tier C node; viewers/conservation/logos.
R8 omics/microbiology/systems/multi-omics/stats: count matrices, normalisation, DE (R reference CI), enrichment, diversity, flux balance, networks, ODE, PCA/clustering/plots.
R9 domains in waves of 10–20; preserve supplied definitions; implemented only when at least one tool works and is tested; coverage report per wave.
R10 accessibility, low-end performance, crash tests, privacy/data-safety, signed AAB, honest store listing, GitHub APK, optional F-Droid.
Track S: S1 offline Mol*/3Dmol.js and preparation log; S2 quality badges/metrics; S3 variant mapping/interface/pocket; S4 node prediction/confidence/experimental comparison; S5 rendering/export/structure benchmark.
Track I: I1 ligand prep/descriptors; I2 node docking with redocking/enrichment; I3 node MD with stability/reference runs; I4 ADMET and PK/PD/PBPK accuracy/applicability; I5 variant-effect and virtual-cohort Research Mode.
Track P: P0 intended use, legal/ethics/regulatory advice, advisers; no patient-related feature before gate. P1 genotype ingestion/QC/annotation/build handling Research Mode/public test data. P2 small owner-approved PGx gene set and validation. P3 guideline mapping/report Research Mode. P4 human-curated variant evidence assistant. P5 advisory review/clinician usability. P6 Clinical Mode flag, audit/RBAC/signoff/internal validation. P7 regulatory planning/prospective evaluation. Further disease areas only after P7 evidence.
Track G: G1 privacy/security; G2 license register; G3 QMS; G4 fairness/ancestry; G5 paper evidence pipeline.

## PART 14 — RESEARCH PAPER
Choose framing and venue with owner after checking current scope/requirements. Candidates: Bioinformatics Application Note, BMC Bioinformatics, JOSS, PLOS Computational Biology Software. Possible papers: platform (R), structure/in-silico (S/I), PGx validation (P1–P3).
Generate correctness reports from validation; performance (runtime/memory/battery/thermal where practical, named devices, raw JSON); reproducibility (provenance round-trip and reproduce-all clean checkout); registry coverage; ancestry fairness. Optional usability only with ethics approval/exemption, consent and predefined tasks.
Paper source/figures only from validation/benchmarks; no hand-edited numbers. Every claim maps to registry/benchmark evidence; limitations stated. Release artifacts: tagged release, Zenodo DOI, CITATION.cff, benchmark archive, license table. Preprint only after evidence. Owner supplies authors, affiliations, funding and COI. Never invent references; verify every citation.

## PART 15 — ENGINEERING RULES
Python 3.10+ typed; Rust stable/clippy clean; C++17+ sanitizers; Kotlin lint/ktlint; TypeScript strict. Runners use argument arrays only (never shell=True), timeouts, memory caps, cancellation, captured output, exit checks and version logging. Parsers reject malformed input specifically, no silent coercion, bounded memory and streaming. Offline-first/no telemetry; network only user-triggered pack downloads or configured node; minimal permissions; authenticated/encrypted node. No secrets, large binaries or datasets in git; CI size budgets. Never download executable code at runtime. Pin dependencies/engines/models/packs, read upstream license and record docs/third-party.md. Flag GPL/AGPL and explain distribution implications before bundling. Do not choose project LICENSE. Research-use disclaimer until Part 12.2 is satisfied.

## PART 16 — GUARDRAILS
1 Never autonomously prescribe, dose, diagnose or make emergency decisions.
2 No clinical claims without matching validation and regulatory standing.
3 Public builds Research Mode only.
4 No real patient data before P0.
5 In-silico results are predictions, labelled with measured accuracy.
6 Verify/version every database, model and engine; restrictive licenses need owner decision.
7 No invented numbers, results, references or validations.
8 No dangerous pathogen/toxin design or enhancement.
9 No bulk documents, books or papers.
10 Direction changes only through DECISIONS with owner approval.

## PART 17 — WORKING PROTOCOL AND PUBLISHING CHECKLIST
For each phase write docs/phase-<id>-plan.md; build vertical slices (code/tests/types/docstrings/registry); run tests/linters; update statuses. Stop at phase end and report done, validated, device-verified, not done, risks and paper evidence. Gates: R1 go/no-go; LICENSE; P0; GPL/AGPL bundling; new language; engine tier changes; paper framing/venue/authors; human participants or real patient data; NORTH_STAR changes. If ambiguous ask; if blocked report; never fake functionality/results/citations.
Publishing checklist: owner-selected compatible LICENSE; honest README status and generated coverage; PRIVACY/store data-safety match behaviour; 16 KB verified/current target SDK/signed AAB/size budgets; validation/benchmark archive; reproduce-all clean checkout; Zenodo DOI/CITATION/CHANGELOG/tag; manuscript claims cross-checked; Clinical Mode disabled in public builds and Research use only visible.

## PART 18 — FIRST SESSION
1 Create four direction files from this master, then place master in docs/origin.
2 Show them for owner approval and list open decisions: license, target jurisdictions, paper framing, clinical advisers, first PGx gene set and target devices.
3 Then begin Track R/R0 and stop at its exit gate.
