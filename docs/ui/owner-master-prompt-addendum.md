# Owner UI master prompt — additive requirements only

**Received:** 2026-11-08  
**Authority:** Supplement to `KINETICS_UI_SPEC.md` and the archived master. Existing repository master, approved decisions, schemas, architecture and phase gates take precedence wherever wording overlaps or conflicts. This document captures only additional requirements and implementation details from the latest owner prompt; it does not replace or silently amend existing specifications.

## Repository-first audit and plan
Before UI implementation, audit README, Gradle/build files, source tree, existing screens, token generation, brand asset inventory and image dimensions. Kinetics is an Android-native Compose application with a typed orchestration boundary; do not introduce React Native, Flutter or a parallel UI framework. Record the concrete file plan, token changes, motif architecture, affected screens and test plan before changing screens.

Existing repository records remain authoritative for logo identity and asset release gates. Preserve every supplied logo byte-for-byte; never infer that an image is a logo or synthesize missing approved variants. Record asset paths, formats and dimensions in the audit.

## Additional visual-system requirements
- Delicate, refined, culturally rooted scientific-workspace treatment: hairline borders, tonal elevation, restrained shadows, generous whitespace and rounded surfaces. Avoid emoji, clip-art, neon, heavy gradients and decorative clutter.
- Keep decoration subordinate to data. Decorative textures must not reduce text contrast; use surface scrims where needed.
- Gentle motion only; respect reduced-motion and reduced-transparency settings. Avoid per-frame motif animation and expensive runtime rasterization.
- Use a 4dp spacing base, at least 48dp interactive targets (the repository's stricter Android accessibility baseline wins over 44px), flexible dynamic type, visible focus, screen-reader labels, RTL-safe layout and keyboard/switch navigation where supported.
- Theme must be system-following with explicit user override only if compatible with the existing settings schema and appearance architecture. Contrast validation must be automated for all semantic foreground/background pairs; target WCAG AA (4.5:1 normal text, 3:1 large text). Do not hard-code component colours or edit generated theme outputs manually.

## Typography and brand reconciliation
The new prompt proposes Great Vibes, Cormorant Garamond, IBM Plex Sans and IBM Plex Mono, plus Devanagari coverage. These are candidate families only. Existing approved typography decisions/catalogue and licensing policy win if they differ. Do not change the selected families or bundle fonts solely because this prompt lists alternatives. If the supplied Kinetics logo already contains its wordmark, do not typeset the brand name. Any script face is restricted to a brand accent; functional and scientific content must remain highly legible. Verify exact upstream version, licence, glyph coverage (including Devanagari fallback), weights, file size and offline rendering before bundling.

## Motif system — new additive feature proposal
Implement only after confirming it fits the current Track U architecture and roadmap gates:
- Data-driven manifest, one SVG per motif, single-colour `currentColor`, stroke-based, seamless/tileable, target size ≤3KB and tile size 28–64px.
- Initial proposed cultural/folk-art pool (24): Paisley/Kalka; Jaali lattice; Padma lotus; Kolam/Rangoli; Madhubani fish/leaf; Mor pankh; Kalamkari vine; Pattachitra border; Chikankari floral jaal; Bandhani dots; Ajrakh geometry; Phulkari diamonds; Mandala rosette; Mughal arch repeat; Dravidian pillar band; Athangudi tile; Warli geometric border; Gond dot-and-line; Sanganeri/Bagru sprig; Patola grid; Kantha stitch; Ambi mango kalka; miniature-painting floral border; Toda embroidery bands.
- Manifest fields: `id`, `name`, `origin`, `file`, `tileSize`, `tags`, `densityScore` (1–5), `surfaces`, `lightOpacity`, `darkOpacity`, `credit`.
- Cultural descriptions must be researched and respectful. No deity imagery, sacred symbols or religious script as decoration; do not caricature or misattribute regional traditions.
- Pure deterministic picker: `pickDailyMotifs(date, stableInstallId, history)`; seed by local ISO date plus stable anonymous install identifier; same-day stable selection, local-midnight rotation and live 400ms cross-fade only when motion is allowed.
- Assign distinct motifs to hero, workspace cards, list cards, login surfaces, splash and drawer. Avoid same-screen repeats, vary adjacent tags/density, exclude density 4–5 from dense/table list cards, avoid same-slot motifs from the preceding seven days and fall back safely for small/empty pools.
- User texture preference: Daily (Auto), Pin a motif, Off. Persistence must use the approved settings/storage architecture and privacy constraints; stable ID must be anonymous and not expose identity.
- Render textures behind content, decorative/accessibility-hidden and non-interactive; opacity governed by tokens/manifest, with contrast evaluated against worst-case background pixels.
- About/drawer may display a modest motif name, origin and factual credit.

## Additional screen composition requirements
Where the actual screen map and capabilities support them, consider:
- Splash: brand asset centered, restrained daily motif and secondary organization mark; respect platform splash-screen APIs and do not delay launch for ornament.
- Login: centered responsive card, clear email/username and password fields, show/hide control, validation, loading/error/lockout states and biometric fallback only where authentication capability exists. Never imply biometric availability without runtime capability checks.
- Dashboard: preserve actual app navigation and capabilities. Desired composition is brand row, navigation/welcome region, actual workspace carousel, then “Today in your lab” content such as current projects, work/jobs, notifications and recent results. Every data item must be real or explicitly marked sample; do not invent active jobs, ETAs, percentages, scores or notifications.
- Drawer, profile menu and About: keep navigation sections distinct from account/security/preferences. Bind every action to an existing capability; unavailable actions must be labelled or omitted rather than decorative dead controls.
- Carousel cards: adapt to actual workspace registry; no hard-coded fictitious workspaces. Snap/peek/scale effects must remain accessible and reduced-motion-safe.
- Pull-to-refresh, skeletons, empty/error states and retry actions must use actual data/loading/error state.

## Engineering and acceptance additions
- Prefer reusable Compose components and typed state holders consistent with existing MVVM/UDF and orchestrator boundaries; do not copy web-specific ARIA APIs into Compose. Use semantics and accessibility APIs native to Android.
- Motif picker unit tests: deterministic same-day selection, day change, distinct assignments, density constraints, 7-day history avoidance, empty history/pool fallback and midnight rollover.
- Token contrast tests for every text/surface pair, not only a hand-picked subset.
- Light/dark screenshot or Paparazzi/Compose screenshot coverage for Login and Dashboard, plus adaptive viewport checks. Test at 360dp, 390dp, larger phones and tablets; tablet list cards may use two columns if supported by the app's responsive architecture.
- README must explain theme tokens, motif addition/manifest, deterministic daily rotation, pin/off settings and exact logo handling once implemented.
- Keep commits focused and app buildable. Do not declare a screen or design complete without screenshot and accessibility evidence.

## Deferred pending authoritative reconciliation
No screen replacement, token replacement, font change, or motif implementation is authorized by this addendum alone. First reconcile with the complete owner master, current decisions, UI roadmap and capability registry. The owner's later detailed instruction may further refine this document.
