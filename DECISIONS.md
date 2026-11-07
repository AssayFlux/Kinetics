# Kinetics — Decision Log
Open questions are not decisions. Record date, context, options, choice, consequences and approver. Changes to direction, scope, language, engine tier, license, data source or regulatory posture require an entry.

## Decision register
| ID | Date | Topic | Status | Approver |
|---|---|---|---|---|
| D-000 | 2026-11-07 | Adopt owner master and living direction files | Approved — owner approved baseline in chat | Project owner |
| D-001 | 2026-11-07 | Project LICENSE | Approved — Apache-2.0 selected; canonical LICENSE grant file still to be added and verified | Project owner |
| D-002 | 2026-11-07 | Target jurisdictions and applicable privacy/medical-device laws | Approved strategic scope — global, including future clinical use; jurisdiction-specific clearance remains mandatory | Project owner; qualified advisers required for implementation |
| D-003 | 2026-11-07 | Research-paper framing and venue(s) | Approved — multiple papers over time; owner requests guidance at milestones | Project owner |
| D-004 | 2026-11-07 | Clinical advisory board/advisers | Approved — defer recruitment until software is more mature; P0 remains blocked pending qualified advisers | Project owner |
| D-005 | 2026-11-07 | Gene-scope breadth | Approved strategic direction — both a comprehensive PGx gene panel and a broad cross-domain gene catalogue; exact inventories and rollout are staged by evidence | Project owner |
| D-006 | 2026-11-07 | Target Android devices/minimum support matrix | Approved — Android 10+ (API 29), 64-bit ARM; low-end, mid-range and flagship test tiers | Project owner |
| D-007 | 2026-11-07 | Source-master archival | Resolved operationally — reconstructed from owner's complete chat-supplied master at docs/origin/KINETICS_MASTER.md; not represented as a Git move | Owner instruction |

## D-000 — Direction baseline (approved)
- Context: Owner supplied complete Kinetics master and instructed work to follow Parts 1–18 with approval gates.
- Options: (a) adopt master and derive living direction files; (b) implement without controlled baseline.
- Choice: (a), approved by the project owner in chat on 2026-11-07.
- Consequences: R0 is current workstream; no scientific claims or clinical features without evidence/gates. Master is historical source; NORTH_STAR/ROADMAP/DECISIONS become operational source of truth after approval.
- Approver: Project owner (explicit approval received 2026-11-07).

## Open decisions
1. Paper framing/venue: multiple papers over time. Start with a platform/software-methods paper only after R1–R3 evidence is adequate and the target venue's current requirements are reviewed; pursue separate domain papers only after the relevant workflows have independent validation. Owner supplies/approves authorship, affiliations, funding and competing interests. Guide the owner through framing, evidence readiness and venue selection at the appropriate milestones.
2. Clinical advisers: owner chose to defer recruitment until the software is more mature. Revisit after the research-platform maturity milestone (target: R3), and before P0 or any PGx/clinical-scope work. P0 remains blocked until the required qualified expertise is identified and engaged.
3. Gene scope (D-005): owner has superseded the earlier focused six-gene selection and requested a large, broad gene scope. Clarify whether this means a comprehensive PGx panel or a cross-domain gene catalogue spanning Kinetics' genomics and other scientific domains. Do not freeze a gene list or claim implementation until clarified. Any PGx panel remains subject to qualified-adviser review, evidence, licensing and validation; P0 and patient/clinical gates remain mandatory.
4. Target devices (D-006): Android 10+ (API 29), 64-bit ARM, with low-end, mid-range and flagship test tiers. This is a target matrix, not a claim that every device is verified.

## D-005 — Gene-scope breadth (reopened; clarification pending)
- Date: 2026-11-07.
- Context: The owner initially selected a focused six-gene PGx starter set, then clarified that the intended scope should cover a much larger and broader range of genes.
- Superseded choice: The six-gene list (CYP2D6, CYP2C19, CYP2C9, VKORC1, TPMT and DPYD) is no longer the agreed scope.
- Current owner direction: Plan for a large, expandable gene scope rather than a fixed six-gene panel.
- Clarification required: Determine whether this means (a) a comprehensive PGx gene panel, or (b) a broad cross-domain gene catalogue for genomics and related Kinetics capabilities. Do not invent a gene count, freeze a list, or treat catalogue coverage as implemented functionality before clarification.
- Consequences: A broad catalogue must be staged by evidence, reference availability, caller/assay reliability, ancestry coverage, licensing, compute feasibility and independent validation. PGx and any patient-related/clinical scope remain gated by qualified advisers, P0, jurisdiction-specific legal/ethics/regulatory requirements and owner approval. Research Mode remains the only public mode; no patient-data or clinical use is authorized.
- Approver: Project owner, explicit clarification in chat on 2026-11-07.

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
- Consequences: The project intends to distribute its own code under Apache-2.0. Each third-party engine, dependency, model and data pack remains subject to separate license verification; this decision does not relicense third-party materials. Add the canonical Apache-2.0 LICENSE text in a separate repository change before representing the grant as present.
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
