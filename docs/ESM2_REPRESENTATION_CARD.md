# ESM-2 protein representation card

> **Platform context:** This document describes a focused component of Kinetics. The complete cross-disciplinary scope is catalogued in `docs/SCIENCE_DOMAIN_CATALOGUE_100.md`; catalogue inclusion is not implementation or clinical-validation evidence.


> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

## Identity

- Model: `facebook/esm2_t6_8M_UR50D`
- Publisher/source: Meta AI, distributed through Hugging Face
- Immutable model revision: `8c576d2aba1b27317e9321c8491d72f00d1b110a`
- Tokenizer revision: same immutable revision
- License: MIT as declared on the Hugging Face model page; re-check the license before redistributing weights or derived artifacts.
- Architecture: ESM-2, 6 transformer layers, 8 million parameters, 320-dimensional hidden representation.
- Pretraining corpus family: UniRef50 (UR50/D).

## Intended research use

This repository uses the pretrained model as a fixed protein-sequence representation for exploratory enzyme–substrate kinetic modelling. It is not fine-tuned by the feature-generation step. The pooled vector is concatenated with a Morgan fingerprint for the current classical baseline; per-atom graph tensors are stored separately for future graph-aware models.

## Input and preprocessing

- Input is a single amino-acid sequence.
- Whitespace is removed and residues are uppercased.
- Accepted symbols: the standard 20 amino acids plus B, Z, X, U and O.
- Empty sequences, unsupported symbols and sequences longer than the configured limit are rejected. The default limit is 1,022 residues to leave room for BOS/EOS under the model's 1,026-token positional limit.
- No automatic truncation, sequence imputation, homology reduction or construct inference is performed.
- Mean pooling includes residue tokens only; BOS, EOS and padding tokens are excluded.

## Output

- One 320-dimensional float32 vector per sequence for this checkpoint.
- The feature archive preserves source record IDs, normalized sequences, target values, chemical representations and requested split-group labels.
- The adjacent feature manifest records model/tokenizer revisions, pooling, maximum length, device, Python/PyTorch/Transformers/tokenizers versions, RDKit version, source identifiers and versions, archive SHA-256 and runtime environment.

## Known limitations and risks

- This is a general-purpose protein language model, not an enzyme-kinetics-specific predictor. Embedding quality does not establish Km or kcat predictive validity.
- Pretraining data and model design can encode taxonomic, evolutionary and sequence-coverage biases. Performance may degrade on remote homologs, unusual proteins, engineered sequences or proteins with extensive noncanonical residues.
- Mean pooling removes residue-level localization and can obscure catalytic-site or domain-specific information.
- The representation contains no explicit substrate, assay pH, temperature, organism, construct, cofactors or buffer context.
- The default limit excludes longer sequences rather than silently truncating them; users must define and document any domain-specific segmentation strategy.
- This model output is not a probability, calibrated confidence, structural model, clinical result or evidence of biochemical mechanism.
- Bitwise-identical outputs across hardware, CUDA kernels and library builds are not guaranteed. The exact runtime and model revisions are recorded; a real-data reproducibility study remains required.

## Reproducibility and provenance

The feature builder pins the full model and tokenizer commit SHA, uses evaluation mode and inference mode, disables remote custom code, and includes the revision, feature schema, inference settings, device policy and relevant software versions in cache keys. Cache files are non-pickle NPZ archives written atomically. Feature NPZ files have adjacent JSON manifests with input/source hashes and output SHA-256.

The repository's automated tests use a deterministic fixture encoder to test cache invalidation, batching, archive alignment and manifests. They do not download or execute the full ESM checkpoint. Before scientific benchmarking, run the pinned model on a documented environment, repeat inference on representative sequences, record numerical differences and establish hardware-specific tolerances.

## References

- [Hugging Face model repository and pinned checkpoint](https://huggingface.co/facebook/esm2_t6_8M_UR50D/tree/8c576d2aba1b27317e9321c8491d72f00d1b110a)
- [Official ESM repository and model-family documentation](https://github.com/facebookresearch/esm)
- Lin et al. (2023), *Evolutionary-scale prediction of atomic-level protein structure with a language model*, Science 379, 1123–1130. See the official ESM repository for model family and release details.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
