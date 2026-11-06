# Step 6 implementation status

**Native molecular visualization and simulation: foundation implemented; full step remains in progress.**

Implemented in this change:
- C++17/CMake molecular scene core and command-line PDB inspector.
- First-model PDB parsing with preservation of atom serials, residue/chain identity, alternate location, element, occupancy, B-factor and coordinates in angstrom.
- Explicit CONECT-only bonds, strict duplicate/dangling-reference validation and no silent distance-based bond inference.
- Validated atom selection/highlight sets and an atom-to-atom distance reference operation.
- Versioned JSON scene contract and a Python bridge that invokes the native binary without a shell, validates the returned scene, and records the source SHA-256.
- Parameter-validated OpenMM/GROMACS simulation-plan schema recording force field, water model, integrator, timestep, steps, temperature, pressure, seed and input hash. Plans explicitly say planned_not_executed.

Not yet accepted as complete:
- This first parser supports PDB only; mmCIF and biological assemblies are not implemented.
- No GPU renderer, camera/interactive desktop viewer, molecular surfaces or interaction overlays are implemented.
- The simulation interface currently produces a traceable plan only. It does not generate engine-specific OpenMM/GROMACS input decks or execute simulations.
- Native cross-platform build/test evidence must pass CI; reference fixtures are minimal and do not replace validation against reviewed reference structures.
- No representative performance profile exists; no optimization or performance claim is made.

See docs/NATIVE_MOLECULAR_ENGINE.md for scope, limitations, build instructions and acceptance gaps.
