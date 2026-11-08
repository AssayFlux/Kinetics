# Kinetics UI specification — current approved direction

**Current authority:** `docs/ui/kinetics-visual-design-system.md` (D-015, owner-approved 2026-11-08).  
**Status:** Design direction approved; native Compose implementation and evidence remain in progress.

## Current visual contract
- Default: **Light Classic** — warm ivory/cream, deep maroon, restrained gold and peacock teal.
- Appearance: coherent Dark Classic and System options; no neon theme as a product direction.
- Composition: rounded hero/surfaces, spacious central horizontal workspace carousel with adjacent cards partially visible, pagination dots and stacked cards below.
- Screens: splash, login, dashboard, navigation drawer, profile/settings and appearance, implemented only with real capabilities and real app state.
- Typography roles: Great Vibes (limited wordmark accent, only if logo has no wordmark), Cormorant Garamond display, IBM Plex Sans functional UI, IBM Plex Mono scientific data; font binaries require licence/glyph/size/offline review.
- Motifs: optional curated Indian classical/folk-inspired SVG system, with factual attribution, cultural review, contrast tests, deterministic rotation and Daily/Pin/Off controls. Do not enable before its gates pass.
- Preserve owner-supplied logos and reference images byte-for-byte. Never invent metrics, jobs, ETAs, projects, analysis outputs or authentication capability.

## Architecture and quality constraints
- Native Jetpack Compose; retain MVVM/UDF, typed orchestration and scientific/domain separation.
- Existing verified responsive window-class/navigation strategy remains active; do not claim fold-aware behaviour without WindowManager integration and tests.
- Minimum 48dp touch targets, dynamic type, screen-reader semantics, visible focus, RTL, keyboard/switch navigation and reduced-motion support.
- Automated WCAG AA contrast checks: 4.5:1 normal text and 3:1 large text/essential non-text controls, including worst-case motif backgrounds.
- One canonical token source; generated outputs are not manually edited.
- Existing licensing, privacy, security, offline-first and Research Mode-only public-build rules remain mandatory.

## Historical directions — not current instructions
D-009's three neutral proposals, D-010/D-011 dark-futuristic/Obsidian Cyan default, and D-014's earlier Light Classic navy/teal palette and font proposal are superseded by D-015. They remain in `DECISIONS.md` for audit history only. D-012 responsive navigation and D-013 owner layout references remain active where compatible.

## Evidence and implementation status
The generated six-screen concept is a visual reference, not a running-app screenshot. Palette values and font families are documented in the canonical design system but still require contrast/licence verification. No screen, motif, accessibility outcome, screenshot or device support is complete until implementation and evidence are committed.

## Required next work
Follow the inventory → semantic tokens → shared Compose primitives → real-data screen refinement → optional motif system → screenshot/contrast/accessibility tests → owner review sequence in the canonical design system.
