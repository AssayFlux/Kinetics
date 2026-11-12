# Track G — security verification matrix

**Status:** test specification and source-level review only. No independent penetration test or physical-device security assessment is claimed.

| Test ID | Threat / control | Test procedure | Expected result | Evidence required | Status |
|---|---|---|---|---|---|
| SEC-001 | Manifest permissions | Inspect source and merged release/debug manifests | Only justified permissions; no INTERNET permission while remote features are disabled | Merged manifest, build SHA, reviewer | OPEN |
| SEC-002 | Exported components | Enumerate merged manifest components and intent filters | Only intentional launcher/export surfaces; no unintended providers/services | Manifest report and test | OPEN |
| SEC-003 | SAF URI revocation | Revoke read permission between import/resume stages | Fail closed; no path escape, crash loop or stale plaintext | Device logs with synthetic files | OPEN |
| SEC-004 | Malformed/oversized inputs | Run bounded malformed corpus and fuzz parsers | Reject safely within resource limits; no unbounded allocation | Corpus hashes, resource limits and run output | PARTIAL — existing unit tests; fuzz campaign open |
| SEC-005 | Path traversal/symlink | Supply traversal names and symlink/race scenarios to pack/cache/import paths | Writes remain under app-private canonical roots | Automated test and device result | OPEN |
| SEC-006 | Concurrent workers | Schedule duplicate/conflicting jobs and cancel/retry | Single valid state transition; no plaintext or metadata race | WorkManager test and device run | OPEN |
| SEC-007 | Process death | Kill process at each file/DB commit boundary | Recover or fail closed; no silent success or orphan plaintext | Fault-injection matrix | OPEN |
| SEC-008 | Keystore invalidation | Invalidate/remove key and reopen ciphertext | Authentication/key failure is explicit; no downgrade or false recovery | Device test and recovery record | OPEN |
| SEC-009 | Logging | Search source and capture logcat during error/exception paths | No input content, plaintext, key, token or sensitive path in logs | Static scan and redacted logcat | OPEN |
| SEC-010 | WebView bridge | Fuzz origin, message schema, size, type and lifecycle | Reject unknown origins/messages; no arbitrary JS/native execution | Bridge tests and security review | OPEN |
| SEC-011 | Data-pack integrity | Mutate manifest, payload, checksum, version and rollback order | Reject invalid packs; checksum is not treated as publisher authentication | Tests and signed-publisher decision | PARTIAL — checksum/metadata guards; publisher trust unresolved |
| SEC-012 | Dependency supply chain | Resolve all build graphs and scan exact artifacts | Versions, hashes, source, license and vulnerability status trace to artifact | Resolved SBOM and review report | OPEN |
| SEC-013 | Backup/export privacy | Inspect backup rules and test SAF export/backup restore | No automatic sensitive backup; export is explicit and clearly disclosed | Device evidence | PARTIAL — source manifest disables backup |
| SEC-014 | Remote boundary | Inspect permissions, routes and network traffic | No app network transfer while remote mode is disabled | Merged manifest and network capture | PARTIAL — no INTERNET permission in source manifest |
| SEC-015 | Vulnerability reporting | Exercise private reporting channel and incident intake | Report reaches assigned security owner without public exploit details | Channel test and assigned owner | OPEN |
| SEC-016 | Independent assessment | External assessor reviews mobile app, native/Python surfaces and release artifact | Findings tracked, remediated and independently retested | Signed assessor report and closure records | OPEN — external |

## Execution rules

- Run only with synthetic/non-personal test fixtures until P0 and applicable approvals are complete.
- Preserve tool versions, source commit, artifact hash, device/API/ABI and raw result for every run.
- A test specification or unit test is not a passed device test.
- Critical/high findings block release unless remediated and independently retested; no self-waiver.
- Do not publish exploit details before coordinated disclosure.
