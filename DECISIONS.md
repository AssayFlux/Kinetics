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
