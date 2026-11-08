# Kinetics theme and typography proposals

**Status:** Owner authorized best-judgement completion; Obsidian Cyan is selected as the default dark direction. U0 remains open pending token generation, gallery and validation.

## Owner's direction
- Dark-first, futuristic, premium scientific workbench.
- Three selectable theme families: very light classic, deep dark, and neon.
- Keep AssayFlux organization artwork byte-for-byte; do not recolour, redraw, or use its colours as an inferred seed.
- Offer 20+ genuinely distinct font families spanning professional, futuristic, stylish, certificate/serif, scientific monospace, and accessibility roles.

## Palette families
- Light: 4 combinations — Porcelain Blue, Ivory Sage, Cloud Lilac, Sandstone Copper.
- Dark: 5 combinations — Obsidian Cyan, Midnight Violet, Graphite Ice, Deep Ocean, Carbon Amber.
- Neon: 4 combinations — Cyberpunk, Toxic Lime, Ultraviolet, Plasma.

Previews:
- [Light family](../../assets/design-previews/light-family.svg)
- [Dark family](../../assets/design-previews/dark-family.svg)
- [Neon family](../../assets/design-previews/neon-family.svg)

Full colour values are in `design/tokens.json`. These are proposals and have not passed WCAG contrast/CVD audits. Do not treat every accent/background pairing as approved.

## Typography
26 distinct candidate families are catalogued in `design/typography-catalogue.yaml`. Proposed defaults are Inter for UI and JetBrains Mono for sequence/data text. The app currently uses platform fonts; candidate font binaries must not be bundled until exact upstream versions, licences, language coverage, APK size, font scale and legibility are reviewed.

Families include Roboto, Inter, IBM Plex Sans, Source Sans 3, Noto Sans, Manrope, Plus Jakarta Sans, Sora, Space Grotesk, Exo 2, Rajdhani, Orbitron, Oxanium, Michroma, Audiowide, Cinzel, Cormorant Garamond, EB Garamond, Libre Baskerville, Merriweather, Roboto Slab, IBM Plex Mono, JetBrains Mono, Fira Code, Source Code Pro and Atkinson Hyperlegible.

## Current Compose prototype
The app shell now has a dark default and an in-app Light / Dark / Neon family selector. This is an initial implementation, not the final token-generated design system. Selection is saved across activity recreation only; durable encrypted settings persistence is still required. Token-to-Compose/CSS generation and UI quality validation remain U0 work.
