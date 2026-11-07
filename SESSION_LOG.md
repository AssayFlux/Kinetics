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
