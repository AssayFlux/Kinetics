# Kinetics

Kinetics is an offline-first, Android-native scientific workbench under active development. R0 foundations are complete; Research Platform R1–R10 remain in progress. Track S preparation and bounded implementation are owner-authorized in parallel where dependencies permit. Kinetics is not yet a validated scientific application or v0.1 release.

## Project direction
- [NORTH_STAR.md](NORTH_STAR.md) — mission, scope and guardrails.
- [ROADMAP.md](ROADMAP.md) — phases, dependencies and exit gates.
- [DECISIONS.md](DECISIONS.md) — owner decisions and open questions.
- [SESSION_LOG.md](SESSION_LOG.md) — evidence-based session history.
- [docs/origin/KINETICS_MASTER.md](docs/origin/KINETICS_MASTER.md) — historical master specification.
- [Track S discovery and design roadmap](docs/track-s/discovery-and-design-roadmap.md) — unknown-sequence analysis, genome annotation, genetic-code investigation and protein design.

## Current status
- R0 foundations are owner-accepted and complete. R1–R10 remain in progress; none is represented as complete. Source implementation is reported separately from scientific validation and exit evidence.
- Research Mode is the only mode intended for public builds. Clinical/patient workflows remain disabled and gated.
- Latest verified integrated CI: [run #1792](https://github.com/AssayFlux/Kinetics/actions/runs/42460656392), commit `2f426d4b70a10c3ddf4c5acbd9fd961937effb1a`. Python lint/format/type/registry/design-token checks and 119 tests passed (3 optional-dependency tests skipped). Android arm64 debug APK/AAB build, package alignment, artifact verification and Android JVM unit-test task passed.
- Build artifact: [download APK + AAB + build log](https://github.com/AssayFlux/Kinetics/actions/runs/42460656392/artifacts/13610030667). The artifact is an unsigned debug build and expires after 14 days. APK SHA-256: `21e29a2c78ba58ddd5601d67859dbb966f340c1ab0927a6c798f4cc50fe29324`. AAB SHA-256: `0b4bdbf87e3ec9c8dfcc0444f8dcbfab5d9b5922772f26e4c0dee2375bef04a5`.
- CI does not run an emulator or physical-device tests. No app launch, SAF lifecycle, scientific runtime, cold-start, memory, accessibility or device-compatibility claim is made. The APK still requires installation and hands-on runtime verification.
- The current Compose shell and design system are under active development, not a finished responsive/accessibility-proven product. See [UI specification](docs/android-ui-ux-spec.md) and [verified Android specs](docs/ui/verified-specs.md).
- No scientific capability is claimed as independently validated; computational predictions are hypotheses, not experimental proof. No clinical functionality or patient-data workflow is authorized.
- Project code is licensed under Apache-2.0. Third-party dependencies, engines, models and data packs retain their own licenses and require separate review; see [third-party inventory](docs/third-party.md).

## Developer checks
Requires Python 3.10+.
```bash
python -m pip install -r requirements-dev.txt
ruff check scripts tests
mypy scripts python/kinetics
python scripts/check_registry.py
pytest
scripts/reproduce-all
python scripts/check_android_artifacts.py
```
The reproduction command reports that no evidence jobs are registered. The Android artifact verifier requires non-empty APK/AAB outputs and records their SHA-256 hashes. Green CI does not imply Android runtime, scientific or physical-device validation.

## Local Android build
For a reproducible Linux x86_64 build, use the [local Android build guide](docs/local-android-build.md) and `scripts/build_android_local.sh`; the same script runs in the authorized GitHub Actions build job. Termux on arm64 is not the supported NDK build host; GitHub Actions is the current reproducible build lane.

## Scope and safety
Research outputs must carry provenance, uncertainty and limitations. Computational predictions are not experimental proof. Kinetics does not autonomously diagnose, prescribe, dose or make emergency decisions. No patient-related feature may be developed before P0 and applicable approvals.

## License
Original Kinetics project code is licensed under Apache-2.0; see [LICENSE](LICENSE). Third-party dependencies, engines, models and data packs retain their own terms and require separate review.
