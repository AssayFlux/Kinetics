# Kinetics

Kinetics is an offline-first, Android-native scientific workbench under active development. R0 foundations are complete; Research Platform R1–R10 remain in progress. Source implementations exist across several phases, but required integration, scientific validation, licensing, Android verification and release evidence are still outstanding. Track S is deliberately sequenced after the complete R-track exit gate. Kinetics is not yet a validated scientific application or v0.1 release.

## Project direction
- [NORTH_STAR.md](NORTH_STAR.md) — mission, scope and guardrails.
- [ROADMAP.md](ROADMAP.md) — phases, dependencies and exit gates.
- [DECISIONS.md](DECISIONS.md) — owner decisions and open questions.
- [SESSION_LOG.md](SESSION_LOG.md) — evidence-based session history.
- [docs/origin/KINETICS_MASTER.md](docs/origin/KINETICS_MASTER.md) — historical master specification.

## Current status
- R0 foundations are owner-accepted and complete. R1–R10 remain in progress; none is represented as complete. Phase plans document source implementation separately from validation and exit evidence.
- Research Mode is the only mode intended for public builds. Clinical/patient workflows remain disabled and gated.
- Latest verified CI run: [run #1650](https://github.com/AssayFlux/Kinetics/actions/runs/42450892141), commit `b5a591aa2b0545188409eacc0eb76043b4143fb8`. Python checks/tests and Android arm64 debug APK/AAB build, package-alignment verification and JVM unit tests passed.
- The CI build lane does not run an emulator or physical-device tests. The APK/AAB are unsigned debug artifacts; no app launch, SAF, lifecycle, scientific runtime, cold-start or memory claim is made. See [docs/android-feasibility.md](docs/android-feasibility.md) and [docs/ci-build-evidence.md](docs/ci-build-evidence.md).
- No scientific capability is claimed as validated; no clinical functionality or patient-data workflow is authorized.
- Project code is licensed under Apache-2.0. Third-party dependencies retain their own licenses; see [docs/third-party.md](docs/third-party.md).

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
For a reproducible Linux x86_64 build, use the [local Android build guide](docs/local-android-build.md) and `scripts/build_android_local.sh`; the same script runs in the authorized GitHub Actions build job. Neither lane runs Android emulators or physical-device tests.

## Scope and safety
Research outputs must carry provenance, uncertainty and limitations. Computational predictions are not experimental proof. Kinetics does not autonomously diagnose, prescribe, dose or make emergency decisions. No patient-related feature may be developed before P0 and applicable approvals.

## License
Original Kinetics project code is licensed under Apache-2.0; see [LICENSE](LICENSE). Third-party dependencies, engines, models and data packs retain their own terms and require separate review.
