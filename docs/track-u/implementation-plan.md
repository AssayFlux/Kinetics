# Track U — User interface implementation and verification plan

**Status:** STARTED — Step 1 (documented base implementation) on 2026-11-17  
**Sequence:** Sixth and final track, R → S → I → P → G → U (D-023)  
**Design authority:** Owner-supplied Premium Minimal Monochrome Design System — V1 (D-024)  
**Platform:** Existing native Android Jetpack Compose application  
**Baseline:** main commit e6c98e0b506223aed65b00d1c39f0916ef2a0446  
**Scope:** Research Mode only. This plan is not a claim of usability validation, accessibility conformance, security certification, device support or release readiness.

## 1. Gate and baseline assessment

Track G's bounded G0–G7 engineering foundation was reported CLOSED on exact main commit 31b1618c4e843d0ec90feb2ceae0d0e4fb1615b1; exact-head CI workflow 44108451571 passed 9/9 jobs. The overall G acceptance remains OPEN for independent reviews, owner policy/risk acceptance, full resolved SBOM/licensing, physical-device checks, named specialist appointments and operational exercises. Those carry-forward obligations do not prevent starting U's bounded engineering foundation; they are not waived by U.

Pre-existing U0–U3 code and documents are retained as partial baseline, not retroactively accepted. Current source includes a four-destination Compose shell (Home, Work, Explore, Settings), adaptive bottom bar/rail/drawer classification, Light/Dark/System theme preference, a biometric local app-lock path, a horizontal dashboard carousel, registry-backed Explore catalogue, WorkManager/SAF job flows and bounded FASTA/FASTQ launch cards. CI evidence previously cited for some source is historical and must be rechecked at the new exact head. The complete UI remains incomplete.

## 2. Owner design contract — V1

The new owner-supplied 20-section prompt is authoritative for active UI design under D-024. Implement exact values from the prompt rather than substituting another aesthetic:

- Reference viewport 393 × 852 dp; responsive compact 360 × 800, large 430 × 932 and tablet 600 dp+.
- 4 dp spacing rhythm; 20 dp standard horizontal padding (16 compact, 24 large); 24 dp section separation; 16 dp card padding.
- Typography: 28/24/20/16/14/13/12/11 sp roles with the specified weights; tabular numerals for statistics and system font scaling.
- Light palette: canvas #FAF9F6, surface #FFFFFF, secondary surface #F2F1ED, text #171717, secondary #686868, disabled #A3A3A3, border #E5E3DE, divider #ECEAE6, icon #292929.
- Dark palette: canvas #121212, surface #1B1B1B, secondary surface #242424, text #F5F5F5, secondary #A5A5A5, disabled #686868, border #333333, divider #292929, icon #E8E8E8.
- Status colours only for semantic success/warning/error/information, with text/icon cues as well.
- System/Light/Dark appearance; restrained radii and measured dimensions for app bar, drawer, buttons, inputs, cards, lists, dialogs, sheets, bottom navigation and avatars.
- Native safe areas, keyboard handling, natural scrolling, reduced motion, focus, semantic labels and accessible touch targets.
- No unnecessary gradients, shadows, excessive rounding, decorative illustrations, colour or motion.

## 3. Product truth and screen map

The UI must reflect actual repository capability, not a generic scientific app.

| Destination / flow | Real source of truth | Rule |
|---|---|---|
| Home | ResearchStore jobs, import action, runtime diagnostics | Counts and activity derive from real persisted jobs; empty state when none |
| Work | SAF import, WorkManager lifecycle, encrypted ResearchStore, export/provenance actions | Show actual states; preserve cancel/resume/recovery/delete/export semantics |
| Explore | capabilities/registry.yaml and Android dispatcher map | Show maturity/availability; only show Run when a real dispatcher, input contract and result path exist |
| Settings | persisted appearance, diagnostics, biometric local lock and app settings | No fake account/profile, inert settings or false security promises |
| Authentication / local lock | existing local app-lock and AndroidX BiometricPrompt integration | Clearly distinguish local app lock from remote account sign-in; no invented identity provider |
| Research analysis | current FASTA QC and FASTQ quality-summary launch paths | Do not imply all registry tools are runnable |
| Results / provenance / export | existing durable job and analysis paths | Never fabricate results, provenance, progress or completion |

## 4. Work packages

### U0 — Design foundation
1. Reconcile canonical semantic tokens to V1 light/dark values and remove obsolete palettes from active selection while retaining historical/catalogue records only where harmless.
2. Make token generation deterministic for Compose and WebView CSS; generated files remain generated.
3. Implement shared Compose primitives for app bar, buttons, fields, cards, rows, chips, dialogs, bottom sheets, status, spacing and typography.
4. Preserve owner logos and reference assets byte-for-byte; audit actual asset paths and integrate only verified assets.
5. Provide a real component gallery and screenshot harness, not a static concept.

### U1 — Application shell and navigation
1. Refine compact bottom navigation, adaptive rail/drawer and screen content widths.
2. Add real destination map and accessible drawer grouping; no dead destinations.
3. Add global search only over real registry/jobs where supported; no fabricated results.
4. Implement first-run/onboarding only for actual local setup and Research Mode disclosure.
5. Ensure process-death persistence for preferences and navigation where required.

### U2 — Security and privacy surfaces
1. Audit biometric local lock, device-credential fallback, lifecycle, lockout and recovery.
2. Implement FLAG_SECURE/Recents behavior only after threat/privacy impact and owner-facing disclosure are reviewed.
3. Audit encrypted settings, consent, data inventory and deletion/export disclosures.
4. Preserve Keystore-loss behavior: do not imply ciphertext recovery when key material is lost.
5. Add negative, lifecycle, migration and UI security tests.

### U3 — Scientific workflows and result presentation
1. Integrate only real dispatchers and typed contracts.
2. Complete durable result/provenance viewing and truthful progress/failure/cancel/retry behavior.
3. Add sequence and kinetics screens only against implemented engine operations and test fixtures.
4. Export through SAF with explicit success/partial-failure outcomes and provenance.
5. Keep clinical/PGx interpretation disabled and Research Mode only.

### U4 — Scientific viewers
Mol*/3Dmol.js, alignment, tree, chart and chemistry viewers only after S1–S3 contracts, dependency/licence approval, secure offline bridge and measured low-end-device performance budgets. Do not add viewer libraries before approval.

### U5 — Genomics / PGx / in-silico screens
Only after P1–P3 and I2–I4 dependencies. Synthetic/public non-patient fixtures only under existing gates. No patient-facing or clinical interpretation while P0 is blocked.

### U6 — Quality, localisation and usability
Responsive window matrix, RTL, font scaling, screen readers, keyboard/switch navigation, reduced motion, contrast, screenshot diffs, performance, process death, rotation, resize, offline, storage and usability evidence.

## 5. Two-step execution model

**Step 1 — documented base implementation:** implement U0–U6 to the extent permitted by dependency gates; add source, contracts, docs and automated tests; build a coherent, integrated UI foundation. Planned or blocked dependency work remains explicitly marked and cannot be faked.

**Step 2 — integration audit, tests and corrections:** audit the exact Step 1 commit; inspect all call paths and visible controls; run generator checks, Kotlin/JVM/UI tests, Android arm64 APK/AAB build, accessibility/contrast/screenshot checks, migration/security tests and applicable Python/native integration tests; fix failures and rerun. Device/emulator checks are separate from CI. Close only bounded engineering work supported by exact-head evidence; independent and physical-device obligations remain OPEN.

## 6. Integration contract

- Kotlin/Compose owns presentation, lifecycle, permissions, local persistence orchestration and WorkManager integration.
- Python owns scientific analysis/orchestration; C++ owns performance-critical core; Rust owns security boundaries, per D-018.
- Compose must call existing typed app/domain/store interfaces; no scientific logic in UI and no UI bypass of storage/security services.
- Existing JSON Schema engine envelope remains authoritative for cross-language scientific messages. No schema/interface change is authorized by this UI plan.
- SAF URI grants, encrypted staging, authenticated chunks, Keystore key lifecycle, SQLite transactions, cancellation and export semantics must remain intact.
- No new dependency, font binary, icon family, viewer engine, network service or telemetry without licence/security/architecture review.

## 7. Verification and evidence

Record exact source commit, workflow URL, toolchain, commands, job outcomes, APK/AAB SHA-256, generated-file reproducibility, screenshots, contrast measurements, accessibility semantics and device details. A compile is not a UI test; a CI screenshot is not physical-device verification. Mark unavailable checks NOT RUN or BLOCKED.

Required test families:
- Token generator determinism and source/generated parity.
- Theme persistence across process restart and System mode behavior.
- Navigation and every interactive control's real action/state transition.
- Home/Work empty, loading, success, partial, failure and recovery-required states.
- SAF import/export, cancellation, resume, process death, Keystore loss and encrypted storage regression.
- Explore registry maturity and dispatcher gating.
- Accessibility: minimum 48 dp targets, labels, focus, TalkBack, 200% font scale, contrast and reduced motion.
- Window matrix: 360×800, 393×852, 430×932, tablet 600 dp+, landscape, split-screen, RTL and keyboard.
- Offline behavior and no unintended network/telemetry.

## 8. Explicit non-goals and blockers

- No generic fabricated user profile, cloud account, fake login, sample research jobs or placeholder success.
- No claims of device support without named-device evidence.
- No patient data, clinical mode, diagnosis, treatment, dosing or clinical PGx interpretation; P0 remains NOT APPROVED.
- No motif/font/viewer additions until their respective provenance, licence, accessibility and dependency gates pass.
- No fold/hinge-safe claim until WindowManager posture integration and tests exist.
- G independent/operational acceptance obligations remain carry-forward and are not declared complete.

## 9. Current disposition — audited 2026-11-18

Track U remains OPEN. PR #76 merged the Step 1 monochrome foundation to main as `dea7bec731f3e6bdc3732899dd3feeed2703bbc3`. The compiler correction is included. U0–U3 remain partial; U4 is blocked/partial source; U5 is blocked/not implemented as a complete UI; U6 has not passed. The exact-main workflow `44208315663` was still running its Android arm64 APK/AAB build at the time of the audit. No APK success is claimed until artifacts and hashes are verified. See `docs/track-u/completion-audit.md` for package-by-package outstanding work, dependencies and exact closure evidence. No percentage is reported.
