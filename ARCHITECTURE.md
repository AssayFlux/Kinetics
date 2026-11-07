# Kinetics — System architecture

## Objective
A modular, platform-first biomedical research and precision-health research platform with independently versioned scientific domains, a shared evidence/data foundation and a native visualization engine. Scientific modules must remain usable from Python/CLI without launching the desktop application.

## Layers
1. Experience: CLI and researcher workflows during foundation development; polished desktop and Android applications after the scientific platform and stable APIs are ready. Low-memory Android performance is a first-class architectural constraint from the beginning.
2. Application: projects, workflows, access control, jobs and reports.
3. Scientific domains: genomics, transcriptomics, proteomics, structure, kinetics, chemistry, pharmacology, imaging, systems biology and multi-omics.
4. Intelligence: task-specific ML, multimodal models, uncertainty, retrieval and model registry.
5. Evidence/data: canonical entities, provenance, datasets, experiments and artifacts.
6. Native systems: C++ visualization/image engine and Rust services.
7. Infrastructure: local-first storage, optional approved compute, packaging, observability and security.

## Language ownership

### Python
Scientific methods, bioinformatics, cheminformatics, data ingestion, ML, experiment tracking, workflow definitions, APIs and reporting. Python modules expose typed inputs/outputs and do not require the desktop renderer.

### C++
Native 3D and image engine: scene graph, camera, GPU resources, molecular representations, meshes, volume rendering, image processing and geometry. Evaluate maintained options such as VTK/ITK and graphics APIs through prototypes before choosing dependencies.

### Rust
Secure project/file services, concurrency, bounded jobs, cancellation, streaming, integrity checks, resource limits and selected profiled CPU utilities. Keep services small and auditable.

### Interoperability
Use versioned schemas and APIs, narrow C ABI boundaries, PyO3/maturin for selected Rust bindings and pybind11/C ABI for C++ only where justified. Specify ownership, lifetimes, threading, cancellation, errors and ABI versions. Never pass unmanaged pointers across boundaries.

## Data architecture
- SQLite for local metadata, indexes, project records and workflow state.
- PostgreSQL when governed multi-user transactions are needed.
- Parquet/Arrow for tabular scientific data.
- NumPy/memory maps for dense numerical arrays.
- HDF5/Zarr for chunked arrays and imaging.
- Standard domain formats: DICOM, NIfTI, OME-TIFF, PDB/mmCIF, FASTA/GenBank, VCF, BAM/CRAM and others as appropriate.
- Object storage for large approved artifacts.
- Safetensors/framework formats for model weights with full lineage.

Raw source data remain immutable. Every artifact records schema, source, version, hash, license/access class, transformation and producing software.

## Evidence model
Entities include biological (gene, transcript, variant, protein, organism, cell, tissue), molecular (compound, complex, reaction, pathway), biomedical (disease, phenotype, sample, cohort, image), evidence (publication, database record, assay, study, guideline) and computational (dataset, workflow, model, prediction, simulation, report). Relationships carry source, context, evidence class, quality and population applicability.

## Workflow model
Each step declares inputs/outputs, configuration, random seeds, environment, resource limits, checkpoints, cancellation, logs, failure states, output hashes, lineage and permission scope. No silent network downloads, shell execution or private-data transmission.

## Visualization pipeline
Format validation → metadata/coordinate normalization → CPU/GPU processing → scene graph → rendering → interaction/measurement → export. Coordinate systems, units, voxel spacing, transforms and provenance are explicit. Rendering never modifies source images.

## AI boundary
Models are task-specific and registered with intended use, training data provenance, evaluation, calibration, subgroup performance, known failure modes and license. Kinetics Ecosystem is a separate project using permission-scoped APIs; read-only by default and user approval for consequential operations.

## Security and deployment
Use least privilege, encryption, secrets management, signed updates, audit logs, backup/recovery and threat modelling. Sensitive genetic/health data require lawful basis, consent where applicable, minimization, retention and deletion controls. Deployment profiles: local desktop, institutional server, approved cloud/HPC, later Android, and a separate clinical environment only after authorization.
