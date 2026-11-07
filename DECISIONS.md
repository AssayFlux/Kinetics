# Kinetics — Decision Log
Open questions are not decisions. Record date, context, options, choice, consequences and approver. Changes to direction, scope, language, engine tier, license, data source or regulatory posture require an entry.

## Decision register
| ID | Date | Topic | Status | Approver |
|---|---|---|---|---|
| D-000 | 2026-11-07 | Adopt owner master and living direction files | Approved — owner approved baseline in chat | Project owner |
| D-001 | 2026-11-07 | Project LICENSE | Approved — Apache-2.0 selected; canonical LICENSE grant file still to be added and verified | Project owner |
| D-002 | 2026-11-07 | Target jurisdictions and applicable privacy/medical-device laws | Open — qualified advice required | Project owner + advisers |
| D-003 | 2026-11-07 | Research-paper framing and venue(s) | Open — decide after evidence and venue review | Project owner |
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
1. Jurisdictions: owner identifies countries/regions; obtain qualified advice before relevant data/features.
2. Paper framing/venue: owner decides after evidence exists and current venue requirements are checked. Owner supplies authors, affiliations, funding and competing interests.
3. Clinical advisers: identify clinical pharmacologist/pharmacist, clinical geneticist and physician; P0 cannot pass without them.
4. First PGx gene set: choose with advisers based on guideline maturity, reference materials and caller reliability.
5. Target devices: owner specifies Android devices and emulator targets before feasibility/support claims.

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
