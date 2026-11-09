"""Explicit, versioned NCBI genetic-code translation; never infer a code from one sequence."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


_CODON_ORDER = "TCAG"
_STANDARD_AMINO_ACIDS = (
    "FFLLSSSSYY**CC*W"
    "LLLLPPPPHHQQRRRR"
    "IIIMTTTTNNKKSSRR"
    "VVVVAAAADDEEGGGG"
)
_STANDARD_CODONS = tuple(
    first + second + third
    for first in _CODON_ORDER
    for second in _CODON_ORDER
    for third in _CODON_ORDER
)
_STANDARD_TABLE = dict(zip(_STANDARD_CODONS, _STANDARD_AMINO_ACIDS, strict=True))


@dataclass(frozen=True)
class GeneticCode:
    table_id: int
    name: str
    starts: frozenset[str]
    table: Mapping[str, str]

    @property
    def stops(self) -> frozenset[str]:
        return frozenset(codon for codon, amino_acid in self.table.items() if amino_acid == "*")


def _code(
    table_id: int,
    name: str,
    starts: str,
    overrides: Mapping[str, str] | None = None,
) -> GeneticCode:
    table = dict(_STANDARD_TABLE)
    if overrides:
        table.update(overrides)
    return GeneticCode(
        table_id,
        name,
        frozenset(starts.split()),
        MappingProxyType(table),
    )


GENETIC_CODES: Mapping[int, GeneticCode] = MappingProxyType({
    1: _code(1, "Standard", "TTG CTG ATG"),
    2: _code(
        2, "Vertebrate Mitochondrial", "ATT ATC ATA ATG GTG",
        {"ATA": "M", "TGA": "W", "AGA": "*", "AGG": "*"},
    ),
    4: _code(
        4, "Mold, Protozoan and Mycoplasma/Spiroplasma Mitochondrial",
        "TTA TTG CTG ATT ATC ATA ATG GTG", {"TGA": "W"},
    ),
    5: _code(
        5, "Invertebrate Mitochondrial", "TTG ATT ATC ATA ATG GTG",
        {"ATA": "M", "TGA": "W", "AGA": "S", "AGG": "S"},
    ),
    11: _code(
        11, "Bacterial, Archaeal and Plant Plastid", "TTG CTG ATT ATC ATA ATG GTG",
    ),
})


def translate_coding_sequence(
    sequence: str,
    *,
    table_id: int = 1,
    frame: int = 0,
    cds: bool = False,
    trim_partial_codon: bool = False,
) -> dict[str, object]:
    """Translate canonical DNA/RNA with an explicit NCBI table and reading frame.

    With cds=True, require a table-specific valid start, terminal stop and no
    internal stops; the initiator is represented as methionine and terminal stop
    is omitted. This function does not identify genes or infer the organism's code.
    """
    if (
        isinstance(table_id, bool)
        or not isinstance(table_id, int)
        or table_id not in GENETIC_CODES
    ):
        raise ValueError(f"Unsupported NCBI genetic code table: {table_id}")
    if not isinstance(frame, int) or isinstance(frame, bool) or frame not in (0, 1, 2):
        raise ValueError("frame must be the integer 0, 1 or 2")
    if not isinstance(cds, bool) or not isinstance(trim_partial_codon, bool):
        raise ValueError("cds and trim_partial_codon must be booleans")
    normalized = "".join(sequence.split()).upper().replace("U", "T")
    if not normalized:
        raise ValueError("Coding sequence must not be empty")
    invalid = sorted(set(normalized) - set("ACGT"))
    if invalid:
        raise ValueError(f"Only unambiguous DNA/RNA bases are supported: {''.join(invalid)}")

    coding = normalized[frame:]
    remainder = len(coding) % 3
    if remainder and not trim_partial_codon:
        raise ValueError("Sequence length in the selected frame is not divisible by three")
    if remainder:
        coding = coding[:-remainder]
    if not coding:
        raise ValueError("No complete codons remain in the selected frame")

    code = GENETIC_CODES[table_id]
    codons = [coding[index:index + 3] for index in range(0, len(coding), 3)]
    if cds:
        if codons[0] not in code.starts:
            raise ValueError(f"CDS start codon {codons[0]} is invalid for table {table_id}")
        if codons[-1] not in code.stops:
            raise ValueError(f"CDS terminal codon {codons[-1]} is not a stop for table {table_id}")
        if any(codon in code.stops for codon in codons[:-1]):
            raise ValueError("CDS contains an internal in-frame stop codon")
        protein = "M" + "".join(code.table[codon] for codon in codons[1:-1])
    else:
        protein = "".join(code.table[codon] for codon in codons)

    warnings = [
        "Translation uses the explicitly selected NCBI table; no genetic-code inference was performed",
        "No gene boundary, transcript, strand, reading-frame or biological function was inferred",
        "Only unambiguous canonical DNA/RNA bases are accepted",
    ]
    if remainder:
        warnings.append(f"Trimmed {remainder} trailing base(s) outside a complete codon")
    return {
        "protein": protein,
        "table_id": code.table_id,
        "table_name": code.name,
        "frame": frame,
        "cds_validation": "passed" if cds else "not_requested",
        "codon_count": len(codons),
        "start_codon": codons[0] if cds else None,
        "terminal_stop_codon": codons[-1] if cds else None,
        "trimmed_trailing_bases": remainder,
        "warnings": warnings,
    }
