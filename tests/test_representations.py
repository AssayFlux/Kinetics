import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from kinetics_core.chemistry import molecular_graph_features, murcko_scaffold_id
from kinetics_core.features import (
    DEFAULT_ESM_REVISION,
    ESM2Encoder,
    ObservationFeatureBuilder,
    morgan_fingerprint,
)
from kinetics_core.sequence_clustering import cluster_sequences


class FakeEncoder:
    max_residues = 1022

    def __init__(self, revision="fixture-revision"):
        self.revision = revision
        self.calls = []

    def metadata(self):
        return {
            "encoder": "fixture",
            "model_revision": self.revision,
            "device_policy": "cpu",
        }

    def encode_many(self, sequences):
        self.calls.append(list(sequences))
        return [
            np.asarray([len(sequence), sum(map(ord, sequence)) % 101], dtype=np.float32)
            for sequence in sequences
        ]


def test_esm_encoder_requires_immutable_revision_and_pins_default():
    assert len(DEFAULT_ESM_REVISION) == 40
    encoder = ESM2Encoder()
    assert encoder.model_revision == DEFAULT_ESM_REVISION
    assert encoder.tokenizer_revision == DEFAULT_ESM_REVISION
    with pytest.raises(ValueError, match="immutable"):
        ESM2Encoder(model_revision="main")
    with pytest.raises(ValueError, match="max_residues"):
        ESM2Encoder(max_residues=1023)


def test_feature_cache_is_reused_and_revision_invalidates(tmp_path):
    cache = tmp_path / "cache"
    first_encoder = FakeEncoder("rev-a")
    first = ObservationFeatureBuilder(cache_dir=cache, encoder=first_encoder)
    smiles = "C[C@H](O)C(=O)O"
    one = first.transform_many(["ACDE", "ACDE"], [smiles, smiles], batch_size=1)
    assert one.shape == (2, 2050)
    assert len(first_encoder.calls) == 1
    assert len(first_encoder.calls[0]) == 1

    second_encoder = FakeEncoder("rev-a")
    second = ObservationFeatureBuilder(cache_dir=cache, encoder=second_encoder)
    two = second.transform_many(["ACDE"], ["O=C(O)[C@@H](O)C"])
    assert np.array_equal(one[0], two[0])
    assert second_encoder.calls == []

    changed_encoder = FakeEncoder("rev-b")
    changed = ObservationFeatureBuilder(cache_dir=cache, encoder=changed_encoder)
    changed.transform_one("ACDE", smiles)
    assert len(changed_encoder.calls) == 1


def test_feature_archive_has_aligned_rows_and_manifest(tmp_path):
    frame = pd.DataFrame({
        "target": ["km", "km", "kcat"],
        "source": ["db", "db", "db"],
        "source_record_id": ["001", "002", "003"],
        "canonical_value": [1e-3, 2e-3, 3.0],
        "sequence": ["ACDE", "FGHI", "KLMN"],
        "smiles": ["CCO", "CCN", "CCC"],
        "protein_cluster_id": ["p1", "p2", "p3"],
    })
    builder = ObservationFeatureBuilder(
        cache_dir=tmp_path / "cache", encoder=FakeEncoder()
    )
    archive = builder.transform_frame(
        frame,
        target="km",
        output_path=tmp_path / "km_features.npz",
        group_columns=("protein_cluster_id",),
        batch_size=1,
    )
    with np.load(archive, allow_pickle=False) as data:
        assert data["X"].shape == (2, 2050)
        assert data["source_record_ids"].tolist() == ["001", "002"]
        assert data["protein_cluster_id"].tolist() == ["p1", "p2"]
        assert data["feature_schema_version"].tolist() == ["2.0"]
        assert data["graph_atom_features"].shape == (6, 9)
        assert data["graph_edge_index"].shape == (2, 8)
        assert data["graph_bond_features"].shape == (8, 4)
        assert data["graph_atom_offsets"].tolist() == [0, 3, 6]
        assert data["graph_edge_offsets"].tolist() == [0, 4, 8]
        metadata = json.loads(data["feature_metadata_json"][0])
        assert metadata["protein"]["model_revision"] == "fixture-revision"
        assert metadata["chemical"]["include_chirality"] is True
    manifest_path = Path(str(archive) + ".manifest.json")
    manifest = json.loads(manifest_path.read_text())
    assert manifest["rows"] == 2
    assert manifest["feature_shape"] == [2, 2050]
    assert manifest["archive"]["sha256"]
    assert manifest["source_record_ids_sha256"]


def test_feature_builder_rejects_bad_inputs_and_batch_size(tmp_path):
    builder = ObservationFeatureBuilder(cache_dir=None, encoder=FakeEncoder())
    with pytest.raises(ValueError, match="unsupported amino-acid"):
        builder.transform_one("ACD*", "CCO")
    with pytest.raises(ValueError, match="Invalid SMILES"):
        builder.transform_one("ACDE", "not-smiles")
    with pytest.raises(ValueError, match="batch_size"):
        builder.transform_many(["ACDE"], ["CCO"], batch_size=0)


def test_morgan_fingerprint_preserves_stereochemistry_by_default():
    left = morgan_fingerprint("N[C@@H](C)C(=O)O")
    right = morgan_fingerprint("N[C@H](C)C(=O)O")
    assert left.shape == (2048,)
    assert not np.array_equal(left, right)
    achiral = morgan_fingerprint("N[C@@H](C)C(=O)O", include_chirality=False)
    achiral_other = morgan_fingerprint("N[C@H](C)C(=O)O", include_chirality=False)
    assert np.array_equal(achiral, achiral_other)


def test_molecular_graph_preserves_atom_stereochemistry_and_bidirectional_edges():
    left = molecular_graph_features("N[C@@H](C)C(=O)O")
    right = molecular_graph_features("N[C@H](C)C(=O)O")
    assert left["atom_features"].shape[1] == 9
    assert left["edge_index"].shape[0] == 2
    assert left["edge_index"].shape[1] == left["bond_features"].shape[0]
    directed = set(zip(left["edge_index"][0], left["edge_index"][1]))
    assert directed == {(end, start) for start, end in directed}
    assert set(left["atom_features"][:, 5]) != set(right["atom_features"][:, 5])
    with pytest.raises(ValueError, match="Invalid SMILES"):
        molecular_graph_features("invalid")


def test_murcko_scaffold_stereochemistry_policy_is_explicit():
    left = "C[C@H]1CCCCC1"
    right = "C[C@@H]1CCCCC1"
    assert murcko_scaffold_id(left) == murcko_scaffold_id(right)


def _fake_mmseqs(tmp_path, monkeypatch, *, omit_last=False):
    executable_dir = tmp_path / "bin"
    executable_dir.mkdir()
    executable = executable_dir / "mmseqs"
    executable.write_text(
        "#!/usr/bin/env python3\n"
        "import pathlib, sys\n"
        "if sys.argv[1] == 'version':\n"
        " print('MMseqs2 fixture 1.0')\n"
        "else:\n"
        " fasta = pathlib.Path(sys.argv[2])\n"
        " prefix = pathlib.Path(sys.argv[3])\n"
        " ids = [line[1:] for line in fasta.read_text().splitlines() if line.startswith('>')]\n"
        " rows = [(ids[0], ids[0])] + ([(ids[0], ids[1])] if len(ids) > 1 else [])\n"
        + (" rows = rows[:1]\n" if omit_last else "")
        + " pathlib.Path(str(prefix) + '_cluster.tsv').write_text(''.join(a+'\\t'+b+'\\n' for a,b in rows))\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    monkeypatch.setenv(
        "PATH", str(executable_dir) + os.pathsep + os.environ.get("PATH", "")
    )


def test_mmseqs_wrapper_records_hashes_and_checks_complete_mapping(tmp_path, monkeypatch):
    _fake_mmseqs(tmp_path, monkeypatch)
    frame = pd.DataFrame({
        "source_record_id": ["r1", "r2"],
        "sequence": ["ACDE", "ACDF"],
    })
    mapping, manifest_path = cluster_sequences(
        frame, output_dir=tmp_path / "clusters", threads=1
    )
    result = pd.read_csv(mapping)
    assert result["source_record_id"].tolist() == ["r1", "r2"]
    manifest = json.loads(manifest_path.read_text())
    assert manifest["input_records_all_assigned_once"] is True
    assert manifest["input_fasta"]["sha256"]
    assert manifest["mapping"]["sha256"]
    assert manifest["version"] == "MMseqs2 fixture 1.0"


def test_mmseqs_wrapper_rejects_invalid_or_unassigned_sequences(tmp_path, monkeypatch):
    _fake_mmseqs(tmp_path, monkeypatch, omit_last=True)
    frame = pd.DataFrame({
        "source_record_id": ["r1", "r2"],
        "sequence": ["ACDE", "ACDF"],
    })
    with pytest.raises(RuntimeError, match="does not cover each input"):
        cluster_sequences(frame, output_dir=tmp_path / "incomplete")
    invalid = frame.copy()
    invalid.loc[0, "sequence"] = "ACD*"
    with pytest.raises(ValueError, match="Invalid amino-acid"):
        cluster_sequences(invalid, output_dir=tmp_path / "invalid")
