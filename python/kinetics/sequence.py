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

def parse_fasta(text: str) -> list[SequenceRecord]:
    records: list[SequenceRecord] = []
    header: str | None = None
    chunks: list[str] = []
    for line_no, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith(";"):
            continue
        if line.startswith(">"):
            if header is not None:
                records.append(_fasta_record(header, chunks))
            header, chunks = line[1:].strip(), []
            if not header:
                raise ValueError(f"FASTA line {line_no}: empty identifier")
        elif header is None:
            raise ValueError(f"FASTA line {line_no}: sequence before first header")
        else:
            chunks.append(line)
    if header is not None:
        records.append(_fasta_record(header, chunks))
    if not records:
        raise ValueError("FASTA contains no records")
    return records

def _fasta_record(header: str, chunks: list[str]) -> SequenceRecord:
    fields = header.split(maxsplit=1)
    seq = _normalise("".join(chunks))
    if not seq:
        raise ValueError(f"FASTA record {fields[0]!r}: empty sequence")
    return SequenceRecord(fields[0], seq, fields[1] if len(fields) > 1 else "")

def parse_fastq(text: str) -> list[tuple[SequenceRecord, str]]:
    lines = [line.rstrip("\r") for line in text.splitlines() if line.strip()]
    if len(lines) % 4:
        raise ValueError("FASTQ must contain complete four-line records")
    output = []
    for i in range(0, len(lines), 4):
        head, seq, plus, quality = lines[i:i+4]
        if not head.startswith("@") or not plus.startswith("+"):
            raise ValueError(f"FASTQ record {i//4+1}: invalid header or separator")
        seq = _normalise(seq)
        if len(seq) != len(quality):
            raise ValueError(f"FASTQ record {i//4+1}: sequence/quality length mismatch")
        if not seq:
            raise ValueError(f"FASTQ record {i//4+1}: empty sequence")
        output.append((SequenceRecord(head[1:].split()[0], seq, head[1:]), quality))
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
                     gap: int = -2) -> dict[str, object]:
    """Global linear-gap alignment. Returns one deterministic optimal traceback."""
    x, y = _normalise(a), _normalise(b)
    if not x or not y:
        raise ValueError("Both sequences must be non-empty")
    rows, cols = len(x) + 1, len(y) + 1
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
