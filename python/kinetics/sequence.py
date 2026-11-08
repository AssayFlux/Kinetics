"""Deterministic sequence parsing and analysis primitives; research use only."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

DNA = frozenset("ACGTRYSWKMBDHVN")
RNA = frozenset("ACGURYSWKMBDHVN")
PROTEIN = frozenset("ACDEFGHIKLMNPQRSTVWYBXZJUO*")
_COMPLEMENT = str.maketrans("ACGTRYMKSWBDHVNacgtrymkswbdhvn", "TGCAYRKM SWVHDBNtg cayrkm swvhdbn".replace(" ", ""))

@dataclass(frozen=True)
class SequenceRecord:
    identifier: str
    sequence: str
    description: str = ""

def _normalise(sequence: str) -> str:
    return "".join(sequence.split()).upper()

def iter_fasta_records(lines: Iterable[str]):
    """Yield FASTA records incrementally from an iterable of text lines."""
    header: str | None = None
    chunks: list[str] = []
    found = False
    for line_no, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith(";"):
            continue
        if line.startswith(">"):
            if header is not None:
                found = True
                yield _fasta_record(header, chunks)
            header, chunks = line[1:].strip(), []
            if not header:
                raise ValueError(f"FASTA line {line_no}: empty identifier")
        elif header is None:
            raise ValueError(f"FASTA line {line_no}: sequence before first header")
        else:
            chunks.append(line)
    if header is not None:
        found = True
        yield _fasta_record(header, chunks)
    if not found:
        raise ValueError("FASTA contains no records")


def parse_fasta(text: str) -> list[SequenceRecord]:
    """Parse FASTA text; use iter_fasta_records for large streaming inputs."""
    return list(iter_fasta_records(text.splitlines()))

def _fasta_record(header: str, chunks: list[str]) -> SequenceRecord:
    fields = header.split(maxsplit=1)
    seq = _normalise("".join(chunks))
    if not seq:
        raise ValueError(f"FASTA record {fields[0]!r}: empty sequence")
    return SequenceRecord(fields[0], seq, fields[1] if len(fields) > 1 else "")

def parse_fastq(text: str) -> list[tuple[SequenceRecord, str]]:
    """Parse wrapped FASTQ sequence and quality lines with exact length matching."""
    lines = text.splitlines()
    output: list[tuple[SequenceRecord, str]] = []
    index = 0
    while index < len(lines):
        while index < len(lines) and not lines[index].strip():
            index += 1
        if index >= len(lines):
            break
        header = lines[index]
        if not header.startswith("@") or not header[1:].strip():
            raise ValueError(f"FASTQ line {index + 1}: invalid record header")
        header_fields = header[1:].split(maxsplit=1)
        identifier = header_fields[0]
        description = header_fields[1] if len(header_fields) > 1 else ""
        index += 1

        sequence_chunks: list[str] = []
        while index < len(lines) and not lines[index].startswith("+"):
            if not lines[index].strip():
                raise ValueError(f"FASTQ line {index + 1}: empty sequence line")
            sequence_chunks.append(lines[index].strip())
            index += 1
        if index >= len(lines):
            raise ValueError(f"FASTQ record {identifier!r}: missing '+' separator")
        plus = lines[index]
        plus_identifier = plus[1:].strip().split(maxsplit=1)
        if plus_identifier and plus_identifier[0] != identifier:
            raise ValueError(f"FASTQ record {identifier!r}: separator identifier mismatch")
        index += 1

        sequence = _normalise("".join(sequence_chunks))
        if not sequence:
            raise ValueError(f"FASTQ record {identifier!r}: empty sequence")
        quality_chunks: list[str] = []
        quality_length = 0
        while index < len(lines) and quality_length < len(sequence):
            quality = lines[index]
            if not quality:
                raise ValueError(f"FASTQ line {index + 1}: empty quality line")
            quality_chunks.append(quality)
            quality_length += len(quality)
            index += 1
        if quality_length != len(sequence):
            raise ValueError(
                f"FASTQ record {identifier!r}: sequence/quality length mismatch"
            )
        quality = "".join(quality_chunks)
        if any(not 33 <= ord(char) <= 126 for char in quality):
            raise ValueError(f"FASTQ record {identifier!r}: invalid quality character")
        output.append((SequenceRecord(identifier, sequence, description), quality))
    if not output:
        raise ValueError("FASTQ contains no records")
    return output

def validate_sequence(sequence: str, alphabet: Iterable[str] = DNA) -> None:
    invalid = sorted(set(_normalise(sequence)) - set(alphabet))
    if invalid:
        raise ValueError(f"Invalid symbols: {''.join(invalid)}")

def sequence_statistics(sequence: str) -> dict[str, float | int]:
    seq = _normalise(sequence)
    if not seq:
        raise ValueError("Sequence is empty")
    counts = Counter(seq)
    canonical = sum(counts[b] for b in "ACGT")
    return {"length": len(seq), "gc_fraction": (counts["G"] + counts["C"]) / len(seq),
            "ambiguous_count": len(seq) - canonical, "a": counts["A"], "c": counts["C"],
            "g": counts["G"], "t": counts["T"], "other": len(seq) - canonical}

def reverse_complement(sequence: str) -> str:
    seq = _normalise(sequence)
    validate_sequence(seq, DNA)
    return seq.translate(_COMPLEMENT)[::-1]

def transcribe(sequence: str) -> str:
    seq = _normalise(sequence)
    validate_sequence(seq, DNA)
    return seq.replace("T", "U")

def kmer_counts(sequence: str, k: int, *, canonical_only: bool = True) -> dict[str, int]:
    seq = _normalise(sequence)
    if k < 1:
        raise ValueError("k must be >= 1")
    counts: Counter[str] = Counter()
    alphabet = set("ACGT")
    for i in range(len(seq) - k + 1):
        word = seq[i:i+k]
        if not canonical_only or set(word) <= alphabet:
            counts[word] += 1
    return dict(sorted(counts.items()))

def needleman_wunsch(a: str, b: str, *, match: int = 2, mismatch: int = -1,
                     gap: int = -2, max_cells: int = 4_000_000) -> dict[str, object]:
    """Global linear-gap alignment. Returns one deterministic optimal traceback."""
    x, y = _normalise(a), _normalise(b)
    if not x or not y:
        raise ValueError("Both sequences must be non-empty")
    rows, cols = len(x) + 1, len(y) + 1
    if max_cells < 1 or rows * cols > max_cells:
        raise ValueError("Alignment exceeds the configured memory-cell limit")
    score = [[0] * cols for _ in range(rows)]
    trace = [[""] * cols for _ in range(rows)]
    for i in range(1, rows):
        score[i][0], trace[i][0] = i * gap, "U"
    for j in range(1, cols):
        score[0][j], trace[0][j] = j * gap, "L"
    for i in range(1, rows):
        for j in range(1, cols):
            choices = (score[i-1][j-1] + (match if x[i-1] == y[j-1] else mismatch),
                       score[i-1][j] + gap, score[i][j-1] + gap)
            best = max(choices)
            score[i][j] = best
            trace[i][j] = "D" if choices[0] == best else ("U" if choices[1] == best else "L")
    ax, ay, i, j = [], [], len(x), len(y)
    while i or j:
        direction = trace[i][j]
        if direction == "D": ax.append(x[i-1]); ay.append(y[j-1]); i -= 1; j -= 1
        elif direction == "U": ax.append(x[i-1]); ay.append("-"); i -= 1
        elif direction == "L": ax.append("-"); ay.append(y[j-1]); j -= 1
        else: raise RuntimeError("Invalid alignment traceback")
    return {"score": score[-1][-1], "aligned_a": "".join(reversed(ax)),
            "aligned_b": "".join(reversed(ay)), "algorithm": "Needleman-Wunsch-linear-gap",
            "scoring": {"match": match, "mismatch": mismatch, "gap": gap}}


def trim_fastq_ends(
    record: SequenceRecord, quality: str, *, phred_offset: int = 33,
    minimum_quality: int = 20, minimum_length: int = 1,
) -> dict[str, object] | None:
    """Trim terminal low-quality bases only; returns None when below minimum_length.

    This does not perform adapter trimming, sliding-window trimming or paired-read rescue.
    """
    if phred_offset not in (33, 64):
        raise ValueError("Phred offset must be explicitly 33 or 64")
    if not 0 <= minimum_quality <= 93 or minimum_length < 1:
        raise ValueError("Quality threshold must be 0..93 and minimum_length >=1")
    if len(record.sequence) != len(quality):
        raise ValueError("Sequence/quality length mismatch")
    scores = [ord(char) - phred_offset for char in quality]
    if any(score < 0 or score > 93 for score in scores):
        raise ValueError("Quality character outside supported Phred range")
    left, right = 0, len(scores)
    while left < right and scores[left] < minimum_quality:
        left += 1
    while right > left and scores[right - 1] < minimum_quality:
        right -= 1
    if right - left < minimum_length:
        return None
    trimmed = SequenceRecord(
        record.identifier, record.sequence[left:right], record.description,
    )
    return {
        "record": trimmed,
        "quality": quality[left:right],
        "trimmed_left": left,
        "trimmed_right": len(quality) - right,
        "algorithm": "terminal low-quality trimming",
        "limitations": ["No adapter trimming", "No sliding-window quality model"],
    }
