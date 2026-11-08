# Kinetics Design System

**Status:** skeleton; not a complete component library or gallery.

The Android library module now compiles generated Compose palette/spacing tokens from `design/tokens.json`; the app shell consumes the Obsidian Cyan, Light and Neon generated palettes. A reusable development-only `KineticsComponentGallery` composable previews those palette families and Material 3 components. It includes the owner-supplied Home background, Home/Work/Explore/Settings, window-responsive navigation and a centred 840dp readable-content cap.

Current navigation uses stable Material 3 NavigationBar, NavigationRail and PermanentNavigationDrawer with a live app-window classifier. It is not yet NavigationSuiteScaffold or fold-posture aware.

U0 exit still requires:
- add a debug-only route/activity that hosts the component gallery and screenshot tests;
- reusable semantic status/tier, Research Mode and connectivity components;
- adaptive navigation suite and fold/hinge posture support;
- component gallery with every component/theme/window size;
- screenshot-test harness, automated accessibility checks and token-only styling lint;
- device evidence and owner-approved visual gate.

Do not claim U0 complete until these run and are recorded.
