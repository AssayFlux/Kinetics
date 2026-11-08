# KINETICS — UI/UX Master Specification

**Status:** Owner-supplied specification, received 2026-11-08. Extends `docs/origin/KINETICS_MASTER.md`; does not replace it.  
**Authority:** Follow the owner's Parts 0–14 exactly. Record implementation and evidence in `docs/ui/`, `design/`, `DECISIONS.md`, `ROADMAP.md`, `capabilities/registry.yaml` and `SESSION_LOG.md`.

This file is the complete owner-supplied UI/UX master spec. It is preserved verbatim as supplied in the project conversation. The operationally adopted decisions, verified platform facts, implementation evidence and open gates are maintained in the linked living files.

## Non-negotiable rules
1. “World's best” is an aspiration, never a claim. Quality claims require measured evidence.
2. Every screen, setting and security feature must map to a capability or schema entry.
3. No scientific logic in Compose/WebView. UI calls a typed orchestrator.
4. Verify Android/Material guidance and record sources in `docs/ui/verified-specs.md`.
5. Unspecified choices are conservative and logged in `DECISIONS.md`.
6. Brand assets belong to the owner. Do not invent, redraw, recolour, or improve them.

## Parts
- Part 0 — Rules for the assistant
- Part 1 — Brand assets and owner-supplied asset contract
- Part 2 — Design principles and measurable quality bars
- Part 3 — Device and window matrix
- Part 4 — Responsive layout system
- Part 5 — Navigation and screen map
- Part 6 — Screen outlines
- Part 7 — Design tokens and theming
- Part 8 — Settings catalogue
- Part 9 — Security and privacy UI/enforcement
- Part 10 — Frontend/backend wiring
- Part 11 — Accessibility and performance budgets
- Part 12 — Mandatory repository records
- Part 13 — Track U roadmap and approval gates
- Part 14 — First UI session

## Owner-specified numerical starting points
Use the values in the supplied specification only as starting values. The verified current Android window-size classes are recorded in `docs/ui/verified-specs.md`. In particular, compact <600dp, medium 600–840dp, expanded 840–1200dp, large 1200–1600dp, extra-large ≥1600dp; compact height <480dp, medium 480–900dp, expanded ≥900dp. Do not equate a device category with a window class.

## Brand asset contract
Required owner inputs and release-blocking placeholders are listed in `assets/brand/README.md`. The existing repository file `Assets/Brand Logo.svg` is preserved and is not assumed to be the approved master or an app logo.

## U0 gate
Engineering may implement U0 foundations and repair the existing UI build. Do not lock a final visual direction or claim UI quality bars passed until the owner selects a direction and the required measurements exist. Present three directions with real gallery screenshots when the app build and gallery are working; then stop for the owner's choice.

## Full source
The complete owner-supplied message in this project conversation is the authoritative detailed source for Parts 0–14. This file records the scope and rules without silently converting aspirations into implementation claims.
