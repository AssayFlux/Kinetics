import hashlib
import json

import numpy as np
import pytest

from kinetics_core.multimodal import (
    _graph_summary,
    fit_multimodal_model,
    predict_multimodal_model,
)


def _archive(path, *, start, count, target="km"):
    rows = np.arange(start, start + count)
    protein = np.stack([
        np.linspace(0.0, 1.0, 4) + index * 0.03 for index in rows
    ]).astype(np.float32)
    morgan = np.asarray(
        [[index % 2, (index // 2) % 2] for index in rows],
        dtype=np.float32,
    )
    x = np.concatenate((protein, morgan), axis=1)
    atom_rows = np.tile(
        np.asarray([[6, 3, 0, 1, 0, 0, 3, 0, 12.0],
                    [8, 1, 0, 0, 0, 0, 3, 0, 16.0]], dtype=np.float32),
        (count, 1),
    )
    bond_rows = np.tile(
        np.asarray([[1, 0, 0, 0], [1, 0, 0, 0]], dtype=np.float32),
        (count, 1),
    )
    arrays = {
        "X": x,
        "y_log10": np.linspace(-4.0, -2.0, count, dtype=np.float32),
        "target": np.asarray([target]),
        "source_record_ids": np.asarray([f"record-{index}" for index in rows]),
        "feature_schema_version": np.asarray(["2.0"]),
        "feature_metadata_json": np.asarray(['{"fixture":"v1"}']),
        "feature_model": np.asarray(["ESM-2"]),
        "fingerprint_radius": np.asarray([2]),
        "fingerprint_bits": np.asarray([2]),
        "graph_atom_features": atom_rows,
        "graph_bond_features": bond_rows,
        "graph_atom_offsets": np.arange(0, 2 * count + 1, 2, dtype=np.int64),
        "graph_edge_offsets": np.arange(0, 2 * count + 1, 2, dtype=np.int64),
        "protein_cluster_id": np.asarray([f"protein-{index}" for index in rows]),
        "scaffold_id": np.asarray([f"scaffold-{index}" for index in rows]),
        "context_numeric_columns": np.asarray(["ph"]),
        "context_categorical_columns": np.asarray(["organism"]),
        "context_raw__ph": np.linspace(6.0, 8.0, count),
        "context_raw__organism": np.asarray(
            ["organism-a" if index % 2 else "organism-b" for index in rows]
        ),
    }
    np.savez_compressed(path, **arrays)
    raw = path.read_bytes()
    manifest = {
        "target": target,
        "rows": count,
        "archive": {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw),
        },
        "sources": ["synthetic-fixture"],
        "source_versions": ["fixture-v1"],
        "license_ids": ["CC0-1.0"],
    }
    path.with_suffix(path.suffix + ".manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    return path


def test_graph_summary_is_row_aligned_and_fixed_width(tmp_path):
    archive = _archive(tmp_path / "features.npz", start=0, count=3)
    with np.load(archive, allow_pickle=False) as loaded:
        summary = _graph_summary({key: loaded[key] for key in loaded.files})
    assert summary.shape == (3, 24)
    assert np.isfinite(summary).all()
    assert summary[0, -2] == 2
    assert summary[0, -1] == 1


def test_graph_summary_rejects_corrupt_offsets():
    payload = {
        "X": np.zeros((2, 3), dtype=np.float32),
        "graph_atom_features": np.ones((4, 9), dtype=np.float32),
        "graph_bond_features": np.ones((4, 4), dtype=np.float32),
        "graph_atom_offsets": np.asarray([0, 2, 4]),
        "graph_edge_offsets": np.asarray([0, 3, 4]),
    }
    with pytest.raises(ValueError, match="offsets"):
        _graph_summary(payload)


def test_multimodal_train_and_inference_round_trip(tmp_path):
    train = _archive(tmp_path / "train.npz", start=0, count=8)
    test = _archive(tmp_path / "test.npz", start=8, count=4)
    result = fit_multimodal_model(
        train, test, target="km", output_dir=tmp_path / "model",
        group_array="protein_cluster_id",
        holdout_group_arrays=("protein_cluster_id", "scaffold_id"),
        n_splits=2, hidden_layer_sizes=(8,), max_iter=8, random_state=7,
        git_revision="a" * 40,
    )
    assert result["model_family"] == "Kinetics-Multi feature-fusion MLP"
    assert result["cross_validation"]["strategy"] == "group_k_fold:protein_cluster_id"
    assert result["n_held_out"] == 4
    assert "applicability_domain" in result
    assert "raw assay context with fold-local preprocessing" in result["input_modalities"]
    model = tmp_path / "model" / "km_kinetics_multi.joblib"
    output = tmp_path / "inference.csv"
    predicted = predict_multimodal_model(model, test, output)
    assert predicted["n_predictions"] == 4
    assert output.is_file()
    predictions = __import__("pandas").read_csv(output)
    assert "within_applicability_domain" in predictions.columns
    metrics = json.loads(
        (tmp_path / "model" / "km_kinetics_multi_metrics.json").read_text()
    )
    assert metrics["target"] == "km"
    assert metrics["graph_summary_dimension"] == 24
    assert (tmp_path / "model" / "km_kinetics_multi_experiment_manifest.json").is_file()


def test_multimodal_rejects_target_mismatch(tmp_path):
    train = _archive(tmp_path / "train.npz", start=0, count=8)
    test = _archive(tmp_path / "test.npz", start=8, count=3, target="kcat")
    with pytest.raises(ValueError, match="target"):
        fit_multimodal_model(
            train, test, target="km", output_dir=tmp_path / "model",
            group_array="protein_cluster_id", n_splits=2,
            hidden_layer_sizes=(8,), max_iter=2, git_revision="a" * 40,
        )


def test_multimodal_cli_commands_are_exposed():
    from kinetics_core.cli import build_parser

    parser = build_parser()
    fit_args = parser.parse_args([
        "fit-multi", "--train", "train.npz", "--test", "test.npz",
        "--target", "km", "--output-dir", "out", "--hidden-layers", "64,32",
        "--git-revision", "a" * 40,
    ])
    assert fit_args.command == "fit-multi"
    assert fit_args.hidden_layers == "64,32"
    predict_args = parser.parse_args([
        "predict-multi", "--model", "model.joblib",
        "--features", "features.npz", "--output", "predictions.csv",
    ])
    assert predict_args.command == "predict-multi"


def test_multimodal_rejects_feature_manifest_checksum_mismatch(tmp_path):
    train = _archive(tmp_path / "train.npz", start=0, count=8)
    test = _archive(tmp_path / "test.npz", start=8, count=4)
    manifest_path = test.with_suffix(test.suffix + ".manifest.json")
    manifest = json.loads(manifest_path.read_text())
    manifest["archive"]["sha256"] = "0" * 64
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="checksum/size"):
        fit_multimodal_model(
            train, test, target="km", output_dir=tmp_path / "model",
            group_array="protein_cluster_id",
            holdout_group_arrays=("protein_cluster_id", "scaffold_id"),
            n_splits=2, hidden_layer_sizes=(8,), max_iter=2,
            git_revision="a" * 40,
        )


def test_multimodal_uses_independent_calibration_archive(tmp_path):
    train = _archive(tmp_path / "train.npz", start=0, count=8)
    test = _archive(tmp_path / "test.npz", start=8, count=4)
    calibration = _archive(tmp_path / "calibration.npz", start=12, count=4)
    result = fit_multimodal_model(
        train, test, target="km", output_dir=tmp_path / "model",
        calibration_archive=calibration,
        group_array="protein_cluster_id",
        holdout_group_arrays=("protein_cluster_id", "scaffold_id"),
        n_splits=2, hidden_layer_sizes=(8,), max_iter=4,
        git_revision="a" * 40,
    )
    assert result["calibration"]["method"] == "split_conformal_absolute_residual"
    assert result["calibration"]["n_calibration"] == 4


def test_multimodal_rejects_calibration_test_group_overlap(tmp_path):
    train = _archive(tmp_path / "train.npz", start=0, count=8)
    test = _archive(tmp_path / "test.npz", start=8, count=4)
    calibration = _archive(tmp_path / "calibration.npz", start=10, count=4)
    with pytest.raises(ValueError, match="calibration and held-out test"):
        fit_multimodal_model(
            train, test, target="km", output_dir=tmp_path / "model",
            calibration_archive=calibration,
            group_array="protein_cluster_id",
            holdout_group_arrays=("protein_cluster_id", "scaffold_id"),
            n_splits=2, hidden_layer_sizes=(8,), max_iter=2,
            git_revision="a" * 40,
        )
