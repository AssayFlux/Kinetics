# Track U — Completion audit and outstanding work

**Audit date:** 2026-11-18  
**Repository:** `AssayFlux/Kinetics`  
**Target branch:** `main` only  
**Audited baseline:** `dea7bec731f3e6bdc3732899dd3feeed2703bbc3`  
**Status:** **OPEN — foundation merged; product integration and acceptance remain incomplete**  
**Design authority:** D-024, owner-supplied Premium Minimal Monochrome V1. Semantic decision colours may be used for status only; monochrome remains the visual authority.

This is an evidence-based gap register, not a completion claim. A source file existing does not prove a complete user journey, accessibility, security assurance, device compatibility or release readiness. Do not mark a row complete without the evidence named below.

## 1. Baseline and build evidence

- PR #76 was merged to `main` as merge commit `dea7bec731f3e6bdc3732899dd3feeed2703bbc3`.
- The merge contains the Step 1 monochrome design-system foundation and the compiler correction `FontWeight.Regular` → `FontWeight.Normal`.
- Exact-main workflow: [run 44208315663](https://github.com/AssayFlux/Kinetics/actions/runs/44208315663), commit `dea7bec731f3e6bdc3732899dd3feeed2703bbc3`.
- At audit time, the Python foundation/tests, Vina smoke, RDKit descriptor fixtures, SPDX inventory, host scientific reference comparisons, RDKit ADMET utility smoke, Node security tests and OpenMM CPU replica smoke jobs reported success.
- The Android arm64 debug APK/AAB job was still running at the audit time, at the build/package-alignment step. Therefore no APK/AAB success, package alignment, artifact hash or download artifact is claimed here.
- The earlier PR workflow `44208257346` is not a substitute for the exact-main build. Its artifacts are not evidence that the merged main commit produced an APK.

## 2. Work-package disposition

| Package | Disposition | What exists | Remaining closure work |
|---|---|---|---|
| U0 — design foundation | PARTIAL | D-024; V1 token source and generated Compose/CSS tokens; typography; reusable Compose primitives; component gallery source | Prove deterministic generation on exact main; audit every active component against owner dimensions; integrate verified owner assets without copying/moving originals; complete interactive gallery and visual regression screenshots |
| U1 — application shell | PARTIAL | Four real destinations (Home, Work, Explore, Settings); compact drawer/bottom navigation and expanded rail; app bar; Light/Dark/System preference; registry-backed Explore; import/job entry points | Complete global search over real jobs/registry; onboarding for actual local setup; route every screen/action; verify process-death and navigation restoration; eliminate or explicitly label every planned/inert destination; complete screen-by-screen migration |
| U2 — security and privacy | PARTIAL / REVIEW REQUIRED | Device-local biometric prompt path; Android credential fallback path; encrypted local store and chunked data paths; delete/export UI; existing recovery-oriented storage code | Threat-model and lifecycle review; biometric failure/lockout/cancel/process-death tests; verify secure-window/Recents policy and disclosure; inventory all local data and metadata; test deletion, orphan cleanup and Keystore loss; confirm no false secure-erasure claim; privacy review and security regression evidence |
| U3 — workflows and results | PARTIAL | SAF import; WorkManager job lifecycle; encrypted staging/storage; FASTA QC and FASTQ quality-summary launch paths; provenance/export paths; structure/chemistry research source components | Audit every capability against registry, dispatcher, typed input/result contract and worker; complete durable result/detail/log/error/retry/cancel/resume screens; verify provenance and export round trips; persist results across process death; do not expose unimplemented tools as runnable |
| U4 — scientific viewers | BLOCKED / PARTIAL SOURCE | Structure viewer source and existing chemistry/research cards are present | Complete S1–S3 interface dependency checks; dependency provenance/licence/security approval; offline bridge threat review; real fixture coverage; low-end ARM64 performance and memory evidence; viewer accessibility and lifecycle tests. Do not add viewer libraries before approval |
| U5 — genomics / PGx / in-silico screens | BLOCKED / NOT IMPLEMENTED AS A COMPLETE UI | Existing registry and limited research launch paths only | Close required P1–P3 and I2–I4 dependencies; preserve P0 NOT APPROVED; build only research-mode screens backed by approved contracts and synthetic/public fixtures; no patient-facing or clinical interpretation |
| U6 — quality and acceptance | NOT PASSED | Device matrix and quality-report documents; some source-level navigation and workflow tests | Run exact-head Kotlin/JVM/UI tests; token parity; screenshot comparisons; WCAG contrast measurement; touch-target bounds; TalkBack; 200% font scale; keyboard/switch access; reduced motion; RTL; landscape/split-screen/tablet; process death/rotation/offline; emulator and named physical-device checks; record results and hashes |

## 3. Screen-level gaps

The canonical screen inventory remains `docs/ui/screen-map.md`. The following are not complete merely because they appear in that map:

- Splash/onboarding and first-run local workspace setup.
- Global search, domain browser, tool search/favourites and a complete tool runner.
- Projects/data packs and complete job detail/log views.
- Dedicated sequence viewer/editor and alignment/tree viewers.
- Complete structure and chemistry viewers with validated offline lifecycle.
- Kinetics lab, charts studio and provenance detail viewer.
- Genomics/variant and PGx research screens, subject to P-track gates and P0 prohibition.
- In-silico job builder, subject to I-track engine gates.
- Complete security/privacy centre, data inventory and deletion controls.
- About/licence presentation and final owner-brand integration.
- Every empty/loading/running/success/partial/failure/cancelled/recovery-required state for each real workflow.

The existing Home/Work/Explore/Settings shell must remain truthful. Do not add fake user profiles, cloud login, demo jobs, fabricated progress, fabricated scientific results or controls with no real action.

## 4. Required exact-head closure evidence

The following evidence must be attached to the commit that is proposed for Track U engineering closure:

1. CI green on exact `main` commit, including Android arm64 debug APK/AAB build and JVM/package tests.
2. APK and AAB (where configured) verified as non-empty, package-aligned, and accompanied by SHA-256 hashes and build-environment record.
3. Generated token outputs reproducible from canonical token source with no diff.
4. Kotlin/Compose tests for navigation, all visible controls, theme persistence, workflow states and recovery.
5. Storage/security regression tests covering SAF, cancellation, resume, deletion, orphan cleanup, encrypted chunk integrity and Keystore-loss behavior.
6. Registry/dispatcher parity: each runnable card maps to a real input contract, dispatcher, result type and provenance path.
7. Contrast measurements for both themes; touch-target bounds; semantics/focus/TalkBack; 200% font scaling; reduced motion; RTL and keyboard/switch navigation.
8. Screenshot evidence for compact 360×800, baseline 393×852, large 430×932, tablet 600dp+, landscape and split-screen.
9. Named emulator and physical-device evidence, including performance and memory measurements on the agreed low-end ARM64 device.
10. Dependency, asset, font, icon and viewer provenance/licence/security review.
11. Updated quality report, screen map, implementation plan and session log reflecting the same exact commit and actual evidence.

A CI compile/build is not proof of UI acceptance, scientific validity, clinical safety or physical-device compatibility. Engine smoke checks are not scientific validation.

## 5. Cross-track carry-forward gates

- Track G independent/operational acceptance obligations remain OPEN as recorded in the implementation plan.
- P0 remains NOT APPROVED. Clinical PGx interpretation, patient-facing diagnosis, treatment or dosing must not be implemented or implied.
- U4 remains dependent on S1–S3 and viewer dependency/security review.
- U5 remains dependent on P1–P3 and I2–I4.
- No UI work may silently change the established Python/C++/Rust ownership boundaries or the JSON Schema engine envelope.

## 6. Closure rule

Track U may be described as **engineering-complete** only after U0–U6 engineering tasks have either passed their explicit acceptance criteria or are documented as externally blocked with an owner, dependency, evidence and non-claim. It may be described as **release-ready** only after all required independent, accessibility, security, scientific and physical-device approvals are separately satisfied.

**Current decision: Track U is OPEN.** The merged commit is a foundation milestone, not Track U completion.