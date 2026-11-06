# Native molecular engine — Step 6 foundation

## Scope and supported platforms

The first native module is a dependency-free C++17 molecular-structure and scene-data core, built with CMake. The declared initial build matrix is Ubuntu, macOS and Windows using each CI runner's default C++ compiler. This is not yet a GPU renderer or desktop viewer: it produces a versioned, render-ready scene contract for a later VTK/Qt or other renderer decision.

## Structure contract

- Input: PDB coordinate files. The first MODEL is selected deterministically; files without MODEL records are treated as one model.
- Atom serial, atom name, alternate location, residue name, chain, residue sequence, insertion code, element, occupancy, temperature factor and Cartesian coordinates are retained.
- Coordinates are finite floating-point values in angstrom. No implicit conversion, centering, alignment, atom renumbering, element inference, alternate-location selection or coordinate mutation is performed.
- Bonds are loaded only from explicit CONECT records. No distance-based bond guessing or chemical bond-order inference is performed. Missing CONECT means no declared bonds.
- Invalid/truncated atom records, duplicate serials, non-finite coordinates and dangling/self CONECT references fail closed.
- mmCIF, crystallographic symmetry, biological assembly expansion, anisotropic displacement tensors and multi-model ensemble browsing are outside this first parser contract.

## Scene and interoperability

The C++ MolecularScene exposes the parsed structure plus validated atom-serial selection and highlight sets. The C++ inspector writes the versioned kinetics.molecular-scene/1.0 JSON contract. The Python bridge launches the explicitly supplied executable without a shell, validates atom/bond references and coordinates, and adds the source file SHA-256 and engine version. The scene schema records coordinate units; callers must not treat coordinates as unitless.

## Measurements

The native reference API includes Euclidean atom-to-atom distance in angstrom. It does not calculate van der Waals contacts, infer interactions, or claim chemically meaningful distances beyond the supplied coordinates. Reference tests compare a known 1.25 Å fixture distance.

## Simulation adapter contract

The build_simulation_plan function validates and records engine/version, input structure hash, force field, water model, integrator, timestep, number of steps, temperature, optional pressure, random seed and expected output names. Supported adapter identifiers are OpenMM and GROMACS. The emitted status is explicitly planned_not_executed. It is not a generated engine input deck and does not run molecular dynamics. Production simulation acceptance still requires engine-specific adapters, reference-system tests, restart/cancellation behavior, energy/temperature stability checks and traceable execution artifacts.

## Build and test

    cmake -S native -B build/native -DKINETICS_BUILD_TESTS=ON
    cmake --build build/native --config Release
    ctest --test-dir build/native --build-config Release --output-on-failure

The CTest fixture checks atom and bond identity, coordinate preservation, known-distance calculation, unit-bearing scene JSON, selection/highlight serialization and invalid selection rejection. Python tests cover the cross-language JSON contract, source hashing and simulation-plan validation.

## Performance policy

No renderer or performance claim is made in this stage. The native reference workload is the checked-in two-atom fixture; meaningful parser/renderer benchmarks must use versioned representative structures, report atom/bond counts, compiler/build flags, hardware, wall time and peak memory. Optimize only after those profiles exist.
