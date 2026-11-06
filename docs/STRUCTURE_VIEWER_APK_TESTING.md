# Kinetics structural biology and APK viewer validation

## What is implemented in this increment

- Biopython-backed structure summary for local PDB/mmCIF files, with SHA-256 source provenance.
- Residue solvent-accessible surface area using Biopython Shrake-Rupley.
- Polymer residue contact search using Biopython NeighborSearch and an explicit heavy-atom distance cutoff.
- C-alpha structural superposition/RMSD using explicit author-numbered residue pairs and Biopython Superimposer.
- Protein sequence alignment using Bio.Align.PairwiseAligner and BLOSUM62.
- A mobile-responsive 3Dmol.js viewer served at `/structure-viewer` and linked from the workbench home page.\n- Loopback workbench APIs for bounded structure summary/SASA/contact analysis (`POST /api/v1/structures/analyze`), explicit-pair C-alpha superposition (`POST /api/v1/structures/superimpose`), and sequence alignment (`POST /api/v1/sequences/align`).
- Viewer controls for cartoon/ribbon, stick, sphere, line and cross representations; optional molecular surface; ligand/non-polymer visibility; residue highlighting; geometric residue contacts; and PNG export.

These functions are computational tools, not independent biological validation. Contact proximity is not proof of binding or functional interaction. SASA depends on the selected model and calculation settings. RMSD is meaningful only when the supplied residue correspondence is valid. No missing residues are reconstructed and no sequence alignment is silently treated as an authoritative structure mapping.

## Install

From a clean environment:

```bash
python -m pip install -e ".[workbench,structures,dev]"
```

The existing `baseline` extra also installs Biopython. MMseqs2, DSSP and PyMOL remain separate executables and must be installed/versioned independently when those workflows are enabled.

## Start the local workbench

```bash
kinetics-workbench --port 8765
```

Open:

- Workbench: `http://127.0.0.1:8765/`
- 3D viewer: `http://127.0.0.1:8765/structure-viewer`

The viewer reads the selected PDB/mmCIF file in the browser. It does not upload or modify the source file. The 3Dmol.js runtime is currently loaded from its upstream CDN, so the first viewer load requires network access. For fully offline APK use, vendor a reviewed, version-pinned 3Dmol.js distribution into the app's assets and update the CSP/asset references accordingly; do not rely on the CDN for an offline acceptance test.

## Android device testing over USB

The workbench intentionally binds to loopback and rejects non-local hosts. Do not expose this unauthenticated local-first service to a Wi-Fi/LAN interface.

With Android Debug Bridge connected and USB debugging authorized:

```bash
adb reverse tcp:8765 tcp:8765
```

The APK's WebView can then open `http://127.0.0.1:8765/structure-viewer` on the device. This keeps the service bound to the development machine's loopback interface. Confirm the Android WebView permits the local file chooser and test both PDB and mmCIF selection. For a production or LAN-connected APK, use the authenticated, tenant-aware deployed API rather than exposing this local workbench.

## Suggested acceptance checks

1. Load a reviewed small PDB fixture and a reviewed mmCIF fixture.
2. Confirm cartoon, stick, sphere, line and cross render modes; toggle surface and non-polymer visibility.
3. Rotate, zoom, pan, reset and export a PNG.
4. Select residues from the sequence strip and confirm the correct chain/residue is highlighted.
5. Compute heavy-atom residue contacts at several cutoffs; compare against an independently reviewed reference calculation.
6. Run the Biopython summary, SASA, contacts, explicit-pair RMSD and sequence-alignment unit tests.
7. Test large structures on representative low-memory Android hardware and record load time, memory use, frame rate and failure behavior.
8. Verify experimental/predicted classification and source license/provenance in the surrounding research record. The viewer alone cannot establish either.
9. Test with screen reader, keyboard navigation, high contrast and zoom. The 3D canvas itself needs accessible textual alternatives for residue and contact information.

## Current limitations / next acceptance gates

- The 3D viewer is browser/WebView-based and requires the upstream 3Dmol.js CDN at present; offline bundling and APK integration testing are still outstanding.
- The current browser contact calculation is exploratory and quadratic in atom count. It should be moved to a bounded worker/server-side spatial index for large structures.
- The viewer has no verified automatic sequence-to-structure alignment workflow yet. Residue highlighting is based on structure-file chain and author residue identifiers.
- Ligand display is present, but automated hydrogen-bond, salt-bridge, covalent-link and binding-site interpretation is not claimed.
- Structural superposition requires explicit residue pairs; automated alignment, insertion-code-aware correspondence, alternate-conformation policy and independent reference validation remain follow-up work.
- No PyMOL renderer, molecular dynamics, docking, or de novo structure prediction is included in this increment.
- APK compatibility, offline operation, accessibility, large-structure performance and scientific acceptance must be tested on actual target devices before release.
