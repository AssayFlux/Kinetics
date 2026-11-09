# Architecture — R0 baseline

This records intended boundaries, not an implemented runtime.

- Android/Kotlin/Jetpack Compose: presentation shell only; no scientific calculations.
- Python: scientific orchestration and reference-level workflows.
- Rust: parsers/QC and performance-sensitive utilities only where measured need justifies them.
- C++17: numerical kernels and JNI boundaries only where feasibility and benchmarks justify them.
- C: upstream C engine cross-compilation only.
- TypeScript/JavaScript: offline WebView visualisation only.
- SQLite: local metadata/provenance store.
- Optional remote node: authenticated, encrypted, user-configured compute; not present in R0.

The registry links tools to engines, data packs and domains. Empty collections are deliberate until concrete capabilities and evidence exist. No new language, engine tier, runtime executable download, clinical feature or network telemetry is introduced. Android implementation choices remain subject to R1 feasibility and owner gates.


## Owner-directed engineering and integration standard

The detailed target language ownership, interface contracts, boundary ABI rules, workflow, testing obligations and project profile are maintained in [ENGINEERING_INTEGRATION_STANDARD.md](ENGINEERING_INTEGRATION_STANDARD.md). The cross-component JSON envelope contract is [engine-envelope-v1.schema.json](../api/engine-envelope-v1.schema.json).

This standard supplements this architecture baseline. It does not imply that target components or interfaces are already implemented. See the status and migration notes in the standard before changing any boundary.
