from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_domain_catalogue_has_at_least_100_domains():
    fetch = load_script("fetch_corpus")
    domains = fetch.domain_catalogue()
    assert len(domains) >= 100
    assert len(domains) == len(set(domains))


def test_license_gate_is_conservative():
    fetch = load_script("fetch_corpus")
    assert fetch.license_allowed("https://creativecommons.org/licenses/by/4.0/")
    assert fetch.license_allowed("CC BY-SA 4.0")
    assert fetch.license_allowed("Public Domain")
    assert not fetch.license_allowed("")
    assert not fetch.license_allowed("CC BY-NC 4.0")
    assert not fetch.license_allowed("CC BY-ND 4.0")
    assert not fetch.license_allowed("All Rights Reserved")


def test_manifest_atomic_shape(tmp_path: Path):
    fetch = load_script("fetch_corpus")
    path = tmp_path / "manifest.json"
    manifest = fetch.load_manifest(path)
    manifest["items"]["example"] = {"status": "downloaded", "sha256": "abc"}
    fetch.save_manifest(path, manifest)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["items"]["example"]["sha256"] == "abc"
    assert not path.with_suffix(".json.tmp").exists()


def test_tokenizer_chunks_overlap_and_boundaries():
    tokenizer = load_script("tokenize_corpus")
    text = " ".join(f"token{i}" for i in range(100))
    pieces = list(tokenizer.chunks(text, max_tokens=20, overlap=5))
    assert len(pieces) > 1
    assert all(count <= 20 for _, _, count in pieces)
    assert pieces[0][0] == 0
    assert pieces[-1][1]


def test_safe_category_routing():
    fetch = load_script("fetch_corpus")
    assert fetch.safe_category("Biomedical engineering") == "engineering"
    assert fetch.safe_category("Cardiology") == "medicine"
    assert fetch.safe_category("Genomics") == "biomedical"
