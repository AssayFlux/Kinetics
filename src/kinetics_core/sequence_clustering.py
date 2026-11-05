"""Reproducible MMseqs2 sequence-cluster assignment wrapper."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess

import pandas as pd

from .provenance import write_json_atomic


def cluster_sequences(
    frame: pd.DataFrame,
    *,
    sequence_column: str = "sequence",
    record_id_column: str = "source_record_id",
    output_dir: str | Path,
    min_sequence_identity: float = 0.4,
    coverage: float = 0.8,
    threads: int = 1,
) -> tuple[Path, Path]:
    """Cluster sequences with MMseqs2 and write record-to-cluster mapping + manifest.

    MMseqs2 must be installed separately. The function records its exact command,
    version output, and parameters. It does not run during repository construction.
    """
    if not 0.0 < min_sequence_identity <= 1.0:
        raise ValueError("min_sequence_identity must be in (0, 1]")
    if not 0.0 < coverage <= 1.0:
        raise ValueError("coverage must be in (0, 1]")
    if threads < 1:
        raise ValueError("threads must be >= 1")
    for column in (sequence_column, record_id_column):
        if column not in frame:
            raise ValueError(f"Missing column: {column}")
    if frame[sequence_column].isna().any() or frame[record_id_column].isna().any():
        raise ValueError("Sequence and record ID columns must not contain missing values")
    if frame[record_id_column].astype(str).duplicated().any():
        raise ValueError("Record IDs must be unique for unambiguous cluster mapping")

    executable = shutil.which("mmseqs")
    if executable is None:
        raise RuntimeError("MMseqs2 executable 'mmseqs' was not found on PATH")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    fasta = output / "sequences.fasta"
    token_to_record: dict[str, str] = {}
    with fasta.open("w", encoding="utf-8") as handle:
        for index, (_, row) in enumerate(frame.iterrows()):
            token = f"kinetics_seq_{index:09d}"
            record_id = str(row[record_id_column])
            sequence = str(row[sequence_column]).strip().upper()
            if not sequence:
                raise ValueError(f"Empty sequence for record {record_id}")
            token_to_record[token] = record_id
            handle.write(f">{token}\n{sequence}\n")

    prefix = output / "mmseqs_clusters"
    temporary = output / "mmseqs_tmp"
    command = [
        executable, "easy-cluster", str(fasta), str(prefix), str(temporary),
        "--min-seq-id", str(min_sequence_identity), "-c", str(coverage),
        "--cov-mode", "0", "--threads", str(threads),
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    cluster_file = Path(f"{prefix}_cluster.tsv")
    if not cluster_file.is_file():
        raise RuntimeError(f"MMseqs2 completed but cluster file is missing: {cluster_file}")
    clusters = pd.read_csv(cluster_file, sep="\t", header=None, names=["representative", "member"])
    clusters["source_record_id"] = clusters["member"].map(token_to_record)
    clusters["cluster_representative_record_id"] = clusters["representative"].map(token_to_record)
    if clusters["source_record_id"].isna().any() or clusters["cluster_representative_record_id"].isna().any():
        raise RuntimeError("MMseqs2 output contains identifiers absent from the input mapping")
    mapping_path = output / "sequence_clusters.csv"
    clusters[["source_record_id", "cluster_representative_record_id"]].to_csv(mapping_path, index=False)
    version = subprocess.run([executable, "version"], check=True, capture_output=True, text=True).stdout.strip()
    manifest_path = output / "sequence_cluster_manifest.json"
    write_json_atomic({
        "tool": "MMseqs2",
        "version": version,
        "command": command,
        "min_sequence_identity": min_sequence_identity,
        "coverage": coverage,
        "coverage_mode": 0,
        "threads": threads,
        "input_records": len(frame),
        "cluster_count": int(clusters["cluster_representative_record_id"].nunique()),
        "mapping_file": mapping_path.name,
        "stdout": completed.stdout[-4000:],
        "stderr": completed.stderr[-4000:],
    }, manifest_path)
    return mapping_path, manifest_path
