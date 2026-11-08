# Accessibility verification protocol

**Status:** Test plan only; no completed TalkBack/accessibility audit is claimed.

## Manual checks on the installed debug build

- TalkBack: every control has a meaningful label, role, state and action; focus order follows visual order; job state and errors are announced without repeated noise.
- Dynamic type: test Android font/display scaling at 100%, 130%, 160% and 200%; no clipped actions or inaccessible status text.
- Contrast: verify text, icons, focus indicators and disabled states against WCAG 2.2 AA contrast targets where applicable.
- Touch targets: interactive targets should be at least 48dp with adequate spacing.
- Keyboard and switch access: all actions reachable, visible focus and predictable activation.
- RTL and localization: verify layout mirroring and text expansion.
- Motion: no essential information conveyed by animation alone; respect system animation settings.
- Error prevention: destructive/export/cancel actions are clearly named and status is recoverable.
- Narrow screens: verify at 320dp width and landscape.

## Automated checks

Add Compose UI tests for semantics, labels, traversal, large-font layout and state announcements. Automated semantics checks complement, but do not replace, TalkBack testing on the target device. Record OS/API, font scale, assistive technology version, screenshots/logs, issues and retest evidence.
