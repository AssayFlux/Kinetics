from __future__ import annotations

import urllib.error
from pathlib import Path

import pytest

from scripts.download_public_datasets import (
    _SafeRedirectHandler,
    download,
    is_catpred_hf_url,
    request_headers,
)


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



def test_credentials_reject_lookalike_hosts_and_userinfo() -> None:
    assert not is_catpred_hf_url(
        "https://huggingface.co.evil.example/datasets/RosettaCommons/CatPred-DB/file"
    )
    assert not is_catpred_hf_url(
        "https://huggingface.co@evil.example/datasets/RosettaCommons/CatPred-DB/file"
    )
    assert not is_catpred_hf_url(
        "http://huggingface.co/datasets/RosettaCommons/CatPred-DB/file"
    )


def test_cross_origin_redirect_strips_bearer_token() -> None:
    from urllib.request import Request

    request = Request(
        "https://huggingface.co/datasets/RosettaCommons/CatPred-DB/resolve/abc/km.csv",
        headers={"Authorization": "Bearer read-secret"},
    )
    redirected = _SafeRedirectHandler().redirect_request(
        request, None, 302, "Found", {}, "https://cdn.example/file"
    )
    assert redirected is not None
    assert not redirected.has_header("Authorization")


def test_same_origin_redirect_keeps_bearer_token() -> None:
    from urllib.request import Request

    request = Request(
        "https://huggingface.co/datasets/RosettaCommons/CatPred-DB/resolve/abc/km.csv",
        headers={"Authorization": "Bearer read-secret"},
    )
    redirected = _SafeRedirectHandler().redirect_request(
        request,
        None,
        302,
        "Found",
        {},
        "https://huggingface.co/datasets/RosettaCommons/CatPred-DB/resolve/abc/km.csv?download=true",
    )
    assert redirected is not None
    assert redirected.get_header("Authorization") == "Bearer read-secret"

def test_missing_token_does_not_add_authorization_header() -> None:
    headers = request_headers(
        "https://huggingface.co/datasets/RosettaCommons/CatPred-DB/resolve/abc/km.csv"
    )
    assert "Authorization" not in headers


def test_gated_dataset_error_is_actionable_and_removes_partial_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    class DeniedOpener:
        def open(self, *args, **kwargs):
            raise urllib.error.HTTPError(
                "https://huggingface.co/datasets/RosettaCommons/CatPred-DB/file",
                403,
                "Forbidden",
                hdrs=None,
                fp=None,
            )

    monkeypatch.setattr(
        "urllib.request.build_opener", lambda *handlers: DeniedOpener()
    )
    destination = tmp_path / "km.csv"
    with pytest.raises(RuntimeError, match="review and accept its access conditions"):
        download(
            "https://huggingface.co/datasets/RosettaCommons/CatPred-DB/resolve/abc/km.csv",
            destination,
        )
    assert not destination.exists()
    assert not destination.with_suffix(".csv.part").exists()
