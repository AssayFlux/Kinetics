# Track U — Completion audit and outstanding work

**Audit date:** 2026-11-18  
**Repository:** `AssayFlux/Kinetics`  
**Target branch:** `main` only  
**Current engineering review baseline:** `aeec1d0e8918e14455f627fc5aa5cf933322b634` (per-capability carousel, individual service destinations and blueprint header; exact-head CI pending)
**Audit and quality-report documentation commit:** `cb79b9110ff50a69b1b58d78a8b13e3c8843cf3b`  
**Status:** **ENGINEERING INTEGRATION IN PROGRESS — distinguish code work from external/device acceptance**  
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
| U1 — application shell | PARTIAL | Three destinations (Home, Work, Settings); compact drawer/bottom navigation and expanded rail; app bar; System-default Light/Dark preference; registry-backed Home carousel and service list; import/job entry points | Complete global search over real jobs/registry; onboarding for actual local setup; route every screen/action; verify process-death and navigation restoration; eliminate or explicitly label every planned/inert destination; complete screen-by-screen migration |
| U2 — security and privacy | PARTIAL / REVIEW REQUIRED | Device-local biometric prompt and credential fallback; foreground-return re-authentication; AES-GCM encrypted inputs; fail-closed Keystore-loss handling; read-only encrypted-orphan inventory; explicit Settings data inventory; analysis-work cancellation on job deletion | Lifecycle/device tests for prompt cancellation, lockout and credential fallback; merged-manifest/backup/network audit; Keystore fault injection; deletion/orphan cleanup regression; owner decision on FLAG_SECURE/Recents; decision on SQLite metadata/result encryption; independent mobile security/privacy review. See `u2-security-privacy.md` |
| U3 — workflows and results | PARTIAL | SAF import; WorkManager import/analysis lifecycle; encrypted input staging; FASTA QC; newly integrated FASTQ QC with explicit Phred+33/+64; digest-bound result persistence; structured FASTA/FASTQ result preview; provenance and SAF export | Embedded-runtime FASTQ fixtures; result schema validation; process-death/retry/cancel tests; export round trips; registry/dispatcher parity for every runnable action; broader durable detail/log/failure flows. See `u3-scientific-workflows-results.md` |
| U4 — scientific viewers | BOUNDED ANDROID STRUCTURE/CHEMISTRY INTEGRATION IMPLEMENTED; DEVICE/SCIENCE ACCEPTANCE OPEN | Service destinations route to hardened offline PDB/mmCIF interactive 3D coordinate viewer with session/PNG/SVG/state export and full-screen mode; SDF/MOL graph preview with full-screen mode; S3 ligand-site and apo-pocket candidate screens; no third-party viewer runtime dependency | Physical low-end ARM64 performance/memory, supported WebView matrix, accessibility/lifecycle/import-export tests and independent S1–S3 scientific concordance remain open. Alignment/tree/chart and full 3D chemistry viewers are not claimed. See docs/track-u/u4-scientific-viewers.md |
| U5 — genomics / PGx / in-silico screens | PARTIAL — AGGREGATE VCF QC INTEGRATED; PGx/IN-SILICO REMAIN GATED | The relevant genomics/variant service destinations include bounded aggregate-only VCF syntax/QC with institutional-authorization attestation, no sample/genotype output, no persistence/export; PGx and host-engine gate disclosures are explicit | P1 reference concordance/source terms/device validation; P2 licensed definitions and biological concordance; P3 licensed guideline evidence; I2 redocking/cross-docking; I3 force-field/biomolecular validation; I4 licensed datasets/model calibration. Owner-authorized research testing is open under D-024 within the declared institutional approval; no PGx interpretation or Android host-engine launcher. See docs/track-u/u5-genomics-pgx-research.md |
| U6 — quality and acceptance | NOT PASSED | Device matrix and quality-report documents; some source-level navigation and workflow tests | Run exact-head Kotlin/JVM/UI tests; token parity; screenshot comparisons; WCAG contrast measurement; touch-target bounds; TalkBack; 200% font scale; keyboard/switch access; reduced motion; RTL; landscape/split-screen/tablet; process death/rotation/offline; emulator and named physical-device checks; record results and hashes |

U2–U5 extension records: `u2-security-privacy.md`, `u3-scientific-workflows-results.md`, `u4-scientific-viewers.md` and `u5-genomics-pgx-research.md`. These describe concrete source additions and their still-open acceptance evidence; none waives external/device gates.\n\n## 3. Owner blueprint implementation (2026-11-18)\n\n- Added `docs/ui/owner-blueprint-implementation.md` and linked it from `KINETICS_UI_SPEC.md`; the two owner reference images remain in `Assets/` unchanged.\n- Replaced the old Home service catalogue with a horizontal carousel generated from the 68 individual capability entries plus Public Reference Databases. Domain cards are clickable and open a dedicated service destination.\n- Home now presents four summary panels for runtime readiness, research work, recent activity and local data/reference access.\n- Existing Public Database, FASTA/FASTQ, structure, chemistry, genetic-code and VCF workflows were moved into relevant service destinations where their current composables exist. Catalogue entries are shown with honest execution caveats; registration is not presented as proof of an Android dispatcher.\n- Replaced compact bottom navigation and expanded rail with the hamburger drawer. Added top-right profile entry with an explicit no-remote-account disclosure. Password reset, remote sign-in and user ID are not simulated because no identity backend exists.\n- Restored safe-drawing inset handling.\n- **Not yet accepted:** exact-head CI for the latest UI commit, screenshot comparison against both owner images, physical-device interaction/accessibility testing, login-screen visual alignment, real account backend, and complete per-capability Android dispatchers. Regression tests now cover one card per catalogue entry, ID-based routing, the five-indicator pager window, and the four dashboard panels. The current biometric screen remains a local device lock and is not a remote login form. The four unlabeled controls in the owner sketch are not assigned invented credential semantics; matching the login layout beyond the existing biometric unlock requires an owner-approved local credential design or a real identity backend.\n\n## 4. Screen-level gaps

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

The Home/Work/Settings shell must remain truthful. Do not add fake user profiles, cloud login, demo jobs, fabricated progress, fabricated scientific results or controls with no real action.

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
- D-025 authorizes research testing within the declared institutional approval; clinical PGx interpretation, patient-facing diagnosis, treatment or dosing must not be implemented or implied.
- U4 remains dependent on S1–S3 and viewer dependency/security review.
- U5 remains dependent on P1–P3 and I2–I4.
- No UI work may silently change the established Python/C++/Rust ownership boundaries or the JSON Schema engine envelope.

## 6. Closure rule

Track U may be described as **engineering-complete** only after U0–U6 engineering tasks have either passed their explicit acceptance criteria or are documented as externally blocked with an owner, dependency, evidence and non-claim. It may be described as **release-ready** only after all required independent, accessibility, security, scientific and physical-device approvals are separately satisfied.

**Current decision: Track U is OPEN.** The merged commit is a foundation milestone, not Track U completion.

## 6. Engineering work versus external acceptance

Engineering closure is not held open merely because a scientific or ethics approval is pending. Complete all work that can be completed safely in code: user journeys, local workflows, input bounds, deterministic outputs, persistence where appropriate, recovery, export, automated regression tests, UI states, accessibility semantics, build reproducibility and documentation.

The following are external/owner gates rather than ordinary coding tasks: ethics approval for a defined protocol; data-use permissions and licences; qualified clinical/PGx review; independent scientific concordance; owner risk decisions; physical-device testing where no device is attached to CI. The app must not imply that those approvals have been granted.

The presentation brief is docs/ethics-committee/engineering-evidence-brief.md. It records the supported research-only demo path, local data handling, explicit exclusions and evidence gaps without claiming ethics approval.


## 7. Public database retrieval integration — 2026-11-18

### Source implementation now present
- `PublicDatabaseClient.kt`: allow-listed HTTPS adapters for NCBI Gene/nuccore/protein, UniProtKB and RCSB PDB mmCIF-by-entry-ID.
- `PublicDatabaseCard.kt`: Home search and retrieval controls, sequence analysis dispatch, saved-record listing and deletion.
- `PublicRecordStore.kt`: encrypted app-private source payload cache using Android Keystore AES-GCM chunked files; SQLite metadata index.
- `StructureViewer.kt`: accepts fetched RCSB mmCIF, invokes the existing Python preparation/parser and opens the offline structure viewer.
- `KineticsUi.kt`: connects public structure retrieval to the existing Home structure viewer.
- `PublicDatabaseClientValidationTest.kt`: input-validation tests for unsupported databases, malformed accessions and malformed PDB IDs.

### Current truthful status
- NCBI nucleotide/protein and UniProt FASTA: retrieval, encrypted payload save and existing on-device FASTA QC are wired in source.
- RCSB PDB entry ID: mmCIF retrieval, encrypted payload save and existing parser/viewer handoff are wired in source.
- NCBI Gene: metadata search plus linked nucleotide/protein discovery through ELink; selected linked records use the existing FASTA retrieval and QC path.
- Saved records: visible and deletable; saved mmCIF can be reopened in the viewer and saved FASTA can be re-analysed. A richer saved-record detail/history browser remains open.
- Source payload encryption is implemented; SQLite metadata and analysis JSON remain plaintext within app-private storage.
- RCSB search is entry-ID based, not text/ligand/organism discovery.
- Provider retry/cancellation, release/licence metadata, cache quotas, physical-device behavior and scientific validation remain open.

### Required verification
- Run `2985` (`44229328602`) on commit `3dfc8b903f6928b65e673b2bb9a7ffb0586ff335`: arm64 APK/AAB build and 16 KiB native alignment checks PASSED; Android JVM unit-test compilation FAILED because `ResearchStoreMigrationTest.kt` passed `1L` where an `Int` byte-count argument is required. The test fixture was corrected at commit `2334b0703553e833adbf6a8de44c28826aebf05a`. The produced APK/AAB belongs to the older `3dfc` commit and is not the exact-main release candidate.\n- Earlier runs `2959` and `2971` failed on pre-fix commits: a Kotlin runtime-status type mismatch and governance identifier-range checks. Those source issues were corrected in subsequent main commits.\n- Latest exact-main CI run after the test correction is queued; do not claim release verification until its Android build, JVM tests, artifact inspection and hash capture all pass.
- Do not report APK availability until artifact enumeration confirms a non-empty APK and its SHA-256.
- An APK/AAB was produced by run 2985 on an older commit, but that run's JVM test stage failed and the artifact is not current-main evidence. No successful APK artifact has been verified for the latest main commit.
- Device tests must cover network failure, malformed response, large structure, Keystore loss, saved-record deletion, FASTA result persistence and actual 3D viewer opening.
- Track U remains OPEN. Public retrieval source integration is not equivalent to U-track completion or scientific validation.


## 8. Public database integration follow-through — 2026-11-18

- The integration checklist is committed at `docs/track-u/public-database-integration-checklist.md`; it separates implemented source paths from provider expansion, parser work, reliability and acceptance evidence.
- The public database rulebook status is reconciled with implementation: NCBI Gene ELink discovery, saved-record listing/deletion, FASTA re-analysis and mmCIF reopen are present in source. Metadata/analysis SQLite remains plaintext; raw payloads alone are encrypted.
- Workflow `44233607824` was created for `e89c475a2ad2fe4c5451926f077d5d1a9bb434a9`. Host-side scientific smoke/test jobs reported success; Android test/build was still running at audit refresh. No final Android conclusion or exact-head APK artifact is claimed.
- The earlier Android compiler failure was isolated to a test fixture passing a Long expression to a ByteArray size parameter. The fixture was corrected at `e89c475a2ad2fe4c5451926f077d5d1a9bb434a9`. This correction is not verified until exact-head JVM tests pass.
- Documentation commits trigger a new exact-head run. At refresh, workflow `44233969938` for `ca95e2816d93feffc29b487195d7b7c3fa445e8c` was pending.
- Track U and public database integration remain OPEN. Continue with exact-head CI, provider journey and encrypted-record lifecycle tests, retrieval cancellation/retry/cache management, typed parser/engine integration, then physical-device and accessibility acceptance.
