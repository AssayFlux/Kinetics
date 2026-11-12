# Track G — accountability and review cadence

**Effective date:** 2026-11-12  
**Authority:** D-023 sequencing; repository owner instruction to execute Track G.  
**Status:** role model defined; named non-owner appointments and governance-policy acceptance remain open.

## Accountability model

A role is not a person. A role marked UNASSIGNED is an explicit gap, not an implied appointment. The repository owner may implement engineering controls but cannot self-certify independent review.

| Role ID | Accountability | Current assignment | Independence / limitation |
|---|---|---|---|
| G-ROLE-OWNER | Scope, policy decisions, risk acceptance, release authorization | Repository owner (GitHub: AssayFlux) | Cannot replace independent assessor, qualified counsel, ethics committee or peer review |
| G-ROLE-ENG | Architecture, implementation, CI, build provenance and technical remediation | UNASSIGNED — appointment required | Implementer must not mark own security/scientific work independently reviewed |
| G-ROLE-SEC | Threat model, vulnerability triage, security review and incident coordination | UNASSIGNED — appointment required | Independent mobile security assessor required before release |
| G-ROLE-SC | Capability claims, validation protocols, scientific review and uncertainty | UNASSIGNED — appointment required | Domain-qualified independent reviewers required for validation |
| G-ROLE-DATA | Dataset/model provenance, access, retention and redistribution records | UNASSIGNED — appointment required | Source-specific rights decisions require qualified review |
| G-ROLE-PRIV | Data flows, privacy requirements, retention and privacy incidents | UNASSIGNED — appointment required | Qualified privacy/legal advice required for applicable jurisdictions |
| G-ROLE-QUALITY | Requirements traceability, change control, defects/CAPA and quality records | UNASSIGNED — appointment required | QMS applicability advice remains external |
| G-ROLE-RELEASE | Artifact inventory, provenance, release checklist and rollback | UNASSIGNED — appointment required | Release approval remains a separate owner decision |
| G-ROLE-PUB | Authorship, claims, conflicts, journal declarations and submission | UNASSIGNED — appointment required | Every author must approve final manuscript and declarations |

## Review cadence

| Trigger | Minimum review | Required record |
|---|---|---|
| Every substantial change | Requirements, risk, test and change-impact review | Commit/PR, reviewer, affected control IDs, CI run |
| Every dependency/data/model update | Version/hash/source/license/provenance review | Updated third-party/data register and generated inventory |
| Every CI release candidate | Exact-head tests, artifact hashes, SBOM coverage and unresolved-finding review | Build evidence record tied to commit and artifact digest |
| Monthly while active | Open risks, vulnerabilities, CAPA, role assignments and evidence freshness | Dated governance review record |
| Before public release | Security, privacy, licensing, accessibility, scientific, device and owner gates | Completed release checklist and recorded decision |
| Before manuscript submission | Claim ledger, reproducibility, authorship, conflicts, permissions and data availability | Author-approved submission packet |
| After incident or material change | Containment, impact, root cause, corrective action and effectiveness | Incident/CAPA record and closure authority |

## Decision and record rules

- Record the decision date, decision-maker, scope, rationale, evidence revision, limitations, expiry/review date and superseded decision.
- A repository commit proves a file changed; it does not prove the underlying control operated.
- No role may approve its own independent assessment.
- Unassigned roles and unavailable external evidence remain OPEN.
- Risk acceptance is time-bounded and cannot waive law, ethics, platform policy or P0.
- Revisit appointments and cadence at each Track G review; do not invent names or credentials.

## Current acceptance

The owner has authorized execution of Track G. That instruction is not, by itself, acceptance of a QMS, appointment of qualified role-holders, acceptance of residual security/privacy risk, legal advice, ethics determination or release authorization.
