# Workbench UI acceptance programme

> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

## Implemented in the repository

- Dark scientific visual system with responsive 12-column dashboard layout.
- Project creation/selection, dataset intake, allow-listed workflow queueing,
  dataset and experiment registries, job history/logs, report generation and
  artifact downloads.
- Responsive 3Dmol.js structure viewer with PDB/mmCIF file selection,
  molecular representations, surface/non-polymer toggles, residue selection,
  sequence mapping, contact calculation, evidence analysis and PNG export.
- Keyboard focus indicators, semantic labels/status regions and reduced-motion
  handling.
- CI static acceptance checks for the responsive/accessibility contract.

## Automated acceptance

Run:

```bash
python -m pytest -q tests/test_workbench.py tests/test_workbench_ui.py
python -m ruff check tests/test_workbench_ui.py src/kinetics_core/workbench
```

The UI tests are structural regression checks. They do not simulate a browser,
WebGL rendering, touch gestures, screen readers or physical-device performance.

## Required release-gate device matrix

Record device model, OS/WebView/browser version, viewport, test date, result,
and issue link for every row. Do not mark this section passed without a human
tester recording the result.

| Target | Required checks | Status |
|---|---|---|
| Desktop Chromium, 1440×900 | Dashboard flow, upload, queue, logs, reports, downloads, keyboard-only navigation | Not yet physically/browser acceptance-tested |
| Desktop Firefox, 1366×768 | Layout, forms, tables, errors, keyboard navigation | Not yet physically/browser acceptance-tested |
| iOS Safari, current supported iOS | Responsive layout, file picker, scrolling, zoom, VoiceOver, WebGL viewer | Requires device run |
| Android Chrome/WebView, mid-range device | File picker, touch rotate/pan/zoom, PDB and mmCIF, memory/load behavior | Requires device run |
| Android WebView, low-memory device | Large-structure failure behavior, recovery, export, touch controls | Requires device run |
| Screen reader | Labels, status announcements, table navigation, textual alternatives | Requires assistive-technology run |

## Known release blockers / limitations

- The 3Dmol.js viewer currently loads its runtime from the upstream CDN; it is
  not an offline-ready APK asset. Vendor and pin a reviewed build before
  claiming offline support.
- Real device/browser testing cannot be inferred from CI or static tests.
- Large-structure performance and WebGL context-loss behavior require
  representative hardware measurements.
- A WebGL canvas is not fully accessible by itself; retain the textual residue,
  mapping, contact and analysis outputs as alternatives.

A release may claim responsive implementation and automated structural checks
once CI passes. It must not claim full device acceptance, offline APK readiness,
or accessibility acceptance until the matrix above is completed and recorded.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
