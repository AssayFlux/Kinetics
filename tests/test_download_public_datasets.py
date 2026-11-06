from __future__ import annotations

import urllib.error
from pathlib import Path

import pytest

from scripts.download_public_datasets import download, request_headers


def test_hugging_face_token_is_scoped_to_catpred_dataset_host() -> None:
    headers = request_headers(
        "https://huggingface.co/datasets/RosettaCommons/CatPred-DB/resolve/abc/km.csv",
        "read-secret",
    )
    assert headers["Authorization"] == "Bearer read-secret"
    github_headers = request_headers(
        "https://raw.githubusercontent.com/maranasgroup/CatPred-DB/abc/file.csv",
        "read-secret",
    )
    assert "Authorization" not in github_headers


def test_missing_token_does_not_add_authorization_header() -> None:
    headers = request_headers(
        "https://huggingface.co/datasets/RosettaCommons/CatPred-DB/resolve/abc/km.csv"
    )
    assert "Authorization" not in headers


def test_gated_dataset_error_is_actionable_and_removes_partial_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def denied(*args, **kwargs):
        raise urllib.error.HTTPError(
            "https://huggingface.co/datasets/RosettaCommons/CatPred-DB/file",
            403,
            "Forbidden",
            hdrs=None,
            fp=None,
        )

    monkeypatch.setattr("urllib.request.urlopen", denied)
    destination = tmp_path / "km.csv"
    with pytest.raises(RuntimeError, match="review and accept its access conditions"):
        download(
            "https://huggingface.co/datasets/RosettaCommons/CatPred-DB/resolve/abc/km.csv",
            destination,
        )
    assert not destination.exists()
    assert not destination.with_suffix(".csv.part").exists()
