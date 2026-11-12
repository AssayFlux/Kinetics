# Canonical brand and logo assets

All repository artwork now lives under the single lowercase **`assets/`** tree. The former root-level `Assets/` directory has been consolidated; its files were moved by reusing their original Git blobs, so the supplied binary artwork was not recompressed or edited.

## Brand masters

| Asset | Purpose |
|---|---|
| `brand-logo.svg` | Owner-supplied organization/brand master vector. This is byte-identical to the former `Assets/Brand Logo.svg` (same Git blob SHA). |
| `organization-logo.gif` | Owner-supplied animated organization logo, preserved byte-for-byte from the former `Assets/Organization Logo.gif`. |
| `kinetics-logo.gif` | Owner-supplied Kinetics animation/logo, preserved byte-for-byte from the former `Assets/Kinetics.gif`. |
| `kinetics-background.jpg` | Original image formerly named `Kinetics.png`; its bytes are JPEG, so the canonical filename correctly uses `.jpg`. The Android drawable uses the same blob. |
| `app-logo.svg` | Development placeholder for a separately approved square app icon; not interchangeable with the organization logo. |
| `app-logo-foreground.svg`, `app-logo-monochrome.svg` | Adaptive/monochrome icon placeholders pending final owner-approved app-mark assets. |

## Design references

- `../design-previews/dashboard-reference.jpg` — owner-supplied dashboard reference.
- `../design-previews/login-reference.jpg` — owner-supplied login reference.
- `../design-previews/laboratory.gif` — supplied laboratory animation/reference.

## Brand usage and release gate

See [brand-usage.md](brand-usage.md) for the remaining owner-confirmation items. Official brand colour values, minimum size, clear space, approved backgrounds, variant permissions and usage/clearance terms are not inferred from artwork.

Debug builds may use explicitly marked app-icon placeholders during development. Release builds remain blocked by `verifyOwnerBrandAssets` until every required owner-approved app asset and usage rule is supplied. Preserve the owner artwork; do not recolour, redraw, crop, stretch, simplify or optimize it without explicit approval.
