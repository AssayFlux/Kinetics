# Screen map and capability mapping

**Current shell:** Home · Work · Explore · Settings. The complete product destinations below remain planned until implemented and connected to registry capabilities. Navigation adapts from bottom bar to rail to permanent drawer based on the live app window.

| Screen ID | Screen | Registry capability | Current status |
|---|---|---|---|
| ui.home | Home dashboard / import entry | ui.home | source present; proof pending |
| ui.work | Work / job list and actions | ui.work | source present; registry gate/tests pending |
| ui.explore | Scientific capability catalogue | ui.explore | source present; registry gate/tests pending |
| ui.settings | Settings / theme family and diagnostics | ui.settings | partial; registry gate pending |
| ui.domains | Domain browser/detail | ui.domains | planned |
| ui.tools | Tool search/favourites/runner | ui.tools | planned |
| ui.data | Projects/imports/data packs | ui.data | planned |
| ui.jobs | Job detail and logs | ui.jobs | planned |
| ui.onboarding | Splash and onboarding | ui.onboarding | planned |
| ui.sequence | Sequence viewer/editor | ui.sequence | planned |
| ui.alignment | Alignment viewer | ui.alignment | planned |
| ui.tree | Tree viewer | ui.tree | planned |
| ui.structure | 3D structure viewer | ui.structure | planned |
| ui.chemistry | Chemistry viewer | ui.chemistry | planned |
| ui.kinetics | Kinetics lab | ui.kinetics | planned |
| ui.genomics | Genomics/variants | ui.genomics | planned |
| ui.pgx | PGx Research Mode report | ui.pgx | planned |
| ui.insilico | In-silico job builder | ui.insilico | planned |
| ui.charts | Charts studio | ui.charts | planned |
| ui.packs | Data pack manager | ui.packs | planned |
| ui.provenance | Provenance viewer | ui.provenance | planned |
| ui.export | Export/share | ui.export | planned |
| ui.node | Remote node setup | ui.node | planned |
| ui.security | Security/privacy centre | ui.security | planned |
| ui.about | About/licenses | ui.about | planned |
| ui.component_gallery | Development component gallery | ui.component_gallery | composable present; debug route and proof pending |

Explore describes capability maturity; it is not a promise that all research tools can run from Android UI. Tool availability must be driven by the registry and a real dispatcher.

## D-016 required destinations and current truth
| Screen ID | Screen | Required behavior | Current status |
|---|---|---|---|
| ui.splash | Brand splash | Owner assets, platform launch behavior, no artificial delay | planned |
| ui.auth | Local app-lock/authentication boundary | Honest local-vs-account distinction, secure fallback and recovery | not implemented |
| ui.biometric | Biometric unlock | AndroidX BiometricPrompt, enrollment/capability checks, Keystore-backed operation, lockout and recovery | not implemented |
| ui.dashboard | D-015 dashboard | Real workspace carousel, owner brand, truthful live data and empty states | partial; old hero remains |
| ui.navigation | Navigation/drawer | Every destination navigates or is explicitly unavailable | partial; four destinations only |
| ui.profile | Profile and security | Real local profile/preferences/security actions; no fabricated account | planned |
| ui.appearance | Appearance | Persistent Light/Dark/System selection; no inert controls | partial; session-only state |
| ui.explore | Scientific capability catalogue | Registry-backed availability and clear maturity | informational catalogue; launch/dispatch not connected |
| ui.work | Work/job list | Real import/job lifecycle actions | implemented source; test and device evidence required |

D-016 acceptance applies to every row: a screen is not complete until its actions, persistence, accessibility and relevant tests are demonstrated on the exact tested artifact.
