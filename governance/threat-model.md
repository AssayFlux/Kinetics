# Kinetics UI threat supplement

**Status:** scoped UI-specific supplement to the canonical [security and privacy threat model](../docs/security-threat-model.md). It is not a second, competing application-wide threat model and is not independently reviewed.

| Threat ID | Threat | UI surface | Initial mitigation | Required verification |
|---|---|---|---|---|
| UI-T-01 | Lost/stolen device or shoulder surfing | Local DB/files, Recents, visible project content | Keystore encryption; privacy masking/lock requirements; sensitive-window protection where approved | Key-loss, lock timeout, Recents/screenshot and notification tests |
| UI-T-02 | Malicious import | SAF picker, import preview, parser handoff | Streaming, bounded parsers, strict format allow-list, no shell execution | Malformed/oversized corpus, fuzzing and resource limits |
| UI-T-03 | Malicious remote node | Future node pairing and result screens | Network disabled by default; explicit pairing and send-preview; no silent transfer | Any future implementation requires TLS, certificate lifecycle, MITM/replay tests and P0/privacy review |
| UI-T-04 | Malicious app interaction | Intents, clipboard, exported activities and overlays | Minimise exported components; avoid sensitive clipboard; re-authenticate sensitive actions | Merged-manifest and interaction tests |
| UI-T-05 | WebView injection | Offline viewer HTML/JS bridge | Local assets, strict CSP, no remote content, typed allow-list bridge | Bridge fuzzing, origin policy and lifecycle tests |

## Defaults requiring explicit owner review

- No network by default; offline-only is the active architecture boundary.
- No automatic cloud backup of sensitive research data.
- Sensitive project screenshot/Recents protection is a requirement pending UX/device review.
- App lock and separate vault lock remain subject to recovery, accessibility and owner review.
- No panic wipe until consequences are reviewed.
- Clinical Decision Support Mode remains unavailable.

Keystore key loss may make ciphertext irrecoverable; replacing the key does not recover data. Hardware-backed guarantees vary by device. These cases require device testing and must not be represented as solved by a UI mockup.
