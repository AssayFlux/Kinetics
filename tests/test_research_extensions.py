import numpy as np
import pandas as pd
import pytest

from kinetics_core.applicability import ApplicabilityDomain
from kinetics_core.context import AssayContextEncoder
from kinetics_core.uncertainty import conformal_interval, conformal_quantile
from kinetics_core.quality import audit_observations


def test_context_encoder_ignores_unselected_identifier_and_handles_unknown_category():
    train = pd.DataFrame({
        "ph": [6.0, 7.0, None],
        "temperature_k": [298.0, 303.0, 310.0],
        "organism": ["A", "B", "A"],
        "source_record_id": ["r1", "r2", "r3"],
    })
    encoder = AssayContextEncoder(
        numeric_columns=("ph", "temperature_k"),
        categorical_columns=("organism",),
    ).fit(train)
    test = pd.DataFrame({
        "ph": [6.5],
        "temperature_k": [300.0],
        "organism": ["unseen"],
        "source_record_id": ["test-id"],
    })
    encoded = encoder.transform(test)
    assert encoded.shape[0] == 1
    assert np.isfinite(encoded).all()
    assert "source_record_id" not in " ".join(encoder.get_feature_names_out())


def test_context_encoder_rejects_missing_configured_column():
    encoder = AssayContextEncoder(
        numeric_columns=("ph",), categorical_columns=()
    )
    with pytest.raises(ValueError, match="missing configured"):
        encoder.fit(pd.DataFrame({"temperature_k": [298.0, 300.0]}))


def test_conformal_quantile_and_original_unit_interval():
    q = conformal_quantile([1.0, 2.0, 3.0], [1.1, 1.8, 3.2], alpha=0.1)
    assert q == pytest.approx(0.2)
    result = conformal_interval(np.asarray([2.0]), q, target="km")
    assert result["canonical_unit"] == "M"
    assert result["lower"][0] == pytest.approx(10**1.8)
    assert result["upper"][0] == pytest.approx(10**2.2)


def test_applicability_domain_flags_far_query():
    reference = np.asarray([[0.0, 0.0], [0.1, 0.0], [0.0, 0.1], [0.1, 0.1]])
    monitor = ApplicabilityDomain(quantile=0.75).fit(reference)
    near = monitor.score([[0.05, 0.05]])
    far = monitor.score([[100.0, 100.0]])
    assert bool(near["within_domain"][0])
    assert not bool(far["within_domain"][0])
    assert "not a probability" in near["interpretation"]


def test_quality_audit_flags_conflicting_duplicate_without_dropping_rows():
    frame = pd.DataFrame({
        "target": ["km", "km", "kcat"],
        "source": ["db", "db", "db"],
        "source_record_id": ["r1", "r1", "r1"],
        "canonical_value": [1e-3, 2e-3, 2.0],
        "canonical_unit": ["M", "M", "s^-1"],
        "sequence": ["AAAA", "AAAA", None],
    })
    annotated, audit, report = audit_observations(frame)
    assert len(annotated) == 3
    assert len(audit) == 1
    assert audit.iloc[0]["status"] == "conflicting_duplicate"
    assert report["n_conflicting_groups"] == 1
    assert annotated.loc[0, "duplicate_status"] == "conflicting_duplicate"
    assert annotated.loc[2, "duplicate_status"] == "unique"



def test_raw_context_archive_alignment_and_design_matrix(tmp_path):
    from kinetics_core.context import attach_context_archive, context_design_matrix
    from kinetics_core.modeling import _load_feature_file

    archive = tmp_path / "features.npz"
    context_csv = tmp_path / "context.csv"
    output = tmp_path / "features_context.npz"
    np.savez_compressed(
        archive,
        X=np.asarray([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], dtype=np.float32),
        y_log10=np.asarray([-3.0, -2.0, -1.0], dtype=np.float32),
        source_record_ids=np.asarray(["a", "b", "c"]),
        target=np.asarray(["km"]),
    )
    pd.DataFrame({
        "source_record_id": ["a", "b", "c"],
        "ph": [6.0, None, 8.0],
        "organism": ["x", "y", "x"],
    }).to_csv(context_csv, index=False)
    attach_context_archive(
        str(archive), str(context_csv), str(output),
        numeric_columns=("ph",), categorical_columns=("organism",),
    )
    payload = _load_feature_file(output)
    design = context_design_matrix(payload)
    assert list(design.columns) == ["base_0", "base_1", "ph", "organism"]
    assert design.shape == (3, 4)
    assert np.isnan(design.loc[1, "ph"])


def test_context_pipeline_fits_unknown_categories_safely():
    from sklearn.linear_model import Ridge
    from kinetics_core.context import make_context_pipeline

    train = pd.DataFrame({
        "base_0": [0.0, 1.0, 2.0, 3.0],
        "ph": [6.0, 7.0, None, 8.0],
        "organism": ["a", "b", "a", "b"],
    })
    pipeline = make_context_pipeline(
        Ridge(), numeric_columns=("ph",), categorical_columns=("organism",),
        base_dimension=1,
    )
    pipeline.fit(train, np.asarray([0.0, 1.0, 2.0, 3.0]))
    predicted = pipeline.predict(pd.DataFrame({
        "base_0": [4.0], "ph": [7.5], "organism": ["unseen"]
    }))
    assert predicted.shape == (1,)
    assert np.isfinite(predicted).all()



def test_subgroup_diagnostics_keep_small_groups_visible_and_report_coverage():
    from kinetics_core.metrics import subgroup_regression_report

    result = subgroup_regression_report(
        [1.0, 1.1, 2.0, 2.1, 2.2, 3.0],
        [1.0, 1.0, 2.0, 2.0, 2.0, 3.0],
        ["a", "a", "b", "b", "b", "small"],
        target="km",
        min_group_size=2,
        conformal_quantile_log10=0.2,
    )
    assert result["n_groups"] == 3
    assert result["groups"][0]["status"] == "reported"
    assert result["groups"][2]["status"] == "insufficient_group_size"
    assert result["groups"][0]["empirical_interval_coverage"] == 1.0
