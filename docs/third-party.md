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
| Chaquopy 17.2.0 | Upstream states 12.0.1+ is MIT/free-open-source; verify exact release artifact and transitive packages before distribution | Isolated R1 prototype; Python 3.11 / SDK / NDK and custom Biopython wheel build succeed; debug APK/AAB build and static 16 KB ELF inspection passed in CI | R1 candidate only; not selected for production |
| Biopython 1.88 | Upstream Biopython License Agreement applies to most files; some files are explicitly dual-licensed under that agreement or BSD-3-Clause; file-level audit required | Custom CPython 3.11 / arm64-v8a wheel built and packaged; APK/AAB static ELF 16 KB checks passed; Android runtime and file-level license audit pending | Not approved for production bundling; file-level license and ABI review required |
| SciPy (version TBD) | BSD-3-Clause | No compatible CPython 3.11 / arm64-v8a distribution found in Chaquopy indexes; custom build/alternative not yet evaluated | Not approved for bundling; required architecture candidate remains unresolved |\n| Parasail v2.6.2 (candidate) | Battelle BSD-style license; source/binary notice retention and citation requirements; restrictions on Battelle name use | Candidate sequence-alignment engine; upstream describes C99 SIMD Smith–Waterman, Needleman–Wunsch and semi-global algorithms, CMake build and ARM cross-compilation; Android build not yet attempted | Evaluation only; no product bundling approval; pin/audit source and preserve license/citation obligations before adoption |\n| Mol* 5.13.1 (candidate) | MIT license; preserve copyright and permission notice; audit bundled/transitive assets | Candidate offline macromolecular viewer; npm distribution and viewer bundle documented; local asset packaging/WebView worker and WebGL behavior not tested | Evaluation only; not bundled or approved |\n| RDKit (candidate) | BSD-3-Clause upstream core license; audit bundled/transitive dependencies and contributed modules | Mature C++ cheminformatics toolkit; official build documentation describes CMake builds, but does not establish Android arm64 support; Boost/dependency and binary-size burden not measured | Alternative chemistry engine candidate; Android feasibility not established; not approved for bundling |

References:
- https://chaquo.com/chaquopy/documentation/
- https://chaquo.com/chaquopy/doc/current/versions.html
- https://chaquo.com/chaquopy/license/
- https://github.com/chaquo/chaquopy/blob/master/LICENSE.txt

No R1 candidate is approved for bundling by this entry. GPL/AGPL and other restrictive terms remain subject to explicit owner review. The project's own license is Apache-2.0 by owner decision D-001; the canonical LICENSE grant file remains pending.


Biopython references:
- Upstream license: https://github.com/biopython/biopython/blob/master/LICENSE.rst
- Upstream installation/build requirements: https://pypi.org/project/biopython/
- Chaquopy FAQ and Android wheel build guidance: https://chaquo.com/chaquopy/doc/current/faq.html and https://github.com/chaquo/chaquopy/tree/master/server/pypi



Parasail references:
- Upstream repository and build documentation: https://github.com/jeffdaily/parasail
- Pinned release tag: https://github.com/jeffdaily/parasail/tree/v2.6.2
- Exact upstream license text: https://github.com/jeffdaily/parasail/blob/v2.6.2/LICENSE.md
- Scientific citation: Daily J. (2016). Parasail: SIMD C library for global, semi-global, and local pairwise sequence alignments. BMC Bioinformatics 17:1–11. doi:10.1186/s12859-016-0930-z


Mol* references:
- https://github.com/molstar/molstar
- https://github.com/molstar/molstar/blob/master/LICENSE
- https://www.npmjs.com/package/molstar

RDKit references:
- https://github.com/rdkit/rdkit
- https://github.com/rdkit/rdkit/blob/master/license.txt
- https://www.rdkit.org/docs/Install.html
