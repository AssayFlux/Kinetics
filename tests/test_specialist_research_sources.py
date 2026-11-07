from scripts.fetch_specialist_sources import ACCEPTED, accepted_license, metadata_map


def test_specialist_sources_accept_explicit_reusable_licenses():
    assert accepted_license("CC0")
    assert accepted_license("CC BY 4.0")
    assert accepted_license("CC-BY-4.0")
    assert accepted_license("CC BY-SA 4.0")
    assert accepted_license("https://creativecommons.org/licenses/by/4.0/")


def test_specialist_sources_reject_restricted_and_unknown_licenses():
    assert not accepted_license("CC BY-NC 4.0")
    assert not accepted_license("CC BY-ND 4.0")
    assert not accepted_license("All rights reserved")
    assert not accepted_license(None)


def test_oapen_metadata_is_normalized():
    values = metadata_map({"metadata": [
        {"key": "dc.title", "value": "Open textbook"},
        {"key": "dc.rights", "value": "CC BY 4.0"},
    ]})
    assert values["dc.title"] == ["Open textbook"]
    assert accepted_license(values["dc.rights"][0])


def test_enabled_specialist_sources_have_implemented_adapter():
    import json
    from pathlib import Path

    registry = json.loads(Path("database/sources/knowledge_sources.json").read_text())
    sources = {x["id"]: x for x in registry["sources"]}
    for source_id in ("openalex", "arxiv", "uniprot", "rcsb_pdb", "oapen", "figshare", "dryad"):
        assert sources[source_id]["enabled"] is True
        assert sources[source_id]["adapter_status"] == "implemented"
