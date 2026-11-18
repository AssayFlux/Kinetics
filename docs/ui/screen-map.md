# Screen map and capability mapping

**Current shell:** Home · Work · Settings in the hamburger drawer; individual scientific services launch from the Home carousel; Profile opens from the top-right avatar. There is no persistent bottom bar or navigation rail. Planned rows are not exposed as fake navigation actions.

| Screen ID | Screen | Registry capability | Current status |
|---|---|---|---|
| ui.home | Owner-blueprint dashboard | ui.home | four live summary panels and repository-backed horizontal service-area carousel implemented; visual/device acceptance pending |
| ui.work | Work / job list and actions | ui.work | source present; import/job actions exist; repository-backed service carousel; full analysis dispatcher not connected |
| ui.services | Service carousel destinations | capability catalogue | 68 capability cards plus Public Reference Databases; each card is keyed by capability ID and opens a dedicated service detail page; execution dispatch remains bounded and must not be inferred from catalogue status |
| ui.settings | Settings / theme family and diagnostics | ui.settings | partial; persistent Light/Dark/System preference and diagnostics; accessibility/device proof pending |
| ui.domains | Service domain detail | ui.domains | individual capability-ID service detail pages implemented; richer search/favourites/typed execution routing remain open |
| ui.tools | Tool search/favourites/runner | ui.tools | planned |
| ui.data | Projects/imports/data packs | ui.data | planned |
| ui.jobs | Job detail and logs | ui.jobs | planned |
| ui.onboarding | Splash and onboarding | ui.onboarding | planned |
| ui.sequence | Sequence viewer/editor | ui.sequence | FASTA basic QC and FASTQ quality-summary launch cards exist; dedicated sequence viewer/editor remains planned |
| ui.alignment | Alignment viewer | ui.alignment | planned |
| ui.tree | Tree viewer | ui.tree | planned |
| ui.structure | Offline structure viewer | ui.structure | service-destination PDB/mmCIF Canvas viewer; JSON/PNG/SVG/state export; physical-device acceptance open |
| ui.chemistry | Chemistry graph viewer | ui.chemistry | service-destination SDF/MOL graph-only preview; no RDKit sanitization or full 3D bond rendering claim |
| ui.kinetics | Kinetics lab | ui.kinetics | planned |
| ui.genomics | Genomics/variants | ui.genomics | service-destination aggregate-only VCF syntax/QC for synthetic or authorized public non-patient data; no sample/genotype output or reference concordance |
| ui.pgx | PGx Research Mode report | ui.pgx | NOT ENABLED; P0 NOT APPROVED, licensed definitions and independent P2/P3 evidence outstanding |
| ui.insilico | In-silico job builder | ui.insilico | NOT ENABLED on Android; host adapters only, compute-node/force-field/model and independent I2–I4 evidence gates remain |
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
| ui.auth | Local app-lock/authentication boundary | Honest local-vs-account distinction, secure fallback and recovery | local biometric/device-credential lock screen implemented; visual match to owner login blueprint and lifecycle/device recovery acceptance remain open; no cloud identity |
| ui.biometric | Biometric unlock | AndroidX BiometricPrompt, enrollment/capability checks, Keystore-backed operation, lockout and recovery | source implemented; ARM64 build/JVM task passed CI #2039; device verification and recovery review pending |
| ui.dashboard | Owner login/dashboard blueprint | Owner-reference composition, live summaries, interactive service carousel and navigation | dashboard composition and per-capability carousel source implemented; owner-image comparison, screenshot/device verification and final visual refinement pending |
| ui.navigation | Hamburger drawer | Home, Work and Settings are drawer destinations; no persistent bottom bar or rail | source implemented; adaptive/device interaction verification pending |
| ui.profile | Profile and security | Real local profile/preferences/security actions; no fabricated account | local profile disclosure implemented; remote account, user ID, password reset and sign-out unavailable until identity backend exists |
| ui.appearance | Appearance | Persistent Light/Dark/System selection; no inert controls | preference source implemented; CI/device verification and D-015 appearance preview pending |
| ui.explore | Scientific capability catalogue | Registry-backed availability and clear maturity | 68 capability cards plus Public Reference Databases; exact Android runner availability is shown honestly per service |
| ui.work | Work/job list | Real import/job lifecycle actions | source implemented; full test and device evidence required |

D-016 acceptance applies to every row: a screen is not complete until its actions, persistence, accessibility and relevant tests are demonstrated on the exact tested artifact.

## Design authority

D-024 owner V1 monochrome specification in `docs/ui/ui-spec.md` is the active visual authority. D-015 is historical where its visual language conflicts. Preserve owner assets byte-for-byte; do not claim screenshot fidelity until repository reference images have been visually compared with actual running-app screenshots.
