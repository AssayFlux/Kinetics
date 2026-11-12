# Changelog

All notable project changes will be recorded here.

## Unreleased
- Started Track G G0–G7 engineering controls: canonical threat model and UI supplement, security verification matrix, source-level data-flow inventory, role/cadence model, requirements traceability, CAPA template, 130-capability claims matrix, dependency decision register, publication integrity and operational procedures.
- Added CI structural checks for governance registers and reproducible capability-claims matrix; Android CI now archives resolved Gradle/Cargo dependency reports and cached Maven artifact hashes. These are engineering controls only; independent reviews and operating exercises remain open.
- Reworked the repository README into a concise project landing page with track status, scoped engineering-gate percentages, collapsible track details, navigation badges and the supplied animated brand/Kinetics logos.
- Consolidated legacy `Assets/` artwork into the lowercase `assets/` tree while preserving original Git blobs; corrected the JPEG extension of the former `Kinetics.png` file and updated active asset documentation.
- Updated the owner-approved sequential track order to **R → S → I → P → G → U** (D-023); Track U now follows Track G, with its pre-existing partial implementation retained and further work gated on G's two-step exit.
- Established the owner-approved direction baseline and R0 repository foundation.
- Added bounded Android SDF/MOL graph preview and host RDKit descriptor adapter; chemistry output remains exploratory.
- Added optional AutoDock Vina 1.2.7 host docking runner and a disabled-by-default authenticated Node worker.
- Added optional OpenMM 8.6.1 CPU replica runner with bounded DCD output; no biomolecular force field is bundled.
- Added PK/PD reference models, a SciPy ODE comparison, scaffold-aware ADMET evaluation metrics/applicability tools, metadata-only source inventory and synthetic aggregate cohort/effect simulations.
- These additions are research engineering foundations, not independently validated scientific or clinical capabilities.
