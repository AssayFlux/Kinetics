# Kinetics threat model — UI/security scope

**Status:** v1 draft; not independently reviewed. Research Mode only. Not a compliance claim.

| Threat | Surface | Initial mitigation | Required verification |
|---|---|---|---|
| Lost/stolen device | Local DB/files/Recents | Keystore encryption, optional app/vault lock, hide Recents, FLAG_SECURE for sensitive projects | Key-loss, lock timeout, backup exclusion and screenshot tests |
| Malicious import | SAF documents/parsers | Streaming, bounded parsers, strict formats, no shell execution | Fuzz importers, malformed/oversized corpus, resource limits |
| Malicious remote node | Node endpoint/results | Network off by default, explicit pairing, TLS pinning, send-preview, never-leave-device lock | Certificate rotation/revocation, MITM and replay tests |
| Shoulder surfing | Visible content/notifications | Research Mode banner, masking, notification privacy | Manual privacy review |
| Malicious app | Intents/clipboard/overlays | Minimise exported components, avoid sensitive clipboard, re-authenticate sensitive actions | Manifest audit and interaction tests |
| Supply chain | Gradle/Python/Rust/C++/WebView | Pin versions, SBOM, license review, no runtime executable downloads | Resolved transitive SBOM, provenance and vulnerability review |
| WebView injection | Viewer HTML/JS bridge | Offline assets, strict CSP, no remote content, typed allow-list bridge | Bridge fuzzing and origin-policy tests |

## Security defaults awaiting owner gate
- No network by default; offline-only default.
- No automatic cloud backup of sensitive research data.
- Sensitive project screenshot/Recents protection default on.
- App lock and separate vault lock remain optional until UX, biometric fallback and recovery behavior are reviewed.
- No panic wipe until consequences are owner-reviewed.
- Clinical Decision Support Mode remains unavailable.

Keystore key loss may make ciphertext irrecoverable; replacing the key does not recover data. Hardware-backed guarantees vary by device. Independent security review is required before real patient data.
