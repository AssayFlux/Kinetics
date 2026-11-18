# Baseline and branch governance

**Policy version:** 1.0  
**Applies to:** all Kinetics source, build, scientific data, documentation and release artifacts.

## 1. Release states are distinct

A version moves through these states in order:

1. **Declared** — version metadata and scope exist.
2. **Candidate** — source is under release stabilization; acceptance gates remain open.
3. **Built** — a clean build completed on the exact commit and produced verified artifacts.
4. **Accepted** — required automated, scientific, security, device, legal and owner acceptance evidence is recorded.
5. **Frozen baseline** — the accepted commit is tagged and protected from mutation.

A version string, passing subset of CI, cancelled workflow, old artifact, or successful compilation step is not a release.

## 2. v0.1.0 baseline immutability

Before freeze, v0.1.0 is a candidate and may receive narrowly scoped release-blocker fixes.

After freeze:

- The v0.1.0 annotated tag and its target commit are immutable. Never force-move, delete/recreate, or retarget them.
- The baseline source tree is read-only. Do not commit, rebase, squash, amend, regenerate, reformat, or cherry-pick changes onto the frozen baseline.
- Do not update baseline dependencies, lockfiles, generated files, UI, scientific methods, documentation or build scripts in place.
- All new work goes to the development branch and future version.
- A critical defect is fixed on a new patch branch (for example v0.1.1), with a new version, tests, release notes and provenance. The v0.1.0 baseline remains unchanged.
- Any backport is a new patch release derived from the frozen tag; it never changes the original tag or commit.
- Preserve the original APK/AAB, SHA-256, build logs, SBOM, toolchain record, test reports and release notes as immutable evidence.

The GitHub repository administrator must enable branch protection/rulesets and tag protection for the release tag pattern. CI policy checks are defense in depth, not a substitute for GitHub-side access controls. The connector used for this repository cannot configure those administrative protections; do not claim they are enabled until verified in repository settings.

## 3. Branch model

- `main`: integration line; never represents an immutable released baseline by itself.
- `release/0.1.0`: stabilization candidate only. Merge only fixes required by v0.1.0 acceptance gates. Freeze it only after exact-head build and all acceptance gates pass.
- `develop/v0.1.2`: forward development for the scientific rulebook and computation architecture. No unreviewed merge into the frozen baseline.
- `release/0.1.1` (if required): patch/hardening line derived from the frozen v0.1.0 tag; never rewrite the tag.
- Feature branches: short-lived, scoped, tested and merged through reviewed pull requests.

A branch name is not proof of protection. Verify GitHub branch rules before relying on required reviews, status checks or force-push restrictions.

## 4. Change-control rules

Every change must:

1. State its target release and requirement/issue.
2. Identify affected app workflows, Python APIs, Android dispatchers, capability registry, schemas, data packs, docs and generated artifacts.
3. Include tests for behaviour and negative/error paths.
4. Preserve input/output compatibility or document a schema/API migration.
5. Record dependency version, source, checksum and licence impact.
6. Preserve provenance, units, parameter defaults, deterministic seeds and method limitations for scientific outputs.
7. Update user-facing claims only when implementation and evidence support them.
8. Update changelog, release manifest and relevant audit documents.
9. Pass CI on the exact commit intended for merge/release.
10. Receive review before merge; release approval remains an explicit owner decision.

No force push to shared branches. No direct commits to a frozen baseline. No secret, patient-identifiable data, private research data, signing keys or credentials in Git.

## 5. Versioning

- Python distribution version, Python `__version__`, Android `versionName`, changelog and release manifest must agree.
- Android `versionCode` is monotonically increasing and must never be reused for a different artifact.
- Semantic version changes require a changelog entry and release-plan update.
- A dependency-only rebuild is a new artifact with its own source commit and hashes; it is not silently substituted for a previously published artifact.
- Do not label a prerelease or candidate as stable.

## 6. Scientific integrity

- Separate implementation, Android integration, independent validation, device acceptance and clinical approval.
- A registry entry, test pass, smoke test, database record or model output does not alone establish scientific validation.
- Every generated/predicted result must identify method class (rule-based, physics-based, statistical, AI prediction or retrieval), inputs, parameters, version, provenance, uncertainty and limitations.
- Clinical and patient-specific interpretation stays disabled unless separately authorized through the relevant ethics, legal, regulatory and clinical gates.

## 7. v0.1.0 freeze checklist

- [ ] Release candidate commit identified and reviewed.
- [ ] Exact commit CI green, including APK build, JVM tests, Python suite, native/package checks.
- [ ] APK installed and exercised on named ARM64 device and supported emulator; workflow, recovery, import/export and upgrade evidence archived.
- [ ] UI, accessibility, security, privacy, licensing, notices and dependency/SBOM review accepted.
- [ ] Scientific capability claims match the release scope and evidence.
- [ ] Owner approves release notes, artifact hashes and distribution.
- [ ] Annotated `v0.1.0` tag created once and protected against update/deletion.
- [ ] Baseline manifest changed to `frozen` with exact tag, commit, APK SHA-256, CI run and evidence links.
- [ ] GitHub-side branch/tag rules verified and documented.

Until all boxes are checked, status must remain **CANDIDATE — NOT FROZEN**.
