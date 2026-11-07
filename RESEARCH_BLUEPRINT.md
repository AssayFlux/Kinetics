# Kinetics Research Blueprint

> 160-domain acquisition scope register: docs/SCIENCE_DOMAIN_CATALOGUE_100.md. This catalogue defines intended breadth; it is not evidence that every domain is implemented or clinically validated.
> **Project-wide direction:** Follow the authoritative [Kinetics mission](KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

**Project:** AssayFlux/Kinetics  
**Status:** Research plan — hypotheses and proposed experiments, not validated findings  
**Publication ambition:** Peer-reviewed paper + open-source software  
**Data strategy:** Publicly available datasets and databases  
**Compute strategy:** Limited local resources; frozen pretrained embeddings, caching, CPU baselines, and selective cloud GPU use  
**Primary contribution:** Integrated multimodal learning with generalization and reliability evaluation

---

## 1. Executive summary

### Proposed title

**Kinetics: An Integrated, Uncertainty-Aware and Resource-Efficient Framework for Generalizable Enzyme–Substrate Kinetic Prediction**

Short alternative: **Generalizable Enzyme Kinetics Prediction through Multimodal Learning and Calibrated Uncertainty**.

### Scientific question

Can an integrated model combining protein sequence representations, substrate molecular graphs, and experimental assay context predict enzyme kinetic parameters for unseen enzyme–substrate combinations while identifying predictions that are unreliable?

### Central hypothesis

An interaction-aware multimodal model that combines protein language representations, molecular graph representations, and available assay metadata will improve predictive performance and/or reliability over simpler feature-concatenation baselines, particularly under protein-family and chemical-scaffold distribution shift.

This is a hypothesis to test, not a result to claim in advance.

### Intended outputs

1. A versioned, provenance-preserving public-data benchmark (Kinetics-KDB).
2. A reproducible benchmark suite with leakage-resistant evaluation.
3. A resource-conscious multimodal model for log10(Km) and log10(kcat).
4. Calibrated uncertainty and out-of-distribution (OOD) assessment.
5. A deployable inference path with documented mobile constraints.
6. A peer-reviewed manuscript and open-source release.

### Scope discipline

The first paper should focus on Km and kcat. Treat Ki, kcat/Km as an independently derived endpoint, and structure-aware modeling as extensions unless sufficient clean data and compute are available. Do not promise wet-lab validation unless a collaborating laboratory is secured.

---

## 2. Literature positioning and gap analysis

The field already contains models that combine protein and substrate information. Therefore, Kinetics should not claim novelty simply for using ESM embeddings, molecular fingerprints, graph neural networks, attention, multitask prediction, or uncertainty estimation individually.

### Relevant prior work to review and reproduce

| Work/resource | Relevance to Kinetics | How to use it |
|---|---|---|
| UniKP (Nature Communications, 2023) | Unified kinetic parameter prediction using enzyme and substrate representations | Reproducibility baseline; inspect data curation and split protocol |
| CatPred (Nature Communications, 2025) | Catalytic parameter prediction using protein/structure and substrate information; includes uncertainty-related modeling | Strong comparator; carefully align target definitions and evaluation |
| CataPro (Nature Communications, 2025) | Kinetic prediction and enzyme engineering/generalization applications | Compare generalization claims and test design |
| KinForm (npj Systems Biology and Applications, 2026) | Kinetics-informed representations | Review for overlap with proposed representation and objectives |
| DLKcat | Established kcat prediction dataset/model | Baseline and data-source audit |
| ESM-2 | Pretrained protein language representations | Frozen, cached protein feature extraction |
| Molecular GNN literature | Chemical graph representations | Substrate encoder baseline and proposed modality |

Starting references (verify versions, publication details, data licenses, and released code before citing in a manuscript):

- UniKP: https://www.nature.com/articles/s41467-023-44113-1
- CatPred: https://pmc.ncbi.nlm.nih.gov/articles/PMC11871309/
- CataPro: https://pmc.ncbi.nlm.nih.gov/articles/PMC11923063/
- KinForm: https://pmc.ncbi.nlm.nih.gov/articles/PMC13194986/
- DLKcat: https://academic.oup.com/bioinformatics/article/36/15/4223/5857583
- ESM repository: https://github.com/facebookresearch/esm

### Defensible research gap to investigate

**A need for carefully standardized, leakage-resistant evaluation of integrated enzyme–substrate kinetic prediction under simultaneous protein and chemical distribution shifts, with explicit assessment of uncertainty, assay context, and computational cost.**

This is a proposed gap, not a proven absence in the literature. The literature review must test it systematically, including newer work and preprints.

### Research questions

- **RQ1 — Interaction:** Does protein–substrate interaction learning outperform simple concatenation or fingerprint-based fusion?
- **RQ2 — Context:** Does assay metadata improve prediction when conditions are available, and how does missing metadata affect results?
- **RQ3 — Generalization:** How well do models perform on unseen protein clusters, unseen chemical scaffolds, and both simultaneously?
- **RQ4 — Reliability:** Do uncertainty estimates identify high-error and OOD predictions, and are prediction intervals calibrated?
- **RQ5 — Efficiency:** What predictive and reliability performance is retained after model compression and mobile deployment?

### Novelty decision gate

Before implementation of the full architecture, create a literature matrix with columns for: targets, dataset size and provenance, sequence representation, substrate representation, interaction mechanism, assay metadata, split design, external validation, uncertainty method, calibration, inference cost, code/data availability.

If a recent paper already addresses the proposed combined gap, narrow the contribution to the demonstrable missing element—for example, rigorous double-cold-start evaluation, condition-aware reliability, or reproducible low-resource deployment.

---

## 3. Dataset strategy: Kinetics-KDB

### 3.1 Public sources

Use public sources subject to their access terms and redistribution licenses:

- **BRENDA:** enzyme information and kinetic measurements — https://www.brenda-enzymes.org/
- **SABIO-RK:** reaction kinetics and experimental context — https://sabiork.h-its.org/
- **UniProt:** protein accessions, sequences, organism and annotation — https://www.uniprot.org/
- **PubChem:** compound identifiers and chemical structures — https://pubchem.ncbi.nlm.nih.gov/
- **Rhea:** curated biochemical reactions and reaction identifiers — https://www.rhea-db.org/
- **Published benchmark releases:** DLKcat, UniKP and CatPred, where reuse and redistribution terms permit.

Do not assume that database access implies permission to redistribute a merged database. Record the license and terms for every source. Prefer scripts that retrieve records through supported APIs or downloads; avoid brittle scraping.

### 3.2 Build in stages

**Stage A — Reproduce existing benchmarks.** Obtain released benchmark data and reproduce at least one established method, preferably UniKP or CatPred, using documented target definitions and splits where feasible.

**Stage B — Build a harmonized core.** Import compatible BRENDA/SABIO-RK measurements and resolve protein and compound identifiers. Retain source record IDs and references.

**Stage C — Add context and provenance.** Add assay pH, temperature, organism, mutation, cofactors, reaction context, kinetic equation, measurement type and source.

**Stage D — Release a benchmark card.** Report inclusion/exclusion rules, counts at each curation stage, missingness, overlap with source benchmarks, license constraints, split definitions and known biases.

Do not merge overlapping published datasets and count duplicate measurements as independent observations.

### 3.3 Suggested record schema

| Field | Meaning |
|---|---|
| record_id | Stable Kinetics-KDB measurement identifier |
| source_database, source_record_id | Original provenance |
| reference_id, doi | Publication or source reference |
| sequence, uniprot_id | Protein sequence and identifier |
| organism, ec_number, mutation | Biological context |
| smiles, inchikey, pubchem_cid | Substrate identity |
| parameter_type | Km or kcat |
| value_original, unit_original | Original reported value and unit |
| value_si, unit_si | Normalized value and unit |
| ph, temperature | Assay conditions, including original units |
| kinetic_equation | Experimental/model context where available |
| measurement_qualifier | Exact, approximate, upper/lower bound, etc. |
| replicate_group | Links genuine replicate observations |
| curation_flags | Ambiguity, conflict, missingness, standardization notes |

Store raw source records separately from normalized training tables. Never overwrite original values.

### 3.4 Unit handling and target definitions

Normalize Km to molar (M) and kcat to inverse seconds (s^-1), while retaining original values and units.

Targets:

    y_Km   = log10(Km in M)
    y_kcat = log10(kcat in s^-1)

For matched measurements:

    log10(kcat/Km in M^-1 s^-1) = y_kcat - y_Km

If Km is instead expressed in mM, kcat/Km is in mM^-1 s^-1; the log10 numerical value differs by 3 from the M^-1 s^-1 convention. Never mix conventions.

Only derive catalytic efficiency from measurements that are scientifically compatible (same enzyme variant, substrate, and relevant assay context). Do not pair unrelated Km and kcat observations.

### 3.5 Curation rules

1. Validate protein sequences and reject or flag non-standard residues according to a documented policy.
2. Validate SMILES with RDKit; preserve original strings and record standardized forms.
3. Resolve salts, tautomers, stereochemistry and mixtures conservatively; do not erase chemically meaningful distinctions.
4. Convert units using explicit, tested conversion tables.
5. Preserve inequality qualifiers and censored measurements; do not treat bounds as exact values.
6. Detect duplicates using protein, substrate, parameter, reference and assay context.
7. Keep genuine replicates linked; investigate conflicting values rather than silently averaging.
8. Track missing metadata explicitly and include missingness indicators in models.
9. Exclude records with unresolved identity or unit ambiguity from the primary benchmark; retain a separate audit table.
10. Publish a curation log and source-level counts.

Quality, provenance and independent test coverage are more important than maximizing the number of rows.

---

## 4. Model architecture: Kinetics-Multi

### 4.1 Design overview

Three input streams feed a compact interaction/fusion module:

1. Protein sequence encoder: frozen ESM-2 8M with cached residue embeddings.
2. Substrate encoder: small molecular message-passing neural network (MPNN/GIN), with Morgan fingerprints retained as a baseline.
3. Assay-context encoder: small MLP for numerical and categorical metadata, plus explicit missingness indicators.

The fused representation feeds separate Km and kcat prediction heads. An uncertainty head estimates observation-level (aleatoric) variance; independently trained ensemble members estimate model (epistemic) disagreement. A held-out calibration set is used for conformal intervals.

### 4.2 Protein representation

Initial encoder: facebookresearch/esm model facebook/esm2_t6_8M_UR50D.

- Freeze the pretrained encoder initially.
- Extract residue-level embeddings where feasible, and masked/padded sequence information correctly.
- Cache embeddings with model version, sequence hash, truncation policy and preprocessing version.
- Use a learned projection to a shared dimension (initially 128 or 256).
- Compare residue-level pooling/attention pooling with mean pooling.
- Fine-tuning is a later experiment only if compute and data justify it.

Important: a mobile inference pipeline for unseen sequences still needs a sequence encoder. An XGBoost/ONNX regressor alone cannot generate a new protein embedding.

### 4.3 Substrate representation

Convert validated SMILES to molecular graphs using RDKit.

Atom features may include atomic number, formal charge, aromaticity, hybridization, chirality and degree. Bond features may include bond type, aromaticity, ring membership and stereochemistry.

Start with a small 3-layer MPNN or GIN and global graph pooling. Keep Morgan fingerprints (e.g., radius 2, 2048 bits) as a strong, cheap baseline. Compare learned graph representations with fingerprints before adding more complexity.

### 4.4 Protein–substrate interaction

Let P be projected residue embeddings and S be projected atom embeddings. A cross-attention block can condition protein residues on the substrate:

    A = softmax((P Wq)(S Wk)^T / sqrt(d))
    H_protein_given_substrate = A (S Wv)

Pool the interaction representation and combine it with substrate and context representations. Start with one or two attention heads and a small hidden dimension.

Attention is a learned statistical interaction, not proof of physical binding or catalytic residue identity. Do not interpret attention weights as experimental evidence.

### 4.5 Assay context

Potential inputs: pH, temperature (normalized to Kelvin or a documented standard), organism embedding, enzyme variant/mutation descriptors, experimental source and relevant cofactor/reaction context.

- Add explicit missingness indicators.
- Fit normalization statistics on training data only.
- Avoid using source/reference IDs as shortcuts that leak target values.
- Test source metadata both included and excluded to quantify source-bias risk.
- Do not impute unknown pH/temperature as if observed.

### 4.6 Prediction and uncertainty heads

Predict log10(Km in M) and log10(kcat in s^-1) with separate heads. A Gaussian negative log-likelihood head is one candidate for aleatoric uncertainty:

    L = 0.5 * log(sigma^2) + (y - mu)^2 / (2 * sigma^2)

Use numerical safeguards and compare with deterministic regression. Train 3–5 independently initialized models as a starting ensemble; quantify epistemic uncertainty through between-model disagreement.

Use a separate calibration partition for conformal prediction. Report empirical coverage and interval width on untouched test partitions. If data are strongly grouped or heteroscedastic, assess group-conditional or normalized conformal approaches rather than assuming exchangeability without qualification.

### 4.7 Structural features: optional extension

Only after the sequence/graph/context model is working, evaluate inexpensive structure-derived features (e.g., confidence, secondary structure, solvent accessibility, geometric summaries or curated active-site annotations). AlphaFold DB: https://alphafold.ebi.ac.uk/

Structure availability and confidence are not uniform. Do not imply predicted structures establish substrate binding. Full docking is not required for the first paper and may be too expensive/noisy for this resource profile.

---

## 5. Experimental design

### 5.1 Baselines

| ID | Model | Purpose |
|---|---|---|
| B1 | Morgan + XGBoost | Substrate-only baseline |
| B2 | ESM-2 pooled embedding + XGBoost | Protein-only baseline |
| B3 | ESM-2 + Morgan + XGBoost | Existing Kinetics baseline |
| B4 | ESM-2 + molecular GNN | Learned chemistry baseline |
| B5 | Simple concatenation + MLP | Fusion baseline |
| B6 | Protein–substrate cross-attention | Proposed interaction model |
| B7 | B6 + assay context | Context-aware proposed model |
| B8 | B7 + uncertainty/ensemble | Reliability model |

Reproduce at least one published comparator on identical partitions where code/data licensing and implementation permit. Document deviations rather than claiming exact reproduction.

### 5.2 Leakage-resistant splits

Use at least four regimes:

- **Random split:** conventional reference, not the headline generalization result.
- **Protein-cluster split:** hold out sequence clusters (MMseqs2); report identity and coverage thresholds.
- **Chemical-scaffold split:** group by Bemis–Murcko scaffold; explicitly handle acyclic compounds and scaffold-empty cases.
- **Double-cold-start split:** test records contain both unseen protein clusters and unseen chemical scaffold groups.

Ensure duplicate measurements, linked replicates and repeated source records cannot cross partitions. Fit all preprocessing and feature-selection statistics on training data only. Keep a validation set for model selection and a separate calibration set for uncertainty calibration. The final test set must remain untouched until evaluation.

A 30% sequence-identity clustering threshold can be explored as a stringent setting, but report sensitivity to alternative thresholds and alignment coverage. Scaffold splits should also be audited for near-duplicate analogues.

### 5.3 Ablations

- Remove ESM-2 protein features.
- Replace GNN with Morgan fingerprints.
- Remove cross-attention and use concatenation.
- Remove assay metadata.
- Remove uncertainty head.
- Compare single model with ensemble.
- Add/remove optional structure features.
- Evaluate missing-context and complete-context subsets separately.

### 5.4 Metrics

For each target, report RMSE, MAE and R² on log10 values. Also report Spearman correlation and, where informative, Pearson correlation. Include group-bootstrap confidence intervals, repeated seeds and statistical comparisons appropriate to grouped observations.

For reliability, report:
- Prediction interval coverage at predeclared nominal levels.
- Mean/median interval width.
- Calibration error or coverage deviation.
- Negative log-likelihood where distributional assumptions are justified.
- Error versus predicted uncertainty.
- OOD detection AUROC/AUPRC, with a clearly defined OOD label and baseline.

Do not use a single metric to declare a model best. Report performance by split, target, source, metadata completeness and relevant subgroups.

### 5.5 External validation and biological case study

Reserve an independent dataset/source if possible. Check overlap at protein, substrate, publication and assay levels before calling it external validation.

A biological case study could examine a well-represented enzyme family, substrate series, or enzyme variants. Include predictions, uncertainty, nearest training examples and limitations. Wet-lab validation would strengthen the paper substantially, but should be described as future work if no laboratory collaboration is available.

### 5.6 Mobile deployment evaluation

Measure on a real ARM/Android device:
- Model artifact size.
- Peak memory.
- Cold-start and warm latency.
- CPU utilization.
- Energy use if measurable.
- Agreement with the research model.
- Uncertainty/interval preservation after compression.

Benchmark actual runtime performance. Do not assume FP16 or dynamic INT8 accelerates tree ensembles. A mobile pipeline for unseen sequences must include a compatible protein encoder or a separately distilled encoder, as well as chemical featurization.

---

## 6. Limited-compute implementation strategy

### Suggested starting configuration

| Component | Initial setting |
|---|---|
| Protein encoder | ESM-2 8M, frozen |
| Protein features | Cached residue embeddings |
| Molecular encoder | 3-layer compact GNN |
| Shared dimension | 128 initially; test 256 |
| Cross-attention | 1–2 heads |
| Prediction heads | Separate Km and kcat |
| Ensemble | 3 members initially |
| Classical baseline | XGBoost |
| Neural training | Small batches, early stopping |

These are starting points, not validated optimal hyperparameters.

### Workload allocation

- **Local CPU:** data cleaning, RDKit processing, classical baselines, split generation, metrics and tests.
- **CPU or occasional cloud GPU:** batched frozen ESM-2 embedding extraction.
- **Cloud GPU when available:** small GNN/cross-attention training and ensemble members.
- **Android CPU:** final inference benchmarking.

Cache embeddings and molecular graphs by content hash. Avoid repeated downloads and recomputation. Store configs, random seeds, environment versions and logs. Use a small pilot subset before processing the full dataset.

### Mobile deployment options

First compare a compact distilled sequence encoder plus a lightweight prediction head against the full ESM-2 path. If the encoder cannot run acceptably on-device, document a hybrid workflow (local or remote embedding generation) rather than claiming fully offline prediction.

---

## 7. Repository roadmap

The existing repository contains an initial prototype with preprocessing, ESM-2/Morgan features, XGBoost training, mobile optimization and CLI prediction. Treat it as a baseline, not a validated research pipeline.

### Proposed repository structure

    Kinetics/
    ├── README.md
    ├── RESEARCH_BLUEPRINT.md
    ├── CITATION.cff
    ├── LICENSE
    ├── pyproject.toml
    ├── configs/
    │   ├── baseline.yaml
    │   ├── multimodal.yaml
    │   └── evaluation.yaml
    ├── data/
    │   ├── raw/                 # ignored; user downloads separately
    │   ├── interim/
    │   ├── processed/
    │   ├── splits/
    │   └── README.md            # sources, licenses, retrieval instructions
    ├── docs/
    │   ├── DATA_CARD.md
    │   ├── MODEL_CARD.md
    │   ├── BENCHMARK_PROTOCOL.md
    │   └── MOBILE_DEPLOYMENT.md
    ├── src/
    │   ├── data/
    │   │   ├── adapters/
    │   │   ├── schema.py
    │   │   ├── normalize.py
    │   │   ├── deduplicate.py
    │   │   └── splits.py
    │   ├── features/
    │   │   ├── protein.py
    │   │   ├── molecule.py
    │   │   └── cache.py
    │   ├── models/
    │   │   ├── baselines.py
    │   │   ├── protein_encoder.py
    │   │   ├── molecule_gnn.py
    │   │   ├── fusion.py
    │   │   ├── multitask.py
    │   │   └── uncertainty.py
    │   ├── evaluation/
    │   │   ├── metrics.py
    │   │   ├── calibration.py
    │   │   ├── ood.py
    │   │   └── benchmark.py
    │   ├── deployment/
    │   │   ├── export.py
    │   │   └── benchmark_mobile.py
    │   └── predict.py
    ├── scripts/
    │   ├── download_public_data.py
    │   ├── build_dataset.py
    │   ├── generate_splits.py
    │   ├── extract_features.py
    │   ├── train.py
    │   └── evaluate.py
    ├── tests/
    │   ├── test_units.py
    │   ├── test_schema.py
    │   ├── test_deduplication.py
    │   ├── test_splits.py
    │   ├── test_features.py
    │   └── test_prediction.py
    ├── experiments/
    │   ├── README.md
    │   └── results/             # compact tracked summaries only
    └── paper/
        ├── outline.md
        ├── figures/
        └── supplementary/

This is a target structure; migrate incrementally rather than creating empty scaffolding all at once.

### Highest-priority repository changes

**P0 — Scientific validity**
1. Add a formal data schema, source provenance and unit conversion tests.
2. Add duplicate/replicate handling and curation reports.
3. Implement protein-cluster, scaffold and double-cold-start splits.
4. Add leakage tests that prove groups do not cross partitions.
5. Add a fixed benchmark harness with saved split manifests.

**P1 — Model development**
6. Keep current ESM-2 + Morgan + XGBoost as a reproducible baseline.
7. Add molecular graph featurization and a compact GNN.
8. Add interaction/fusion and assay metadata in separate ablatable modules.
9. Add multitask heads and uncertainty evaluation.

**P2 — Reliability and publication**
10. Add group-bootstrap confidence intervals, calibration and OOD metrics.
11. Add experiment configs, seeds, environment locks and model/data cards.
12. Add external validation and mobile runtime benchmarking.

### Reproducibility requirements

Every run should save:
- Git commit SHA.
- Dataset version and checksum.
- Split manifest and grouping thresholds.
- Model/configuration file.
- Random seed.
- Package and hardware information.
- Training log and checkpoint.
- Metrics JSON and prediction table.
- Feature-cache version and pretrained model identifier.

Do not commit private/raw data or model weights without checking source terms and repository size. Use Git LFS or a research artifact repository for large permitted artifacts.

---

## 8. Paper plan

### Proposed manuscript structure

1. **Abstract:** problem, gap, approach, evaluation design and actual measured results.
2. **Introduction:** enzyme kinetics importance, limitations of existing prediction, precise research questions and contributions.
3. **Related work:** kinetic datasets, protein language models, molecular GNNs, multimodal learning, uncertainty and generalization.
4. **Data and curation:** sources, schema, normalization, provenance, exclusions, duplicate handling and dataset statistics.
5. **Methods:** encoders, interaction module, context, multitask losses, uncertainty and calibration.
6. **Evaluation protocol:** random and grouped splits, double-cold-start, external validation, metrics and statistical analysis.
7. **Results:** baseline comparison, generalization, ablations, uncertainty, subgroup analysis and mobile efficiency.
8. **Case study:** a selected enzyme family or substrate series.
9. **Discussion:** biological interpretation, failure modes, dataset bias, missing metadata and limitations.
10. **Conclusion:** supported claims and next steps.
11. **Availability:** code, permitted data, configs, checkpoints and reproducibility instructions.

### Figures to prepare

- **Figure 1:** Overall Kinetics-Multi architecture.
- **Figure 2:** Dataset assembly, harmonization and exclusion flow.
- **Figure 3:** Split design and protein/scaffold overlap audit.
- **Figure 4:** Baseline and proposed-model performance across evaluation regimes.
- **Figure 5:** Calibration, uncertainty versus error and OOD behavior.
- **Figure 6:** Mobile model size, latency and predictive agreement.

### Tables

- Dataset source and quality summary.
- Model and baseline specifications.
- Performance by split and target.
- Ablation results.
- Uncertainty/calibration results.
- Mobile deployment metrics.

### Potential journals

Select only after results and scope are clear:
- Bioinformatics
- Briefings in Bioinformatics
- BMC Bioinformatics
- Journal of Cheminformatics
- Nature Communications (a substantially higher bar for novelty, validation and broad impact)

Do not optimize the project around a journal name before the scientific contribution is demonstrated.

---

## 9. Project milestones

| Phase | Deliverable | Exit criterion |
|---|---|---|
| 0. Literature audit | Literature matrix and novelty statement | Closest prior work compared; gap narrowed |
| 1. Data foundation | Kinetics-KDB v0.1 | Provenance, units and QC tests pass |
| 2. Baselines | Reproducible benchmark | Baselines run on fixed manifests |
| 3. Generalization | Grouped and double-cold-start splits | Leakage audit passes |
| 4. Integrated model | GNN + protein + context fusion | Ablations complete |
| 5. Reliability | Ensemble and conformal evaluation | Calibration assessed on held-out data |
| 6. External validation | Independent evaluation/case study | Overlap audit documented |
| 7. Mobile release | Compressed inference prototype | Real-device measurements recorded |
| 8. Publication | Manuscript and artifacts | Results reproducible from documented commands |

Suggested order matters more than calendar dates. Do not begin with the full neural architecture before data quality and splits are trustworthy.

---

## 10. Risks and mitigation

| Risk | Mitigation |
|---|---|
| Existing work already covers parts of the proposed novelty | Complete literature matrix; narrow claims |
| Data overlap and leakage | Stable IDs, replicate groups, cluster/scaffold split audits |
| Inconsistent assay conditions | Preserve context; stratify and analyze missingness |
| Sparse double-cold-start data | Report support/counts; use repeated group splits; avoid overclaiming |
| Limited compute | Freeze ESM-2, cache features, compact GNN, staged experiments |
| Unreliable uncertainty estimates | Separate calibration set; evaluate coverage and width |
| Mobile ESM-2 infeasibility | Distill encoder or disclose hybrid inference |
| Database redistribution restrictions | Publish retrieval/processing scripts and metadata where redistribution is not allowed |
| Overinterpretation of attention | Treat attention as model behavior, not causal biochemical evidence |

---

## 11. Minimum viable first paper versus stretch goals

### Minimum viable publishable study

- High-quality, traceable public benchmark.
- Reproducible ESM-2 + Morgan + XGBoost baseline.
- At least one established published comparator.
- Protein-cluster and chemical-scaffold splits.
- Double-cold-start evaluation if data support it.
- Integrated graph/context model with ablations.
- Proper uncertainty calibration.
- Independent validation or a carefully qualified limitation.

### Stretch goals

- Structure-aware features.
- Enzyme engineering case study.
- Experimental wet-lab validation.
- Distilled fully offline mobile model.
- Additional targets such as Ki.

The stretch goals should not delay a rigorous core study.

---

## 12. Immediate next actions

1. Audit the current repository and preserve the existing pipeline as the baseline.
2. Create a literature comparison spreadsheet and verify the closest competing work.
3. Obtain the released UniKP, DLKcat and CatPred benchmark data and check licensing/overlap.
4. Define the canonical record schema and unit conversion tests.
5. Generate immutable random, protein-cluster and scaffold split manifests.
6. Reproduce the current ESM-2 + Morgan + XGBoost baseline.
7. Only then implement the GNN, context encoder and cross-attention model.

### Definition of success

Kinetics is ready for manuscript submission only when its central claims are supported by reproducible experiments, leakage-resistant evaluation, uncertainty assessment, transparent data provenance and a fair comparison with relevant prior methods.

**Do not describe the model as state-of-the-art, validated, clinically useful, or experimentally accurate unless the corresponding evidence exists.**

---

## References and resources

- UniKP: https://www.nature.com/articles/s41467-023-44113-1
- CatPred: https://pmc.ncbi.nlm.nih.gov/articles/PMC11871309/
- CataPro: https://pmc.ncbi.nlm.nih.gov/articles/PMC11923063/
- KinForm: https://pmc.ncbi.nlm.nih.gov/articles/PMC13194986/
- DLKcat: https://academic.oup.com/bioinformatics/article/36/15/4223/5857583
- ESM: https://github.com/facebookresearch/esm
- BRENDA: https://www.brenda-enzymes.org/
- SABIO-RK: https://sabiork.h-its.org/
- UniProt: https://www.uniprot.org/
- PubChem: https://pubchem.ncbi.nlm.nih.gov/
- Rhea: https://www.rhea-db.org/
- AlphaFold DB: https://alphafold.ebi.ac.uk/

*This document is a research plan. Literature claims, dataset counts, licenses, software compatibility and model performance must be independently verified and updated before manuscript submission.*


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](KINETICS_MISSION.md), expanded [vision](VISION.md), and [emergency and humanitarian resilience requirements](docs/EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
