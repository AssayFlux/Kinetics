import pandas as pd

from src.data_preprocessing import clean_dataframe


def test_clean_dataframe_validates_and_logs_targets():
    frame = pd.DataFrame({
        "sequence": ["ACDEFG", "ACDZX", "MKWVTF"],
        "smiles": ["CCO", "CCO", "not-a-smiles"],
        "km": [10.0, 1.0, 2.0],
        "kcat": [100.0, 2.0, 3.0],
    })
    cleaned, stats = clean_dataframe(frame)
    assert len(cleaned) == 1
    assert cleaned.loc[0, "log10_km"] == 1.0
    assert cleaned.loc[0, "log10_kcat"] == 2.0
    assert stats["invalid_sequences"] == 1
    assert stats["invalid_smiles"] == 1


def test_unit_conversion_to_standard_units():
    frame = pd.DataFrame({
        "sequence": ["ACDEFG"],
        "smiles": ["CCO"],
        "km": [1000.0],
        "kcat": [60.0],
    })
    cleaned, _ = clean_dataframe(frame, km_unit="uM", kcat_unit="min^-1")
    assert cleaned.loc[0, "km"] == 1.0
    assert cleaned.loc[0, "kcat"] == 1.0
