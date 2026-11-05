# Scientific architecture: enzyme kinetic prediction

## Research objective

Kinetics focuses on computational estimation of enzyme kinetic parameters from protein and substrate information, initially targeting Michaelis constant (Km) and turnover number (kcat). The platform must preserve the distinction between measured kinetic observations and model predictions.

## Scientific data model

Km and kcat are different measured quantities and may be published in separate tables, under different assay conditions, and with different sample identifiers. They must be represented as independent observations. They may only be linked when the source explicitly identifies a shared enzyme construct, substrate/reaction, and compatible experimental context.

Canonical units are molar (M) for Km and reciprocal seconds (s^-1) for kcat. Raw values and units must remain available in source records. Conversions are allowed only from explicit, unambiguous source units.

Retain, where available:
- protein sequence and stable accession;
- substrate structure and stable chemical identifier;
- organism, strain, enzyme construct, mutations;
- assay pH, temperature, cofactors, buffer, and experimental method;
- source database record ID and primary publication DOI;
- source version, retrieval date, license, and content checksum.

Missing context must remain missing; it must not be imputed as a known assay condition.

## Prediction architecture

The baseline combines protein sequence representations and chemical structure fingerprints. This is a useful starting point, not a presumed optimal architecture. The software should support modular encoders, feature ablations, context-aware models, and alternative regression methods without changing the canonical observation schema.

## Evaluation design

Random row splits are retained only as a diagnostic baseline. Scientific generalization requires stronger evaluation:
1. protein sequence-cluster holdout;
2. chemical scaffold holdout;
3. double-cold holdout where both protein group and substrate scaffold are unseen;
4. temporal or external-source evaluation when data permit.

All split assignments must be saved. Duplicate measurements, homologous sequences, repeated compounds, and near-identical records must be audited before model evaluation. Hyperparameter selection must not use the final external test set.

## Statistical reporting

Report metrics separately for Km and kcat. Include log-scale metrics and interpretable original-unit errors. Report sample counts, target distributions, uncertainty, calibration, subgroup performance, and failure cases. Avoid presenting a single aggregate score across the two targets.

## Interpretation and limitations

Predicted Km and kcat are estimates conditional on the training data and feature representation. They are not experimental measurements. Assay context, enzyme construct, substrate identity, temperature, pH, and organism can materially affect observed values. Applicability-domain warnings and uncertainty are required before scientific interpretation.

## Publication direction

A credible software/methods paper should establish:
- a transparent and versioned public-data curation pipeline;
- leakage-resistant benchmark protocols;
- reproducible baselines and ablation studies;
- uncertainty and applicability-domain analysis;
- independent or temporal validation where feasible;
- a documented software API and artifact provenance.

The paper's novelty and scientific conclusions must be determined from completed comparative experiments, not assumed during implementation.
