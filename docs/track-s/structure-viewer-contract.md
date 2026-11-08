# Track S1 — Offline structure viewer contract

**Status:** S1 preparation started in parallel with R1–R10 on owner instruction (2026-11-08). This is not a completed viewer.

## Scope and non-goals

S1 will provide offline loading and rendering of user-selected PDB/mmCIF structures, with a reproducible preparation record. The initial viewer must display coordinates and annotations without inventing bonds, protonation, secondary structure, confidence, or biological conclusions. R5 scientific analysis remains separately validated and is not replaced by visualization.

## Current implementation

- `python/kinetics/structure_view.py` builds deterministic `kinetics.structure-view.v1` payloads.
- Payloads use Angstrom coordinates, stable field names, a configurable atom-count ceiling, finite-coordinate checks, duplicate-serial rejection, bounded annotations, and explicit limitations.
- `tests/test_structure_view.py` covers serialization determinism, empty/unsupported inputs, atom limits, duplicate serials, non-finite coordinates, and schema rejection.
- Capability `structure.viewer_payload` is registered as implemented source with evidence_level none. This is a preparation utility, not a renderer or validated scientific result.

## Rendering and security contract

1. The viewer bundle must be local and version-pinned. No remote scripts, CDN, telemetry, or network fallback.
2. Candidate Mol* is MIT-licensed, but the exact release archive, package lock, transitive dependencies, worker assets, fonts, and notices must be audited before vendoring. No candidate is approved for redistribution yet.
3. WebView file/content access, mixed content, universal file URL access, and debugging are disabled in release configuration unless a documented test demonstrates a narrowly required exception.
4. The JavaScript bridge is allow-listed and typed. It must not expose arbitrary evaluation, filesystem access, Android context, intents, or generic method dispatch.
5. Only app-owned local assets and validated serialized payloads may be loaded. Enforce payload byte and atom limits before WebView handoff.
6. Persist a preparation log containing input SHA-256, source format, parser/version, atom count, dropped-record counts (if any), coordinate unit, payload schema, viewer version, and limitations. Never log raw sequence/genomic or patient-associated identifiers.
7. Rendering failure must preserve the original input and preparation record, show a user-safe error, and never silently modify coordinates.
8. Exported screenshots/figures must identify the source hash, viewer version, representation, and display settings; they are visualization artifacts, not evidence of scientific validation.

## Exit evidence still required

- Exact viewer version and completed license/transitive dependency review.
- Reproducible offline asset bundle and integrity hashes.
- Typed bridge implementation plus positive/negative bridge tests.
- PDB/mmCIF fixture screenshots and load/selection/colour/save-state tests.
- WebView hardening tests, offline network-denial test, and large-structure memory/latency benchmark.
- Device verification on a defined low-end arm64 device and adaptive UI matrix.
