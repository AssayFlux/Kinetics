# Kinetics cross-platform blank UI layouts

Structural wireframes only. The original `Brand Logo.svg` is referenced unchanged. Content regions are intentionally empty: no sample metrics, fabricated records, charts, projects, or assumed system states.

## Files
- `kinetics-windows.html` — Windows desktop shell
- `kinetics-macos.html` — macOS desktop shell with window controls
- `kinetics-linux.html` — Linux desktop shell
- `kinetics-android.html` — Android phone shell with bottom navigation
- `kinetics-layout.css` — shared responsive tokens and breakpoints

## Reference artboards
| Platform | Reference viewport | Layout |
|---|---:|---|
| Windows | 1440 × 960 CSS px | Header, navigation rail, fluid workspace |
| macOS | 1440 × 960 CSS px | Header with window controls, navigation rail, fluid workspace |
| Linux | 1440 × 960 CSS px | Desktop header, navigation rail, fluid workspace |
| Android | 412 × 915 CSS px | Compact app bar, scrollable workspace, bottom navigation |

These are CSS-pixel reference viewports, not fixed output resolutions. Layouts use fluid grid tracks, rem spacing, and breakpoints at 1100px, 760px, and 480px. Device-pixel ratio, zoom, and available window size determine physical display dimensions.

## Shared measurements
- Desktop header: 72px; Android app bar: 60px
- Desktop navigation rail: 256px; 216px at medium widths; icon-only at narrow widths
- Android bottom navigation: 68px
- Spacing scale: 4, 8, 12, 16, 20, 24, 32px
- Border: 1px; corner radius: 8px / 12px / 16px
- Content grids: 4 / 2 / 3 columns on wide desktop; collapse responsively

## Brand asset
All HTML files load `./Brand Logo.svg` directly. The original asset is not modified, recoloured, copied, or recreated.

## Preview
Open an HTML file in a modern browser. Keep the HTML and CSS beside `Brand Logo.svg`. These are editable HTML/CSS layouts, not native OS binaries.
