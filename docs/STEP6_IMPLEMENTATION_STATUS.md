# Step 6 implementation status

> **Platform context:** This document describes a focused component of Kinetics. The complete cross-disciplinary scope is catalogued in `docs/SCIENCE_DOMAIN_CATALOGUE_100.md`; catalogue inclusion is not implementation or clinical-validation evidence.


> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

**Native molecular visualization and simulation: foundation implemented; full step remains in progress.**

Implemented in this change:
- C++17/CMake molecular scene core, command-line PDB inspector and deterministic CPU XY PPM preview renderer.
- First-model PDB parsing with preservation of atom serials, residue/chain identity, alternate location, element, occupancy, B-factor and coordinates in angstrom.
- Explicit CONECT-only bonds, strict duplicate/dangling-reference validation and no silent distance-based bond inference.
- Validated atom selection/highlight sets and an atom-to-atom distance reference operation.
- Versioned JSON scene contract and a Python bridge that invokes the native binary without a shell, validates the returned scene, and records the source SHA-256.
- Parameter-validated OpenMM/GROMACS simulation-plan schema recording force field, water model, integrator, timestep, steps, temperature, pressure, seed and input hash. Plans explicitly say planned_not_executed.

Not yet accepted as complete:
- This first parser supports PDB only; mmCIF and biological assemblies are not implemented.
- No GPU-accelerated 3D renderer, camera/interactive desktop viewer, molecular surfaces or depth-aware interaction overlays are implemented. The current XY preview is a diagnostic projection, not a full molecular viewer.
- The simulation interface currently produces a traceable plan only. It does not generate engine-specific OpenMM/GROMACS input decks or execute simulations.
- Native cross-platform build/test evidence must pass CI; reference fixtures are minimal and do not replace validation against reviewed reference structures.
- No representative performance profile exists; no optimization or performance claim is made.

See docs/NATIVE_MOLECULAR_ENGINE.md for scope, limitations, build instructions and acceptance gaps.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
