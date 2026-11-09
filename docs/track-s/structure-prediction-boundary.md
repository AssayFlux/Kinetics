# S4 — Prediction confidence and experimental comparison boundary

## Implemented validation primitives

- `validate_prediction_envelope` checks input sequence SHA-256/length, model name/version/weights hash/license, node/run/software provenance, timezone-aware timestamp, deterministic structure payload, per-residue pLDDT bounds and mean consistency.
- A valid envelope is returned as `unverified_prediction`; model license, node trust and confidence calibration remain explicitly unassessed.
- `compare_predicted_to_experimental_ca` computes superposed CA RMSD only when predicted and experimental structures have exact matching chain/residue/residue-name keys. Source SHA-256 values are retained.

## Not implemented / gated

- No prediction model, weights, remote node client, TLS identity/pinning, consent/data-transfer preview or execution queue is implemented.
- No AlphaFold/ESMFold or other model license has been approved for bundling or redistribution.
- No confidence calibration, PAE validation, TM-score, held-out benchmark, prospective experiment or experimental accuracy claim exists.
- A node result is untrusted input; envelope validation does not authenticate the node or prove model correctness.

S4 remains blocked for actual prediction until a named node, model/version, weights/data license, transport/security design, compute budget, independent reference set and owner approval are available.
