# Kinetics — Owner-approved visual design system

**Decision:** D-015 (2026-11-08)  
**Status:** Approved visual direction; implementation and verification in progress  
**Platform:** Existing native Android Jetpack Compose application  
**Precedence:** This document is the current product-visual authority. The archived master, NORTH_STAR, capability registry, security/privacy rules, architecture, scientific scope and phase gates remain authoritative for their respective subjects. Where old UI-only proposals conflict with this document, D-015 wins.

## 1. Design intent

Kinetics is a refined, premium scientific research workspace with a subtle Indian-inspired visual identity. It should feel calm, confident, welcoming and scientifically rigorous—not a generic futuristic console, pastel template or ornamental lifestyle app.

The owner-approved visual direction is represented by the supplied repository references `assets/design-previews/dashboard-reference.jpg` and `assets/design-previews/login-reference.jpg`, alongside the six-screen showcase (splash, login, dashboard, navigation drawer, profile/settings and appearance) reviewed on 2026-11-08. Treat these as the owner's visual references, not screenshots of the running app or a pixel-perfect specification. Analyse their composition and apply the D-015 visual language in the real app while preserving actual workflows and capabilities.

## 2. Core visual language

- **Default theme:** Light Classic — warm ivory/cream canvas, white/ivory cards, deep maroon as the principal action/brand accent, restrained gold and peacock teal accents, dark warm text.
- **Dark theme:** retain a complete accessible dark counterpart; it must feel deliberate and premium, not a simple inversion.
- **Surfaces:** spacious rounded cards, large rounded hero/container, subtle tonal layering, hairline borders, restrained shadows and generous whitespace.
- **Composition:** clear top brand/navigation region; a prominent horizontal workspace carousel with one central card and partially visible adjacent cards; pagination indicators; then spacious vertically stacked research/work cards. Keep the owner-reference composition while adapting to real information architecture and window sizes.
- **Controls:** simple, obvious, touch-friendly, consistent; no ornamental controls or fake functionality.
- **Scientific content:** legible, information-dense where necessary, with explicit units, uncertainty, provenance and status. Decorative motifs must never obscure data.
- **Avoid:** pastel-first styling, neon, heavy gradients, emoji/clip-art, decorative clutter, illegible script controls, fake metrics, fabricated jobs/ETAs/projects/results and invented research capabilities.

## 3. Palette tokens

The following are approved design starting values from the owner's master prompt and visual review. They are not automatically WCAG-passing. Contrast must be measured for every semantic foreground/background pairing; adjust derived tokens where needed without changing the overall palette identity.

### Light Classic
| Token | Value | Role |
|---|---|---|
| canvas | #FBF4E6 | warm page background |
| hero | #7B1E34 | primary maroon region |
| heroDeep | #5E1527 | pressed/deep maroon |
| surface | #FFFDF8 | primary card |
| surfaceAlt | #F7E6C8 | warm inset/card |
| gold | #D9A441 | restrained highlight |
| teal | #146C70 | secondary scientific accent |
| rose | #B83A5B | selected status accent |
| turmeric | #F2C14E | caution/highlight accent only |
| border | #E6D3A8 | subtle outline |
| text | #2B1B14 | primary text |
| textMuted | #5A4638 | secondary text |
| track | #EFE0BF | track/divider background |

### Dark Classic
| Token | Value | Role |
|---|---|---|
| canvas | #120E18 | page background |
| hero | #2A1530 | hero region |
| surfaceInset | #3B2547 | inset |
| surface | #1E1726 | primary card |
| gold | #E3B655 | restrained highlight |
| teal | #4FB3B0 | secondary accent |
| rose | #E58A9B | selected status accent |
| border | #3A2F4A | outline |
| text | #F2E8D5 | primary text |
| textMuted | #B8A9C9 | secondary text |
| track | #3A2F4A | track/divider background |

Semantic roles—not raw hex values—must be consumed by Compose components. Scientific charts must use separately validated, colour-vision-aware categorical, sequential and diverging palettes.

## 4. Typography

Typography is role-based and subject to exact font-file licensing, glyph coverage, offline rendering and size verification before bundling.

- **Brand calligraphic accent:** Great Vibes (candidate; only for a limited wordmark/signature accent, and only if the approved Kinetics logo does not already contain the wordmark).
- **Editorial display headings:** Cormorant Garamond (candidate; selected large headings only).
- **Functional/UI/body:** IBM Plex Sans (candidate; fallback to platform sans-serif).
- **Scientific data/code:** IBM Plex Mono (candidate; fallback to platform monospace).
- **Indic scripts:** verified system/packaged fallback with Devanagari coverage where required. Do not promise glyph coverage before testing.
- Never use calligraphic or display faces for controls, dense text, tables, labels, accessibility announcements or scientific notation.
- Do not redraw, recolour, crop destructively or synthesize the owner's supplied logo assets. Do not typeset a second Kinetics wordmark over a logo that already contains one.

## 5. Motif and cultural texture system

A curated library of up to 24 tileable, single-colour SVG motifs may be implemented after the motif audit and cultural attribution review. Candidate traditions include Paisley/Kalka, jaali lattice, lotus geometry, kolam/rangoli, Madhubani botanical/fish forms, peacock-feather geometry, Kalamkari vines, Pattachitra borders, Chikankari floral jaal, Bandhani dots, Ajrakh geometry, Phulkari diamonds, mandala rosettes, Mughal arch repeats, Athangudi tiles, Warli borders, Gond dot-line forms, Sanganeri/Bagru sprigs, Patola grids, Kantha stitches, miniature-painting floral borders and Toda embroidery bands.

Requirements:
- Research origin, spelling, cultural meaning and attribution; never invent provenance or present a pan-Indian generalisation as a specific regional tradition.
- No deity imagery, sacred symbols or religious script used as decoration.
- Keep motifs subtle, behind content, decorative and excluded from accessibility semantics.
- Manifest metadata must include stable ID, name, region/origin, asset path, tile size, tags, density, permitted surfaces, light/dark opacity and factual credit.
- Motif assets must be lightweight, seamless, single-colour/currentColor SVGs; verify tile quality and sanitise SVG input.
- Deterministic picker based on local ISO date and anonymous stable install identifier; same-day deterministic choice, local-midnight rotation, no same-slot repeat for seven days where pool size permits, no same-screen repeats, density restrictions for tables/lists and safe fallback for small pools.
- User controls: Daily (Auto), Pin a motif, Off. Persist using the approved settings architecture; stable identifier must not expose identity.
- Respect reduced motion; no continuous animation. Any transition must be restrained and optional.
- Do not ship motifs until cultural review, credits, rendering, worst-case contrast and tests pass.

## 6. Screen direction

### Splash
Use the approved brand artwork, centered and unmodified, with a restrained optional motif and secondary organisation mark only where the correct asset exists. Respect Android splash APIs and never delay launch for decoration.

### Authentication
Responsive centered card; actual username/email and password fields; show/hide password, validation, loading/error/lockout states only when implemented. Biometrics are shown only when the runtime authentication capability and enrollment checks pass. Never invent account identity or authentication success.

### Dashboard
Brand/navigation row and real profile affordance; welcome/summary region only with truthful content; central workspace carousel with partial adjacent cards and pagination; then real research activity such as actual projects, jobs, notifications and recent results. Empty states must be honest. No fake project counts, progress, ETA, job state or result.

### Drawer
Clear grouped navigation with meaningful labels, icons from the approved icon system, dividers and organisation attribution only when the approved asset is available.

### Profile/settings
Account, security, appearance, language, accessibility and About entries only when backed by real settings/capabilities. Sign-out must perform actual sign-out.

### Appearance
Light / Dark / System controls; texture preference Daily (Auto) / Pin / Off only when implemented. Clearly display selected state and preview approved motifs. No fake theme state.

## 7. Layout, motion and accessibility

- Native Compose only; retain existing MVVM/UDF, typed orchestration and domain/UI separation.
- Respect verified Android app-window size classes and existing responsive shell; adapt carousel card widths, margins and navigation without assuming device category equals window class.
- Minimum interactive target 48dp; preserve visible focus, screen-reader labels, dynamic type, keyboard/switch access, RTL-safe layouts and sufficient spacing.
- WCAG AA target: 4.5:1 normal text and 3:1 large text / essential non-text controls, measured against all semantic token combinations. Include texture overlays in worst-case contrast tests.
- Respect system font scaling, reduced motion and reduced transparency. Avoid motion as the sole status cue.
- Use semantic status labels and icons; colour is never the only signal.

## 8. Engineering and asset constraints

- Audit current Compose screens, tokens, settings persistence, assets, build/dependency and accessibility architecture before screen changes.
- One canonical token source; generated outputs are never edited manually.
- Preserve all owner-supplied assets byte-for-byte. Record file path, type, dimensions, hash and intended use.
- No new framework, dependency, font binary, engine or remote service without repository licensing/security review and required approval.
- The UI consumes real registry-backed capabilities. Do not add decorative mock scientific outputs to production screens.
- All sensitive research data remains subject to existing privacy/security policy; no patient data or clinical mode is authorised by this visual decision.

## 9. Required implementation sequence and evidence

1. Inventory existing UI files, assets, token generator, typography catalogue, settings and navigation; document mapping.
2. Create canonical Light Classic and Dark Classic semantic tokens and verify generator determinism.
3. Implement shared Compose primitives and theme plumbing; keep the app buildable.
4. Refine dashboard, authentication, drawer, profile and appearance in dependency order using real app state.
5. Add motifs only after provenance, sanitisation, contrast, picker and settings tests.
6. Add screenshot tests for compact, medium, expanded, large, light/dark, font scale, RTL and accessibility states where supported.
7. Run automated contrast, token consistency, UI tests, JVM tests and Android build; record exact commit, commands, toolchain and results.
8. Obtain owner visual review against the six-screen concept and original reference images. Device screenshots and physical-device verification are separate evidence from CI.

## 10. Acceptance checklist

- [ ] No obsolete dark-futuristic/neon default remains in active UI or docs.
- [ ] Light Classic is the default; Dark Classic and System are coherent.
- [ ] Actual logo artwork is preserved and correctly placed.
- [ ] Carousel composition is implemented with truthful app data.
- [ ] Typography roles and fallbacks work at large font scales and with Indic scripts.
- [ ] All semantic contrast pairs pass the documented thresholds.
- [ ] Motif attribution, sanitisation, deterministic rotation and user controls are tested before enabling.
- [ ] Accessibility, RTL, keyboard, reduced motion and adaptive layouts are checked.
- [ ] Screenshot evidence is committed and reviewed.
- [ ] README, UI spec, decision log, session log and release claims match implementation status.

## 11. Status honesty

This document approves the design direction, not implementation completion. The generated showcase is conceptual reference art, not a screenshot of the running app. No screen, font, motif, contrast result, accessibility result or device support claim is considered complete without repository implementation and evidence.
