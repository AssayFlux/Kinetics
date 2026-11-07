# Kinetics

**Kinetics is an Android-first scientific toolbox for biological scientists.** The target product connects scientific tools to computational engines and curated, versioned data packs. It is not intended to be a books, papers, literature-search, or bulk-document archive.

## Current repository status

This repository is transitioning from an existing Python scientific research platform with Rust infrastructure and C++ structure support toward the Android-first architecture. The Android application, on-device execution matrix, and device validation are **not yet implemented or verified**.

| Area | Status | Device status |
|---|---|---|
| Existing Python research/curation code | Existing; individual tools require registry mapping and validation | Not verified on Android |
| Rust infrastructure | Existing; not yet an Android FFI engine | Not verified |
| C++ molecular structure foundation | Existing; native build tests exist | Not verified on Android |
| Android Kotlin/Compose shell | Planned | No |
| 160-domain catalogue | Preserved; registry conversion started | Not applicable |
| Enzyme kinetics fitting suite | Planned pending source and benchmark audit | No |
| Remote Compute Node | Planned; existing infrastructure requires contract review | Remote only when explicitly configured |

A passing software test is not scientific validation. No capability is advertised as scientifically validated or device-verified unless its registry record and benchmark/device evidence support that status.

## Product principles

- Offline-first for Tier A tools; no telemetry by default.
- No user data leaves the device unless the user explicitly configures a Remote Compute Node.
- Runtime downloads are data packs only, never executable engines.
- Every capability has a status (planned, implemented, validated) and runs_on_device flag.
- Results carry provenance: input hash, parameters, tool/engine versions and timestamp.
- Preserve all 160 catalogue domains; catalogue membership does not imply implementation.
- No clinical decision use. Research tools require domain-appropriate validation.

## Target architecture

- android/: thin Kotlin + Jetpack Compose shell, permissions, SAF file picker and background jobs; no science logic.
- python/kinetics/: Python scientific logic and desktop/remote test surface.
- rust/: parsers, QC and performance-critical routines with FFI.
- cpp/: native numerical/structure kernels.
- engines/: pinned engine manifests and build recipes; no committed binaries.
- datapacks/: license-checked, versioned manifests; no bulk data committed.
- domains/: one YAML definition per catalogue domain.
- capabilities/registry.yaml: tool → engine → data-pack → domain mappings.
- remote-node/: optional authenticated compute endpoint for Tier C engines.

## Development

Existing Python, Rust, C++, browser-workbench and Terraform CI remains in place while migration is staged. The domain registry checker is run in CI. See AUDIT.md, docs/android-feasibility.md, and docs/phase-0-plan.md.

## Scientific-use disclaimer

Research use only. Outputs are not intended for diagnosis, treatment selection, clinical decisions, or other regulated use. Users are responsible for evaluating methods, assumptions, input quality, uncertainty and suitability for their research.
