# Track G — operational governance controls

**Status:** operating procedure draft; named operators and completed exercises remain open.

## 1. Incident severity and response

| Severity | Examples | Initial response target | Required actions |
|---|---|---|---|
| SEV-1 Critical | Suspected data exfiltration, signing-key compromise, exploitable remote code execution, sensitive data exposure | Immediately upon discovery | Stop affected release/workflow, preserve evidence, restrict access, notify owner and qualified security/privacy contacts |
| SEV-2 High | Authentication bypass, significant local data disclosure, high-impact dependency exploit | Same working day | Contain affected component, assess scope, prepare remediation and disclosure plan |
| SEV-3 Moderate | Limited integrity/availability issue without sensitive disclosure | Within 3 working days | Triage, reproduce, assign owner and corrective action |
| SEV-4 Low | Documentation/control drift or low-impact defect | Next governance review | Record and schedule proportionate correction |

Targets are internal process goals, not a staffed 24/7 response commitment. No public security SLA is claimed.

## 2. First-response checklist

1. Record discovery time, reporter, affected commit/artifact, environment and symptoms.
2. Do not place secrets, patient data or exploit payloads in public issues.
3. Preserve logs and hashes; restrict access to evidence containing sensitive material.
4. Disable or isolate the affected feature/release path where safe; preserve recoverability.
5. Assess confidentiality, integrity, availability, user impact, affected versions and jurisdictions.
6. Engage qualified security/privacy/legal advisers where required.
7. Track remediation, regression test, independent retest, disclosure and owner decision.
8. Record residual risk, review date and closure authority in the incident/CAPA records.

## 3. Stop-work and release rollback

Any team member may raise a stop-work concern. The project owner or delegated incident commander records the stop decision and scope. Release owner must be able to halt distribution, revoke/replace affected artifacts where possible, publish an advisory and restore the last known-good version. No rollback is considered successful until integrity and user impact are checked.

P0, patient/clinical restrictions and legal/ethics obligations cannot be overridden by an operational stop/rollback procedure.

## 4. Access and secrets

- Keep credentials, signing keys, tokens and private reports out of Git, issues, CI logs and artifacts.
- Use least-privilege repository and CI permissions; review access at least monthly and on role changes.
- Keep production signing material outside repository and ordinary CI artifacts.
- Rotate exposed credentials, document scope and verify revocation.
- Do not claim an access review until an actual dated review record exists.

## 5. Backup and recovery

- Define backup scope, encryption, retention, restore authority and key recovery before release.
- Test restoration from a clean environment with integrity hashes.
- Test Keystore invalidation and explain unrecoverable encrypted local data accurately.
- Do not describe deletion of app-visible files as guaranteed physical erasure on flash media.
- Record recovery time, data loss window, failures and corrective actions.

## 6. Tabletop exercise templates

No exercise is marked complete by this template. Run with synthetic data and record participants, scenario, decisions, timestamps, evidence, gaps and CAPA IDs.

| Exercise ID | Scenario | Required decisions | Status |
|---|---|---|---|
| OPS-TT-01 | Suspected malicious dependency discovered after debug build | Stop distribution, identify affected commits/artifacts, revoke/replace, assess notices | NOT RUN |
| OPS-TT-02 | User reports lost device and inaccessible encrypted project | Explain key-loss boundary, assess backup, avoid false recovery promise | NOT RUN |
| OPS-TT-03 | Accidental export of confidential research file | Contain destination access where possible, scope copies, notify appropriately, record limitations | NOT RUN |
| OPS-TT-04 | Parser crash / storage exhaustion from hostile import | Disable path, preserve synthetic reproducer, remediate and regression-test | NOT RUN |
| OPS-TT-05 | New request to process patient data | Stop request, reject intake, refer to P0/qualified review, preserve research-only boundary | NOT RUN |

## 7. Periodic governance review record

Create a dated record at `docs/track-g/reviews/YYYY-MM-DD.md` covering: open control IDs, new/closed risks, dependency/data changes, CI and artifact evidence, vulnerabilities, CAPA effectiveness, role appointments, incidents, publication claims, P0 status and owner decisions. Do not backdate reviews.
