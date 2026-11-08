# UI quality report

**Status:** NOT PASSED. This report distinguishes source-level checks from visual/device evidence. Last updated: 2026-11-08.

| Area | Acceptance bar | Result | Evidence |
|---|---|---|---|
| Contrast | WCAG 2.2 AA: 4.5:1 text; 3:1 large text/UI | NOT MEASURED | — |
| Touch targets | ≥48×48dp; ≥8dp spacing | NOT MEASURED | No bounds audit |
| TalkBack | Manual pass every screen | NOT RUN | — |
| Switch Access / keyboard | Complete focus and action pass | NOT RUN | — |
| Large text | 200% without clipping/overlap | NOT RUN | — |
| Display size | Largest supported setting | NOT RUN | — |
| Responsiveness | Full device/window matrix | NOT RUN | device-matrix.md |
| Navigation logic | Boundary tests for bottom/rail/drawer | SOURCE TEST ADDED; CI PENDING | WindowLayoutTest.kt |
| Fold/hinge behavior | WindowManager posture and hinge avoidance | NOT IMPLEMENTED | — |
| Performance | Macrobenchmark/Perfetto on named low-end arm64 device | NOT RUN | — |
| Robustness | Soak test; process death/rotation/resize state | NOT RUN | — |
| Usability | Consented scientist task study | NOT RUN | — |
| Consistency | Token-only styling; CI lint | NOT IMPLEMENTED | — |

No “best”, WCAG-conformant, accessible, device-responsive, performant or production-ready claim is permitted until evidence is attached. A successful APK build is not a UI quality pass.
