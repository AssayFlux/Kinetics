# Astronaut × Kinetics assistant integration

## Status

This is the integration contract and first domain-tool layer. Both repositories are under active development; this document does **not** claim that the Android UI, network bridge, or end-to-end assistant is already connected.

- **Astronaut** is the Android assistant shell: Kotlin, Jetpack Compose, Room chat history, imported local LiteRT-LM models, task routing, and offline document/OCR/retrieval services.
- **Kinetics** is the scientific domain engine: protein/SMILES validation, enzyme kinetic prediction, training and evaluation.
- **Boundary:** Astronaut owns conversation and model inference. Kinetics exposes narrowly scoped scientific tools. Do not copy the entire Astronaut Android application into this Python repository.

Astronaut currently documents local inference using an imported `.litertlm` model; no model is bundled. Its backend currently focuses on dataset registration and optional training jobs, not chat inference. Its feature-status document also marks several services as not yet wired end-to-end into the chat UI.

## Target architecture

```text
Astronaut Android (Compose chat, Room history, local LiteRT-LM)
        |
        | assistant tool request / structured JSON
        v
Kinetics tool adapter (this repository)
        |
        +--> validate sequence and substrate SMILES
        +--> run trained Km / kcat model when model artifacts exist
        +--> return units, model status, warnings and provenance
        |
        v
Astronaut local model explains the result to the user
```

The LLM must not invent predictions. A prediction is available only when a trained Kinetics model artifact exists and the prediction tool returns successfully. The assistant should distinguish a model estimate from an experimental measurement and disclose missing assay context and out-of-distribution uncertainty.

## Tool contract (first version)

Tool name: `kinetics_predict`

Input:
- `sequence`: protein sequence using the 20 standard amino acids.
- `smiles`: substrate SMILES.

Successful output:
- `log10_km`: predicted log10(Km), with Km represented in mM.
- `km_mM`: predicted Km in mM.
- `log10_kcat`: predicted log10(kcat), with kcat represented in s^-1.
- `kcat_s-1`: predicted kcat in s^-1.
- `status` and `limitations`: model availability and interpretation warnings.

The first implementation lives in `src/assistant_tools.py`. It is a Python-callable tool adapter, not yet an HTTP endpoint. Astronaut can integrate it through a future authenticated Kinetics API or a local service on the same device/network. Do not expose an unauthenticated prediction service to the public internet.

## Recommended implementation stages

1. **Domain tool (added here):** stable validation and prediction wrapper around the existing `src.predict.predict` function.
2. **Kinetics service:** add a small API only after deciding where inference runs (Android device, local workstation, or hosted server). Keep model loading outside individual requests and add request limits/authentication.
3. **Astronaut bridge:** add a typed tool-call contract and a registered provider/tool in the Kotlin app; route Kinetics questions to the tool and pass only returned structured results into the local model prompt.
4. **Chat UX:** display tool activity, model version/status, units and warnings; persist conversation as Astronaut already does.
5. **Validation:** integration tests with a tiny fixture model, Android device tests, timeout/offline handling, and explicit user-visible fallback when the Kinetics engine is unavailable.

## Security and privacy

- Never put provider/API keys in source code, Android resources, or the APK.
- If a hosted LLM is added later, keep its credentials on a trusted backend and make network use explicit.
- Treat protein sequences, SMILES, uploaded papers and retrieved text as untrusted input, not as instructions.
- Do not upload user sequences or chat history to a third party without clear consent.
- Keep local-only mode possible; if the Kinetics Python runtime is not available on Android, show that the scientific prediction tool is unavailable rather than silently sending data elsewhere.

## Current limitations

The existing Kinetics baseline requires a trained `models/kinetics_model.joblib` (and may download ESM-2 weights for unseen sequences). The repository does not yet contain trained model weights or a production API. Its baseline also uses a random split and has not been scientifically validated. The assistant must not imply that predictions are experimentally verified or calibrated.
