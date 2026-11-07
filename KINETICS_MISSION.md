# Kinetics — Foundational Mission and Global Ambition

**Status:** Authoritative project direction. This document governs product scope, architecture, scientific priorities and release decisions.  
**North star:** Build an open, interoperable, evidence-centred biomedical intelligence infrastructure that helps humanity understand health and disease and accelerates the discovery, evaluation and responsible delivery of more precise prevention and treatment.

## 1. The mission

Kinetics is being built as a broad, continuously expanding system for biological science, biomedical research and precision-health translation. Its purpose is to connect fragmented knowledge and data across molecular, cellular, tissue, organism, population and clinical scales—then turn those connections into reproducible analyses and carefully qualified insights.

The long-term ambition is to help researchers and qualified healthcare professionals investigate why people differ in disease risk, biology, treatment response and adverse effects; discover and validate biomarkers and therapeutic targets; compare treatment hypotheses; and develop better-informed, individualized care strategies.

Kinetics should become a platform on which many scientific disciplines, datasets, analytical methods, models, workflows and future applications can work together. It is not limited to enzyme kinetics, protein structures, genomics, a single disease, a single modality, or a single user interface.

This is an ambitious long-horizon direction, not a claim that Kinetics currently has world-leading scale, comprehensive coverage, clinical validity or treatment efficacy. The ambition must be earned through open science, real data, reproducible engineering, independent validation and responsible partnerships.

## 2. What the system is intended to connect

### Molecular and genetic sciences
- DNA, RNA, genomes, genes, transcripts, regulatory elements, variants, haplotypes, epigenetics, splicing and pharmacogenomics.
- Protein sequences, domains, structures, complexes, folding, dynamics, mutations, function and molecular interactions.
- Chemical compounds, metabolites, lipids, reactions, pathways, molecular properties, targets, binding and pharmacology.
- Enzymology, kinetics, biochemistry, molecular simulation and biophysical measurements.

### Systems and organismal biology
- Transcriptomics, proteomics, metabolomics, lipidomics, glycomics, microbiomics, metagenomics, single-cell and spatial omics.
- Cell biology, immunology, microbiology, neuroscience, physiology, endocrinology, developmental biology, pathology and systems biology.
- Organism, tissue, cell-state, environmental and longitudinal context.
- Microscopy, medical imaging, spatial data and other validated biomedical modalities.

### Medicine, health and translational evidence
- Diseases, phenotypes, symptoms, biomarkers, clinical measurements and patient-reported outcomes.
- Clinical trials, guidelines, systematic reviews, publications, real-world evidence and carefully governed clinical datasets.
- Pharmacokinetics, pharmacodynamics, drug–gene interactions, drug–drug interactions, contraindications, toxicity and treatment-response heterogeneity.
- Prevention, screening research, diagnosis-support research, treatment research, rehabilitation and longitudinal outcomes.
- Lifestyle-related evidence including nutrition, physical activity, sleep, stress, environment and behavioural context.

The domain list is intentionally extensible. New fields should be added through versioned data contracts, source adapters, evidence models and validation plans—not by forcing unlike data into one generic table.

## 3. The connected intelligence vision

Kinetics should support an auditable chain of reasoning:

**Person / cohort / research question → consented and quality-checked data → domain-specific interpretation → cross-domain biological relationships → evidence synthesis → task-specific analysis and prediction → uncertainty and safety assessment → human-reviewed research or care decision → outcome tracking and learning.**

For example, a research workflow may trace a variant to a transcript and protein consequence, examine structural and functional evidence, connect the protein to pathways and disease biology, compare pharmacological evidence, evaluate relevant clinical context, and present possible research or care considerations with citations, limitations and uncertainty.

This chain is a framework for investigation—not a promise that every molecular association predicts an individual's outcome. Causal claims, treatment effects and clinical utility require appropriate study designs and independent evidence.

## 4. Future outputs and use cases

Kinetics aims to support, as evidence and authorization permit:

1. **Research discovery:** generate and prioritize testable hypotheses, identify knowledge gaps and design experiments.
2. **Molecular interpretation:** connect genetic variation, molecular structure, function, pathways and phenotypes.
3. **Precision-health research:** study biological individuality, risk factors, biomarkers and response heterogeneity.
4. **Therapeutic research:** compare targets, compounds, mechanisms, efficacy evidence, safety signals and resistance mechanisms.
5. **Pharmacogenomic research:** summarize validated gene–drug evidence and its population and prescribing-context limitations.
6. **Clinical evidence support:** assemble traceable evidence summaries for qualified professionals within a defined and validated intended use.
7. **Lifestyle evidence support:** contextualize nutrition, movement, sleep and other lifestyle evidence without overstating genetic determinism or replacing professional care.
8. **Population and public-health research:** investigate cohort patterns, inequities, environmental context and transportability while protecting privacy.
9. **Scientific education and reproducibility:** make methods, provenance, assumptions, results and limitations inspectable.

No recommendation should be produced merely because a model can produce a score. Every high-impact output must state what evidence supports it, what is inferred, what is unknown, for whom it may apply, and what review is required.

## 5. Data and knowledge principles

- Treat the repository as the versioned home for schemas, source catalogues, manifests, ingestion code, reproducible examples, tests and documentation.
- Use SQLite as the primary embedded/local metadata and indexing database, with carefully chosen complementary formats and stores for large arrays, structures, images, raw archives and model artifacts.
- Preserve raw source records separately from normalized entities, derived features, simulations and predictions.
- Every dataset and assertion must retain source, release, retrieval date, license/access terms, identifiers, checksum, transformation lineage and attribution.
- Model evidence as typed, contextual and time/version-aware relationships; preserve disagreement, uncertainty, missingness and provenance.
- Build source adapters incrementally. A source being catalogued does not mean its data are downloaded, licensed for redistribution, normalized or validated.
- Never scrape or redistribute restricted data without permission. Respect consent, data-use agreements, privacy law and provider terms.
- Make data tiers explicit: tiny redistributable reference packs in Git; larger approved data via Git LFS or external object storage; user/private data outside public Git history; federated retrieval where bulk mirroring is not permitted.

## 6. Intelligence and scientific standards

- Use domain-specific pipelines and models before multimodal fusion. Fuse modalities only when data quality, sample linkage and scientific rationale support it.
- Distinguish observation, curated assertion, statistical association, causal hypothesis, simulation, model prediction and clinical evidence.
- Record model purpose, training/evaluation data, version, feature pipeline, license, calibration, uncertainty, applicability domain, subgroup performance and known failure modes.
- Prevent leakage across people, samples, families, sites, time, protein homology and chemical scaffolds as relevant to each task.
- Require strong baselines, external validation, reproducibility, negative-result capture and independent review.
- Evaluate bias, ancestry/population coverage, missingness, fairness, transportability and performance under distribution shift.
- Never represent model-generated explanations as causal proof.

## 7. Clinical safety, governance and human responsibility

Kinetics begins as research and scientific decision-support infrastructure. It is not currently a medical device or autonomous clinician.

It must not independently diagnose, prescribe, choose or change medication, set dosage, or direct treatment. It must not imply that a genetic result alone determines disease, drug response or lifestyle. Clinical-facing functionality must be separately scoped for a defined intended use and jurisdiction.

Before any clinical deployment, the relevant module must pass:
- ethics and privacy review, lawful data access, consent and governance;
- analytical and clinical validation on representative independent populations;
- prospective evaluation where required to establish clinical utility;
- safety, usability, cybersecurity, quality and risk-management processes;
- clinician oversight, transparent evidence, auditability and appropriate regulatory authorization;
- post-deployment monitoring, incident handling, drift detection and update controls.

When evidence is insufficient, conflicting, out of scope or unsafe, the system must abstain and explain why. Emergency and high-risk scenarios require clear escalation to qualified care.

## 8. Archive-first offline data strategy

Kinetics must support safe, bounded-memory inspection and selective querying of compressed scientific archives without requiring full extraction. Ordinary ZIP/ZIP64 is an import and packaging format; indexed, independently compressed chunks and domain-specific random-access formats are required for efficient selective reads. SQLite is the local catalogue and provenance index, while large scientific objects remain in separate content-addressed storage. Offline analysis is limited to data physically available in local or attached storage. The implementation plan is maintained in [docs/ARCHIVE_FIRST_OFFLINE_DATA_ARCHITECTURE.md](docs/ARCHIVE_FIRST_OFFLINE_DATA_ARCHITECTURE.md).

## 9. Performance, accessibility and device strategy

Kinetics must be useful on powerful research workstations and constrained devices. Small Android devices are a first-class performance constraint, not an afterthought.

- Keep the scientific core independent from any one user interface.
- Build streaming, bounded-memory, resumable and incremental data workflows.
- Use lazy loading, compact indexes, quantized or otherwise optimized inference only after validation, and cache-aware storage.
- Separate metadata from large structures, images, arrays and model weights.
- Profile CPU, RAM, storage, battery, network and thermal behaviour on representative low-end Android hardware.
- Allow heavy training, large simulations and bulk processing to run on suitable remote or workstation compute, with explicit consent and secure transfer.
- Build the complete platform foundation and stable APIs before investing in a polished end-user application. Then build desktop and Android experiences against those stable contracts.

## 10. Build order and programme discipline

The user-directed sequence is binding:

1. Establish the mission, governance, architecture, data rights and cross-domain contracts.
2. Integrate the scientific data foundation, source registry, ingestion, normalization, provenance, search, storage and update mechanisms across the planned domains.
3. Implement and connect scientific analysis capabilities, validation pipelines, model infrastructure and reproducible workflows.
4. Complete security, privacy, performance, reliability, deployment and recovery foundations.
5. Only then build the polished end-user application and domain-specific experiences.
6. After the integrated system exists, conduct comprehensive software testing, scientific benchmarking, data validation, model training/evaluation, device testing, researcher usability studies and clinical validation programmes as appropriate.

Testing and security checks still run continuously during development; the sequence means comprehensive system-level acceptance and training happen after the integrated foundation is assembled, not that code is left untested.

## 11. Definition of success

Success is not measured by the number of source names in a catalogue, lines of code, model parameters or unsupported claims of being the world's largest. It is measured by:
- breadth and quality of lawfully accessible scientific coverage;
- depth and correctness of cross-domain identity and evidence links;
- reproducible ingestion and analysis at meaningful scale;
- independently benchmarked scientific performance and honest uncertainty;
- equitable performance and transparent limitations;
- secure, private and accessible operation across device classes;
- useful collaboration with researchers, clinicians, patients and institutions;
- validated improvements in research efficiency and, only where proven, clinical outcomes.

The phrase "world's biggest system" expresses the scale of the ambition. Kinetics should strive to become one of the most comprehensive, connected and useful platforms in its field, while earning every scientific and clinical claim through evidence.

## 12. Mandatory decision filter

Every future feature, dependency, dataset, model, UI, infrastructure change and roadmap item must answer:

1. Which part of the Kinetics mission does it advance?
2. Which scientific domain(s) and entities does it support?
3. What data rights, provenance and privacy requirements apply?
4. How does it connect to the shared evidence model without erasing domain semantics?
5. How will correctness, uncertainty, performance and safety be tested?
6. Does it preserve the foundation-first sequence and constrained-device strategy?
7. What is implemented, what is only planned, and what evidence proves completion?

If a proposal does not advance the mission or protect the system's integrity, it should not be added merely for novelty.

---

**Permanent project reminder:** Kinetics is a long-horizon, cross-disciplinary biomedical and precision-health research platform. Build the complete scientific foundation first; build the application afterwards; validate everything before any clinical use.
