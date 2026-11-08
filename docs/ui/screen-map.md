# Screen map and capability mapping

**Current shell:** Home · Work · Explore · Settings. The complete product destinations below remain planned until implemented and connected to real app state and registry capabilities. Navigation adapts from bottom bar to rail to permanent drawer based on the live app window.

| Screen ID | Screen | Registry capability | Current status |
|---|---|---|---|
| ui.home | Home dashboard / import entry | ui.home | source present; D-015 refinement, brand integration and visual/device proof pending |
| ui.work | Work / job list and actions | ui.work | source present; import/job actions exist; registry-backed catalogue only; full analysis dispatcher not connected |
| ui.explore | Scientific capability catalogue | ui.explore | registry-backed catalogue; bounded FASTA and FASTQ QC cards launch from Explore; remaining listed tools are not dispatched |
| ui.settings | Settings / theme family and diagnostics | ui.settings | partial; persistent Light/Dark/System preference and diagnostics; accessibility/device proof pending |
| ui.domains | Domain browser/detail | ui.domains | planned |
| ui.tools | Tool search/favourites/runner | ui.tools | planned |
| ui.data | Projects/imports/data packs | ui.data | planned |
| ui.jobs | Job detail and logs | ui.jobs | planned |
| ui.onboarding | Splash and onboarding | ui.onboarding | planned |
| ui.sequence | Sequence viewer/editor | ui.sequence | FASTA basic QC and FASTQ quality-summary launch cards exist; dedicated sequence viewer/editor remains planned |
| ui.alignment | Alignment viewer | ui.alignment | planned |
| ui.tree | Tree viewer | ui.tree | planned |
| ui.structure | 3D structure viewer | ui.structure | planned |
| ui.chemistry | Chemistry viewer | ui.chemistry | planned |
| ui.kinetics | Kinetics lab | ui.kinetics | planned |
| ui.genomics | Genomics/variants | ui.genomics | planned |
| ui.pgx | PGx Research Mode report | ui.pgx | planned; P0 blocks patient-facing interpretation |
| ui.insilico | In-silico job builder | ui.insilico | planned; I2/I3 engine gates remain |
| ui.charts | Charts studio | ui.charts | planned |
| ui.packs | Data pack manager | ui.packs | planned |
| ui.provenance | Provenance viewer | ui.provenance | planned |
| ui.export | Export/share | ui.export | planned |
| ui.node | Remote node setup | ui.node | planned |
| ui.security | Security/privacy centre | ui.security | planned |
| ui.about | About/licenses | ui.about | planned |
| ui.component_gallery | Development component gallery | ui.component_gallery | composable present; debug route and proof pending |

Explore describes capability maturity; it is not a promise that all research tools can run from Android UI. A capability is launchable only when its real input contract, dispatcher, typed result, viewer, provenance and tests are connected.

## D-016 required destinations and current truth

| Screen ID | Screen | Required behavior | Current status |
|---|---|---|---|
| ui.splash | Brand splash | Owner assets, platform launch behavior, no artificial delay | planned; original artwork integration pending |
| ui.auth | Local app-lock/authentication boundary | Honest local-vs-account distinction, secure fallback and recovery | not implemented; do not invent cloud identity |
| ui.biometric | Biometric unlock | AndroidX BiometricPrompt, enrollment/capability checks, Keystore-backed operation, lockout and recovery | source implemented; CI/device verification and recovery review pending |
| ui.dashboard | D-015 dashboard | Owner-reference composition, real workspace carousel, owner brand, truthful live data and empty states | horizontal carousel source exists; full D-015 visual refinement, reference-image comparison, brand integration and screenshot/device verification pending |
| ui.navigation | Navigation/drawer | Every destination navigates or is explicitly unavailable | partial; four destinations only |
| ui.profile | Profile and security | Real local profile/preferences/security actions; no fabricated account | planned |
| ui.appearance | Appearance | Persistent Light/Dark/System selection; no inert controls | preference source implemented; CI/device verification and D-015 appearance preview pending |
| ui.explore | Scientific capability catalogue | Registry-backed availability and clear maturity | catalogue plus FASTA/FASTQ QC launch cards; other capabilities remain non-runnable |
| ui.work | Work/job list | Real import/job lifecycle actions | source implemented; full test and device evidence required |

D-016 acceptance applies to every row: a screen is not complete until its actions, persistence, accessibility and relevant tests are demonstrated on the exact tested artifact.

## Design authority

D-015 in `docs/ui/kinetics-visual-design-system.md` is the sole active visual authority. Historical neon/Obsidian Cyan and pre-D-015 palettes remain audit history only. Preserve owner assets byte-for-byte; do not claim screenshot fidelity until the repository reference images have been visually compared with actual running-app screenshots.
