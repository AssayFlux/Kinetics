# Kinetics — Master roadmap

> 160-domain acquisition scope register: docs/SCIENCE_DOMAIN_CATALOGUE_100.md. This catalogue defines intended breadth; it is not evidence that every domain is implemented or clinically validated.
> **Mission authority:** This document is governed by [KINETICS_MISSION.md](KINETICS_MISSION.md). Kinetics is a cross-disciplinary biomedical and precision-health research platform—not only an enzyme-kinetics project. All domains, datasets, models and applications must align with the mission, preserve provenance and clinical safety, and follow the foundation-first build order. Small Android devices are a first-class performance target.

**Horizon:** multi-year and potentially decade-scale. Time bands are planning estimates, not promises.  
**Build principle:** architecture and functional scope first; comprehensive training, testing, benchmarking and scientific evaluation after the integrated implementation is assembled. Continuous engineering checks, security review and safety controls remain active throughout.

## Programme 0 — Governance and project control (Year 0–1)
1. Adopt vision and research-first clinical boundary.
2. Maintain a capability register: implemented, experimental, planned, deprecated.
3. Establish architecture decision records, semantic versioning and deprecation policy.
4. Classify data: public, licensed, controlled research, personal and sensitive health/genetic.
5. Create threat model, privacy principles, consent, retention and deletion policies.
6. Define evidence grades, claim review and publication integrity.
7. Audit software, dataset and model licenses.
8. Establish contributor, code review, security disclosure and risk-register processes.
**Exit:** approved governance, threat model, data classification and capability-status policy.

## Programme 1 — Core platform architecture (Years 0–2)
1. Refactor Python package into domain modules without losing current scientific functionality.
2. Define versioned entities for genes, variants, proteins, structures, compounds, reactions, assays, samples, cohorts, diseases, images, experiments and evidence.
3. Establish typed configuration, validation, logging and error contracts.
4. Define plugin/adapter contracts and versioned APIs.
5. Build resumable workflows with checkpoints, cancellation and resource limits.
6. Create artifact/model/dataset registry with hashes, lineage, licenses and provenance.
7. Add packaging, locked environments, migrations, backup and recovery.
8. Establish CI for formatting, static analysis, tests, dependency/security scans and builds.
**Exit:** stable documented contracts, reproducible install, migration policy and automated quality pipeline.

## Programme 2 — Biomedical data and knowledge foundation (Years 1–3)

**Purpose:** Build the lawful, provenance-preserving scientific knowledge archive and the shared data layer that every domain can use.

1. Maintain a versioned source registry covering scientific domains, publishers, repositories, books, papers, datasets, APIs, licenses, access conditions and rate limits.
2. Build explicit source adapters; no undocumented scraping, access-control bypass or assumed redistribution rights.
3. Resolve canonical identifiers and cross-references with recorded confidence and unresolved-match queues.
4. Preserve immutable raw snapshots and separate normalized, extracted, tokenized, indexed and derived artifacts.
5. Record source IDs, citations, release/retrieval time, license/access terms, checksums and transformation lineage for every object.
6. Implement format-aware extraction/OCR, normalization, deduplication, chunking, tokenization, full-text indexing and source-linked retrieval.
7. Build validation, duplicate/conflict review, rejected-record audits and domain-aware metadata/ontology mapping.
8. Build quality dashboards for rights, provenance, coverage, missingness, processing state, source health and corpus growth.
9. Use fit-for-purpose storage: SQLite/PostgreSQL metadata, Parquet/Arrow tables, Zarr/HDF5 arrays and content-addressed object storage.
10. Build the provenance-aware knowledge graph incrementally; every assertion retains source, context, evidence class and version.
11. **Minimum first corpus milestone: 10,000 books plus 10,000 research papers.** Maintain separate book/paper counts and separate discovered, rights-reviewed, downloaded, verified, extracted, tokenized, indexed and searchable totals. Publish only manifest-backed counts; transfer ceilings and planned targets are never reported as actual growth.
12. Support local/offline retrieval first, with optional permissioned remote APIs and federated upstream queries where bulk mirroring is not permitted.

**Exit:** source and license review is reproducible; the archive reaches the 10k-book/10k-paper minimum with verified processing and searchable counts; selected domain datasets have immutable manifests/data cards; retrieval results link back to source evidence; storage, restore and update procedures are tested. The milestone is a minimum, not a cap on future growth.

## Programme 3 — Genomics, transcriptomics and variant science (Years 1–4)
1. Support validated FASTA/FASTQ, BAM/CRAM, VCF/BCF and annotation adapters.
2. Manage reference genomes/transcriptomes with assembly and version tracking.
3. Orchestrate QC, alignment and variant workflows using established tools.
4. Normalize and annotate variants; link evidence and transcript consequences.
5. Add expression and differential-expression workflows.
6. Add splicing, isoform and regulatory-element analysis.
7. Add single-cell and spatial transcriptomics.
8. Integrate pharmacogenomic sources as cited evidence, not automated medical advice.
9. Report population-frequency, ancestry and reference-bias limitations.
**Exit:** benchmark concordance, external reference checks and documented population limitations.

## Programme 4 — Proteomics and structural biology (Years 1–5)
1. Sequence, motif, domain, homology and conservation services.
2. Protein language-model embedding and training infrastructure.
3. PDB/mmCIF and predicted-structure ingestion.
4. Structure quality, chain mapping, missing residues and alternate conformations.
5. Secondary structure, solvent accessibility, contacts and geometry.
6. Mutation/stability/function and interaction hypotheses.
7. Protein complexes and interfaces.
8. Structural search/alignment adapters (e.g. Foldseek and alternatives).
9. Protein engineering design tracking.
**Exit:** curated structural benchmarks and clear separation of experimental/predicted structures.

## Programme 5 — Enzyme kinetics and biochemical systems (Years 1–4)
1. Reconcile legacy paired-target code with canonical one-measurement-per-row observations.
2. Complete public kinetics adapters after schema/license review.
3. Extend Kinetics-KDB with provenance, assay conditions, qualifiers, replicates and conflict handling.
4. Represent Km, kcat, Ki and catalytic efficiency as typed endpoints with valid derivation rules.
5. Capture reaction, cofactors, pH, temperature, buffer and assay method.
6. Add enzyme family/reaction-class analyses.
7. Compare classical, sequence, graph, structure-aware and context-aware models.
8. Add protein/chemical cold-start, temporal and external-source evaluation.
9. Add calibrated uncertainty, applicability and subgroup analysis.
10. Connect predictions to experimental prioritization and feedback.
**Exit:** versioned benchmark, reproduced baselines, leakage audit and publication-quality evaluation.

## Programme 6 — Cheminformatics and therapeutic discovery (Years 2–6)
1. Compound registry with stereochemistry, salts, tautomers and canonical identity.
2. Reaction representation and transformation tracking.
3. Descriptors, fingerprints, similarity and scaffold analysis.
4. Target–ligand evidence integration.
5. Reproducible docking/virtual-screening adapters.
6. Property, selectivity and developability research.
7. ADMET/toxicity research with endpoint-specific governance.
8. Multi-objective lead optimization.
9. Chemical applicability and uncertainty reporting.
10. Experimental hand-off and negative-result capture.
**Exit:** external benchmarks and experimental confirmation for strong discovery claims.

## Programme 7 — C++ 3D and imaging engine + Rust systems layer (Years 1–6)
### C++ engine
1. Prototype candidate renderer/toolkits and choose based on platform, performance, licensing and maintainability.
2. Build scene graph, camera, picking, materials, lighting and annotations.
3. Add molecular atoms/bonds/ribbons/surfaces/fields.
4. Add meshes, point clouds and spatial geometry.
5. Add volume rendering for CT/MRI/PET and microscopy.
6. Add slice views, registration transforms, segmentation overlays and measurement.
7. Add streaming, tiled data, GPU memory budgets and level-of-detail.
8. Add deterministic screenshots and scene serialization.
### Rust layer
1. Build safe file/data loading and resource lifecycle services.
2. Implement bounded background jobs, cancellation and resource accounting.
3. Secure project/file access and integrity checks.
4. Add streaming and metadata validation services.
5. Expose narrow, versioned APIs to C++ and Python.
6. Use parallel CPU processing only where profiling supports it.
7. Add FFI safety rules, fuzzing and ABI compatibility tests.
### Imaging
1. DICOM, NIfTI and microscopy format adapters with metadata validation.
2. De-identification workflows and privacy controls.
3. 2D/3D/4D navigation, volume rendering and registration.
4. Segmentation, morphology and quantitative analysis.
5. AI-assisted segmentation with human correction and uncertainty.
6. Link image data to governed sample/cohort identifiers.
7. Validate against public benchmarks and expert annotations.
**Exit:** format conformance, geometry accuracy, reproducible rendering, FFI safety and image-analysis benchmark evidence.

## Programme 8 — Molecular simulation and physical modelling (Years 3–7)
1. Validate molecular preparation and simulation adapters.
2. Record force fields, solvent, ions, protonation, boundary conditions and parameters.
3. Build reproducible molecular dynamics workflows.
4. Store/stream trajectories and analyze conformational ensembles.
5. Visualize binding-site dynamics.
6. Evaluate docking/free-energy methods only when justified by data and expertise.
7. Compare simulation outputs with experimental evidence.
8. Track sampling adequacy and failure modes.
**Exit:** reproducible benchmark protocols and expert-reviewed limitations.

## Programme 9 — Disease systems biology and multi-omics (Years 3–8)
1. Build pathway, interaction and regulatory network layers.
2. Integrate genomics, epigenomics, transcriptomics, proteomics, metabolomics, lipidomics and microbiome.
3. Add single-cell and spatial multi-omics.
4. Add batch/confounder-aware statistics.
5. Support enrichment, network propagation and perturbation analysis.
6. Add causal inference with explicit assumptions and sensitivity analysis.
7. Model longitudinal progression and response heterogeneity.
8. Integrate imaging-derived phenotypes.
9. Evaluate cohort reproducibility, fairness and subgroup performance.
**Exit:** independent cohort replication and documented confounder/bias analysis.

## Programme 10 — Predictive and multimodal intelligence (Years 3–8)
1. Define task registry and model interfaces.
2. Develop modality-specific encoders before large fusion models.
3. Integrate sequence, structure, chemistry, omics, imaging and context where data justify it.
4. Add transfer/multitask learning with strict splits.
5. Add calibration, uncertainty and out-of-distribution detection.
6. Test explainability faithfulness; explanations are not causal proof.
7. Build model registry, cards and lineage.
8. Add resource-aware inference, caching and hardware acceleration.
9. Benchmark robustness, subgroup failures and compute cost.
**Exit:** task-specific external validation and explicit limitations; no universal intelligence claims.

## Programme 11 — End-user research application (after integrated scientific foundation; Years 3–7)
**Dependency:** Do not begin the polished end-user application until the cross-domain data, scientific workflows, evidence model, security/privacy controls, stable APIs and integration gates are ready. The existing local workbench is engineering/research-operator tooling, not the final patient-facing or full product application.
1. Select UI framework after accessibility and renderer prototypes.
2. Build project/workspace and local-first storage.
3. Add dataset explorer and sequence/structure/compound viewers.
4. Integrate native 3D workspace.
5. Add workflow designer with inputs, outputs, logs and provenance.
6. Add experiment tracking, notebook/script integration and artifact browser.
7. Add omics and imaging workspaces.
8. Add reproducible report builder.
9. Add permissions, encryption options, audit and safe import/export.
10. Add collaboration after identity and synchronization are secure.
**Exit:** usability/accessibility studies, stable project format and recovery tests.

## Programme 12 — Kinetics Ecosystem AI (separate repository; Years 2–7)
1. Keep AI runtime independent from scientific core.
2. Define versioned, permission-scoped Kinetics APIs; read-only by default.
3. Build evidence retrieval with citations and dates.
4. Add grounded question answering over approved project data.
5. Add workflow planning and explicit approval for consequential operations.
6. Add sandboxed computation and audit logs.
7. Evaluate hallucination, provenance, adversarial inputs and safe failures.
8. Support offline models only where licensing, hardware and measured quality permit.
9. Support hypothesis/experiment planning as assistance, never automated truth.
**Exit:** independently evaluated assistant with auditable tool use and no privilege escalation.

## Programme 13 — Treatment-response and precision-health research (Years 5–10+)
1. Define specific disease/treatment research questions—not a universal recommender.
2. Establish governed cohorts, consent and ethics.
3. Integrate pharmacogenomic, molecular, physiological and longitudinal evidence.
4. Study PK/PD, exposure, response, toxicity and heterogeneity.
5. Validate biomarkers in independent cohorts.
6. Design prospective studies with qualified clinical partners.
7. Include patient-reported outcomes and clinician workflow research.
8. Evaluate fairness, calibration, missingness and transportability.
9. Create evidence summaries only for validated, defined intended uses.
10. Establish quality/risk management, cybersecurity, usability and post-deployment monitoring as required.
**Exit:** ethics approval, prospective clinical evidence, independent validation and jurisdiction-specific authorization for each clinical use.

## Programme 14 — Android application and constrained-device experience (after stable platform APIs; Years 3–8+)
1. Stabilize mobile-safe APIs and synchronization.
2. Reuse Rust services and portable C++ components where feasible.
3. Build native Android UX and accessibility.
4. Add encrypted local storage, secure authentication and consent-aware sync.
5. Add selected 3D, image review and lightweight analysis.
6. Evaluate ONNX/mobile inference only after end-to-end feature pipeline validation.
7. Optimize thermal, battery, memory, network and offline behavior.
8. Keep heavy training and large simulations on appropriate compute.
9. Test device compatibility, security, privacy and usability.
**Exit:** stable desktop APIs, mobile threat model, device benchmarks and validated use cases.

## Programme 15 — Publication, community and sustainability (continuous)
1. Publish methods papers for independently evaluated modules.
2. Release benchmark/dataset/model cards and data-use statements.
3. Provide tutorials, APIs, notebooks and reproducible sample projects.
4. Build scientific and clinical advisory collaborations where needed.
5. Maintain contributor pathways, security disclosure and long-term maintenance.
6. Track dependency health, licensing, funding and compute sustainability.
7. Publish limitations, negative results and corrections.

## Universal gates

- **Data:** provenance, rights, validation, quality and leakage audit.
- **Software:** unit/integration tests, static analysis, security, clean install and migration.
- **Performance:** representative latency, memory, throughput and reproducible profiles.
- **Science:** baselines, suitable splits, external validation, uncertainty and subgroup analyses.
- **Imaging:** geometry, format conformance, benchmark accuracy and reader usability.
- **AI:** grounded citations, tool audit, adversarial testing and safe failure.
- **Clinical:** defined intended use, ethics, prospective validation, human factors, quality/risk controls and regulatory authorization.

## Immediate execution checklist

This checklist is the near-term queue, not a replacement for the 15-programme roadmap or the active 10-step completion programme.

1. Reconcile package, API, dependency, migration and security contracts under Step 1.
2. Acquire an authorized, licensed real Kinetics-KDB snapshot; audit source semantics and publish an immutable release.
3. Execute the pinned ESM-2 and MMseqs2 workflows on reviewed data and retain repeatability and resource evidence.
4. Run the predeclared protein-cold, scaffold-cold and double-cold model evaluations; obtain independent scientific review.
5. Complete the Python structural PDB/mmCIF reference checks while keeping the native C++ PDB parser scope explicit.
6. Complete local workbench researcher, accessibility, real-data, install/upgrade and recovery acceptance.
7. Keep remote production blocked until scientific workers, per-job isolation, tenant security and restore drills pass.
8. Expand additional scientific domains only through versioned contracts, reviewed sources, tests and domain-specific validation.
9. Build polished desktop and Android applications against stable APIs and measured hardware requirements.
10. Keep precision-health and clinical translation behind separate evidence, ethics, oversight and jurisdictional authorization gates.

## Explicit exclusions

- No autonomous diagnosis, prescribing, medication changes or treatment selection.
- No unsupported claim of clinical readiness, universal treatment capability or scientific validation.
- No patient data, secrets or restricted datasets in the public repository.
- No large model, bulk download or costly simulation without a justified research question, rights review and resource budget.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](KINETICS_MISSION.md), expanded [vision](VISION.md), and [emergency and humanitarian resilience requirements](docs/EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
