# Research reporting and figure conventions

> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

The reporting utilities generate Markdown experiment summaries and target-specific diagnostic figures. They do not create publication claims automatically.

## Minimum report content

- Research question and experiment ID.
- Input artifact hashes and source provenance manifest.
- Target-specific split strategy and sample counts.
- Cross-validation and held-out metrics, clearly separated.
- Log10 and original-unit errors.
- Runtime/dependency metadata.
- Dataset/method citations.
- Limitations and interpretation cautions.

## Figure conventions

Generate parity and residual figures independently for Km and kcat. Axes must identify the target and scale. Save high-resolution output and retain the exact prediction table and plotting inputs. Do not combine metrics for different targets into a single score without a scientifically justified definition.

## Reproducibility

Every figure and table must be regenerable from saved row-level predictions, metrics, and experiment manifests. If an input artifact or citation is unavailable, report that limitation rather than reconstructing it from memory.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
