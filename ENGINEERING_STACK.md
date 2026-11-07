# Kinetics — Engineering stack

> **Mission authority:** This document is governed by [KINETICS_MISSION.md](KINETICS_MISSION.md). Kinetics is a cross-disciplinary biomedical and precision-health research platform—not only an enzyme-kinetics project. All domains, datasets, models and applications must align with the mission, preserve provenance and clinical safety, and follow the foundation-first build order. Small Android devices are a first-class performance target.

## Responsibility map

| Domain | Language | Role |
|---|---|---|
| Scientific modules | Python | Bioinformatics, chemistry, kinetics, omics, pharmacology, ML |
| Workflow/API layer | Python + Rust | Typed workflows, orchestration, queues and resource governance |
| 3D visualization | C++ | Renderer, scene graph, GPU resources, molecular/volume visualization |
| Image/geometry processing | C++ + selected Rust | Image transforms, meshes, spatial and performance-critical analysis |
| Systems services | Rust | Secure file/project boundaries, concurrency, integrity and streaming |
| Desktop UI | To be selected | Accessibility and native renderer integration |
| Android | Kotlin + portable C++/Rust | Mobile UI, secure state, selected native components |

## Python candidates
BioPython, pysam, RDKit, NumPy, SciPy, pandas/Polars, PyArrow, xarray, PyTorch, scikit-learn, XGBoost, FastAPI, Pydantic, pytest, Hypothesis, Ruff and mypy. Select per module; pin supported versions and avoid hidden model downloads.

## C++ candidates
Prototype VTK (scientific visualization), ITK (medical imaging), Qt or equivalent desktop integration, OpenGL/Vulkan or a portability layer, CMake/Ninja, clang-format, clang-tidy, sanitizers and a maintained test framework. Capabilities: molecular atoms/bonds/ribbons/surfaces, meshes, volume rendering, slice views, registration, segmentation overlays, measurements, GPU budgets and deterministic export.

## Rust candidates
Serde, Tokio only for truly async services, Rayon when profiling justifies parallelism, tracing, PyO3/maturin, cargo fmt/clippy/test/audit and fuzzing. Use Rust for bounded jobs, cancellation, safe file access, integrity and resource accounting. Minimize and audit unsafe code.

## Contract policy
1. Define schemas before bindings.
2. Version every API and serialized artifact.
3. Specify units, coordinate systems, shapes, dtypes and null semantics.
4. Document memory ownership and thread safety.
5. Prefer process isolation across trust/failure boundaries.
6. Add FFI only for measured performance or UX benefit.
7. Test cross-language round trips, cancellation and error paths.
8. Never expose unrestricted filesystem, shell or network access to plugins/AI.

## Storage policy
SQLite for metadata, not tensors/images. PostgreSQL for multi-user transactions when needed. Parquet/Arrow for tables; Zarr/HDF5 for chunked arrays; canonical domain formats for source data; object storage for large artifacts. Each object has stable ID, schema version, hash, provenance, license/access class and retention policy.

## Performance policy
Profile before optimizing; cache deterministic embeddings/transforms; maintain CPU baselines and optional GPU paths; stream large volumes; use chunking/memory maps; budget RAM/VRAM/disk/latency/throughput/battery/thermal behavior. Mobile inference requires the complete validated feature pipeline, not merely exported model weights.

## Quality gates
Python: typing, lint, tests, reproducible environments, dependency audits.
C++: sanitizers, static analysis, parser fuzzing, CPU/GPU parity and rendering benchmarks.
Rust: clippy, tests, fuzzing, dependency audits, unsafe-code review and concurrency stress.
Cross-stack: API compatibility, data round trips, crash recovery, reproducible builds and security review.
