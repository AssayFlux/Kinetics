# Owner-supplied brand assets

The owner-provided organization master is stored at `Assets/Brand Logo.svg`. The file at `assets/brand/brand-logo.svg` is an exact Git-blob copy of that master (same SHA); it has not been redrawn, recoloured, simplified or optimized.

## Remaining owner-approved inputs
- `app-logo.svg`: Kinetics app mark as an editable master vector. The repository also contains `Assets/Kinetics.gif`; it is preserved as supplied but is not silently converted into a different logo.
- `app-logo-foreground.svg`: transparent adaptive-icon foreground derived/approved by the owner.
- `app-logo-monochrome.svg`: owner-approved single-colour mark for themed/notification icons.
- `app-logo-background.svg` or `app-logo-background.txt`: approved background artwork or solid hex colour.
- `brand-logo-light.svg` and `brand-logo-dark.svg`: owner-approved variants. The master is not automatically recoloured to create these.
- `brand-usage.md`: official hex colours, minimum size, clear space, forbidden changes, approved backgrounds and permissions.

## Build policy
Debug builds may use the explicitly marked app-icon placeholders while the UI is being developed. Release builds remain blocked by `verifyOwnerBrandAssets` until every required owner-approved asset and usage rule is supplied. Do not infer brand colours from artwork.
