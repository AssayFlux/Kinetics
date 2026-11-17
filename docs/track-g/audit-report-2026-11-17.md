# Track G — Governance, assurance and publication readiness: closure audit

**Audit date:** 2026-11-17  
**Repository:** `AssayFlux/Kinetics`, branch `main`  
**Engineering baseline:** `7fdfce3147b5df2e4be6261beba48c7a41bf0bbe`  
**Prior exact-head baseline workflow:** [#44098272029](https://github.com/AssayFlux/Kinetics/actions/runs/44098272029), 9/9 jobs passed.  
**Final audit-increment workflow:** [#44106428668](https://github.com/AssayFlux/Kinetics/actions/runs/44106428668); result to be confirmed after this documentation increment.

## Decision

**G0–G7 bounded research-only governance software foundation: IMPLEMENTED.**  
**Track G engineering audit: pending exact-head verification of the final audit increment.**  
**Overall Track G acceptance: OPEN.**

This is not a legal opinion, privacy determination, ethics decision, QMS certification, security certification, scientific validation, regulatory clearance, publication endorsement or release authorization.

## Verified engineering foundation

| Work package | Repository implementation | Automated evidence | Non-automated evidence still open |
|---|---|---|---|
| G0 Governance | Stable control IDs, 30-control register, eight-row requirements traceability, role/cadence model and decision links | Structural checker and regression tests | Owner policy acceptance; named accountable role appointments |
| G1 Security | Canonical cross-stack threat model, UI supplement, 16-case security matrix, security policy and incident procedure | Android source configuration guardrails; parser/import unit tests | Merged-manifest and physical-device tests, fuzzing, private vulnerability-channel exercise, independent assessment/retest |
| G2 Supply chain | Source SPDX inventory, dependency decision register, build dependency capture | CI captures Gradle runtime/build-environment graphs, Cargo tree/metadata, resolved artifact hashes and Android Python-wheel hashes | Complete resolved SPDX/CycloneDX SBOM, build-tool/plugin completeness, vulnerability/license review, file-level notices and bundle decisions |
| G3 Quality | Requirements traceability, change/review cadence, CAPA register template, release checklist | Governance structure and traceability checks | QMS applicability advice, actual review records, CAPA effectiveness evidence and owner-approved release controls |
| G4 Privacy | Eight source-level data-flow entries, data classifications, privacy policy and prohibited-data boundary | Android source manifest guardrails (no INTERNET permission, backup disabled, cleartext disabled) | Merged-manifest/provider/device/network tests, retention/deletion UX evidence, qualified privacy/legal advice and jurisdiction decisions |
| G5 Scientific integrity | Generated capability claims matrix for 68 executable tool capabilities; conservative wording and validation/device/license gaps | Registry-to-claims reproducibility and structure tests | Independent truth sets, biological/clinical validation, ancestry/subgroup/missingness analyses and domain review |
| G6 Publication | Claim-evidence ledger schema, publication integrity and authorship/reproducibility protocol | Ledger structure check | Evidence-backed claim rows, reproducible literature review, author/contribution/conflict approvals and peer/editor decisions |
| G7 Operations | Incident response, stop-work, rollback, access, backup/recovery and five tabletop scenarios | Structural checks keep the scenarios explicit as templates | Named operators, tabletop exercises, access review, restore exercise and dated governance review |

## Exact-head automated baseline

Workflow [#44098272029](https://github.com/AssayFlux/Kinetics/actions/runs/44098272029) passed 9/9 jobs on `622ffc1705fda3161478b710fe2f5a4af65c6287`.

- Python: 534 passed, 9 skipped.
- Ruff and mypy: passed.
- Governance checker and generated capability-claims reproducibility check: passed.
- Android arm64 debug APK/AAB build, package alignment and JVM unit tests: passed.
- Host numerical/reference and engine smoke jobs, dependency inventory job and Node worker security tests: passed.

The final G increment adds explicit validation of the 16 security test IDs, eight data-flow IDs, eight G requirement rows, unassigned specialist roles and five not-run tabletop templates. It also adds regression tests and expands raw dependency evidence capture. The final increment must pass workflow [#44106428668](https://github.com/AssayFlux/Kinetics/actions/runs/44106428668) before this audit can be called exact-head verified.

## Explicit non-claims and open gates

1. **Roles:** the repository owner is identified; specialist security, science, privacy, data, quality, release and publication roles remain UNASSIGNED. No credentials or appointments are invented.
2. **Licensing:** the project license is Apache-2.0. Third-party artifact and data redistribution decisions remain unresolved. Raw dependency reports and hashes are not a complete SBOM or legal clearance.
3. **Security:** no independent penetration/mobile security assessment or physical-device security test is recorded. A source threat model and passing CI are not a penetration test.
4. **Privacy:** the inspected source manifest has no INTERNET permission, disables backup and disallows cleartext traffic. Merged-manifest, OEM/provider behavior, on-device traffic and jurisdictional legal review remain unverified.
5. **Scientific integrity:** generated claims describe software implementation conservatively. No independent biological/clinical validation, ancestry coverage result or generalisability claim is created by this audit.
6. **Publication:** the manuscript claim ledger has no supported claim rows. No authorship, funding, conflict, literature novelty, journal fit or peer-review decision is fabricated.
7. **Operations:** tabletop templates remain NOT RUN. No access review, backup restore, incident response exercise or CAPA effectiveness check is claimed.
8. **P0:** remains BLOCKED / NOT APPROVED. No patient/clinical data, human-subject work, individual PGx interpretation, diagnosis, treatment/dosing recommendation or Clinical Mode is authorized.

## Track-order disposition

Under D-023, Track G precedes Track U. G's bounded software implementation and exact-head audit may be closed only after the final workflow succeeds. Overall governance acceptance and all external gates remain carry-forward obligations; they are not waived by engineering closure. Track U must not be represented as having passed G's external acceptance gates.

## Final status vocabulary

- **Engineering foundation:** implemented.
- **Automated verification:** baseline passed; final audit increment pending at report authoring.
- **Independent/external assurance:** open.
- **Operational exercises:** not run.
- **Overall Track G acceptance:** open.
