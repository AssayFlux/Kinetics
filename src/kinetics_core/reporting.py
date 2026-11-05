"""Markdown report generation for completed computational experiments."""
from __future__ import annotations

from pathlib import Path
from typing import Any


def render_experiment_report(
    *,
    experiment_manifest: dict[str, Any],
    metrics: dict[str, Any],
    limitations: list[str],
    citations: list[str] | None = None,
) -> str:
    """Render a concise, provenance-aware report without inventing missing evidence."""
    target = metrics.get("target", "not specified")
    held_out = metrics.get("held_out", {})
    log_metrics = held_out.get("log10", {})
    raw_metrics = held_out.get("original_scale", {})
    cv = metrics.get("cross_validation", {})
    environment = experiment_manifest.get("environment", {})
    packages = experiment_manifest.get("package_versions", {})

    def value(mapping: dict, key: str) -> str:
        result = mapping.get(key)
        return "not reported" if result is None else str(result)

    package_lines = "\n".join(
        f"- {name}: {version if version is not None else 'not installed'}"
        for name, version in sorted(packages.items())
    ) or "- Not recorded"
    citation_lines = "\n".join(f"- {item}" for item in (citations or [])) or "- Not supplied"
    limitation_lines = "\n".join(f"- {item}" for item in limitations) or "- Not documented"

    return f"""# Kinetics experiment report

## Research target

- Target: {target}
- Experiment ID: {experiment_manifest.get('experiment_id', 'not recorded')}
- Research question: {experiment_manifest.get('research_question', 'not recorded')}
- Created: {experiment_manifest.get('created_at', 'not recorded')}

## Data and provenance

Input artifacts and checksums are recorded in the experiment manifest. Consult that manifest for source identifiers, retrieval dates, and file hashes. This report does not infer dataset license or publication details.

## Evaluation design

- Cross-validation strategy: {value(cv, 'strategy')}
- Number of folds: {value(cv, 'folds')}
- CV RMSE mean (log10): {value(cv, 'rmse_mean_log10')}
- CV RMSE standard deviation (log10): {value(cv, 'rmse_std_log10')}
- Held-out observations: {value(metrics, 'n_held_out')}

## Held-out performance

### Log10 scale
- MAE: {value(log_metrics, 'mae')}
- RMSE: {value(log_metrics, 'rmse')}
- R-squared: {value(log_metrics, 'r2')}

### Original measurement scale
- Canonical unit: {value(held_out, 'canonical_unit')}
- MAE: {value(raw_metrics, 'mae')}
- RMSE: {value(raw_metrics, 'rmse')}
- Median absolute relative error: {value(raw_metrics, 'median_absolute_relative_error')}
- Median fold error: {value(raw_metrics, 'median_fold_error')}

## Runtime environment

- Python: {environment.get('python', 'not recorded')}
- Platform: {environment.get('platform', 'not recorded')}

{package_lines}

## Limitations

{limitation_lines}

## Dataset and method citations

{citation_lines}

## Interpretation

Predictions are computational estimates, not experimental measurements. A completed run and its metrics do not establish external validity, causal mechanism, or suitability for a particular application. Interpret results in light of the split design, assay metadata, uncertainty, and documented applicability limits.
"""


def write_experiment_report(
    *,
    experiment_manifest: dict[str, Any],
    metrics: dict[str, Any],
    limitations: list[str],
    destination: str | Path,
    citations: list[str] | None = None,
) -> Path:
    output = Path(destination)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_experiment_report(
            experiment_manifest=experiment_manifest,
            metrics=metrics,
            limitations=limitations,
            citations=citations,
        ),
        encoding="utf-8",
    )
    return output
