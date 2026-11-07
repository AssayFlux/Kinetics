# Kinetics — Decision Log
Open questions are not decisions. Record date, context, options, choice, consequences and approver. Changes to direction, scope, language, engine tier, license, data source or regulatory posture require an entry.

## Decision register
| ID | Date | Topic | Status | Approver |
|---|---|---|---|---|
| D-000 | 2026-11-07 | Adopt owner master and living direction files | Approved — owner approved baseline in chat | Project owner |
| D-001 | 2026-11-07 | Project LICENSE | Approved — Apache-2.0 selected; canonical LICENSE grant file still to be added and verified | Project owner |
| D-002 | 2026-11-07 | Target jurisdictions and applicable privacy/medical-device laws | Approved strategic scope — global, including future clinical use; jurisdiction-specific clearance remains mandatory | Project owner; qualified advisers required for implementation |
| D-003 | 2026-11-07 | Research-paper framing and venue(s) | Approved — multiple papers over time; owner requests guidance at milestones | Project owner |
| D-004 | 2026-11-07 | Clinical advisory board/advisers | Open — identities/commitments not supplied | Project owner |
| D-005 | 2026-11-07 | First PGx gene set | Open — no genes selected | Project owner + clinical advisers |
| D-006 | 2026-11-07 | Target Android devices/minimum support matrix | Open — no devices selected | Project owner |
| D-007 | 2026-11-07 | Source-master archival | Resolved operationally — reconstructed from owner's complete chat-supplied master at docs/origin/KINETICS_MASTER.md; not represented as a Git move | Owner instruction |

## D-000 — Direction baseline (approved)
- Context: Owner supplied complete Kinetics master and instructed work to follow Parts 1–18 with approval gates.
- Options: (a) adopt master and derive living direction files; (b) implement without controlled baseline.
- Choice: (a), approved by the project owner in chat on 2026-11-07.
- Consequences: R0 is current workstream; no scientific claims or clinical features without evidence/gates. Master is historical source; NORTH_STAR/ROADMAP/DECISIONS become operational source of truth after approval.
- Approver: Project owner (explicit approval received 2026-11-07).

## Open decisions
1. Paper framing/venue: multiple papers over time. Start with a platform/software-methods paper only after R1–R3 evidence is adequate and the target venue's current requirements are reviewed; pursue separate domain papers only after the relevant workflows have independent validation. Owner supplies/approves authorship, affiliations, funding and competing interests. Guide the owner through framing, evidence readiness and venue selection at the appropriate milestones.
2. Clinical advisers: identify clinical pharmacologist/pharmacist, clinical geneticist and physician; P0 cannot pass without them.
3. First PGx gene set: choose with advisers based on guideline maturity, reference materials and caller reliability.
4. Target devices: owner specifies Android devices and emulator targets before feasibility/support claims.

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

## New decision template
- Date / ID:
- Context:
- Options:
- Choice:
- Consequences / roadmap impact:
- Approver:
- Evidence:
