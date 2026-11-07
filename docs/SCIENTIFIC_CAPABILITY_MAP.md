# Kinetics scientific capability map

**Purpose:** one capability-level map connecting the Kinetics mission, scientific scope, implementation evidence and engineering sequence. This is the functional capability register; it is not a promise that every listed capability exists today.

**Authority:** [KINETICS_MISSION.md](../KINETICS_MISSION.md) defines why and what Kinetics must protect. [VISION.md](../VISION.md) describes the long-range product ambition. [ROADMAP.md](../ROADMAP.md) defines long-range programmes. [KINETICS_10_STEP_COMPLETION_PROGRAMME.md](KINETICS_10_STEP_COMPLETION_PROGRAMME.md) governs the active engineering sequence. [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) is the current repository evidence snapshot. The [160-domain acquisition register](SCIENCE_DOMAIN_CATALOGUE_100.md) is a source-discovery taxonomy, not a capability checklist.

## 1. Platform-level capabilities

| Capability | Intended responsibility | Repository evidence today |
|---|---|---|
| Scientific knowledge archive | Acquire permitted books, papers and reference resources; preserve originals, licenses, checksums, metadata and provenance; extract, tokenize, index and retrieve source-grounded content | Ingestion, extraction, tokenization, SQLite FTS5 retrieval and release synchronization foundations exist. No 10,000-book + 10,000-paper completed corpus is claimed. |
| Scientific data foundation | Canonical identifiers, domain schemas, source adapters, normalization, quality checks, versioning, lineage and immutable releases | Kinetic observation, identity, curation, provenance, release and SQLite foundations exist; cross-domain contracts are partial. |
| Cross-domain knowledge integration | Link genes, variants, transcripts, proteins, structures, compounds, reactions, pathways, phenotypes, diseases, assays, samples, cohorts and publications with typed evidence | Planned architecture; no complete cross-domain knowledge graph is implemented. |
| Scientific workflow and compute | Reproducible workflows, jobs, bounded resources, cancellation, checkpoints, artifacts, local/remote execution and audit | Local workbench and Rust service foundations exist; remote deployment and scientific worker execution remain unaccepted. |
| Scientific visualization | Data-derived, interactive, accessible views with units, provenance and export | Browser workbench and 3Dmol.js structure viewer exist; native C++ renderer is currently a diagnostic XY preview, not a full GPU 3D engine. |
| Research application | Unified researcher workspaces over stable scientific APIs, with desktop and Android experiences | Local web workbench and four blank responsive HTML/CSS shells exist; no native desktop apps or Android APK are claimed. |
| Offline and humanitarian resilience | Signed, versioned, selective offline packs; low-memory access; removable-media distribution; verified emergency reference content | Requirements and archive-first design are documented; end-to-end emergency packs and field validation remain planned. |
| Responsible intelligence | Task-specific models and retrieval with citations, uncertainty, applicability limits, human review and abstention | Kinetic model foundations and local source-grounded retrieval exist; no universal biomedical intelligence or clinical decision engine is claimed. |

## 2. Scientific capability areas

The following capability areas organize the scientific functions discussed in the Kinetics plan. Each area must have its own data contracts, source/licensing review, tests, domain-specific benchmarks and release boundary. A capability may be exposed through a common workbench, but its scientific semantics must remain domain-owned.

### A. Genomics and genetics
- DNA sequence import and validation: FASTA/FASTQ, quality scores, reference genome/build and sample metadata.
- Read quality control, trimming, alignment/mapping, assembly and contamination checks.
- Gene/transcript annotation, coding regions, regulatory elements, ORFs and repeat analysis.
- Variant normalization and annotation: SNPs, indels, structural variants, CNVs, haplotypes and population frequencies.
- Reference-aware comparisons, pangenomes, inheritance and genotype–phenotype research.
- Primer/PCR design, restriction analysis, plasmids, cloning and CRISPR guide assessment with explicit off-target and validation limits.

**Current status:** basic sequence/FASTA and BioPython foundations only; no complete NGS, variant-calling or clinical variant-interpretation pipeline.

### B. Transcriptomics and cellular biology
- Bulk RNA-seq, single-cell RNA-seq and spatial transcriptomics quality control and quantification.
- Differential expression, splicing, isoforms, non-coding RNA and regulatory analysis.
- Cell-type/state annotation, batch/confounder handling, pseudotime and trajectory analysis.
- Co-expression, gene-regulatory networks and perturbation analysis.
- Tissue, sample, timepoint, platform and cohort-aware metadata.

**Current status:** planned; no complete RNA-seq or single-cell analysis pipeline is established.

### C. Proteomics
- Protein identification, sequence records, isoforms, domains, motifs and physicochemical properties.
- Localization, signal peptides, transmembrane regions, PTMs and protein abundance.
- Mass-spectrometry data workflows, peptide/protein inference and quantitative comparisons.
- Protein–protein interactions, complex composition, stability and homology.
- Evidence-linked functional annotation with experimental/predicted distinctions.

**Current status:** protein sequence/representation and versioned proteomics/structure contracts exist; broad mass-spectrometry and quantitative proteomics workflows remain planned.

### D. Structural biology
- PDB/mmCIF parsing, chain/residue/atom identity, alternate conformations and model/assembly context.
- Explicit sequence-to-structure mapping, missing-residue reporting and coordinate integrity.
- Secondary structure, solvent-accessible surface area, contacts, geometry, ligand pockets and interaction descriptors.
- Structural alignment, RMSD, contact maps, experimental-versus-predicted structure comparison and quality metadata.
- Future folding/prediction, docking and molecular dynamics only through validated, licensed and reproducible adapters.

**Current status:** Python PDB/mmCIF coordinate adapters, selected Biopython analyses and a browser structure viewer are present with fixture tests. Native C++ parser is PDB-only; no full GPU renderer, docking or executed MD is claimed.

### E. Sequence bioinformatics and comparative analysis
- Pairwise/global/local alignment, multiple-sequence alignment and sequence similarity.
- BLAST, HMMER, MMseqs2 and profile/domain search adapters.
- Motif discovery, conserved regions, sequence logos, orthology/paralogy and clustering.
- Sequence-to-structure mapping and reproducible identity/coverage thresholds.

**Current status:** protein pairwise alignment and an MMseqs2 clustering wrapper are present; full search services and broad MSA/profile workflows remain incomplete or unvalidated.

### F. Phylogenetics and evolution
- Multiple-sequence alignment preparation, phylogenetic tree construction and visualization.
- Evolutionary distances, substitution models, bootstrap support and tree comparison.
- Molecular-clock, ancestral-state and selection analyses with explicit assumptions.
- Population genetics, diversity, haplotypes, dN/dS and selection signals.

**Current status:** planned; no validated phylogenetic workflow is established.

### G. Molecular biology and genetic engineering
- DNA/RNA/protein transformations, translation, genetic-code and sequence-feature operations.
- Gene regulation, transcription-factor binding, chromatin and epigenetic evidence.
- Primer design, PCR planning, restriction maps, plasmid and construct annotation.
- CRISPR guide design and off-target analysis as research utilities, not assurances of experimental safety.

**Current status:** basic sequence utilities are available through the BioPython foundation; integrated construct-design workflows remain planned.

### H. Chemistry and cheminformatics
- SMILES, InChI, SDF/MOL and structure validation with stereochemistry preservation.
- Molecular descriptors, fingerprints, similarity, substructure and scaffold analysis.
- Reaction representation, compound identity, conformers and property calculations.
- Future docking, virtual screening, ADMET/toxicity, quantum chemistry and lead optimization with endpoint-specific evidence.

**Current status:** RDKit-based identity, Morgan fingerprints, scaffold annotations and molecular graph features are present in the kinetics workflow; docking, quantum chemistry and broad drug-discovery workflows are not established.

### I. Enzyme kinetics and biochemistry
- Km, kcat and other explicitly typed kinetic/biochemical endpoints.
- Michaelis–Menten and linearized plotting methods, nonlinear fitting, inhibition models and allostery.
- Assay-aware context: pH, temperature, organism, construct, substrate, cofactors and method.
- Unit normalization, duplicate/conflict review, uncertainty, applicability and leakage-resistant evaluation.
- Reaction, pathway, enzyme-family and catalytic-mechanism analysis.

**Current status:** the strongest implemented scientific workstream: canonical kinetic observations, curation, feature/model software, evaluation utilities and workbench commands exist. Real-data scientific validation and independent reproduction remain open.

### J. Systems biology and pathways
- Pathway and reaction networks, gene/protein relationships and regulatory networks.
- Network topology, centrality, enrichment and perturbation analysis.
- Metabolic reconstruction, gene–protein–reaction associations and flux-balance analysis.
- ODE/stochastic models and multiscale simulations with parameter provenance.

**Current status:** planned; no integrated systems-biology engine is established.

### K. Multi-omics
- Genomics, epigenomics, transcriptomics, proteomics, metabolomics, lipidomics and microbiome data.
- Single-cell and spatial multi-omics integration.
- Cross-omics correlation, latent factors, clustering, dimensionality reduction and signatures.
- Batch/confounder-aware analysis and sample/cohort identity controls.

**Current status:** architecture ambition only; integrated multi-omics workflows are not implemented.

### L. Microbiology, virology and metagenomics
- Bacterial, viral, fungal and parasitic sequence/reference workflows.
- Taxonomic classification, metagenomic assembly and functional profiling.
- Microbiome abundance, alpha/beta diversity and host–microbe associations.
- Antimicrobial-resistance and virulence evidence with source and population context.

**Current status:** planned; no complete metagenomics or microbiome workflow is established.

### M. Immunology and immunoinformatics
- Immune-cell, cytokine and immune-pathway evidence.
- Antigen and B/T-cell epitope analysis, MHC/HLA context and antibody sequences.
- TCR/BCR repertoire analysis and immune-response datasets.
- Population-specific limitations, assay evidence and validation controls.

**Current status:** planned; no validated immunoinformatics pipeline is established.

### N. Biostatistics and evidence synthesis
- Descriptive/inferential statistics, regression, Bayesian methods and survival/time-series analysis.
- Missingness, outlier and multiple-testing controls; power/sample-size planning.
- PCA, clustering, multivariate analysis, bootstrap and uncertainty reporting.
- Systematic-review, meta-analysis and evidence-grading workflows.

**Current status:** selected regression, bootstrap, calibration and applicability utilities exist for the current kinetics research; broad biostatistics and evidence-synthesis modules remain planned.

### O. Biomedical imaging and bioengineering
- DICOM, NIfTI, microscopy and OME-format ingestion with geometry and metadata validation.
- CT/MRI/PET/ultrasound and microscopy visualization, registration and segmentation.
- Image-derived phenotypes, quantitative morphology and spatial measurements.
- Biomedical signals, sensors, devices, robotics, prosthetics and biomaterials research.

**Current status:** long-term roadmap scope; no full medical-imaging or bioengineering suite is established.

### P. Pharmacology, toxicology and translational research
- Drug-target, mechanism, pharmacokinetic/pharmacodynamic and dose-response evidence.
- Drug–gene/drug–drug interactions, resistance, toxicity and safety signals.
- Biomarker and treatment-response research with cohort, assay and population context.
- Clinical-trial and guideline evidence synthesis under governance.

**Current status:** long-term research scope only. No treatment recommendations, autonomous diagnosis or prescribing are implemented or authorized.

### Q. Scientific visualization and reporting
- Protein/structure viewers, sequence/genome browsers, alignments and phylogenies.
- Chemical structures, molecular interactions, networks and pathway diagrams.
- Omics heatmaps, volcano/PCA plots, kinetics curves and publication figures.
- Reproducible dashboards and reports linked to source artifacts, units, uncertainty and methods.

**Current status:** selected kinetics reporting, browser workbench and structure-viewer foundations exist; broad visualization coverage remains planned.

### R. Scientific infrastructure and interoperability
- Standard formats, schema/version management, identifiers, provenance and licensing.
- Reproducible pipelines, artifact registries, workflow orchestration, queues and resource budgets.
- Local-first and optional remote compute, CPU/GPU scheduling, indexing, APIs and secure synchronization.
- Project/workspace history, experiment tracking, reports, citations, access control and audit.
- Offline packs, backups, restore, integrity verification and accessibility.

**Current status:** substantial local Python/SQLite/knowledge-ingestion foundations and a Rust/AWS deployment candidate exist; production deployment, complete cross-domain graph, remote scientific execution and emergency field acceptance remain open.

## 3. Implementation status vocabulary

Use these labels consistently in code, UI, documentation and release notes:

- **Implemented:** the described behavior exists in code. Name the exact module or command.
- **Fixture-tested:** automated tests cover synthetic or checked-in fixtures; this is software evidence only.
- **CI-verified:** a named CI run passed for a specific commit and test scope.
- **Real-data executed:** the workflow ran on a reviewed, licensed real dataset; retain manifests and outputs.
- **Scientifically validated:** appropriate independent/reference evaluation supports the stated scientific claim.
- **Production deployed:** a live environment exists and operational evidence is recorded.
- **Clinically validated/authorized:** only for a defined intended use with required clinical, governance and jurisdictional evidence.
- **Planned:** design or roadmap exists without implementation evidence.
- **Blocked:** a named prerequisite or approval prevents progress.

Never collapse these levels into a single green check or a generic "supported" label.

## 4. Dependency-aware implementation sequence

1. **Shared foundation:** mission/governance, data rights, identity, provenance, source registry, domain contracts, immutable artifacts, storage, indexing, retrieval, APIs and workflow execution.
2. **Knowledge archive scale-up:** acquire, verify, extract, tokenize, index and make searchable at least 10,000 books and 10,000 research papers. This is a minimum milestone, not the final corpus ceiling.
3. **Current scientific core:** complete and validate kinetics, protein/chemical representations, sequence/structure foundations and the local researcher workbench.
4. **First domain expansion:** genomics/genetics and transcriptomics, each with reference/version-aware formats, domain contracts and independent benchmarks.
5. **Proteomics and structural depth:** complete protein/structure mapping, quality, interaction and mass-spectrometry workflows.
6. **Chemistry and molecular biology:** broaden reaction, compound, genetic-engineering and therapeutic research adapters.
7. **Living systems:** microbiology, metagenomics, immunology, phylogenetics and systems biology.
8. **Multi-omics and imaging:** cross-modal linkage only when sample identity, cohort context and validation support it.
9. **Advanced modelling:** domain-specific ML, simulation, uncertainty and multimodal methods after strong baselines and external evaluation.
10. **Integrated application:** polished Windows, macOS, Linux and Android experiences after stable APIs and scientific workflows; preserve offline-first operation and low-memory Android performance.
11. **Operational and clinical gates:** security, deployment, accessibility, recovery and researcher acceptance; clinical translation remains a separate authorized programme.

This sequence is a dependency guide. The active engineering step and long-range programme references remain the authoritative schedules.

## 5. Corpus scale milestone and counting rules

The first large-scale knowledge-archive milestone is **at least 10,000 books and 10,000 research papers**. It is a minimum acceptance target, not a claim of current holdings and not a ceiling on future growth.

Report books and papers separately. For each resource, track its stage independently: discovered, rights-reviewed, downloaded, checksum-verified, extracted, normalized, tokenized, indexed and retrievable. A resource counts as **processed** only when the required extraction/normalization/tokenization steps succeeded; it counts as **searchable** only when its content and provenance are present in the active index. Do not count failed, duplicate, inaccessible, restricted or merely discovered records as processed/searchable. Preserve source license and access conditions; a source's public availability does not automatically permit redistribution.

Keep raw files and derived artifacts outside ordinary Git blobs. Use manifests and content hashes to publish truthful cumulative counts, with per-release and current-index figures clearly distinguished. The dashboard must never substitute planned targets or transfer ceilings for verified corpus counts.

## 6. Mapping to the existing roadmap

- Governance, architecture and shared foundations: Roadmap Programmes 0–1.
- Data, books/papers archive, source registry, provenance and knowledge integration: Programme 2.
- Genomics/transcriptomics: Programme 3.
- Proteomics/structure: Programme 4.
- Enzyme kinetics/biochemistry: Programme 5.
- Chemistry/therapeutic discovery: Programme 6.
- Native rendering, imaging and Rust services: Programme 7.
- Molecular simulation: Programme 8.
- Systems biology and multi-omics: Programme 9.
- Predictive intelligence: Programme 10.
- Research application and platform UI: Programme 11; Ecosystem AI remains separate under Programme 12.
- Precision-health research and constrained Android: Programmes 13–14.
- Publication and sustainability: Programme 15.

## 7. Decision rule

Do not add a capability to the active build queue solely because it appears in this map or the 160-domain acquisition taxonomy. Before implementation, define the research question, input/output contracts, authoritative sources and rights, validation dataset/protocol, compute budget, privacy/safety boundary, dependencies and measurable acceptance criteria. Implement the narrowest useful vertical slice, retain provenance and tests, then update [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) with evidence.
