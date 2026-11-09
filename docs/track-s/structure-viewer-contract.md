# Track S1 — Offline structure viewer contract

**Status (2026-11-09):** A dependency-free offline coordinate-renderer prototype and payload contract tests are now present. Android WebView/file-picker integration, device validation and benchmark evidence remain open.

## Scope and non-goals

S1 provides offline display of validated user-selected PDB/mmCIF coordinate payloads, with reproducible preparation provenance. It does not invent bonds, protonation, secondary structure, confidence, quality grades or biological conclusions.

## Current implementation

- `python/kinetics/structure_view.py` builds deterministic `kinetics.structure-view.v1` payloads with Angstrom coordinates, finite-coordinate checks, unique atom serials, bounded annotations, atom ceiling (200,000), serialized-byte ceiling (32 MiB) and explicit limitations.
- `web/viewers/src/structure-viewer.html`, `structure-viewer.css` and `structure-viewer.js` implement a dependency-free Canvas 2D coordinate renderer. It supports drag rotation, wheel zoom, element/chain colouring, nearest-atom selection and an accessible first-500-atom list.
- The viewer validates payload schema, atom count, unique serials, finite coordinates, normalized element labels and the 32 MiB ceiling before rendering. Bounds calculation is iterative and does not spread large coordinate arrays onto the JavaScript call stack.
- The HTML Content Security Policy denies network connections and all default resources; only local script/style assets are permitted. There is no generic JavaScript/native bridge, filesystem access, eval hook, remote loader or telemetry.
- `tests/test_structure_viewer_assets.py` checks local asset references, network-denial policy, bounded payload constants, bridge/eval absence and accessible selection surface.
- The viewer is an original Kinetics implementation with no third-party runtime dependency; therefore there is no external viewer runtime license to approve.

## Remaining integration and exit evidence

1. Bundle the viewer into Android app assets and load through a hardened local asset origin (prefer AndroidX WebViewAssetLoader).
2. Add typed, minimal payload handoff from the Android parser; no generic bridge or arbitrary JS execution.
3. Connect SAF file selection to bounded PDB/mmCIF parsing, canonical Python payload validation and preparation-record persistence.
4. Add parser-to-viewer positive/negative integration tests, selection/colour/reset tests, offline-denial tests and failure-preserves-source tests.
5. Produce fixture screenshots, accessibility checks, memory/latency benchmarks and physical low-end arm64 device evidence.
6. Test supported Android System WebView versions and adaptive window sizes.

The current renderer is a browser-side prototype, not yet an Android-integrated or device-verified viewer. Do not mark S1 complete until the integration and evidence above pass.
