"""Run a real Python-to-C++ scene contract smoke test after the native build."""
from __future__ import annotations

import os
from pathlib import Path

from kinetics_core.native_molecule import inspect_structure

ROOT = Path(__file__).resolve().parents[1]

if os.name == "nt":
    executable = ROOT / "build" / "native" / "Release" / "kinetics-molecule-inspect.exe"
else:
    executable = ROOT / "build" / "native" / "kinetics-molecule-inspect"
fixture = ROOT / "native" / "tests" / "fixtures" / "reference.pdb"
scene = inspect_structure(fixture, executable=executable)
assert len(scene["atoms"]) == 2
assert len(scene["bonds"]) == 1
assert scene["coordinate_unit"] == "angstrom"
assert len(scene["provenance"]["source_sha256"]) == 64
print("Python/C++ molecular scene interoperability passed")
