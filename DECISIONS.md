# KINETICS — DECISIONS LOG
**Rule:** append one dated entry for each decision affecting direction, scope, language, tier, license, data source, privacy, ethics or regulatory posture. No entry is approved unless the owner explicitly approves it.

## D-0001 — Adopt supplied grand masterplan and addendum as governing baseline
- **Date:** 2026-11-07
- **Context:** Establish the project direction system and prevent drift.
- **Options:** (A) Use only the grand masterplan; (B) use only the addendum; (C) use both, with addendum prevailing on conflict.
- **Choice:** C — both documents govern; addendum wins where they conflict.
- **Consequences:** Both plan texts remain in repository root. NORTH_STAR, ROADMAP and DECISIONS are operational source of truth. No external/legacy plan is substituted.
- **Approved by:** Owner instruction in project conversation.

## D-0002 — Repository write policy
- **Date:** 2026-11-07
- **Context:** User specified direct repository work.
- **Options:** Work on a feature branch or commit directly to main.
- **Choice:** Direct commits to `main` only; do not create branches.
- **Consequences:** Verify main head before writes; use fast-forward updates only; stop if head changes unexpectedly.
- **Approved by:** Owner instruction in project conversation.

## D-0003 — Initial operating mode and patient-data boundary
- **Date:** 2026-11-07
- **Context:** Precision-medicine features create patient-safety, privacy and regulatory risk.
- **Options:** Build clinical functionality immediately or begin in Research Mode and gate clinical work.
- **Choice:** Research Mode default; Clinical Decision Support Mode disabled in public builds; no real patient data before P0 passes.
- **Consequences:** Track P0 is a hard gate; no patient-related feature before its exit criteria. No autonomous prescribing.
- **Approved by:** Owner instruction in supplied addendum.

## D-0004 — License and regulatory questions remain unresolved
- **Date:** 2026-11-07
- **Context:** Candidate engines/data and jurisdictional rules require source-text verification and qualified review.
- **Options:** Select candidate licenses/jurisdictions now or defer pending evidence and owner decisions.
- **Choice:** Defer. No restrictive license, jurisdictional regulatory posture or clinical claim is selected by assumption.
- **Consequences:** Track G2 and P0 remain open; OMIM/DrugBank and any restrictive/non-commercial terms require explicit owner decision.
- **Approved by:** No substantive selection made; recorded as open constraint, not an approval to use any candidate.

## D-0005 — Paper framing and clinical advisory appointments
- **Date:** 2026-11-07
- **Context:** Publication and clinical workflow claims need owner choices and qualified contributors.
- **Options:** Choose paper framing/venues and advisers now, or keep candidates open.
- **Choice:** Open; no paper framing, venue, author list or adviser is appointed.
- **Consequences:** Track G5 and P0/P5 cannot be marked complete until resolved and evidenced.
- **Approved by:** Pending owner decision.

## Open decisions register
- [ ] Jurisdictions and applicable legal/regulatory advice (India, EU, US or others).
- [ ] Third-party software, model-weight and data licenses; restrictive items including OMIM and DrugBank.
- [ ] Clinical advisory board: named clinical pharmacologist/pharmacist, clinical geneticist and physician.
- [ ] Initial PGx gene set and gene-specific caller/validation plans.
- [ ] Target Android devices and minimum emulator/desktop/remote-node hardware.
- [ ] Paper framing, paper split, target venues and timing.
- [ ] Project LICENSE (owner-only choice).
- [ ] Any GPL/AGPL dependency/bundling decision.
- [ ] Clinical intended-use statement and regulatory classification at P0.
- [ ] Incidental-findings policy and ethics review/exemption pathway.
