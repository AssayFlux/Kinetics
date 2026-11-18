# UI quality report

**Status:** NOT PASSED — owner dashboard source and navigation regression coverage are implemented; exact-head Android build and visual/device acceptance remain pending. This report distinguishes source-level checks from visual/device evidence. Last updated: 2026-11-18. Android arm64 APK/AAB build and JVM tests passed on commit 841aebd64605a167797fb42e8d49e2fa66557be5 (workflow #44216522668); this is not the latest commit. Python CI on 3300b97c84114cb3ba6eb31fa7655247956430e6 found two VCF fixture failures (538 passed, 2 failed, 9 skipped); the fixture delimiter correction is committed as ad0b1d7b0f0594489cf4623b74df022d80619659, and exact-head verification is pending. No current-head APK success is claimed. See docs/track-u/completion-audit.md for the complete Track U gap register.

| Area | Acceptance bar | Result | Evidence |
|---|---|---|---|
| Contrast | WCAG 2.2 AA: 4.5:1 text; 3:1 large text/UI | NOT MEASURED | — |
| Touch targets | ≥48×48dp; ≥8dp spacing | NOT MEASURED | No bounds audit |
| TalkBack | Manual pass every screen | NOT RUN | — |
| Switch Access / keyboard | Complete focus and action pass | NOT RUN | — |
| Large text | 200% without clipping/overlap | NOT RUN | — |
| Display size | Largest supported setting | NOT RUN | — |
| Responsiveness | Full device/window matrix | NOT RUN | device-matrix.md |
| Navigation logic | Owner hamburger drawer; Home/Work/Settings/Search and avatar profile | SOURCE IMPLEMENTED; exact-head CI and device interaction pending | KineticsUi.kt |
| Fold/hinge behavior | WindowManager posture and hinge avoidance | NOT IMPLEMENTED | — |
| Performance | Macrobenchmark/Perfetto on named low-end arm64 device | NOT RUN | — |
| Robustness | Soak test; process death/rotation/resize state | NOT RUN | — |
| Usability | Consented scientist task study | NOT RUN | — |
| Consistency | Token-only styling; CI lint | TOKEN GENERATION + REPRODUCIBILITY CHECK ADDED; hard-coded value lint NOT IMPLEMENTED | `scripts/gen_design_tokens.py`; CI pending |

No “best”, WCAG-conformant, accessible, device-responsive, performant or production-ready claim is permitted until evidence is attached. A successful APK build is not a UI quality pass.


## Track U V1 baseline update — 2026-11-17
- Active visual contract: owner-supplied monochrome V1 (D-024); exact palette and component dimensions are documented in docs/ui/ui-spec.md.
- Canonical token source migrated for active Light/Dark palettes and V1 spacing/radius values; Compose and WebView generated outputs refreshed.
- Initial reusable Compose primitives added in android/designsystem/.../KineticsComponents.kt.
- Integrated a 56dp app bar and gesture-enabled modal navigation drawer; owner-approved blueprint now removes persistent bottom navigation and rail. This is source implementation, not screenshot or device acceptance.
- NOT YET VERIFIED: exact-main APK/AAB artifact and hashes, screenshot rendering, semantic contrast, TalkBack, 200% font scale, RTL, keyboard/switch navigation, device matrix and physical-device behavior.
- Existing owner logo/reference assets have not been altered. Actual integration remains open pending path/role audit.


## U4–U5 integration update — 2026-11-18

- U4 Explore now explicitly groups the existing offline structure viewer and chemistry graph preview. The structure viewer uses original dependency-free Canvas assets, AndroidX WebViewAssetLoader, disabled network/file/content access, no generic JS bridge, and bounded SAF JSON/PNG/SVG/state export. Automated source/asset tests exist; physical-device, accessibility, performance and independent scientific acceptance remain OPEN.
- U5 Explore now exposes bounded aggregate-only VCF syntax/QC for synthetic or authorized public non-patient data. The screen requires an operator attestation, limits input to 5 MiB, caps records/samples, returns no sample identifiers or genotype strings, and does not persist or export the input/result.
- PGx interpretation and Android docking/OpenMM/ADMET launchers remain unavailable; their dependency and P0 boundaries are disclosed in the UI.
- Exact-head CI, embedded-runtime VCF fixture checks, screenshots, contrast, TalkBack, device performance and independent science/security review are NOT YET PASSED. This update is source integration evidence, not a UI acceptance pass.


## Owner-approved dashboard implementation update — 2026-11-18

- Home source now follows the owner hierarchy: header with hamburger/profile actions, one-card-per-capability horizontal carousel, five-position pagination window and four summary panels.
- The 68 capability catalogue entries and Public Reference Databases are routed by stable IDs to individual service detail pages.
- Persistent bottom navigation and the expanded navigation rail are removed; Home, Work and Settings are in the hamburger drawer.
- Profile discloses that remote account identity is not configured. Biometric unlock remains an Android-managed local device lock.
- Python regression tests now assert the owner carousel structure, capability count, ID-based navigation, five-indicator window and four dashboard panels.
- **Not yet passed:** exact-head Android compile/JVM tests for the latest source, owner-image screenshot comparison, contrast/touch-target measurement, TalkBack, 200% font scale, RTL, keyboard/switch navigation, device matrix, physical-device performance and independent security/scientific reviews.

- Header refinement: Search moved into the hamburger drawer so the Home header presents the hamburger at left and profile/avatar at right, matching the owner reference.
