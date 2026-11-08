# Kinetics

Kinetics is an offline-first, Android-native scientific workbench under active development. R0 foundations are complete; Research Platform R1–R10 remain in progress. Source implementations exist across several phases, but required integration, scientific validation, licensing, Android verification and release evidence are still outstanding. Track S is deliberately sequenced after the complete R-track exit gate. Kinetics is not yet a validated scientific application or v0.1 release.

## Project direction
- [NORTH_STAR.md](NORTH_STAR.md) — mission, scope and guardrails.
- [ROADMAP.md](ROADMAP.md) — phases, dependencies and exit gates.
- [DECISIONS.md](DECISIONS.md) — owner decisions and open questions.
- [SESSION_LOG.md](SESSION_LOG.md) — evidence-based session history.
- [docs/origin/KINETICS_MASTER.md](docs/origin/KINETICS_MASTER.md) — historical master specification.

## Current status
- R0 foundations are complete. R1–R10 are all in progress; none is represented as complete. Phase plans and the integrated implementation inventory document implemented source and outstanding exit evidence.
- Research Mode is the only mode intended for public builds.
- R1 has historical Android arm64 cross-build/static-package evidence, but no current local APK build or Android runtime/device validation is claimed. The owner-directed local build and later device-test campaign remain outstanding.
- GitHub Actions runs host-side source checks only; it does not build APK/AAB files or run Android emulators. See [docs/phase-r1-plan.md](docs/phase-r1-plan.md).
- No scientific capability is claimed as validated; no clinical functionality or patient-data workflow is authorized.
- Project code is licensed under Apache-2.0. Third-party dependencies retain their own licenses; see [docs/third-party.md](docs/third-party.md).

## Developer checks
Requires Python 3.10+.
```bash
python -m pip install -r requirements-dev.txt
ruff check scripts tests
mypy scripts tests
python scripts/check_registry.py
pytest
scripts/reproduce-all
python scripts/check_android_artifacts.py
```
The reproduction command reports that no evidence jobs are registered. The Android artifact gate explicitly reports that APK/AAB build and runtime checks are local-only by owner instruction. Green source CI does not imply Android, scientific or device validation.

## Local Android build
When ready, use the owner-run [local Android build guide](docs/local-android-build.md) and `scripts/build_android_local.sh`. GitHub Actions deliberately does not build APK/AAB files or run Android emulators.

## Scope and safety
Research outputs must carry provenance, uncertainty and limitations. Computational predictions are not experimental proof. Kinetics does not autonomously diagnose, prescribe, dose or make emergency decisions. No patient-related feature may be developed before P0 and applicable approvals.

## License
Original Kinetics project code is licensed under Apache-2.0; see [LICENSE](LICENSE). Third-party dependencies, engines, models and data packs retain their own terms and require separate review.
