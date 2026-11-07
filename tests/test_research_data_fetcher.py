from scripts.fetch_research_data import ALLOWED_EXTENSIONS, license_allowed


def test_zenodo_accepts_explicit_redistribution_licenses():
    assert license_allowed("cc0-1.0")
    assert license_allowed("cc-by-4.0")
    assert license_allowed("cc-by-sa-4.0")
    assert license_allowed("https://creativecommons.org/licenses/by/4.0/")


def test_zenodo_rejects_restricted_or_unknown_licenses():
    assert not license_allowed("cc-by-nc-4.0")
    assert not license_allowed("cc-by-nd-4.0")
    assert not license_allowed("all-rights-reserved")
    assert not license_allowed("")


def test_zenodo_supports_books_tabular_and_biological_formats():
    assert {".pdf", ".epub", ".csv", ".tsv", ".json", ".fasta", ".gb", ".pdb", ".cif"} <= ALLOWED_EXTENSIONS
