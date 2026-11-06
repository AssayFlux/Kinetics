"""Reproducible MMseqs2 sequence-cluster assignment wrapper."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pandas as pd

from .provenance import file_record, write_json_atomic

_VALID_AA = set("ACDEFGHIKLMNPQRSTVWYXBZUO")


def _normalize_sequence(value: object, record_id: str) -> str:
    sequence = "".join(str(value).split()).upper()
    if not sequence:
        raise ValueError(f"Empty sequence for record {record_id}")
    invalid = sorted(set(sequence) - _VALID_AA)
    if invalid:
        raise ValueError(
            f"Invalid amino-acid symbols for record {record_id}: {''.join(invalid)}"
        )
    return sequence


def cluster_sequences(
    frame: pd.DataFrame,
    *,
    sequence_column: str = "sequence",
    record_id_column: str = "source_record_id",
    source_column: str | None = "source",
    output_dir: str | Path,
    min_sequence_identity: float = 0.4,
    coverage: float = 0.8,
    threads: int = 1,
) -> tuple[Path, Path]:
    """Cluster protein entities and map each unique source/record key to one cluster.

    Repeated observations with the same source/record key are collapsed only when
    their normalized sequences agree; conflicting sequences for one key are rejected.
    This supports canonical one-target-per-row tables where one source record may
    yield separate Km and kcat observations.
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
    if frame.empty:
        raise ValueError("At least one sequence record is required")
    if frame[sequence_column].isna().any() or frame[record_id_column].isna().any():
        raise ValueError("Sequence and record ID columns must not contain missing values")

    record_ids = frame[record_id_column].astype(str).tolist()
    if any(not value.strip() for value in record_ids):
        raise ValueError("Record IDs must be non-empty")
    use_source = source_column is not None and source_column in frame.columns
    if use_source:
        if frame[source_column].isna().any():
            raise ValueError("Source IDs must not be missing")
        source_ids = frame[source_column].astype(str).tolist()
        if any(not value.strip() for value in source_ids):
            raise ValueError("Source IDs must be non-empty")
        identity_keys = [
            f"{len(source)}:{source}{record_id}"
            for source, record_id in zip(source_ids, record_ids, strict=True)
        ]
    else:
        source_ids = []
        identity_keys = record_ids

    normalized_sequences = [
        _normalize_sequence(sequence, record_id)
        for sequence, record_id in zip(
            frame[sequence_column].tolist(), record_ids, strict=True
        )
    ]
    identity_sequence: dict[str, str] = {}
    unique_indices = []
    for index, (key, sequence) in enumerate(
        zip(identity_keys, normalized_sequences, strict=True)
    ):
        previous = identity_sequence.get(key)
        if previous is not None and previous != sequence:
            raise ValueError(
                "A source/record identity maps to conflicting protein sequences"
            )
        if previous is None:
            identity_sequence[key] = sequence
            unique_indices.append(index)

    executable = shutil.which("mmseqs")
    if executable is None:
        raise RuntimeError("MMseqs2 executable 'mmseqs' was not found on PATH")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    fasta = output / "sequences.fasta"
    token_to_record: dict[str, str] = {}
    token_to_source: dict[str, str] = {}
    with fasta.open("w", encoding="utf-8", newline="\n") as handle:
        for token_index, row_index in enumerate(unique_indices):
            token = f"kinetics_seq_{token_index:09d}"
            token_to_record[token] = record_ids[row_index]
            if use_source:
                token_to_source[token] = source_ids[row_index]
            handle.write(f">{token}\n{normalized_sequences[row_index]}\n")

    prefix = output / "mmseqs_clusters"
    temporary = output / "mmseqs_tmp"
    command = [
        executable, "easy-cluster", str(fasta), str(prefix), str(temporary),
        "--min-seq-id", str(min_sequence_identity), "-c", str(coverage),
        "--cov-mode", "0", "--threads", str(threads),
    ]
    version_result = subprocess.run(
        [executable, "version"], check=True, capture_output=True, text=True
    )
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    cluster_file = Path(f"{prefix}_cluster.tsv")
    if not cluster_file.is_file():
        raise RuntimeError(f"MMseqs2 completed but cluster file is missing: {cluster_file}")
    clusters = pd.read_csv(
        cluster_file,
        sep="\t",
        header=None,
        names=["representative", "member"],
        dtype=str,
    )
    if clusters.empty or clusters["member"].duplicated().any():
        raise RuntimeError("MMseqs2 output is empty or assigns a member more than once")
    clusters["source_record_id"] = clusters["member"].map(token_to_record)
    clusters["cluster_representative_record_id"] = clusters["representative"].map(
        token_to_record
    )
    if use_source:
        clusters["source"] = clusters["member"].map(token_to_source)
        clusters["cluster_representative_source"] = clusters["representative"].map(
            token_to_source
        )
    if (
        clusters["source_record_id"].isna().any()
        or clusters["cluster_representative_record_id"].isna().any()
    ):
        raise RuntimeError("MMseqs2 output contains identifiers absent from the input mapping")
    mapped_tokens = set(clusters["member"])
    expected_tokens = set(token_to_record)
    if mapped_tokens != expected_tokens:
        raise RuntimeError(
            "MMseqs2 output does not cover every unique protein entity exactly once "
            f"(missing={len(expected_tokens - mapped_tokens)}, "
            f"extra={len(mapped_tokens - expected_tokens)})"
        )

    mapping_path = output / "sequence_clusters.csv"
    mapping_columns = ["source_record_id", "cluster_representative_record_id"]
    if use_source:
        mapping_columns = [
            "source", "source_record_id",
            "cluster_representative_source", "cluster_representative_record_id",
        ]
    clusters[mapping_columns].to_csv(mapping_path, index=False)
    manifest_path = output / "sequence_cluster_manifest.json"
    write_json_atomic({
        "schema_version": "1.0",
        "tool": "MMseqs2",
        "version": version_result.stdout.strip(),
        "command": command,
        "min_sequence_identity": min_sequence_identity,
        "coverage": coverage,
        "coverage_mode": 0,
        "threads": threads,
        "input_observation_rows": len(frame),
        "unique_protein_entities": len(unique_indices),
        "repeated_observation_rows_collapsed": len(frame) - len(unique_indices),
        "record_identity_columns": (
            [source_column, record_id_column] if use_source else [record_id_column]
        ),
        "cluster_count": int(clusters["cluster_representative_record_id"].nunique()),
        "input_fasta": file_record(fasta),
        "mmseqs_cluster_output": file_record(cluster_file),
        "mapping": file_record(mapping_path),
        "mapping_rows": len(clusters),
        "unique_entities_all_assigned_once": len(clusters) == len(unique_indices),
        "observation_rows_resolvable_by_identity_key": True,
        "stdout": completed.stdout[-4000:],
        "stderr": completed.stderr[-4000:],
    }, manifest_path)
    return mapping_path, manifest_path
