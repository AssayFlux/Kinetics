import pytest

from src.assistant_tools import (
    assistant_system_guidance,
    kinetics_predict,
    tool_schemas,
    validate_kinetics_input,
)


def test_validate_normalizes_sequence_and_smiles():
    result = validate_kinetics_input(" met ", "CCO")
    assert result["sequence"] == "MET"
    assert result["smiles"] == "CCO"
    assert result["sequence_length"] == 3


@pytest.mark.parametrize("sequence", ["", "M X", "MOU"])
def test_rejects_invalid_sequences(sequence):
    with pytest.raises(ValueError):
        validate_kinetics_input(sequence, "CCO")


def test_rejects_invalid_smiles():
    with pytest.raises(ValueError):
        validate_kinetics_input("M", "not-a-smiles")


def test_missing_model_is_reported_without_fake_prediction(tmp_path):
    result = kinetics_predict("M", "CCO", model_dir=tmp_path)
    assert result["status"] == "model_unavailable"
    assert "prediction" not in result


def test_tool_contract_and_guidance_are_present():
    assert tool_schemas()[0]["name"] == "kinetics_predict"
    guidance = assistant_system_guidance().lower()
    assert "never invent" in guidance
    assert "experimental measurements" in guidance
