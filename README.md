# Kinetics

Kinetics is planned as an offline-first, Android-native scientific workbench. The repository is at **R0 Foundations**; this is an infrastructure scaffold, not a functioning scientific application.

## Project direction
- [NORTH_STAR.md](NORTH_STAR.md) — mission, scope and guardrails.
- [ROADMAP.md](ROADMAP.md) — phases, dependencies and exit gates.
- [DECISIONS.md](DECISIONS.md) — owner decisions and open questions.
- [SESSION_LOG.md](SESSION_LOG.md) — evidence-based session history.
- [docs/origin/KINETICS_MASTER.md](docs/origin/KINETICS_MASTER.md) — historical master specification.

## Current status
- Research Mode is the only mode intended for public builds.
- No scientific capability is claimed as implemented or validated.
- No Android build, device verification, clinical functionality or patient-data workflow exists.
- No project license has been selected; see [DECISIONS.md](DECISIONS.md).

## R0 developer checks
Requires Python 3.10+.
```bash
python -m pip install -r requirements-dev.txt
ruff check scripts tests
mypy scripts tests
python scripts/check_registry.py
pytest
python scripts/reproduce_all.py
python scripts/check_android_artifacts.py
```
The reproduction command reports that no evidence jobs are registered. Android artifact checks report blocked/not applicable until R1 creates real artifacts. Green R0 CI does not imply Android, scientific or device validation.

## Scope and safety
Research outputs must carry provenance, uncertainty and limitations. Computational predictions are not experimental proof. Kinetics does not autonomously diagnose, prescribe, dose or make emergency decisions. No patient-related feature may be developed before P0 and applicable approvals.

## License
No license is selected yet. All rights reserved by default absent an explicit license grant. Do not assume this repository is open source until the owner records and adds a license.
