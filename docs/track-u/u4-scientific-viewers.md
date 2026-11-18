# U4 — Scientific viewers

**Disposition:** BOUNDED ANDROID VIEWER INTEGRATION IMPLEMENTED; DEVICE AND SCIENTIFIC ACCEPTANCE OPEN.
**Design authority:** D-024 monochrome V1.
**Dependency policy:** no third-party viewer engine or new runtime dependency was added.

## Integrated Home experience

- The Home service carousel and service list surface the structure and chemistry tools without internal track identifiers.
- The structure viewer imports PDB/ENT/CIF/mmCIF and gzip-compressed variants through Android SAF with a 16 MiB expanded-source ceiling and strict UTF-8 decoding.
- Python prepares the deterministic, bounded coordinate payload and source provenance. The viewer uses the dependency-free interactive 3D coordinate projection rendered on Canvas 2D, loaded through AndroidX WebViewAssetLoader at the app-owned asset origin.
- WebView file/content access and network loads are disabled; mixed content is denied; navigation is constrained; there is no generic JavaScript/native bridge, remote script, telemetry or runtime viewer library.
- The full-screen viewer provides rotation, zoom, reset, element/chain colouring, nearest-atom selection and a bounded accessible atom list.
- Session JSON, bounded PNG and SVG snapshots are available through SAF. Interactive view state is serializable/restorable in the session contract.
- The existing chemistry surface imports one local SDF/MOL and gzip-compressed variants and presents explicit-atom formula/mass and graph counts with SHA-256. It deliberately does not claim RDKit sanitization, implicit hydrogen inference, stereochemistry interpretation or drug-likeness.
- Existing S3 structure-site and apo-pocket cards remain visible only as geometry candidate screens with stated limitations. They do not claim affinity, binding, function or druggability.

## Verification present in source

- tests/test_structure_viewer_assets.py verifies CSP network denial, local asset references, no generic bridge/eval/fetch, atom/byte bounds, accessible selection list, Android/Web asset byte parity, hardened WebView settings and bounded PNG/SVG/session-state export.
- tests/test_android_scientific_viewers.py verifies Home routing to the actual structure and chemistry surfaces and checks their offline/dependency boundaries.
- S1–S3 contracts and limitations remain authoritative in docs/track-s/structure-viewer-contract.md and docs/track-s/audit-2026-11-09.md.

## Not claimed / remaining acceptance

- No 3D molecular bond rendering, ligand sanitization, alignment viewer, phylogenetic tree viewer or general charts studio is claimed by this bounded U4 integration.
- No independent structure-quality, ligand-site or pocket biological concordance is claimed.
- Physical low-end ARM64 performance/memory measurements, supported WebView-version matrix, screenshots, TalkBack/keyboard checks, lifecycle and import/export failure tests remain required.
- No S1–S3 external scientific validation gate is waived.

**Decision:** U4's bounded offline structure/chemistry viewer integration is implemented on Home. Device, accessibility, performance and independent scientific acceptance remain open and are carried into U6 and Track S.


## RCSB public structure retrieval — 2026-11-18

- Home accepts a four-character RCSB PDB entry identifier and retrieves its mmCIF record over allow-listed HTTPS.
- The raw record is SHA-256 verified and saved using the app-private Android Keystore AES-GCM chunked cache.
- The fetched record is passed to the existing Python `prepare_structure_viewer_import` adapter and existing offline structure viewer; the 16 MiB parser limit remains enforced.
- This reuses the current coordinate payload and viewer implementation. It does not add bond inference, secondary structure, biological assembly expansion, structure prediction or a new renderer.
- RCSB text search, saved-structure reopen, retry/cancel, source release/licence metadata and physical-device performance remain open. Exact-head CI and device verification are not yet passed.
