from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

from kinetics.genome_annotation import run_pinned_local_gff3_annotator
from kinetics.sequence import SequenceRecord


def _annotator(tmp_path: Path) -> tuple[Path, str]:
    executable = tmp_path / "annotator.py"
    executable.write_text(
        "#!" + sys.executable + "\n"
        "import pathlib, sys\n"
        "args=sys.argv[1:]\n"
        "out=pathlib.Path(args[args.index('--kinetics-output-gff3')+1])\n"
        "out.write_text('##gff-version 3\\\nctg1\\\ttest\\\tgene\\\t1\\\t9\\\t.\\\t+\\\t.\\\tID=g1\\\n')\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    return executable, hashlib.sha256(executable.read_bytes()).hexdigest()


def test_local_annotator_runs_and_validates_gff3_against_input_contig(
    tmp_path: Path,
) -> None:
    executable, digest = _annotator(tmp_path)
    result = run_pinned_local_gff3_annotator(
        [SequenceRecord("ctg1", "ATGAAATAA")],
        executable_path=str(executable),
        executable_sha256=digest,
        annotator_id="synthetic",
        annotator_version="1",
    )
    assert result["annotation"]["feature_count"] == 1
    assert result["conclusion"] == "syntax_and_coordinate_validated_gene_caller_output"


def test_local_annotator_rejects_hash_mismatch_and_out_of_bounds_feature(
    tmp_path: Path,
) -> None:
    executable, digest = _annotator(tmp_path)
    with pytest.raises(ValueError, match="SHA-256"):
        run_pinned_local_gff3_annotator(
            [SequenceRecord("ctg1", "ATGAAATAA")],
            executable_path=str(executable),
            executable_sha256="0" * 64,
            annotator_id="synthetic",
            annotator_version="1",
        )
    executable.write_text(
        "#!" + sys.executable + "\n"
        "import pathlib, sys\n"
        "args=sys.argv[1:]\n"
        "out=pathlib.Path(args[args.index('--kinetics-output-gff3')+1])\n"
        "out.write_text('##gff-version 3\\\nctg1\\\ttest\\\tgene\\\t1\\\t99\\\t.\\\t+\\\t.\\\tID=g1\\\n')\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    digest = hashlib.sha256(executable.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match="beyond supplied contig"):
        run_pinned_local_gff3_annotator(
            [SequenceRecord("ctg1", "ATGAAATAA")],
            executable_path=str(executable),
            executable_sha256=digest,
            annotator_id="synthetic",
            annotator_version="1",
        )
