# Third-party software and data register

No third-party scientific engine, model, database, dataset or runtime payload is bundled by the R0 scaffold.

| Component | Version | Source | License | Use | Approval/status |
|---|---|---|---|---|---|
| pytest, PyYAML, Ruff, mypy, pre-commit | Ranges in requirements-dev.txt / hook revision in config | PyPI and pre-commit hook repository | Upstream terms require review before distribution | Development and CI only | Not bundled in app; audit required before release |

Before adoption, pin an exact version/revision; record canonical source and upstream license; assess redistribution, modification, attribution, patent and network obligations; flag GPL/AGPL or restrictive terms for explicit owner review; record data provenance, consent and update policy.

The project license is unselected (D-001). This file does not grant a license or approve a component for product distribution.


## R1 candidates reviewed by desk research (not adopted)

| Candidate | Upstream licensing / status | Feasibility status | Decision |
|---|---|---|---|
| Chaquopy 17.2 | Upstream states 12.0.1+ is MIT/free-open-source; verify exact release artifact and transitive packages before distribution | Android Gradle integration documented; Python 3.10–3.15 / AGP 7.3–9.5 / min API 24 documented; Biopython and exact NumPy/SciPy Android builds untested | Candidate for R1 prototype only; not selected for production |

References:
- https://chaquo.com/chaquopy/documentation/
- https://chaquo.com/chaquopy/doc/current/versions.html
- https://chaquo.com/chaquopy/license/
- https://github.com/chaquo/chaquopy/blob/master/LICENSE.txt

No R1 candidate is approved for bundling by this entry. GPL/AGPL and other restrictive terms remain subject to explicit owner review. The project's own license remains unselected.
