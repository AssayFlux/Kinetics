# KINETICS — DIRECTION SYSTEM + PRECISION-MEDICINE / IN-SILICO / 3D-STRUCTURE ADDENDUM

This file extends `KINETICS_GRAND_MASTERPLAN.md`. Where the two conflict, this addendum wins. Read both completely. Start at Part A and do not skip it.

## PART A — THE DIRECTION SYSTEM

### A1. Three living source-of-truth files

Create and maintain in repository root:
1. `NORTH_STAR.md`: permanent direction, mission, five tracks, users, measurable goals, non-goals, guardrails and definitions of done for v0.1, v1.0 and clinical-grade release. Direction changes only with owner's explicit approval.
2. `ROADMAP.md`: every phase, gate, dependency and status (`not-started | in-progress | blocked | done | dropped`), with owner and date fields. Generated from plan files and kept current.
3. `DECISIONS.md`: one entry per decision with date, context, options, choice, consequences and approver. Any change to direction, scope, language, tier, license, data source or regulatory posture requires an entry.

Original plan documents are preserved under `docs/origin/` as read-only history when superseded. The two governing plan texts remain in the repository root. Thereafter the three living files above are operational source of truth.

### A2. Session protocol

- **Start:** read NORTH_STAR, ROADMAP, DECISIONS and last session summary. State in two lines the current phase and this session's intended work.
- **During:** every task maps to a ROADMAP item. Otherwise stop and ask whether to add or drop it.
- **Drift check:** before each task and commit ask: "Does this move a ROADMAP item toward its exit gate, and does it respect the guardrails?" If not, do not proceed.
- **End:** update statuses honestly, append decisions, write SESSION_LOG (done, validated, not done, risks, next step), report to owner.
- **Gates:** stop at every phase gate; continue only with explicit owner approval.
- **Honesty:** never mark done or validated without repository evidence.

## PART B — PRESCRIBING TREATMENT SAFELY

Goal: analyse genetic and other biological data and support treatment research because individuals differ biologically. Pharmacogenomics and precision medicine are important but regulated and safety-critical.

**Two modes, enforced in code and app:**

| | Research Mode (default, public builds) | Clinical Decision Support Mode (later, gated) |
|---|---|---|
| Purpose | Analysis, exploration, education, publication | Evidence-linked decision support for licensed clinician |
| Output | Results with provenance and uncertainty | Reports citing guideline, evidence level and caveats; clinician review/sign-off |
| Claims | "Research use only. Not for diagnosis or treatment decisions." | Claims only when clinically validated and regulatory requirements met |
| Availability | On by default | Feature-flagged off in every public build until Part G requirements met |

The app never autonomously prescribes. It creates evidence-linked reports for qualified clinicians (physician, pharmacist, clinical geneticist); clinicians decide. Patient-facing screens provide education and "discuss this with your doctor", never dosing instructions or start/stop directives. Begin with the narrow, guideline-supported pharmacogenomics slice. Broader disease/treatment claims require separate evidence and approval.

## PART C — PRECISION-MEDICINE PIPELINE

### C1. Inputs
VCF, BAM/CRAM, FASTQ, genotyping-array raw data, targeted-panel results and structured context (age, sex, weight, renal/hepatic function, current medicines, allergies, ancestry only if consented). Always carry consent metadata.

### C2. Registered pipeline capabilities
1. Ingest/QC: Rust parsers, format validation, sample identity/sex checks, coverage and call-quality thresholds.
2. Variant calling/normalisation: Tier C remote node; pin and record reference-genome version; never silently mix genome builds.
3. Annotation: population frequency, consequence, clinical significance and gene/drug links.
4. PGx star-allele/diplotype calling and phenotype translation (poor/intermediate/normal/rapid metaboliser). Complex genes such as CYP2D6 require specialised callers and separate validation. Unresolvable calls are indeterminate, never guessed.
5. Guideline mapping: phenotype + drug to CPIC, DPWG or equivalent recommendation; retain guideline version, evidence level and strength.
6. Variant interpretation: ACMG/AMP-style evidence collection is semi-automated only; qualified human curator classifies. Software never gives a final pathogenic label autonomously.
7. Polygenic risk scores only in Research Mode with ancestry-portability warnings.
8. Reports include software/engine/database/guideline versions, provenance, uncertainty, indeterminate results, limitations and clinician sign-off block.
9. Re-analysis stores inputs and versions for reruns as knowledge changes.

### C3. Candidate tools and data — license verification required
| Need | Candidates |
|---|---|
| VCF/BAM | htslib/bcftools/samtools via Rust noodles or wrappers; pysam on node |
| Variant calling | GATK-class or DeepVariant-class pipelines (Tier C); minimap2/BWA |
| Annotation | Ensembl VEP, SnpEff; verify terms; ANNOVAR may restrict use |
| PGx | PharmCAT (Java, node) and specialised callers |
| Guidelines/drug-gene | CPIC, PharmGKB/ClinPGx, DPWG; verify license/attribution |
| Variant evidence | ClinVar, gnomAD, dbSNP, ClinGen; OMIM and DrugBank flagged for owner decision |
| Missense effect | AlphaMissense, ESM predictors, REVEL-class tools; supporting evidence only, licenses/weights verified |

Validation references: consensus genotype reference materials (e.g. CDC Genetic Testing Reference Material Coordination Program), Genome in a Bottle truth sets, 1000 Genomes and concordance against established tools such as PharmCAT. Record sources, versions and tolerances.

### C4. Population fairness
Display ancestry coverage of every database/model. Warn when reliability is lower for an individual's ancestry. Never present scores as equally valid across populations. Include coverage and limitations in validation reports.

## PART D — IN-SILICO LAB

Purpose: scientific hypothesis generation and prioritisation. Computational results are not proof of efficacy or safety. Label every result with method, version, parameters and benchmark performance.

| Capability | Candidate engines (verify licenses) | Tier |
|---|---|---|
| Ligand preparation, descriptors, drug-likeness | RDKit, Open Babel | A/B |
| Docking/virtual screening | AutoDock Vina, smina, GNINA | C |
| Binding-site detection | fpocket and equivalents | B/C |
| Molecular dynamics | OpenMM, GROMACS | C |
| Advanced free energy | GPU alchemical tools | C |
| ADMET/property prediction | RDKit models; documented open models | B/C |
| PK/PD/PBPK | Python/scipy ODE; Rust/C++ only if justified | A/B |
| Variant effect on protein | Structure stability, conservation, language-model scores | B/C |
| Virtual cohort/in-silico trial | Stochastic and ODE models with assumptions | B/C; Research only |

**Mandatory automated validation**
- Docking: redocking pose accuracy on standard benchmark (success by RMSD threshold) and enrichment on decoy benchmark; report failures.
- MD: energy conservation, stability and reproduction of published reference runs where possible.
- ADMET/PK: held-out performance and applicability-domain warnings.
- Every capability publishes measured accuracy in registry and UI.

## PART E — HIGH-QUALITY 3D STRUCTURE ANALYSIS

### E1. Pipeline
1. Obtain experimental PDB/PDBe/mmCIF, predicted AlphaFold DB structures, node predictions (e.g. ColabFold/ESMFold/Boltz-class; verify model and weights terms) and user uploads.
2. Prepare missing residues/atoms, alternate conformations, protonation, ligands, waters, metals and biological assemblies; log every transformation.
3. Assess geometry/stereochemistry (Ramachandran, clashes, rotamers, MolProbity-style), experimental quality (resolution, R-free) and prediction confidence (pLDDT, PAE). Show visible quality badge on every structure.
4. Analyse secondary structure, contacts, interfaces, SASA, H-bonds, salt bridges, disulfides, pockets, flexibility (B-factors/normal modes/MD), structural alignment and RMSD/TM-score, predicted-vs-experimental comparisons.
5. Map variants onto structures by residue, conservation, confidence, interface and active-site membership. Evidence, not verdict.
6. Visualise offline and GPU-accelerated in WebView: Mol* primary for large structures, 3Dmol.js lightweight; mobile LOD, touch controls, saved views/annotations, PNG/SVG/session export. Node can produce publication-quality renders.

### E2. Validation
Compare RMSD, SASA, contacts and secondary structure to reference tools on a fixed benchmark PDB set with documented tolerances. Compare prediction-confidence behaviour on known cases. Machine-generate results.

## PART F — DATA GOVERNANCE, PRIVACY, SECURITY, ETHICS

- Local-first: genomic data remains on device by default; no upload without explicit node configuration and consent.
- Encryption at rest (Android Keystore-backed), encrypted node transport, no sensitive data in logs, secure deletion; backups opt-in.
- Purpose-specific, revocable, recorded consent; separate research, secondary-findings and sharing consent.
- De-identify where possible; no re-identifying joins without consent.
- Clinical mode requires audit logs and role-based access.
- Determine applicable health/data laws for every jurisdiction (e.g. India's DPDP Act, GDPR, HIPAA as applicable); record analysis in DECISIONS and obtain legal review before real patient data.
- Human data/participants require institutional ethics review or documented exemption.
- Decide incidental-findings policy with clinical advisers in advance.
- Report bias/fairness and ancestry coverage.
- No dangerous pathogen or toxin design/enhancement.

## PART G — REGULATORY AND CLINICAL-VALIDITY PATH

Clinical Decision Support Mode cannot ship until all relevant requirements are met:
1. Intended-use statement and regulatory classification before clinical features.
2. QMS and lifecycle practices appropriate to medical-device expectations (e.g. ISO 13485, IEC 62304, ISO 14971, IEC 62366), introduced from clinical-track start.
3. Separate analytical validity, clinical validity and clinical utility evidence.
4. Care-use genotype sources must be from appropriately accredited labs and validated pipelines; record source and refuse unvalidated clinical-grade inputs.
5. Clinical advisory board: clinical pharmacologist/pharmacist, clinical geneticist and physician.
6. Prospective evaluation with ethics approval before clinical-benefit claims.
7. Post-release surveillance, incident reporting, guideline updates and versioned re-analysis.

Until all applicable requirements are met: public builds disable clinical mode, every screen states "Research use only", and no store listing/paper claims clinical use. Obtain qualified jurisdiction-specific legal/regulatory advice.

## PART H — FIVE TRACKS AND ROADMAP

Phases 0–10 in the grand masterplan constitute **Track R**. Add four parallel tracks; all work is enumerated in ROADMAP.

**Track R — Research platform:** foundations; feasibility; app core; v0.1 sequence/protein/kinetics; Rust layer; structure; chemistry; search/phylogenetics; omics; domain rollout; release hardening.

**Track S — Structure excellence**
- S1 Mol*/3Dmol.js offline WebView viewers, structure loading and preparation log.
- S2 Quality badges and benchmark-validated metrics.
- S3 Variant-on-structure mapping, interface and pocket analysis.
- S4 Node prediction using open models, confidence display, predicted-vs-experimental comparison.
- S5 High-quality rendering/export and structure benchmark report for paper.

**Track I — In-silico lab**
- I1 Ligand preparation, descriptors and drug-likeness (on-device where feasible).
- I2 Node docking/virtual screening with redocking and enrichment benchmarks.
- I3 Node MD with stability checks and reproduced reference runs.
- I4 ADMET and PK/PD/PBPK models with documented accuracy and applicability domain.
- I5 Variant-effect and virtual-cohort simulations (Research Mode).

**Track P — Precision medicine, PGx first**
- P0 Gate: intended-use statement, legal/ethics/regulatory advice in DECISIONS, clinical advisers identified. No patient-related feature before gate.
- P1 Genotype ingestion, QC, annotation and genome-build handling (Research Mode; public test data only).
- P2 PGx star-allele/diplotype/phenotype calling for small, guideline-supported gene set; validate against references and established tools.
- P3 Guideline mapping and report generator with provenance, uncertainty and indeterminate handling (Research Mode).
- P4 Variant-interpretation evidence assistant with human curator workflow.
- P5 Clinical advisory review of wording/workflows and clinician usability tests.
- P6 Clinical mode behind feature flag, audit logs, role-based access and sign-off; internal validation study.
- P7 Regulatory submission planning and prospective evaluation (tracked; external activities).
- Further disease areas only after P7 evidence, one at a time.

**Track G — Governance from day one**
- G1 Privacy/security architecture: local-first, encryption, consent.
- G2 Third-party software/data license register; restrictive items require owner decision.
- G3 QMS/software lifecycle documentation beginning at P0.
- G4 Bias and ancestry-coverage reporting.
- G5 Paper evidence generated by validation/benchmarks; claims mapped to registry. Candidate split: platform paper (R), structure/in-silico validation paper (S/I), PGx pipeline validation paper (P, Research Mode). Choose venues with owner after checking current requirements.

Registry requirements: each capability has track, mode, evidence level, ancestry coverage where relevant and data licenses. CI must fail if clinical capabilities lack Part G evidence or are exposed by a build without clinical flag.

## PART I — GUARDRAILS AND NON-GOALS

1. App does not autonomously prescribe, dose, diagnose or make emergency decisions.
2. No clinical claims in app, store listing, README or paper without matching validation and regulatory standing.
3. Public builds ship Research Mode only.
4. No real patient data before P0 passes.
5. In-silico outputs are predictions, labelled with measured accuracy.
6. Every database, model and engine has verified license and version; restrictive licenses require owner decision.
7. No invented numbers, results, references or validations; verify citations against sources.
8. No features for designing/enhancing dangerous pathogens or toxins.
9. Direction changes only through DECISIONS.md with owner approval.

## PART J — FIRST SESSION

1. Create NORTH_STAR, ROADMAP, DECISIONS and SESSION_LOG from the grand masterplan and addendum.
2. Show for owner approval and list open decisions: licenses, jurisdictions, paper framing, clinical advisers, first PGx gene set and target devices.
3. Then begin Track R Phase 0 and stop at its exit gate.
