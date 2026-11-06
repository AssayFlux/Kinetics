"""Deterministic research tools exposed through the Kinetics integration boundary.

Kinetics Ecosystem is a separate project. This module defines provider-neutral
operations and schemas; it does not host an LLM or depend on an assistant runtime.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from rdkit import Chem

STANDARD_AA = set("ACDEFGHIKLMNPQRSTVWY")


def validate_kinetics_input(sequence: str, smiles: str) -> dict[str, Any]:
    """Validate a protein sequence and substrate SMILES without running a model."""
    normalized_sequence = "".join(sequence.split()).upper() if isinstance(sequence, str) else ""
    if not normalized_sequence:
        raise ValueError("Protein sequence is required.")
    invalid = sorted(set(normalized_sequence) - STANDARD_AA)
    if invalid:
        raise ValueError(
            "Sequence contains unsupported amino-acid symbols: " + ", ".join(invalid)
        )
    if not isinstance(smiles, str) or not smiles.strip():
        raise ValueError("Substrate SMILES is required.")
    molecule = Chem.MolFromSmiles(smiles.strip())
    if molecule is None:
        raise ValueError("Substrate SMILES is invalid.")
    return {
        "sequence": normalized_sequence,
        "smiles": Chem.MolToSmiles(molecule, canonical=True),
        "sequence_length": len(normalized_sequence),
    }


def kinetics_predict(
    sequence: str,
    smiles: str,
    model_dir: str | Path = "models",
    cache_dir: str | Path = "data/cache",
) -> dict[str, Any]:
    """Run the existing Kinetics model and return a structured assistant tool result.

    Raises FileNotFoundError when no trained model bundle is installed. Callers
    should surface that state clearly; they must not fabricate substitute values.
    """
    validated = validate_kinetics_input(sequence, smiles)
    bundle = Path(model_dir) / "kinetics_model.joblib"
    if not bundle.is_file():
        return {
            "status": "model_unavailable",
            "message": (
                "No trained Kinetics model bundle is installed. Train and evaluate "
                "the model before requesting a numerical prediction."
            ),
            "input": validated,
            "limitations": [
                "No numerical prediction was generated.",
                "A valid input does not imply that a trained model is available.",
            ],
        }

    from .predict import predict

    values = predict(
        validated["sequence"],
        validated["smiles"],
        model_dir=model_dir,
        cache_dir=cache_dir,
    )
    return {
        "status": "predicted",
        "input": validated,
        "prediction": values,
        "units": {"km": "mM", "kcat": "s^-1"},
        "interpretation": (
            "These are computational estimates, not experimental measurements. "
            "Reliability depends on training-data coverage and assay context."
        ),
        "limitations": [
            "The baseline does not condition predictions on pH, temperature, organism, or construct.",
            "The current baseline has not been scientifically validated for deployment.",
            "Out-of-distribution inputs may produce unreliable estimates.",
        ],
    }


def assistant_system_guidance() -> str:
    """Return domain-specific behavior guidance for a Kinetics research assistant."""
    return (
        "You are the scientific assistant for Kinetics, an enzyme-kinetics research "
        "software project. Explain Km, kcat, enzyme-substrate data, units, workflows, "
        "and scientific limitations clearly. Never invent a numerical prediction: "
        "call the kinetics_predict tool and use only its returned values. Km values "
        "are reported in mM and kcat values in s^-1 by this baseline. Distinguish "
        "computational estimates from experimental measurements. State when the "
        "model is unavailable, when assay context is missing, or when evidence is "
        "insufficient. Do not claim clinical, industrial, or experimental validation."
    )


def tool_schemas() -> list[dict[str, Any]]:
    """Provider-neutral function schema for the separate Kinetics Ecosystem API."""
    return [
        {
            "name": "kinetics_predict",
            "description": (
                "Predict Km and kcat for a protein sequence and substrate SMILES "
                "using an installed Kinetics model. Returns explicit model status "
                "and scientific limitations."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "sequence": {"type": "string", "description": "Protein sequence"},
                    "smiles": {"type": "string", "description": "Substrate SMILES"},
                },
                "required": ["sequence", "smiles"],
                "additionalProperties": False,
            },
        }
    ]
