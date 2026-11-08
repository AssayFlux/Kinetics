# Kinetics — Session Log

## 2026-11-07 — Session 2: Align direction system with complete master
**Phase:** Track R / R0 Foundations  
**Objective:** Archive the owner-supplied master, reconcile roadmap/decision log, and prepare the R0 plan before implementation.

### Done
- Re-read NORTH_STAR.md, ROADMAP.md, DECISIONS.md and prior session entry.
- Reconstructed the complete 18-part master supplied by the owner in this conversation at docs/origin/KINETICS_MASTER.md as read-only history. This is a reconstruction, not a Git move; no root master file existed.
- Updated ROADMAP to reflect actual archive and R0 status.
- Updated DECISIONS: D-007 records archival reconstruction; all six owner decisions remain open.
- Added docs/phase-r0-plan.md.
- NORTH_STAR.md was not changed.

### Validated
- Prior main-branch tree and four living files were read before edits.
- No CI, tests, registry checker, app build, scientific validation, Android feasibility or device verification has been run or claimed.

### Not done
- R0 implementation: skeleton, registry, checker, reproduce-all, pre-commit and CI.
- No LICENSE selected or added.
- No Android/device or scientific work; no P0 or clinical functionality.

### Risks / blockers
- Direction baseline remains proposed until explicit owner approval.
- R0 exit requires actual green CI on empty skeleton.
- License, jurisdictions, paper framing, advisers, PGx gene set and target devices remain open.

### Next step
Present direction documents and open decisions for owner approval. After approval, execute R0 plan and stop at its CI-green exit gate.

### Gate status
WAITING FOR OWNER APPROVAL — direction baseline. R0 implementation has not started.


## 2026-11-07 — Session 3: R0 foundations implementation
**Phase:** Track R / R0 Foundations  
**Objective:** Implement the approved empty-skeleton foundation and verify its automated checks.

### Done
- Owner explicitly approved the NORTH_STAR / ROADMAP / DECISIONS baseline.
- Confirmed current `main` head before implementation.
- Prepared repository skeleton directories for Android, Python, Rust, C++, WebView assets, engines, data packs, domains, remote node, validation, benchmarks, paper and governance.
- Added an intentionally empty capability registry, evidence-job registry, registry checker and negative/positive checker tests.
- Added reproduce-all R0 stub, developer tooling configuration, pre-commit hooks, CI workflow, README and architecture / Android feasibility / third-party records.
- Preserved existing brand assets and historical master archive.
- No LICENSE selected; six owner decisions remain open; P0 remains blocked.

### Validation status
- Automated CI has been configured but its GitHub Actions result has not yet been inspected.
- No local test execution is claimed in this session.
- Android/native toolchain, APK/AAB, 16 KB alignment and package-size checks are explicitly blocked/not applicable in R0.
- No scientific validation, Android feasibility, device verification or clinical evidence is claimed.

### Not done / risks
- R0 is not complete until the actual Actions run is green and any failures are corrected.
- Native and Android checks are deferred to R1; the workflow reports this as a blocker rather than a pass.
- Project license, jurisdictions, paper framing/venue, advisers, initial PGx gene set and target devices remain open.

### Next step
Inspect the GitHub Actions run on `main`, fix any failures, record the actual run URL/result, then stop at the R0 exit gate for owner review.


## 2026-11-07 — Session 4: R0 validation and exit-gate review
**Phase:** Track R / R0 Foundations  
**Objective:** Validate the completed R0 scaffold in GitHub Actions, record evidence and stop at the owner gate.

### Done
- Added the repository metadata and governance entry points: LICENSE status placeholder (no license grant), CHANGELOG, SECURITY, PRIVACY, CONTRIBUTING and CITATION.cff.
- Added executable `scripts/reproduce-all` wrapper and expanded pre-commit checks for Ruff, Black and mypy.
- Strengthened registry checks so implemented tools require implementation metadata; validated tools require existing validation-record IDs; device verification requires a device log; clinical tools require the Part 12 gate/evidence; and public/paper claims may reference only validated tools.
- Kept the six open owner decisions unchanged.

### Validated
- GitHub Actions run 1373: [successful run](https://github.com/AssayFlux/Kinetics/actions/runs/42378594100) on commit `043cffe1c15dbf4361a7323e2febe42155334513`.
- Pre-commit configuration validation passed.
- Ruff lint passed.
- Mypy strict type-check passed.
- Registry validation passed for the intentionally empty R0 registry.
- Unit tests: **11 passed**.
- Reproduction stub ran and correctly reported that no evidence jobs are registered.
- Android artifact check explicitly reported BLOCKED / NOT APPLICABLE: no APK/AAB exists. Native/Android CI job explicitly reports the R1 blockers and does not claim native build success.

### Not done / risks
- No Android application/build, embedded Python, Rust/C++/Kotlin implementation, scientific capability, benchmark, device run, 16 KB alignment result or APK/AAB size result exists.
- No scientific validation, clinical evidence or patient-data workflow exists.
- Project license remains unselected; jurisdictions, paper framing/venue, clinical advisers, initial PGx genes and target devices remain open.
- First CI attempt failed on Ruff lint; issues were corrected, and the subsequent complete run 1373 passed.

### Gate status
**R0 implementation and automated acceptance checks are complete. Awaiting explicit owner acceptance of the R0 exit gate. R1 has not started.**


## 2026-11-07 — Session 5: Final R0 CI verification
**Phase:** Track R / R0 Foundations  
**Objective:** Verify the final R0 documentation/governance commit and leave an accurate owner-gate status.

### Validated
- Final R0 commit: `6746e124ed888afd1d284a6a52d0eb1432b33fe9`.
- GitHub Actions run 1375 on the final R0 commit: [successful run](https://github.com/AssayFlux/Kinetics/actions/runs/42378747002).
- Both workflow jobs completed successfully.
- Pre-commit configuration validation, Ruff lint, strict mypy, registry validation, all **11 tests**, reproduce-all wrapper and Android artifact gate-status check passed.
- The native/Android job passed only its explicit R0 blocker-reporting step. No native or Android build was performed or represented as passed.

### Current state
- R0 implementation and automated acceptance checks are complete.
- R0 exit gate is awaiting explicit owner acceptance. R1 has not started.
- Six owner decisions remain open; the LICENSE file is only a no-license-selected notice, not a license grant.
- No scientific capability, scientific validation, Android feasibility, device verification, patient-data workflow or clinical feature is claimed.

### Next step
Wait for the owner's explicit R0 exit-gate approval. On approval, begin R1 feasibility planning and stop again at its go/no-go gate.


## 2026-11-07 — Session 6: R1 Android feasibility started
**Phase:** Track R / R1 Android feasibility  
**Objective:** Start the R1 feasibility investigation and define evidence requirements without crossing the R1 go/no-go gate.

### Done
- Owner authorised R1 on 2026-11-07; R0 exit is treated as accepted.
- Read NORTH_STAR.md, ROADMAP.md, DECISIONS.md and the prior session log.
- Confirmed current main tree and existing R0 scaffolding.
- Added the R1 phase plan with experiments, evidence protocol, device constraints and exit criteria.
- Updated roadmap: R0 done; R1 in progress. R2 and R3 remain not started.
- NORTH_STAR status metadata now reflects the already-approved baseline; mission and scope are unchanged.

### Not done / validation status
- No Android project, APK/AAB, emulator or physical-device experiment has been run in this session.
- Embedded Python/Biopython, Rust FFI, C++ JNI, real engine, RDKit/alternative, offline viewer, 16 KB alignment, package size, cold-start and memory results are all untested.
- No scientific capability or clinical feature is implemented or validated.
- Target device decision D-006 remains open; six owner decisions remain open.

### Risks / blockers
- Physical-device evidence requires owner-selected or owner-provided arm64 target hardware. Emulator results cannot substitute for it.
- Candidate scientific engines and chemistry libraries require upstream support and license review; restrictive licenses require owner approval.
- R1 go/no-go must be reviewed and approved before R2. R3 depends on R2 and cannot start in parallel.

### Next step
Continue R1 experiments and record raw reproducible evidence in docs/android-feasibility.md. Stop at the R1 go/no-go gate.


## 2026-11-07 — Session 7: Owner decision D-001 — project license
**Phase:** Track R / R1 Android feasibility (in progress)
**Objective:** Record the owner's project-license selection and proceed to the next owner decision without changing R1 scope.

### Done
- Owner selected **Apache License 2.0 (Apache-2.0)** on 2026-11-07.
- Recorded D-001 as approved in DECISIONS.md, including the choice, rationale/options and third-party license caveat.
- Updated ROADMAP.md: five owner decisions remain open; canonical LICENSE grant text remains to be added as a repository task.

### Not done / validation status
- The canonical Apache-2.0 LICENSE file has not yet been added; the repository must not be described as carrying the license grant until that is committed.
- Third-party engines, dependencies, models and data packs still require individual license verification.
- No R1 feasibility result is changed by this governance decision.

### Next step
- Ask the owner to decide D-002: target jurisdictions.


## 2026-11-07 — Session 8: Owner decision D-002 — target jurisdictions
**Phase:** Track R / R1 Android feasibility (in progress)
**Objective:** Record the owner's geographic and long-term clinical ambition while retaining all jurisdiction-specific safety and regulatory gates.

### Done
- Owner selected option 5: global scope, including possible future clinical use.
- Recorded D-002 in DECISIONS.md as an approved strategic scope decision.
- Updated ROADMAP.md: four owner decisions remain open; jurisdiction-specific reviews and approvals remain mandatory.

### Constraints and interpretation
- This is a product ambition, not evidence of legal compliance, regulatory clearance, market authorisation or permission to process patient data anywhere.
- Research Mode remains the only public mode; Clinical Decision Support Mode remains disabled.
- Before patient-data workflows, clinical features/studies or market entry, identify each relevant jurisdiction and obtain qualified local privacy, health-data, medical-device/software, research-ethics and other applicable advice/approvals.
- P0 and all existing clinical, ethics, security and evidence gates remain mandatory. No global approval is presumed.

### Next step
- Ask the owner to decide D-003: research-paper framing and venue strategy.


## 2026-11-07 — Session 9: Owner decision D-003 — research-paper strategy
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Record the owner's publication strategy and set evidence-based publication milestones without changing R1 scope.

### Done
- Owner selected option 4: multiple papers over time.
- Recorded D-003 as approved in DECISIONS.md.
- Updated ROADMAP.md with a staged publication strategy: platform/software-methods paper after adequate R1–R3 evidence, then separate domain papers only after independent validation.
- Recorded the owner's request for guidance at relevant milestones.

### Constraints and interpretation
- This is a publication strategy, not a claim that a paper is ready, submitted, accepted or peer reviewed.
- No unsupported capabilities, fabricated results or broad claims across unvalidated domains.
- Venue requirements, authorship, affiliations, funding, competing interests and manuscript claims require owner review when the evidence and candidate venue are known.
- R1 remains in progress; R2 remains gated on R1 evidence and explicit owner go/no-go approval.

### Next step
- Ask the owner to decide D-004: clinical advisers/advisory board.


## 2026-11-07 — Session 10: Owner decision D-004 — clinical adviser timing
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Record the owner's decision to defer clinical-adviser recruitment while preserving the P0 and clinical-scope gates.

### Done
- Owner selected option 3: defer clinical advisers until the software is more mature.
- Recorded D-004 as approved in DECISIONS.md.
- Updated ROADMAP.md: revisit adviser recruitment at a maturity milestone, targeting after R3 and before P0/PGx work.

### Constraints and interpretation
- No clinical advisers are being represented as recruited or engaged.
- P0 remains blocked until qualified advisers and all other legal, ethics, regulatory, QMS and evidence prerequisites are satisfied.
- No patient-data workflows, clinical studies, PGx gene-set selection or clinical-scope implementation may begin ahead of the required gates.
- Research Mode remains the only public mode; Clinical Decision Support Mode remains disabled.

### Next step
- Ask the owner to decide D-005: initial PGx gene set.


## 2026-11-07 — Session 11: Owner decision D-005 — initial PGx panel breadth
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Record the intended initial PGx panel breadth without selecting genes or bypassing the deferred clinical-adviser gate.

### Done
- Owner selected option 2: target a broader initial panel of approximately 15–20 genes.
- Recorded D-005 as an approved strategic breadth decision in DECISIONS.md.
- Updated ROADMAP.md to reflect the 15–20-gene target while retaining evidence-based staging.

### Constraints and interpretation
- No individual PGx gene has been selected, validated, implemented or clinically endorsed by this decision.
- Exact gene selection is deferred until qualified clinical advisers are engaged after the D-004 maturity checkpoint and before P0/PGx implementation.
- Selection must consider guideline support, reference materials, caller/assay reliability, ancestry coverage, evidence quality, licensing and validation feasibility. Do not pad the panel to meet a numerical target; a smaller or staged panel may be proposed if evidence warrants.
- P0 remains blocked; Research Mode remains the only public mode. No patient-data or clinical use is authorized.

### Next step
- Ask the owner to decide D-006: target Android devices and minimum support matrix.


## 2026-11-07 — Session 12: Correct D-005 to owner-selected six-gene PGx scope
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Correct the PGx decision record to match the owner's explicit option 1 selection.

### Done
- Owner selected option 1: focused starter set of CYP2D6, CYP2C19, CYP2C9, VKORC1, TPMT and DPYD.
- Corrected D-005 in DECISIONS.md. The prior 15–20-gene entry did not match the owner's selection and is superseded by this correction.
- Updated ROADMAP.md and the P2 scope description to reflect the provisional six-gene research scope.

### Constraints and interpretation
- The six genes are a provisional planning scope, not a clinically approved panel, validated assay or implemented capability.
- Qualified advisers must review the list after the D-004 maturity checkpoint and before P0/PGx implementation. Review includes guideline support, reference data, locus/caller limitations (including CYP2D6 structural variation), ancestry coverage, licensing and validation feasibility.
- P0 remains blocked. No patient-data or clinical use is authorized.

### Next step
- Ask the owner to decide D-006: target Android devices and minimum support matrix.


## 2026-11-07 — Session 13: Android target approved; gene scope broadened and reopened
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Record the owner's Android device target and capture the revised broad gene-scope direction without guessing its exact boundary.

### Done
- Owner approved D-006 option 1: Android 10+ (API 29), 64-bit ARM, with low-end, mid-range and flagship device test tiers.
- Updated DECISIONS.md and ROADMAP.md. This is a target matrix, not a verified compatibility claim.
- Owner clarified that the earlier six-gene PGx scope is too narrow and requested a large, broad gene scope.
- Reopened D-005 and superseded the six-gene list; exact scope boundary remains to be clarified.

### Constraints and interpretation
- Clarify whether “all types of gene” means a comprehensive PGx gene panel or a cross-domain gene catalogue spanning Kinetics' genomics and related scientific domains.
- Do not invent a gene count, freeze a list, or claim genes/callers are implemented or validated.
- PGx and all patient-related/clinical work remain subject to qualified advisers, P0, jurisdiction-specific legal/ethics/regulatory requirements and owner approval.
- R1 must test emulator and physical arm64 devices; the target does not establish support for every Android 10+ device.

### Next step
- Clarify the intended breadth of the gene catalogue before revising P2 or creating a gene inventory.


## 2026-11-07 — Session 14: Owner approves both gene-scope dimensions
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Resolve D-005 scope direction for both comprehensive PGx and cross-domain gene coverage.

### Done
- Owner explicitly selected both: (1) a comprehensive, expandable PGx gene panel and (2) a broad cross-domain gene catalogue spanning genomics and relevant Kinetics domains.
- Updated D-005 in DECISIONS.md and the gene strategy/P2 descriptions in ROADMAP.md.
- Defined PGx as a specialised workstream within the wider catalogue, with distinct evidence, reference, caller/assay, interpretation and validation requirements.

### Constraints and interpretation
- The previous six-gene list is not the agreed scope limit.
- No fixed gene count or exhaustive coverage claim is implied. Inventory and implementation waves must be evidence-led.
- Listing a gene does not imply that analysis, caller, assay or interpretation is implemented or validated.
- PGx remains research-only and gated by qualified advisers, P0, jurisdiction-specific legal/ethics/regulatory requirements and owner approval. No patient-data or clinical work is authorized.

### Next step
- Develop the gene-catalogue taxonomy and prioritisation framework as a planned work item after the current R1 feasibility gate; do not interrupt R1 or start R2 before its go/no-go approval.


## 2026-11-07 — Session 15: Direction-file reconciliation and R1 continuation
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Continue repository hygiene and keep the phase gate accurate while awaiting an unambiguous owner approval statement.

### Done
- Reconciled DECISIONS.md after D-001 through D-007 were resolved: replaced the obsolete “Open decisions” section with standing guidance and removed the superseded D-005 clarification-pending text.
- Corrected docs/android-feasibility.md to reflect the approved D-006 Android target and to avoid describing the target matrix as verified device support.
- Clarified that the first Android CI build failed on the missing host-Python prerequisite and that the later workflow result must be checked before any build-success claim.

### Gate and approval status
- The owner's message “R2 & R2 both approved” is ambiguous. A clarification was requested (R1 + R2 or R2 + R3); “Carry on” did not resolve which pair was intended. No new phase approval has been recorded from that exchange.
- R1 remains in progress. R2 remains gated on complete R1 evidence and an explicit R1 go/no-go decision. R3 depends on R2 and must not start early.
- D-001 through D-007 remain recorded as resolved/approved according to their respective scopes. The Apache-2.0 LICENSE grant text is still not installed; the current LICENSE file remains a non-grant placeholder.

### Next step
- Verify the latest Android workflow's terminal status and job steps; continue R1 experiments and record only reproducible evidence. Ask the owner to state the intended approval pair explicitly before changing phase gates.


### R1 CI evidence update — workflow run 1384
- Inspected GitHub Actions run 1384: [workflow run](https://github.com/AssayFlux/Kinetics/actions/runs/42379811746), commit `3bd4e152faf4007e44cd3fc0de63e5a26ecf065e`.
- Python foundation/registry/tests job completed successfully, including Ruff, mypy, registry validation, unit tests and reproduce-all stub.
- Android job successfully provisioned Python 3.11 and Android SDK/NDK. Gradle then failed at `:app:installDebugPythonRequirements`: pip could not find a matching `biopython` distribution in the configured PyPI/Chaquopy indexes.
- APK compilation did not complete; APK alignment, size reporting and artifact upload were skipped. No APK/AAB or Android runtime result is claimed.
- Updated docs/android-feasibility.md with this concrete blocker. Next R1 action: investigate a supported Chaquopy-compatible Biopython distribution/build strategy or a justified alternative, including license and ABI review; then rerun the build.


## 2026-11-07 — Session 16: Owner authorizes R1–R3 execution sequence
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Record the owner's explicit authorization to proceed through R1, R2 and R3 while preserving all phase exit gates.

### Owner approval
- Owner explicitly stated: “Approved R1,R2&R3” on 2026-11-07.
- Interpreted as authorization to execute R1, R2 and R3 sequentially. This resolves the earlier ambiguous “R2 & R2” wording.
- Recorded as D-008 in DECISIONS.md and reflected in ROADMAP.md.

### Gate status (unchanged)
- R1 remains in progress; run 1384's Android build is blocked at Chaquopy Biopython dependency resolution. No APK build/runtime success is claimed.
- R2 remains not started until R1 evidence is complete and the R1 go/no-go is documented.
- R3 remains not started until R2 exit evidence and approval.
- D-008 is execution authorization, not phase acceptance and not a waiver of scientific validation, licensing, physical-device, security, privacy, clinical or P0 gates.

### Next step
- Continue R1 by resolving the Biopython packaging blocker, rerunning Android build, then completing the embedded Python/native/device evidence matrix. Start R2 only after the documented R1 gate passes.


### R1 Biopython packaging investigation — 2026-11-07
- Rechecked the current Android Gradle configuration: Chaquopy 17.2.0, Python 3.11, arm64-v8a, and unpinned `biopython`, `numpy`, `scipy` pip installs.
- Reviewed current Chaquopy FAQ, package-index listing, wheel-build instructions and version-17 pip behavior. The no-matching-distribution error indicates there is no compatible Android distribution available through the configured indexes. Chaquopy documents custom Android-wheel builds for packages not already supported; version 17's normal index installs are binary-only.
- Biopython upstream source builds require Python headers and a C compiler. A normal sdist install cannot be assumed to work in Chaquopy's app build task. Next experiment: inspect exact Android wheel availability, then build a reproducible CPython 3.11 arm64 wheel with Chaquopy's documented toolchain if needed; verify extension linkage, 16 KB ELF alignment, license notices and representative runtime test vectors.
- Biopython licensing is not accurately summarized as BSD-3-Clause for the whole distribution: upstream identifies the Biopython License Agreement for most files and BSD-3-Clause dual licensing for some files. Added a third-party register note; no adoption/bundling approval is implied.
- Updated `docs/android-feasibility.md` and `docs/third-party.md` with the findings and candidate path. No dependency was removed, no build success is claimed, and no production technology choice was made.


### R1 custom Biopython wheel CI experiment — 2026-11-07
- Added `android/biopython-wheel/meta.yaml` pinned to Biopython 1.88.
- Updated the Android Gradle pip configuration to consume a local Android wheel and pin Biopython 1.88 and NumPy 1.26.2.
- Updated the Android CI job to check out Chaquopy 17.2.0, download its CPython 3.11.17 Android target and the Chaquopy NumPy 1.26.2 arm64 wheel, then cross-build Biopython for arm64-v8a using the documented Chaquopy wheel builder.
- CI prints the generated wheel SHA-256 and proceeds to APK/AAB build and 16 KB APK alignment check only if the wheel build succeeds.
- Updated the R1 evidence matrix and third-party register. This is an experiment, not a validated package: the CI run, APK build, emulator import/tests, ELF inspection and physical-device tests are still pending.
- Biopython 1.88 is pinned to a current upstream release; upstream PyPI metadata identifies NumPy as a required dependency and a Biopython-specific license expression. The custom recipe includes NumPy 1.26.2 as a host dependency for the cross-build. No production bundling approval is implied.


### R1 build pipeline correction — 2026-11-07
- Confirmed from the Chaquopy 17.2.0 tag that its Python 3.11 target is 3.11.17-0 and its legacy Android wheel builder uses NDK r27.3.13750724 internally, installing it from ANDROID_HOME if needed. Removed misleading environment overrides which pointed at the app-build NDK rather than the wheel builder's own configured toolchain.
- Confirmed Biopython 1.88 declares NumPy as a required dependency and uses setuptools 74.1+ with native C extension modules. The pinned Chaquopy wheel recipe uses NumPy 1.26.2 as the host/runtime requirement input.
- Added an explicit R1 risk: Chaquopy's Python 3.11 NumPy 1.26.2 Android wheel in the index dates from 2023, before the 16 KB compatibility era. It must be ELF-inspected and runtime-tested; if it fails 16 KB validation, the stack must be rebuilt or moved to a compatible newer Python/package path.
- This correction does not establish wheel-build success, APK/AAB success, or 16 KB compatibility.


### R1 first custom-wheel CI attempt — 2026-11-07
- Latest CI run 42382373740 passed the Python foundation job (Ruff, mypy, registry validation, unit tests and reproduction stub).
- Android job provisioned Java, Python, Android SDK/NDK, installed wheel-builder dependencies, checked out the pinned Chaquopy 17.2.0 source and downloaded its CPython 3.11.17 target plus Biopython 1.88 source.
- The first custom wheel build failed before Biopython compilation: Chaquopy's wheel builder created a libpython.so alias for both libpython3.so and libpython3.11.so; the second ln -s failed because the alias already existed. This is a toolchain alias collision, not a Biopython compiler failure.
- Added an assertion-checked, CI-local patch changing that alias creation to ln -sf, so the version-specific alias takes precedence. This does not modify the pinned upstream repository or claim wheel success; rerun required.
- Aligned the prototype app minSdk to API 29, matching D-006 Android 10+ target rather than leaving an accidental API 24 app floor.


### R1 Biopython wheel build attempt 2 — 2026-11-07
- The SONAME alias patch allowed the second CI attempt to progress through Biopython 1.88 C-extension compilation for aarch64 Android.
- Link failed because Chaquopy's compiler-wrapper.py removed the workspace-local Chaquopy host-library path from the compiler command as outside its allowlisted safe directories. Consequently ld.lld could not resolve -lpython3.11. The compile command was using Chaquopy's Android clang wrapper and the expected 16 KB max-page-size linker flag.
- Patched the pinned CI checkout's compiler-wrapper safe roots to include only GITHUB_WORKSPACE, in addition to its existing safe root. This allows the generated host headers/libraries under the repository's build directory while continuing to reject arbitrary host paths. Both toolchain patches are asserted and scoped to the pinned Chaquopy 17.2.0 build checkout.
- The custom wheel has not yet completed. APK/AAB, runtime, ELF, emulator and physical-device evidence remain outstanding.


### R1 Biopython wheel success / SciPy package blocker — 2026-11-07
- Latest custom-wheel CI attempt successfully built Biopython 1.88 for CPython 3.11 / Android arm64-v8a. Wheel SHA-256: cdf569ea13eb9314e43afeb9bbd3dbdbf95616d138f775a2e12e4cb7ba0cecbf.
- Gradle then consumed the generated local Biopython wheel and downloaded NumPy 1.26.2 successfully. It stopped at SciPy: no matching distribution exists on the configured PyPI/Chaquopy indexes for this Android target. APK compilation did not start.
- Removed SciPy from the mandatory Android pip install only for the next isolated Biopython/NumPy feasibility build. Updated the runtime probe to test SciPy if present and explicitly report it unavailable if absent; an ABI/import error is not swallowed. SciPy remains a required architecture candidate and unresolved R1 item, not silently dropped.
- Added SciPy to the third-party register with BSD-3-Clause upstream licensing noted as a candidate; exact version, Android packaging and redistribution review remain open.
- R1 remains in progress. No APK/AAB, app runtime, emulator, physical-device, 16 KB or performance result is claimed.


### R1 Gradle build attempt after SciPy isolation — 2026-11-07
- CI run 1451 passed the Python foundation job.
- The Android job successfully built the pinned Biopython 1.88 arm64 wheel, installed it from local find-links, and resolved/installed NumPy 1.26.2 plus Chaquopy OpenBLAS/libcxx/libgfortran runtime wheels. SciPy was the only package-resolution blocker and is now kept as a separate unresolved R1 candidate rather than blocking the Biopython/NumPy APK probe.
- Gradle progressed through Python source packaging, proxy generation, resource processing and stopped at Kotlin compilation due to Java target 1.8 vs Kotlin target 17 mismatch.
- Updated app Gradle configuration to set Java source/target compatibility and Kotlin compiler JVM target to 17. Rerun required. No APK/AAB, zipalign, ELF, runtime or device result is yet available.


## 2026-11-07 — Session 15: R1 arm64 build and static 16 KB package evidence
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Complete the first successful Android arm64 packaging experiment and inspect the actual APK/AAB native ELF payloads.

### Done
- Fixed the Java/Kotlin JVM target mismatch by setting both toolchains to Java 17.
- CI run 1454 succeeded on commit `87a5b6f0fcae54de6858bc32d7472379ba09ccc7`: Python foundations and Android arm64 build jobs both green.
- Built and uploaded arm64 debug APK (65,388,299 bytes) and AAB (37,573,255 bytes).
- APK ZIP alignment check passed with `zipalign -c -P 16 -v 4`.
- Downloaded and independently inspected both build artifacts. All 22 native shared libraries in each archive were ELF64 little-endian AArch64; every PT_LOAD segment had 16 KB alignment (`p_align=0x4000`).
- Recorded APK SHA-256 `a6cd53256acfa8d408ef3fddbf8da37c98367f9dbcd082fe9c68ebcb4d53152b`, AAB SHA-256 `def0e546c518f721d839b2c4238df1a95bca75db269ca3206645e3a8c0b46dda`, and workflow artifact digest in `docs/android-feasibility.md`.
- Added a repeatable CI ELF alignment checker and extended the app probe to exercise Bio.PDB parsing alongside SeqIO and NumPy; the latter is packaged but has not run on Android.

### Validated
- Workflow: https://github.com/AssayFlux/Kinetics/actions/runs/42383161737
- Python foundation job passed Ruff, mypy, registry validation, reproduction stub and 11 unit tests.
- Android arm64 Gradle APK/AAB build, Biopython/NumPy installation, ZIP alignment and artifact upload passed.
- Static ELF inspection passed for all native libraries in APK and AAB.

### Not done / blockers
- No Android emulator or physical arm64 device runtime test; no claim that Python/Biopython/NumPy imports or app startup work on-device.
- No 16 KB emulator/device runtime test.
- SciPy Android packaging remains unresolved.
- Rust FFI, C++ JNI, actual scientific engine, RDKit/alternative, offline viewer, SAF/background/cancellation, cold-start and peak RSS remain open.
- Biopython file-level license audit and distribution approval remain open.
- R1 exit gate is not met; R2 must remain gated.

### Next step
Run the expanded Python/Biopython probe on an arm64 Android device/emulator; continue remaining R1 experiments and record owner go/no-go only after the complete evidence matrix.


## 2026-11-07 — Session 16: Expand R1 native and scientific-engine probes
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Extend the arm64 feasibility app beyond packaging into native-language and real algorithm probes.

### Done
- Added a minimal Rust static library under android/native-rust exporting a C ABI numeric function.
- Added C++17 JNI shared-library source and Kotlin bridge (NativeProbe); the app screen now calls both Rust and C++ functions with the expected 3² + 4² = 25 result.
- Wired CMake/NDK into the Android Gradle build and added CI steps to cross-compile Rust for aarch64-linux-android before the arm64 APK build.
- Added Bio.PDB structure parsing and Bio.Align.PairwiseAligner global-alignment test vector to the Python runtime probe. The known vector ACGT vs ACCT with match=2, mismatch=-1, gap-open=-5 and gap-extension=-1 yields score 5.0 on the host Biopython test.
- Evaluated Parasail v2.6.2 as a possible standalone sequence-alignment engine. Its upstream Battelle BSD-style license has source/binary notice retention and citation obligations plus restrictions on Battelle name use; recorded it as an unapproved evaluation candidate in docs/third-party.md.

### Pending validation
- CI run for the integrated Rust/C++/Python probe and native ELF gate must complete successfully.
- No on-device invocation or emulator/physical-device result exists yet.
- Parasail has not been cross-built or adopted. Biopython PairwiseAligner is a real algorithm smoke test but does not replace the separate engine/RDKit evaluation required by the phase plan.

### Remaining R1 blockers
- SciPy Android packaging or a documented and owner-approved compute boundary.
- Rust/C++ native runtime and 16 KB-device verification.
- One domain-appropriate scientific engine decision and measured Android test.
- RDKit or alternative assessment; offline molecular viewer.
- SAF import, background execution, cancellation, cold-start and peak RSS.
- Physical arm64 test devices covering the approved low/mid/flagship tiers.
- Biopython file-level license audit and all dependency redistribution reviews.

### Gate
R1 remains IN PROGRESS. No R1 go/no-go has been issued and R2 remains blocked.


## 2026-11-07 — Session 17: R1 Rust/C++ arm64 build and ELF validation passed
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Validate that the Rust and C++17 native prototypes build, link and satisfy static 16 KB ELF alignment checks in the packaged arm64 artifacts.

### Validated
- CI run 1471: https://github.com/AssayFlux/Kinetics/actions/runs/42384355517 — both jobs succeeded on commit 2683a4f2212f3337593a1ac0ff0d59cc4105f986.
- Rust static library cross-compilation for aarch64-linux-android passed.
- Gradle/CMake compiled and linked the C++17 JNI shared library with the Rust static library.
- Packaged libkinetics_native.so exports both Kotlin JNI entry points and kinetics_rust_sum_squares.
- APK: 65,405,092 bytes; SHA-256 fca08d6ba9b0b0cecb63f93d9f6c0cdeb7d115253cb80a227fd009ea57cabf09.
- AAB: 37,577,400 bytes; SHA-256 1c27e74a9501e32c2381ca387f4de88c2a2373d7da38efd28ca59ed563db1509.
- Workflow artifact archive: 75,471,020 bytes; digest sha256:38f0f76879623d2a243c69dbce0208d9fb2fe646c4370ca2936adef6786e6143.
- Both APK and AAB contain 23 native ELF libraries; all are ELF64 little-endian AArch64 with every PT_LOAD segment aligned to at least 16 KB. The CI checker and zipalign check passed.

### Not done / blockers
- Native Rust/C++ JNI calls have not yet been executed on an Android emulator or physical device.
- The Python/Biopython/NumPy/PairwiseAligner/PDB runtime probe has not yet been executed on Android.
- No 16 KB page-size emulator/device runtime test, physical-device matrix, cold-start or peak-memory measurement.
- SciPy, independent scientific engine, RDKit/alternative, offline viewer, SAF/background/cancellation and license audit remain open.
- R1 exit gate remains unmet; R2 remains blocked.


## 2026-11-07 — Session 18: Prepare physical-device validation handoff
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Make the remaining owner-device tests reproducible and collectable without overstating CI evidence.

### Done
- Added KineticsR1 Logcat output for native JNI and Python runtime reports, including stack traces on failure.
- Added a device runbook to docs/android-feasibility.md with install/launch commands, model/API/ABI/page-size capture, logcat and memory commands, expected test outputs, and five-repeat measurement guidance.
- Recorded that 4 KB Android devices validate the baseline only; a 16 KB runtime test remains separately required.

### Blocked pending device access
- No Android phone has been connected to ADB in this environment. The APK is build-validated but not device-runtime validated.
- Owner needs to connect a representative Android 10+ arm64 device and provide its model/SoC/RAM/API/page-size and run logs. A separate 16 KB emulator/device test is also required.


## 2026-11-08 — Session 19: R1 integrated arm64 build evidence rechecked
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Reconcile the current CI result and maintain an accurate phase gate before further runtime experiments.

### Validated
- Inspected the latest workflow run 1481: https://github.com/AssayFlux/Kinetics/actions/runs/42384785011, commit `a7c3fd885f408bfcd46d487d58f96358129b03b2`.
- Both Python foundation and Android arm64 jobs passed.
- Android CI passed Rust arm64 cross-compilation, Chaquopy 17.2.0 preparation, Biopython 1.88 custom arm64 wheel build, APK/AAB packaging, APK ZIP alignment, static ELF alignment and artifact upload.
- APK: 63 MiB; AAB: 36 MiB. Artifact ID 13579510157; uploaded artifact digest `sha256:1c545a16edbea1453652d7c7321af4610764ad897ec39f04fdf5b66908db45fc`.
- Static ELF checker reports 16,384-byte minimum PT_LOAD alignment for every inspected native library in APK and AAB. This is static package evidence only.
- Updated docs/android-feasibility.md to record run 1481 and explicitly distinguish static build validation from runtime/device validation.

### Not validated / still open
- No Android emulator has been booted by CI and no APK runtime smoke test has run.
- No arm64 physical phone is connected; the owner has not yet supplied the previously requested exact model. Physical-device launch/runtime, low/mid/flagship coverage, cold-start and peak RSS remain blocked.
- Python/Biopython/NumPy and Rust/C++ JNI calls are compiled/packaged but not yet confirmed executing on Android.
- No 16 KB kernel runtime test; ZIP/ELF alignment is not a substitute.
- SciPy packaging, independent domain engine, RDKit/alternative, offline molecular viewer, SAF/background/cancellation, and dependency license/redistribution review remain open.

### Phase gate
- R1 remains IN PROGRESS; no R1 go/no-go is recorded.
- Owner authorization D-008 permits execution of R1, R2 and R3 sequentially, but does not waive the R1 exit gate. R2 remains not started until complete R1 evidence and explicit R1 go/no-go approval. R3 remains dependent on R2 exit evidence and approval.
- No patient data or clinical feature work is authorized; P0 remains blocked.

### Next action
- Continue R1 runtime validation using a 16 KB Android emulator and collect physical-device identity/logs from the owner. Resolve or explicitly scope the remaining scientific/runtime and licensing items before requesting R1 go/no-go.


## 2026-11-08 — Session 20: Owner-directed local Android build workflow and R1–R3 plans
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Apply the owner's instruction to keep APK builds and Android runtime testing out of GitHub Actions, while preparing gated R1–R3 execution plans.

### Done
- Owner explicitly directed: do not build APKs in GitHub Actions and do not run GitHub-hosted Android testing; build locally first and defer device testing.
- Removed the Android arm64 APK/AAB build and Android emulator job from `.github/workflows/ci.yml`. Host-side Python, registry, lint, type and unit-test checks remain.
- Rewrote the R1 phase plan to distinguish historical CI build evidence from the required future local build and owner-device evidence.
- Added detailed, explicitly gated R2 and R3 phase plans. These are plans only; neither phase has started.
- Corrected the third-party register's malformed literal newline separators.
- Updated ROADMAP to reflect the local-build route and explicit R1/R2/R3 gates.

### Evidence and validation boundary
- Historical CI runs 1471 and 1481 remain recorded as successful cross-build/static-package evidence. No fresh local APK build is claimed.
- The previously running Android emulator job is no longer part of the workflow and may have been cancelled by the workflow change; no emulator pass is claimed.
- Python host-side CI is retained. Its next result must be checked after these documentation/workflow commits.
- No Android runtime, physical-device, SciPy, standalone scientific engine, RDKit/alternative, offline viewer or performance pass is claimed.

### Not done / blockers
- R1 remains in progress; local APK build and remaining feasibility evidence are outstanding.
- R2 remains not started until the R1 evidence matrix and explicit owner go/no-go are complete.
- R3 remains not started until R2 exit evidence and approval.
- Canonical Apache-2.0 LICENSE grant file remains outstanding.
- No patient-data or clinical work is authorized; P0 remains blocked.

### Next step
Continue R1 source-side feasibility work and prepare a reproducible local build route. Keep GitHub Actions free of APK/AAB build and Android runtime test jobs. Stop at the R1 owner go/no-go before starting R2.


## 2026-11-08 — Session 21: Local Android build handoff and license file completion
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Make the owner-directed local build reproducible and close the previously approved project-license file task.

### Done
- Added `scripts/build_android_local.sh`, a local-only Linux/WSL2 arm64 debug APK/AAB build procedure using the pinned Rust, Chaquopy, Biopython and NumPy feasibility inputs.
- Added `docs/local-android-build.md` with prerequisites, commands, expected outputs and explicit static-build/runtime evidence boundaries.
- Added a host-side `bash -n` check for the local build script; this does not build an APK or run Android.
- Added the canonical Apache License 2.0 text to the root `LICENSE`, following owner decision D-001 and the Apache Software Foundation's official license text.
- Updated README, DECISIONS, ROADMAP and third-party register to reflect the Apache-2.0 grant file and local Android build workflow.
- Corrected the malformed literal newline sequences in the third-party candidate table.

### Validation boundary
- GitHub Actions remains source-validation-only. Latest workflow run is pending at the time of this log entry; record its final outcome separately.
- The local build script has not been executed on the owner's machine. No fresh local APK/AAB, runtime or device pass is claimed.
- Historical run 1471/1481 build evidence remains static and historical only.

### Remaining gates
- R1 remains IN PROGRESS; SciPy, real scientific engine, RDKit/alternative, offline viewer, app runtime, SAF/lifecycle, performance and local APK build evidence remain open.
- R2 and R3 remain NOT STARTED; their plans are prepared but their predecessor gates have not passed.
- P0 remains blocked; no patient data or clinical features are authorized.


## 2026-11-08 — Session 22: Host-only CI verification after workflow change
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Verify the source-only CI workflow after removing GitHub-hosted Android builds and tests.

### Validated
- Workflow run 42428857132 on commit `aeaeee1b2f8075ce944cf1092f3d0d14c676aa70` completed successfully: https://github.com/AssayFlux/Kinetics/actions/runs/42428857132
- Ruff passed; mypy passed with no issues in 7 source files; registry validation passed; all 11 unit tests passed.
- Reproduction stub ran and correctly reported no registered evidence jobs.
- The local Android build script passed `bash -n` syntax validation.
- No APK/AAB build or Android emulator/runtime test ran in GitHub Actions.

### Remaining status
- R1 remains IN PROGRESS; the local build and remaining Android/scientific feasibility evidence are not yet available.
- R2 and R3 remain NOT STARTED pending predecessor gates.


## 2026-11-08 — Session 23: Final source-only CI rerun
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Verify the final Android artifact-gate wording and local build-script prerequisite corrections.

### Validated
- Workflow run 42428935274 completed successfully on commit `6580e4b254aafa09da4543b490b7af4b457d9637`: https://github.com/AssayFlux/Kinetics/actions/runs/42428935274
- Pre-commit configuration, Ruff, mypy, registry validation, all 11 unit tests, reproduction stub, local-only Android artifact gate and `bash -n scripts/build_android_local.sh` passed.
- This run did not build APK/AAB files and did not run Android emulators or devices.

### Gate
R1 remains IN PROGRESS. Host-side source CI success does not close Android build/runtime/scientific feasibility criteria. R2/R3 remain gated and not started.


## 2026-11-08 — Session 14: Research platform R1–R10 execution mandate
**Phase:** Track R / R1 (in progress; R2–R10 remain dependency-gated)  
**Objective:** Begin a careful, evidence-led execution pass across the Research Platform track without weakening owner-approved phase gates.

### Owner instruction
- Owner instructed: complete Research Platform R1 through R10 carefully; no shortcuts or unsupported completion claims.
- Existing build policy remains: no APK/AAB builds or Android emulator tests in GitHub Actions; local build first, physical-device testing deferred by owner.
- Existing sequential phase gates remain binding. R2 requires R1 evidence and explicit go/no-go; R3 requires R2 exit approval; later work packages retain their listed dependencies and governance gates.

### Repository audit and corrections
- Re-read ROADMAP, NORTH_STAR, DECISIONS, R1/R2/R3 plans, local Android build guide, third-party register and Android feasibility record.
- Confirmed R1 is still incomplete; R2/R3 are planned but not started.
- Corrected ROADMAP's stale statement that the Apache-2.0 LICENSE file remained to be added.
- Corrected ROADMAP R10 wording so it does not imply GitHub Actions APK builds, which the owner explicitly prohibited.
- Corrected stale Android feasibility chronology that incorrectly said no APK/AAB had ever been produced after historical CI runs 1471/1481.

### Commits
- `4f3a86a4bfc2587e7fb815a1a3fd29111538e503` — reconcile Research Platform roadmap and release-channel/build policy.
- `eb587564a0e921e6184ac1d2180c1b1f9bbb0b35` — reconcile Android feasibility chronology and local-only build policy.

### Validation and limitations
- Documentation edits only; no application source changes or new tests were performed in this session.
- No fresh local APK/AAB build, Android runtime/device test, scientific validation or R1 go/no-go is claimed.
- R1's documented technical and owner-device blockers remain open. R2–R10 are not marked complete or started ahead of their dependency gates.

### Next work
- Perform a source-level R1 audit of Android Gradle configuration, Python probe, Rust FFI, C++ JNI, native alignment checker and local build script; fix verified defects and add host-side tests where possible.
- Continue engine, offline viewer, lifecycle, security and licensing investigations with pinned evidence.
- Update phase and roadmap status only when each exit criterion has supporting evidence.


## Session 15 — R1 source audit and ELF checker hardening (2026-11-08)

### Owner instruction
- Owner approved continuation and reiterated the requirement to complete Research Platform R1–R10 carefully, without unsupported completion claims.
- Continue in dependency order. R1 remains the active phase; R2 and R3 remain gated by their documented exit criteria and owner reviews. R4–R10 remain downstream roadmap packages.
- Preserve the owner directive: no APK/AAB builds or Android emulator/device tests in GitHub Actions; local APK build and physical-device testing remain owner-controlled.

### Work completed
- Audited the R1 Android project layout, Gradle configuration, Kotlin probes, Python runtime probe, Rust FFI, C++ JNI and ELF checker.
- Found that the prior ELF checker only compared minimum PT_LOAD p_align with 16 KB. It did not verify ELF program-header bounds/entry sizes, alignment power-of-two, or p_offset/p_vaddr congruence.
- Hardened scripts/check_android_elf_alignment.py to validate ELF64 little-endian version 1, AArch64, program-header table bounds and sizes, PT_LOAD presence, each load segment's 16 KB minimum alignment, power-of-two alignment and p_offset/p_vaddr congruence.
- Added tests/test_android_elf_alignment.py with synthetic valid and invalid ELF fixtures.
- Corrected escaped byte literals after the first CI test run exposed the fixture-signature error. The failed run is retained as a test-driven correction, not hidden.

### Verification
- Host-only CI run 42429935581 passed on commit e1560a3f74165a770438000a650a83019a01432d.
- Ruff passed; mypy passed with 8 source files; registry validation passed; all 15 unit tests passed; reproduction stub, local Android build-script syntax check and owner-directed Android artifact gate passed.
- No APK/AAB was built, no emulator/device test was run, and no Android runtime result is claimed.

### Remaining R1 blockers
- Owner local build and build-log/artifact evidence.
- Android runtime execution of Python/Biopython/NumPy and Rust/C++ JNI probes.
- SciPy architecture decision/experiment; separate scientific engine evaluation; RDKit/alternative; offline structure viewer.
- SAF import, background execution, cancellation/resume, cold-start and peak-memory evidence.
- Complete dependency/source-file license audit and explicit owner R1 go/no-go.
