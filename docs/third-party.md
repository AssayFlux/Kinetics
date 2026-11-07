# Third-party software and data register

No third-party scientific engine, model or database is approved for product bundling. Chaquopy and its scientific package dependencies are configured only in the isolated R1 feasibility prototype; they are not production selections.

| Component | Version | Source | License | Use | Approval/status |
|---|---|---|---|---|---|
| pytest, PyYAML, Ruff, mypy, pre-commit | Ranges in requirements-dev.txt / hook revision in config | PyPI and pre-commit hook repository | Upstream terms require review before distribution | Development and CI only | Not bundled in app; audit required before release |

Before adoption, pin an exact version/revision; record canonical source and upstream license; assess redistribution, modification, attribution, patent and network obligations; flag GPL/AGPL or restrictive terms for explicit owner review; record data provenance, consent and update policy.

The project license decision is Apache-2.0 (D-001); the canonical LICENSE grant file is still pending. This file does not grant a license or approve a component for product distribution.


## R1 candidates reviewed by desk research (not adopted)

| Candidate | Upstream licensing / status | Feasibility status | Decision |
|---|---|---|---|
| Chaquopy 17.2.0 | Upstream states 12.0.1+ is MIT/free-open-source; verify exact release artifact and transitive packages before distribution | Isolated R1 prototype; Python 3.11 and SDK/NDK provisioned in CI; Biopython package resolution still blocks APK compilation | R1 candidate only; not selected for production |\n| Biopython (version to pin) | Upstream Biopython License Agreement applies to most files; some files are explicitly dual-licensed under that agreement or BSD-3-Clause; file-level audit required | No compatible indexed Android wheel found in run 1384; custom Android wheel is an unvalidated candidate | Not approved for bundling; license and ABI review required |

References:
- https://chaquo.com/chaquopy/documentation/
- https://chaquo.com/chaquopy/doc/current/versions.html
- https://chaquo.com/chaquopy/license/
- https://github.com/chaquo/chaquopy/blob/master/LICENSE.txt

No R1 candidate is approved for bundling by this entry. GPL/AGPL and other restrictive terms remain subject to explicit owner review. The project's own license remains unselected.


Biopython references:
- Upstream license: https://github.com/biopython/biopython/blob/master/LICENSE.rst
- Upstream installation/build requirements: https://pypi.org/project/biopython/
- Chaquopy FAQ and Android wheel build guidance: https://chaquo.com/chaquopy/doc/current/faq.html and https://github.com/chaquo/chaquopy/tree/master/server/pypi
