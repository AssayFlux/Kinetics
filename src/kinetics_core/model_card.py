"""Generate transparent model-card documentation from saved run metadata."""
from __future__ import annotations

from pathlib import Path
from typing import Any


def render_model_card(metadata: dict[str, Any]) -> str:
    """Render a Markdown model card; missing evidence is labelled as unavailable."""
    target = metadata.get("target", "not specified")
    if target not in ("km", "kcat"):
        raise ValueError("model-card target must be 'km' or 'kcat'")
    unit = "M" if target == "km" else "s^-1"
    dataset = metadata.get("dataset", {})
    evaluation = metadata.get("evaluation", {})
    limitations = metadata.get("limitations", [])
    intended_use = metadata.get("intended_use", [])
    out_of_scope = metadata.get("out_of_scope_use", [])

    def bullets(items: list[Any]) -> str:
        return "\n".join(f"- {item}" for item in items) if items else "- Not documented"

    return f"""# Model card: {metadata.get('model_name', 'Kinetics model')}

## Summary

- Target: {target}
- Canonical unit: {unit}
- Model version: {metadata.get('model_version', 'not recorded')}
- Software version: {metadata.get('software_version', 'not recorded')}
- Created: {metadata.get('created_at', 'not recorded')}

## Intended use

{bullets(intended_use)}

## Out-of-scope use

{bullets(out_of_scope)}

## Training data

- Dataset: {dataset.get('name', 'not documented')}
- Version: {dataset.get('version', 'not documented')}
- Source: {dataset.get('source_url', 'not documented')}
- License: {dataset.get('license', 'not documented')}
- Number of observations: {dataset.get('n_observations', 'not documented')}
- Curation manifest: {dataset.get('manifest', 'not documented')}

## Evaluation

- Split strategy: {evaluation.get('split_strategy', 'not documented')}
- Test observations: {evaluation.get('n_test', 'not documented')}
- Metrics: {evaluation.get('metrics', 'not documented')}
- Uncertainty method: {evaluation.get('uncertainty_method', 'not documented')}

## Limitations

{bullets(limitations)}

## Reproducibility

- Experiment manifest: {metadata.get('experiment_manifest', 'not documented')}
- Feature encoder: {metadata.get('feature_encoder', 'not documented')}
- Model artifact checksum: {metadata.get('model_sha256', 'not documented')}
- Random seed: {metadata.get('random_seed', 'not documented')}

## Scientific interpretation

Predictions are computational estimates, not experimental measurements. Performance depends on data coverage, assay context, protein/substrate distribution, and evaluation design. A model card is not evidence of external validity; consult the saved experiment report and publication protocol.
"""


def write_model_card(metadata: dict[str, Any], destination: str | Path) -> Path:
    output = Path(destination)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_model_card(metadata), encoding="utf-8")
    return output
