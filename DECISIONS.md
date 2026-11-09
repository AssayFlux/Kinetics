# Kinetics — Decision Log
Open questions are not decisions. Record date, context, options, choice, consequences and approver. Changes to direction, scope, language, engine tier, license, data source or regulatory posture require an entry.

## Decision register
| ID | Date | Topic | Status | Approver |
|---|---|---|---|---|
| D-000 | 2026-11-07 | Adopt owner master and living direction files | Approved — owner approved baseline in chat | Project owner |
| D-001 | 2026-11-07 | Project LICENSE | Approved — Apache-2.0 selected; canonical LICENSE text added at repository root | Project owner |
| D-002 | 2026-11-07 | Target jurisdictions and applicable privacy/medical-device laws | Approved strategic scope — global, including future clinical use; jurisdiction-specific clearance remains mandatory | Project owner; qualified advisers required for implementation |
| D-003 | 2026-11-07 | Research-paper framing and venue(s) | Approved — multiple papers over time; owner requests guidance at milestones | Project owner |
| D-004 | 2026-11-07 | Clinical advisory board/advisers | Approved — defer recruitment until software is more mature; P0 remains blocked pending qualified advisers | Project owner |
| D-005 | 2026-11-07 | Gene-scope breadth | Approved strategic direction — both a comprehensive PGx gene panel and a broad cross-domain gene catalogue; exact inventories and rollout are staged by evidence | Project owner |
| D-006 | 2026-11-07 | Target Android devices/minimum support matrix | Approved — Android 10+ (API 29), 64-bit ARM; low-end, mid-range and flagship test tiers | Project owner |
| D-007 | 2026-11-07 | Source-master archival | Resolved operationally — reconstructed from owner's complete chat-supplied master at docs/origin/KINETICS_MASTER.md; not represented as a Git move | Owner instruction |
| D-008 | 2026-11-07 | Authorization to execute R1–R3 | Approved — proceed sequentially, subject to each phase's evidence, safety and exit gates; not a waiver or completion sign-off | Project owner |
| D-009 | 2026-11-08 | Parallel Track S implementation sequencing | Approved — begin independently implementable S1 preparation while R1–R10 continue; dependent rendering and S2–S5 gates remain | Project owner |
| D-018 | 2026-11-09 | Engineering language ownership and integration standard | Approved — owner-directed target stack and shared JSON Schema contract standard | Project owner |
| D-019 | 2026-11-09 | Sequential track execution order | Approved — R → S → I → P → G, two steps per track; supersedes D-009 parallel sequencing | Project owner |\n| D-020 | 2026-11-09 | Close R host audit and proceed to S | Approved — close the R implementation/host-regression audit on exact-source CI #2126, consolidate documentation, then begin S. Does not waive or relabel open R device, external-science, licensing, security, accessibility or release evidence | Project owner |

## D-000 — Direction baseline (approved)
- Context: Owner supplied complete Kinetics master and instructed work to follow Parts 1–18 with approval gates.
- Options: (a) adopt master and derive living direction files; (b) implement without controlled baseline.
- Choice: (a), approved by the project owner in chat on 2026-11-07.
- Consequences: R0 is current workstream; no scientific claims or clinical features without evidence/gates. Master is historical source; NORTH_STAR/ROADMAP/DECISIONS become operational source of truth after approval.
- Approver: Project owner (explicit approval received 2026-11-07).

## Standing guidance and deferred checkpoints
- D-003: Guide the owner through paper framing, evidence readiness, authorship details and venue selection when R1–R3 evidence is available; this is a staged publication plan, not a manuscript approval.
- D-004: Revisit clinical-adviser recruitment after the research platform reaches the maturity checkpoint (target after R3), and before P0 or any PGx/clinical-scope work. P0 remains blocked until qualified advisers and all other prerequisites are satisfied.
- D-005: Maintain both the comprehensive, expandable PGx workstream and broad cross-domain gene catalogue. Inventory and implementation are evidence-led; catalogue inclusion does not imply implementation or validation.
- D-006: Android 10+ (API 29), arm64-v8a and low/mid/flagship test tiers are target requirements, not verified support claims. R1 must still establish actual device limits.

## D-004 — Clinical adviser timing (approved)
- Date: 2026-11-07.
- Context: Decide when to recruit clinical advisers for Kinetics' possible future clinical/PGx work.
- Options considered: formal advisory board early; recruit one adviser first; defer advisers until software is more mature; remain research-only indefinitely.
- Choice: Defer all clinical adviser recruitment until the software is more mature (owner selected option 3).
- Consequences: Do not spend effort recruiting a clinical advisory board during the current R1 engineering-feasibility phase. Revisit adviser recruitment after the research platform reaches a meaningful maturity milestone (target review point: after R3), and before P0, PGx gene-set selection, patient-related workflows, clinical studies or any clinical-scope implementation. P0 remains blocked until qualified advisers and all other required legal, ethics, regulatory, QMS and evidence prerequisites are satisfied. This timing decision does not authorize patient data, clinical features or clinical claims; Research Mode remains the only public mode and Clinical Decision Support Mode remains disabled. If the project approaches a gated activity earlier than expected, pause and recruit/consult qualified advisers before proceeding.
- Approver: Project owner, explicit selection in chat on 2026-11-07.

## D-003 — Research-paper strategy (approved)
- Date: 2026-11-07.
- Context: Choose a publication strategy that is credible, evidence-led and manageable across Kinetics' broad scientific scope.
- Options considered: software/methods paper; bioinformatics application paper; broad multidisciplinary paper; multiple papers over time.
- Choice: Multiple papers over time (owner selected option 4).
- Consequences: The initial publication should focus on the platform/software/methods and be attempted only when R1–R3 provide sufficient reproducible implementation, validation and benchmark evidence. Later domain-specific papers may be developed separately when each domain has independently validated workflows and appropriate reference comparisons. Do not combine unsupported capabilities into broad claims or invent results. Venue selection, author order, affiliations, funding, competing interests and manuscript claims require later owner review against the venue's then-current requirements. The assistant should guide the owner through these decisions at relevant milestones; this does not replace owner approval or scientific peer review.
- Approver: Project owner, explicit selection in chat on 2026-11-07.

## D-002 — Target jurisdictions (approved strategic scope)
- Date: 2026-11-07.
- Context: Establish the intended geographic ambition for Kinetics, including the possibility of future clinical functionality.
- Options considered: India-first; India + US; India + EU/UK; global research-only; global including future clinical use.
- Choice: Global scope, including future clinical use (owner selected option 5).
- Consequences: The long-term product ambition is international, and future clinical use may be pursued. This is not a finding of legal compliance, regulatory clearance, market authorisation or permission to process patient data in any country. Research Mode remains the only public mode; Clinical Decision Support Mode remains disabled. Before any patient-data workflow, clinical feature, clinical study or market entry, identify each relevant jurisdiction and obtain qualified local privacy, health-data, medical-device/software, research-ethics and other applicable advice/approvals. P0 and all existing clinical, ethics, security and evidence gates remain mandatory. No single global approval is presumed.
- Approver: Project owner, explicit selection in chat on 2026-11-07.

## D-001 — Project license (approved)
- Date: 2026-11-07.
- Context: Select a project-level license that supports academic and commercial adoption while providing explicit patent terms.
- Options considered: MIT, Apache-2.0, GPL-3.0, AGPL-3.0 and proprietary licensing.
- Choice: Apache License 2.0 (Apache-2.0).
- Consequences: The project distributes its own original code under Apache-2.0; the canonical license text is now present at the repository root. Each third-party engine, dependency, model and data pack remains subject to separate license verification; this decision does not relicense third-party materials.
- Approver: Project owner, explicit selection in chat on 2026-11-07.

## D-006 — Android device target (approved)
- Date: 2026-11-07.
- Context: Set the Android OS/ABI target and physical-device test breadth for R1 and later support claims.
- Choice: Option 1 — Android 10+ (API 29), 64-bit ARM (arm64-v8a), with low-end, mid-range and flagship device test tiers.
- Consequences: This is the intended compatibility target and test strategy, not proof that all Android 10+ devices work. R1 must verify emulator and physical arm64 behaviour and establish evidence-based RAM, storage, performance and device support limits. CI/emulator success alone does not constitute physical-device validation. No R1 go/no-go or R2 authorization is implied.
- Approver: Project owner, explicit selection in chat on 2026-11-07.

## New decision template
- Date / ID:
- Context:
- Options:
- Choice:
- Consequences / roadmap impact:
- Approver:
- Evidence:


## D-008 — Authorization to execute R1–R3 sequentially (approved)
- Date: 2026-11-07.
- Context: Owner explicitly approved “R1, R2 & R3” after clarification of the earlier ambiguous “R2 & R2” message.
- Choice: Proceed with the R1, R2 and R3 workstreams in sequence.
- Consequences: This is authorization to execute the approved roadmap phases, not a finding that any phase has passed its exit criteria. R1 remains in progress and currently has a documented Android build blocker at Chaquopy Biopython dependency resolution. R2 may begin only after R1 evidence is complete and the R1 go/no-go is documented; R3 may begin only after R2's exit evidence and approval. All scientific validation, third-party licensing, device verification, security, privacy, clinical and P0 gates remain in force. No clinical mode, patient-data workflow or clinical claim is authorized by this decision.
- Approver: Project owner, explicit approval in chat on 2026-11-07 (“Approved R1,R2&R3”).
- Evidence: Owner approval message in project conversation; phase completion evidence remains outstanding and must be recorded separately.


## D-009 — UI/UX master specification (2026-11-08)
- Context: Owner supplied `KINETICS_UI_SPEC.md` and instructed parallel Track U and R0–R10 work.
- Choice: Adopt the UI specification as governing UI contract and execute U0 foundations now.
- Visual direction: NOT APPROVED. Three neutral proposals (Precision Lab, Field Notes, Dark Instrument) are studies only; owner selection is required before theme lock.
- Brand: Owner assets only. Existing `Assets/Brand Logo.svg` is preserved but not assumed to be approved app/brand master. Placeholders are development-only and block release.
- Security: Offline-only/no automatic cloud backup are conservative proposals; app lock/vault lock/panic wipe remain review items. Clinical mode remains disabled.
- Consequences: U0 records tokens, schema, asset contract, threat-model draft, verified platform facts and quality/device templates. Stop after presenting three working gallery directions for owner choice.
- Approver: Owner authorised execution; visual-direction and security-default sub-gates remain open.


## D-010 — Dark-first visual preference and theme-family scope (2026-11-08)
- Context: Owner supplied the AssayFlux animated organization logo and requested a futuristic dark design, with selectable light, dark and neon palette families and 20+ distinct fonts.
- Choice: Record dark-first/futuristic as the preferred direction; provide 4 light, 5 dark and 4 neon palette proposals and 26 distinct font-family candidates. Initial Compose shell defaults to dark and exposes Light/Dark/Neon selection.
- Not approved: No final palette, exact seed colour, font family bundle, app-logo treatment or design-system direction is locked. The U0 visual gate remains open for owner review.
- Brand constraint: Preserve the uploaded organization logo artwork; no recolouring, redraw, sampling or derivative app mark. Existing `Assets/Brand Logo.svg` remains unchanged.
- Consequences: Theme token generator, contrast/CVD audits, exact font licence audit, durable settings persistence and compact/medium/expanded gallery previews remain required. Font catalogue entries are candidates, not proof of redistribution rights.
- Approver: Owner supplied the direction in chat on 2026-11-08; final U0 visual choice is pending.
- Evidence: `design/tokens.json`, `design/typography-catalogue.yaml`, `docs/ui/theme-proposals.md`, `assets/design-previews/`.


## D-011 — Select Obsidian Cyan as the default UI direction (2026-11-08)
- Context: Owner requested a futuristic dark UI, light/dark/neon theme families, and then authorized us to complete the visual design using best judgement.
- Choice: Use Obsidian Cyan as the default dark-first direction: near-black/navy surfaces, cyan primary actions, electric-blue secondary accents and restrained mint status accents. Retain Light and Neon as selectable alternatives. This is an implementation choice under the owner's broad authorization, not a claim of measured superiority.
- Brand: Do not sample brand artwork for seed colours or alter the organization logo. The owner-provided astronaut background is used as supplied on the Home hero.
- Consequences: Palette contrast/CVD validation, token generation, gallery screenshots, adaptive layouts and owner visual review remain U0 work. Any contrast failure must be fixed in tokens, not by changing the logo.
- Approver: Owner authorized completion by best judgement in chat on 2026-11-08.


## D-012 — Responsive shell implementation strategy (2026-11-08)
- Context: The UI shell needs compact, medium, expanded and large-window navigation while preserving the current stable Material 3 dependency set.
- Choice: Implement live app-window classification in Compose and use Material 3 NavigationBar, NavigationRail and PermanentNavigationDrawer. Compact portrait uses bottom bar; medium/expanded and compact-height windows use rail; large/extra-large (≥1200dp) uses permanent drawer. Readable content is capped at 840dp.
- Deviation: NavigationSuiteScaffold and WindowManager fold-posture APIs are not yet integrated. This is temporary; no fold-aware or hinge-safe claim is permitted. Extend after adaptive-library compatibility and posture tests are verified.
- Evidence: WindowLayout.kt and WindowLayoutTest.kt; CI build/test pending. Device matrix remains NOT RUN.


## D-009 — Parallel Track S implementation sequencing (approved)
- Date: 2026-11-08.
- Context: Owner explicitly directed completion of R1–R10 and commencement of Track S without another approval pause.
- Choice: Begin independently implementable S1 preparation in parallel with R1–R10. This supersedes the earlier sequencing prohibition only to the extent of non-dependent work.
- Consequences: Deterministic structure-view payload preparation and its contract/tests may proceed. Full WebView rendering remains dependent on R1 WebView/runtime feasibility and exact third-party license review. S2–S5 retain all scientific, model-license, node-security and benchmark gates. No phase is complete by this decision; no validation, clinical, patient-data or release gate is waived.
- Approver: Project owner, explicit instruction in chat on 2026-11-08.


## D-013 — Owner-supplied application UI reference designs (2026-11-08)
- Context: Owner added two visual reference assets to the repository: `Assets/App UI - Dashboard Design.jpg` and `Assets/App UI - Login Page Design.jpg`. The owner states these represent the design language they like and wants the Kinetics application UI to follow that language.
- Choice: Treat both images as first-class owner-supplied visual references for the Kinetics product UI. Apply their visual language consistently across dashboard, authentication/onboarding, navigation, cards, typography, spacing, colour, iconography and interaction patterns where the references provide evidence. Preserve the original image files unchanged. Scientific workflow clarity, accessibility, responsive behaviour, offline-first operation and existing brand-asset constraints remain mandatory.
- Boundary: Do not infer detailed visual properties from filenames or replace the reference designs with the existing generic theme proposals. The binary assets are present in the repository, but direct visual inspection is still required before extracting exact tokens or declaring a visual match. The final implementation must be reviewed against the images and validated with real screenshots across supported window classes.
- Approver: Owner explicitly confirmed this preference in project conversation on 2026-11-08.
- Evidence: The two repository assets listed above; visual comparison and screenshot evidence pending.


## D-014 — Light classic visual direction and calligraphic typography (2026-11-08)
- Context: Owner clarified that the dashboard reference's colours are placeholders only, selected a light classic interface, and requested designed calligraphic typography.
- Choice: Set the product's intended default visual direction to Light Classic. Preserve the reference's composition and component language (rounded hero region, prominent carousel, spacious cards, simple top controls and clear content hierarchy), but do not copy its pastel palette. Use a restrained classic scientific palette with light neutral surfaces, dark readable text and a controlled navy/teal accent system; exact colour tokens remain subject to contrast and screenshot validation.
- Typography proposal for implementation: Allura as a limited calligraphic brand signature/wordmark accent; Cormorant Garamond for selected editorial display headings; Inter for navigation, controls and body copy; JetBrains Mono for sequences, identifiers, code and scientific values. Do not use script typography for dense content, controls, labels, tables or scientific notation.
- Licensing and accessibility: These are font-family candidates, not approved bundled binaries. Verify exact upstream releases, licence texts, glyph coverage, weights, file size, rendering and contrast before packaging. Provide accessible sans-serif fallbacks. Do not claim visual completion until real app screenshots are reviewed against the owner's references.
- Supersedes: D-010/D-011 only for the default visual theme and typography direction; it does not remove the option to offer dark themes. D-013's owner-supplied layout references remain primary.
- Approver: Project owner, explicit selection/request in chat on 2026-11-08.
- Evidence: Owner dashboard reference image and chat instruction; login reference and screenshot comparison remain pending.


## D-015 — Owner-approved Kinetics Light Classic visual system (2026-11-08)
- Context: Owner reviewed the six-screen visual concept (splash, login, dashboard carousel, navigation drawer, profile and appearance) and explicitly approved it with “Love it” and directed that the new design be documented and implemented carefully.
- Choice: Adopt the visual system in `docs/ui/kinetics-visual-design-system.md` as the current product UI authority. Light Classic is the default: warm ivory/cream, deep maroon, restrained gold and peacock teal; retain a coherent Dark Classic and System appearance. Preserve the reference composition: rounded surfaces, prominent central horizontal workspace carousel with adjacent cards peeking, pagination, generous spacing and stacked real-data cards. Use culturally respectful, attributed motifs only after their dedicated evidence gates.
- Typography roles: Great Vibes (limited brand-script candidate only if no existing logo wordmark), Cormorant Garamond (display headings), IBM Plex Sans (functional UI/body), IBM Plex Mono (scientific data/code); Indic-script fallback must be verified. Font binaries remain subject to exact version/licence/glyph/size/offline verification before bundling.
- Constraints: Existing Compose architecture, capability registry, real-data-only UI, owner logo bytes, accessibility, privacy, security, offline-first policy, research-only public mode and all R/S/I/P gates remain in force. The generated showcase is concept art, not implementation or screenshot evidence.
- Supersedes: D-009's unresolved three-proposal visual gate; D-010/D-011's dark-futuristic/Obsidian-Cyan default and neon-first direction; D-014's Light Classic navy/teal palette and Allura/Inter/JetBrains Mono typography proposal where inconsistent with D-015. D-012 responsive shell strategy and D-013 owner layout references remain active where compatible. Earlier entries remain in the log for audit history, not as current UI instructions.
- Approver: Project owner, explicit visual approval and implementation instruction in chat on 2026-11-08.
- Evidence: Owner-approved concept review in project conversation; canonical specification at `docs/ui/kinetics-visual-design-system.md`. Implementation, screenshots, contrast and device validation remain open.

## UI decision supersession register
The following historical decisions are retained for auditability but are no longer active design instructions: D-009 (three-proposal visual gate), D-010 (dark-first preference), D-011 (Obsidian Cyan default), and D-014 (previous Light Classic palette/type proposal). D-015 is the current visual authority. D-012 adaptive navigation and D-013 owner layout-reference decisions remain active unless specifically contradicted by D-015.

## D-016 — Integrated build/test cycle and active UI direction reaffirmed
- Date: 2026-11-08.
- Context: Owner found that successful APK compilation had been mistaken for a working application: D-015 was not fully implemented, authentication/biometrics were absent, and several options were inert or informational.
- Choice: Approved. Implement substantial vertical slices, build arm64 APK/AAB, test affected systems and regression suite, inspect/install the exact artifact where hardware permits, fix failures, and repeat. Testing is part of every cycle, not deferred to the end. Record source commit and artifact SHA-256.
- Active design: D-015 Light Classic is the sole current UI authority, with Dark Classic and System. Earlier neon/Obsidian Cyan and pre-D-015 palette proposals are discontinued for active implementation and retained only as historical audit records.
- Authentication boundary: No fictitious cloud/account authentication. Local app-lock must be distinguished from account identity and have secure key lifecycle/recovery. Biometric unlock uses AndroidX BiometricPrompt, runtime capability/enrollment checks, explicit opt-in, credential fallback, lockout/error handling and Keystore-backed cryptographic operations where appropriate. Kinetics never stores biometric templates or passwords.
- Functionality: Every visible control executes a real action, navigates to an implemented screen, or is visibly disabled with an explanation. Research tools are launchable only with registry capability, input contract, dispatcher, result model/viewer and tests. No fake metrics, authentication success or scientific output.
- Evidence: Distinguish source implementation, automated tests, reference validation, CI build, emulator verification and physical-device verification. Build success alone is not a tested app. Missing hardware tests remain blockers.
- Consequences: ROADMAP contains the mandatory cycle. UI screen map, quality report, registry and session log must be updated with each cycle.
- Approver: Project owner, explicit instruction in chat on 2026-11-08.


## D-017 — Owner authorization for safe P-track public-data engineering preparation
- Date: 2026-11-09.
- Context: The owner explicitly reiterated permission to proceed with the P track. The existing P0 boundary distinguishes public, non-patient research preparation from patient-data, human-subject and clinical activities.
- Choice: Proceed immediately with P1 public-data-only engineering preparation in parallel with R/S/I work: catalogue/schema validation, synthetic fixtures, dataset provenance and reproducibility infrastructure, and non-clinical research tooling. Do not wait for P0 to build these safe foundations.
- Constraints: This authorization does not approve patient or human-subject data intake, clinical interpretation, genotype-to-phenotype recommendations, diagnosis/treatment/dosing, Clinical Mode, or claims of clinical validity/utility. P0 remains blocked until the existing legal, ethics, privacy, security, qualified-adviser, validation and owner-approval evidence is complete. D-004 adviser timing remains active; review after R3 and before any P0-gated activity.
- Approver: Project owner, explicit permission reiterated in chat on 2026-11-09.


## D-018 — Owner-directed language ownership and integration contract
- Date: 2026-11-09.
- Context: The owner supplied an explicit engineering role, target stack ownership, integration-first workflow, interface-contract requirements, security rules and response/checklist requirements, and asked that they be documented and followed.
- Choice: Adopt `docs/ENGINEERING_INTEGRATION_STANDARD.md` as the mandatory engineering workflow and target ownership model: Python scientific analysis; C++ performance-critical core; Rust security; Kotlin Android; Swift iPhone; HTML/CSS/TypeScript with Three.js for offline 3D visualisation; Bash build/test/deploy automation only. Adopt JSON Schema as the semantic source of truth for cross-component engine messages, initially `api/engine-envelope-v1.schema.json`.
- Consequences: The standard is normative for new work. Existing code is not represented as conforming merely because it exists. Current Rust/C++ code is a smoke-test probe, Swift and TypeScript/Three.js sources are absent, and current Chaquopy/JNI edges must be migrated or explicitly mapped through reviewed, tested vertical slices. iOS minimum version/team experience remain TBD. No new clinical scope is authorized. No interface is silently changed by this documentation decision.
- Approver: Project owner, explicit instruction in chat on 2026-11-09.


## D-019 — Sequential track order and two-step gates (supersedes D-009)
- Date: 2026-11-09.
- Context: The owner explicitly reset execution order after earlier parallel-track instructions and requires a controlled base-first workflow.
- Choice: Work tracks strictly in this order: **R → S → I → P → G**. For each track, Step 1 builds the documented base; Step 2 audits, tests and completes/fixes remaining base work. Do not begin the next track until the current track's two-step gate has been honestly assessed and reported.
- Consequences: D-009's permission to develop S in parallel with R is superseded for current execution. Dependencies and safety gates remain. Report completion percentage only after the two-step gate and define the denominator; never claim full track completion if documented exit criteria remain unmet.
- Approver: Project owner, explicit instruction in chat on 2026-11-09.


## D-020 — R engineering audit closure and transition to S
- Context: The owner requested completion of the R-track audit, documentation consolidation, and transition to S.
- Evidence: Exact-source commit `888e49bc7108a2609db97d76193a60d5eec175e0`; CI #2126 passed all five jobs, including Android arm64 APK/AAB build, JVM tests, Python 238 passed/4 skipped, host scientific-reference comparisons, RDKit sanity and direct SPDX inventory.
- Choice: Close the R implementation/host-regression audit step, consolidate the repository documentation, and proceed to S as the next engineering track.
- Boundary: This is not a declaration that R1–R10 are all phase-accepted, scientifically validated, device-verified, fully licensed or release-ready. Open R evidence remains in the R audit and master roadmap as carry-forward obligations; dependent S work must respect those gaps.
- Approver: Project owner (explicit instruction in chat, 2026-11-09).
