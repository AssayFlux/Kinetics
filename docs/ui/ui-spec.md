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

## Supersession and implementation enforcement — D-016
Old active design directions are discontinued. Do not implement or restore neon, Obsidian Cyan or pre-D-015 palettes. They remain historical records only. D-015 is the sole active design authority.

The required real-app destinations are splash/onboarding, authentication, dashboard, navigation, profile/security and appearance. They must use actual app state and original owner-supplied assets. Approved concept art is not evidence that a screen exists.

### Authentication and biometric acceptance
- No invented cloud account, remote identity provider or server-side sign-in.
- Clearly label local app lock separately from account authentication.
- Use AndroidX BiometricPrompt with device capability/enrollment checks, explicit opt-in, secure credential fallback, lockout/error handling, lifecycle-safe invocation and Keystore-backed key use where appropriate.
- Never collect, persist or process biometric templates. Never report success unless the cryptographic/authentication operation succeeds.
- Define first-run, disabled biometrics, no enrollment, unavailable hardware, temporary/permanent lockout, credential fallback, key invalidation and recovery behavior.
- Provide a user-visible way to disable biometric unlock and recover access without destroying encrypted research data.

### Working-control acceptance
Tests must prove each interactive element's state transition, navigation, persistence or platform action. Inert decorative controls are unacceptable. Planned/unavailable capabilities must be visibly identified and cannot be presented as runnable. Theme selection must persist across process death and restart. Profile/security settings must be backed by implemented storage and actions.

### Build/test cycle
Every substantial increment must be built, regression-tested and inspected before acceptance. Record exact commit, APK/AAB hash, workflow, test commands/results, screenshots and device details. Never claim all systems work based on compilation alone. See ROADMAP and DECISIONS D-016.
