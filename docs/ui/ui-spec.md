# UI specification — adopted direction and implementation status

**Status:** Track U / U0 in progress. Dark-first futuristic direction selected under owner authorization; full U0 exit criteria are not yet met.

- Owner's complete requirements: `KINETICS_UI_SPEC.md`.
- Product: scientist-first, offline-first, truthful Research Mode workbench.
- Visual direction: Obsidian Cyan default; Light and Neon families remain selectable. See `docs/ui/theme-proposals.md` and `design/tokens.json`.
- Owner artwork: `Assets/Kinetics.png` is preserved and copied byte-for-byte to the Home hero drawable as `kinetics_background.jpg`. The supplied `Assets/Brand Logo.svg` is copied byte-for-byte to `assets/brand/brand-logo.svg`. No recolouring, redraw or inferred brand seed.
- Typography: 26 distinct candidate families are catalogued; font binaries are not bundled until exact licence, version, size, language and accessibility checks pass.
- UI architecture: Compose MVVM/UDF → ViewModel/use case → typed orchestrator; scientific logic stays outside composables.
- Current app shell: compact bottom navigation and Home/Work/Explore/Settings screens; this is a first usable shell, not the complete screen map.
- Tokens: `design/tokens.json`; deterministic Compose/CSS generator: `scripts/gen_design_tokens.py`; generated Compose palette module: `android/designsystem/`; generated WebView CSS: `web/viewers/src/styles/kinetics-tokens.css`; settings schema: `design/settings-schema.yaml`.
- The app shell now consumes generated Obsidian Cyan, Porcelain Blue and Cyberpunk palettes. A development component-gallery composable and generated catalogue exist; a debug-only launch route and screenshot evidence remain open.
- Responsive navigation, design-system gallery, generated Compose/CSS themes, full settings catalogue, security UI and all additional domain/tool screens remain open.
- Quality evidence is recorded honestly in `quality-report.md` and `device-matrix.md`; neither is currently a pass.
