# Step 7 — Rust infrastructure and security foundation

## Status
Implementation foundation only. This crate is not yet a deployed network service and does not claim production authentication, durable job orchestration, remote artifact transport, or a completed disaster-recovery drill.

## Contracts
- OpenAPI 3.1 contract: `docs/api/openapi-v1.yaml`; Rust request/response types live in `contracts.rs` and serialize with explicit API versioning.
- Runtime environment secret wrapper redacts its `Debug` output and never returns values in error messages; production deployments should use a managed secret provider.
- API namespace: `/api/v1` (contract version constant `v1`).
- Job states: `queued → running → succeeded | failed | cancelled`; cancellation is allowed from queued or running; terminal states cannot be reopened.
- Every job carries tenant identity, idempotency key, and explicit runtime, memory, and CPU limits.
- Repeated submission with the same tenant/key and same limits returns the original job; changed limits conflict. A key in another tenant is independent.
- Cross-tenant reads and transitions return not-found to avoid resource enumeration.
- Artifact IDs are lowercase SHA-256 digests. The store derives all paths from the digest, writes immutable content-addressed objects, and verifies hashes on reads.
- Audit events carry actor, tenant, action, resource, outcome, timestamp, and correlation ID. Credential-like values are rejected from event fields.

## Security boundaries and deployment requirements
This crate supplies policy primitives, not an identity provider. Production must validate signed identity-provider tokens at the API gateway, map verified claims to a `Principal`, enforce scopes at every handler, and keep signing/encryption keys in a managed secret store. Never accept caller-supplied tenant IDs as authority; derive tenant identity from verified claims.

The in-memory job registry is a deterministic state-machine reference, not a durable queue. A production adapter must persist transitions transactionally, enforce leases/deadlines and worker heartbeats, implement bounded retries with backoff, propagate cancellation, and guarantee idempotent side effects. Do not run untrusted user code in-process.

The artifact store is a local content-addressed primitive. Production upload/download handlers must authenticate and authorize each request, enforce size/type quotas, stream to a temporary file, fsync, atomically publish, verify hashes, scan/quarantine untrusted content, and use tenant-aware metadata. Backups must include metadata and object data, be encrypted with managed keys, and be restored into an isolated environment with hash verification.

Secrets must be injected at runtime from a secret manager or protected environment. Do not put tokens, passwords, private keys, or customer data in source, fixtures, command arguments, or logs. Audit logs must be append-only in the deployed system, access-controlled, retention-managed, and monitored.

## Threat model (initial)
| Threat | Mitigation in this foundation | Required deployment control |
|---|---|---|
| Cross-tenant IDOR | Tenant checks and not-found behavior | Enforce on every API route; negative integration tests |
| Privilege escalation | Explicit scope checks | Verified identity-provider claims and deny-by-default policy |
| Path traversal | Digest-only artifact path derivation | Quotas, sandboxed storage, symlink-safe deployment |
| Artifact tampering | SHA-256 verification on read | Signed manifests, immutable backups, restore drills |
| Duplicate job submission | Tenant-scoped idempotency | Durable unique constraint and idempotent workers |
| Resource exhaustion | Required per-job resource limits | Enforced cgroups/container quotas and admission control |
| Credential leakage | Audit-field validation | Secret manager, redaction, log scanning and rotation |
| Malicious tools/input | No shell or plugin execution exposed | Isolated workers, allowlists, egress policy and review |

## Validation
Run `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, and `cargo test` from `rust/kinetics-infra`. Python CI remains unchanged; a separate Rust CI job runs these checks. Production acceptance additionally requires API contract tests against a deployed adapter, unauthorized/cross-tenant integration tests, secret scanning, artifact upload/download tests, and a documented backup/restore drill.
