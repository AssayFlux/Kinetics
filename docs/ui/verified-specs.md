# Verified Android and Material specifications

**Verified:** 2026-11-08. Re-check before each release; platform guidance can change.

## Window size classes
Android Developers currently documents width classes:
- Compact: <600dp
- Medium: 600dp to <840dp
- Expanded: 840dp to <1200dp
- Large: 1200dp to <1600dp
- Extra-large: ≥1600dp

Height classes:
- Compact: <480dp
- Medium: 480dp to <900dp
- Expanded: ≥900dp

Classes are based on the app window, not device labels; they can change during rotation, folding and multi-window. Use both width and height when compact height makes multi-pane layouts impractical.

Sources:
- https://developer.android.com/develop/ui/views/layout/use-window-size-classes
- https://developer.android.com/develop/adaptive-apps/guides/use-window-size-classes

## Adaptive navigation
Android Developers documents `NavigationSuiteScaffold` in the Material 3 adaptive navigation suite library. Compact windows can use a navigation bar and expanded windows a navigation rail; exact behavior depends on adaptive window information and current library version.

Source:
- https://developer.android.com/develop/adaptive-apps/guides/build-adaptive-navigation

## Edge-to-edge
On Android 15+ devices, apps targeting SDK 35+ are edge-to-edge by default. Content can draw behind status/navigation bars; apply and test insets, cutouts, IME and navigation-mode behavior. Material 3 components may handle some insets, but this must be checked for the actual scaffold and nested content.

Sources:
- https://developer.android.com/develop/ui/views/layout/edge-to-edge
- https://developer.android.com/about/versions/15/behavior-changes-15

## Not yet verified / deliberately not frozen
- Exact Material 3 navigation bar/rail dimensions and icon/adaptive-icon safe-zone values.
- Splash screen asset constraints and Play Store icon/feature graphic specifications.
- Target SDK / Play policy requirements at release time.
- Biometric, StrongBox, Play Integrity and notification permission behavior for the selected minimum/target SDK.
- Accessibility and performance budgets; these require measurement on the named low-end device.

Do not treat the owner's dp values as current platform mandates until individually confirmed.
