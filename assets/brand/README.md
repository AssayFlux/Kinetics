# Owner-supplied brand assets — required contract

No Kinetics/app identity may be invented or transformed by engineering. Existing `Assets/Brand Logo.svg` is preserved but is not assumed to be the approved master. All files below are placeholders until you supply/approve the real assets.

## Please supply exactly these files

1. `app-logo.svg` — master vector for the Kinetics app mark.
2. `app-logo-foreground.svg` — transparent foreground artwork for Android adaptive icon.
3. `app-logo-monochrome.svg` — single-colour artwork for themed icon/notification use.
4. `app-logo-background.svg` **or** `app-logo-background.txt` — approved solid background colour (hex) or vector background.
5. `brand-logo.svg` — master company/author brand mark.
6. `brand-logo-light.svg` — approved version for light surfaces.
7. `brand-logo-dark.svg` — approved version for dark surfaces.
8. `brand-usage.md` — minimum size, clear space, forbidden changes, official brand colours (hex), approved backgrounds, and whether the existing `Assets/Brand Logo.svg` is an approved master.

## Constraints
- Keep original supplied files byte-for-byte; generated outputs go under `assets/brand/generated/`.
- Do not recolour, redraw, crop, add effects, or derive variants unless the supplied usage rules explicitly authorize it.
- If artwork is illegible at 48dp or notification size, stop and ask; do not “fix” it.
- Release builds must fail if required placeholders remain.
- Feature graphic dimensions and current Play asset rules must be re-verified before store export.

## AssayFlux animated organization mark received

- Owner supplied an animated 1024×1024 AssayFlux GIF in the project conversation on 2026-11-08 (26 frames).
- Treat it as the organization-logo visual reference. Preserve the original artwork and native colours; do not use it as the Kinetics app mark without explicit owner approval.
- Existing `Assets/Brand Logo.svg` remains the repository's existing brand asset. The GIF upload is not silently substituted for that SVG master.
- The uploaded GIF is retained in the conversation attachment. It has not been committed as a second binary copy to avoid duplicating a 9.7 MB animated asset in Git history.
- Official seed colours, clear-space rules and approved light/dark variants still require the owner's `brand-usage.md`.
