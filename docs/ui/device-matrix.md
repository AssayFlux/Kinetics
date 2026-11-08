# UI device and window matrix

**Status:** NOT DEVICE-TESTED. No emulator or physical-device UI evidence is available. Source-level navigation classifier tests do not substitute for rendering tests.

| Scenario | Target window | Result | Evidence |
|---|---|---|---|
| Small phone portrait | ~360×640dp | NOT RUN | — |
| Standard phone portrait | ~411×891dp | NOT RUN | — |
| Large phone portrait | ~480×1000dp | NOT RUN | — |
| Phone landscape / compact height | height <480dp | NOT RUN | — |
| Foldable folded | compact | NOT RUN | — |
| Foldable unfolded portrait | medium/expanded | NOT RUN | — |
| Foldable tabletop/book posture | posture/hinge-aware | NOT RUN | — |
| 8-inch tablet | medium/expanded | NOT RUN | — |
| 10–13-inch tablet | expanded/large | NOT RUN | — |
| Split-screen 50/50 and 30/70 | dynamic | NOT RUN | — |
| Freeform/resizable window | dynamic | NOT RUN | — |
| 200% font scale | all applicable | NOT RUN | — |
| Largest display size | all applicable | NOT RUN | — |
| RTL | all screens | NOT RUN | — |
| Light/dark/neon | all themes | NOT RUN | — |
| High-contrast light/dark | all screens | NOT IMPLEMENTED | — |
| Gesture and 3-button navigation | compact/wide | NOT RUN | — |
| Keyboard/mouse/trackpad/stylus | medium+ | NOT RUN | — |

Source tests: `android/app/src/test/java/org/assayflux/kinetics/WindowLayoutTest.kt` cover compact, compact-height, medium, expanded, large, extra-large and invalid dimensions. CI results are tracked separately.

A screen is not device-verified until its exact device/window, OS, build SHA, procedure, screenshot/evidence and outcome are recorded. Rotation, resizing and fold/unfold state continuity are mandatory.
