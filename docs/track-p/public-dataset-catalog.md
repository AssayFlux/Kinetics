# Public dataset catalogue — P-track preparation

This catalogue is metadata-only. It is not an authorization to download, process,
redistribute, or use any dataset in a patient-facing or clinical workflow.

## Intake rules

- Add only public, non-patient datasets and public reference materials.
- Record the source URL, accession/version, exact license and license URL,
  retrieval timestamp, and SHA-256 of the acquired immutable payload.
- Set `license_review_status: not_reviewed` until a human has reviewed the
  exact terms for the intended use. A license label or public availability is
  not itself approval.
- Set `patient_data: false`; reject any source that contains patient-level
  records, direct identifiers, or data whose public/non-patient status is unclear.
- Do not place payloads in this catalogue. Store only approved metadata here;
  data intake requires a separate reviewed workflow.
- Do not use the catalogue for genotype interpretation, patient stratification,
  clinical recommendations, or Clinical Mode.

## Gate

P0 remains blocked. This file advances only public-data inventory preparation.
No patient data, human participants, clinical feature, or regulatory claim is
authorized by adding an entry. P1–P6 remain gated until P0 and their own
reference, validation, security, and owner gates pass.

## Schema

The machine-readable contract is `api/public-dataset-catalog.schema.json`.
