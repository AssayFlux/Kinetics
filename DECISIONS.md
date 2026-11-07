# Kinetics — Decision Log

This log records decisions that affect direction, scope, language, engine tier, license, data source, privacy, ethics or regulatory posture. Options and consequences must be recorded; owner approval is required where stated. Open questions are not decisions.

## Decision register

| ID | Date | Topic | Status | Approver |
|---|---|---|---|---|
| D-000 | 2026-11-07 | Establish master specification as governing project direction; create four living direction files | Proposed — awaiting owner review | Project owner |
| D-001 | 2026-11-07 | Project LICENSE | Open — no license selected or added | Project owner |
| D-002 | 2026-11-07 | Target jurisdictions and applicable privacy/medical-device laws | Open | Project owner with qualified legal/regulatory advisers |
| D-003 | 2026-11-07 | Research-paper framing and target venue(s) | Open | Project owner |
| D-004 | 2026-11-07 | Clinical advisory board/advisers | Open — identities and commitments not supplied | Project owner |
| D-005 | 2026-11-07 | First PGx gene set | Open — no genes selected | Project owner with clinical advisers |
| D-006 | 2026-11-07 | Target Android devices and minimum supported-device matrix | Open | Project owner |
| D-007 | 2026-11-07 | Exact source-master archival | Blocked — no root `KINETICS_MASTER.md` found in inspected default-branch tree | Project owner |

## D-000 — Direction baseline (proposed)

- **Context:** The project owner supplied a comprehensive Kinetics master specification and instructed that it govern implementation from Part 1, with approval gates and strict scope control.
- **Options:** (a) treat the supplied master as authoritative and derive NORTH_STAR/ROADMAP/DECISIONS/SESSION_LOG; (b) begin implementation without a controlled direction baseline.
- **Proposed choice:** (a), subject to owner review of the four living files.
- **Consequences:** R0 is the only current workstream; no science feature work until its dependencies and gates are satisfied. The master remains historical source material; living files become operational source of truth after approval.
- **Approver:** Pending explicit project-owner approval.

## Open decisions requiring owner input

1. **Project license:** choose only after reviewing intended distribution, dependency compatibility and any GPL/AGPL implications. No LICENSE file or placeholder license text is to be committed as if selected.
2. **Target jurisdictions:** identify intended countries/regions for users and data subjects. Obtain qualified advice on applicable data-protection, research-ethics and medical-device rules before relevant data/features.
3. **Paper framing and venue:** choose only after evidence exists and after checking current scope/requirements of candidate venues. Author names, affiliations, funding and competing interests are owner-supplied.
4. **Clinical advisers:** identify a clinical pharmacologist or pharmacist, clinical geneticist and physician, with roles/availability confirmed before P0 can pass.
5. **First PGx gene set:** select with clinical advisers based on guideline maturity, reference materials, caller reliability and scope. No gene set is assumed here.
6. **Target devices:** specify actual Android phones/tablets and emulator targets, including baseline 4 GB RAM arm64 test device, before feasibility claims or support commitments.
7. **Original master archival:** the inspected `main` tree has no root `KINETICS_MASTER.md`. Confirm whether to reconstruct `docs/origin/KINETICS_MASTER.md` from the supplied session text or provide/commit the canonical file. Do not claim a move has occurred when there was no source file to move.

## Recording a new decision

For each new entry include: date; context; options considered; chosen option; consequences and affected roadmap items; approver; evidence/links where applicable. Do not silently convert an open question into a decision. Changes to NORTH_STAR require explicit owner approval.
