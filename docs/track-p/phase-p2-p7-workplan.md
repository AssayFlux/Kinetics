# Track P — P0–P7 engineering workplan

**Scope:** research-only, synthetic fixtures and public non-patient metadata. **Overall:** in progress; P0 NOT APPROVED; no patient/clinical authorization.

## Verified baseline (2026-11-11)
- Commit `e9faf7165ceeb2ee9af9ed08d663c32d0be10cda`; exact-head workflow [#42998496868](https://github.com/AssayFlux/Kinetics/actions/runs/42998496868), 9/9 jobs passed.
- Python 509 passed, 9 skipped.
- APK 70,389,586 bytes; SHA-256 `636476de0eab15b767815499d4220219f8953ff6e04f21dbb3f42b8903c76789`.
- AAB 40,260,318 bytes; SHA-256 `a0cee244440b16f7af6ab9a55be4a1e3ad976f62520e41057269b7b99abe334b`.
- JVM tests, package alignment, engine smoke checks, RDKit, SPDX, Node security and host reference comparisons passed. Engine smoke checks are not biological validation; no physical-device runtime was performed.

## P0 — governance
Draft intended use, exclusions, data inventory, threat model, quality lifecycle, validation matrix, stop-work procedure and risk register exist. Still required: qualified jurisdiction-specific legal/regulatory advice; competent ethics determination; qualified independent clinical/scientific review; approved privacy impact/lawful-basis assessment; security assessment; QMS applicability/approval; exact-source licensing; independent validation protocol approval; residual-risk disposition; formal owner P0 decision. No appointments or approvals are fabricated. P0 remains NOT APPROVED.

## P1 — public-data and synthetic foundation
Implemented metadata-only candidate catalogue, schema/checker, synthetic reference contract and aggregate-only synthetic VCF QC bound to assembly/accession/release/contig/digest/coordinate provenance. Remaining: independent reference concordance, source terms review, fuzz/resource audit and device workflow tests. Acquired catalogue entries remain empty.

## P2 — allele/haplotype research
Existing source includes provenance-bearing PGx definition parsing and conservative fully phased haplotype matching, plus PharmVar TSV parsing with exact-byte SHA-256 and accession preservation. This increment adds synthetic regression coverage for release/digest metadata, build mismatch, ambiguous definitions, exact match and unphased/incomplete abstention. No clinical star-allele caller, diplotype/phenotype inference, CNV/structural caller or treatment output.

## P3 — guideline evidence
Adds versioned research-only guideline metadata schema with source/version, licence state, build, evidence level and reviewer; clinical_decision_support is hard false. No executable recommendation mapping. Exact-source reuse permissions and independent mapping review remain required.

## P4 — human curation
Adds curation record schema with uncertain outcomes, curator role, mandatory second review and hard prohibition on autonomous final classification/clinical use. Actual qualified curators, adjudicated records and operational audit workflow remain outstanding.

## P5 — ethics preparation
Adds protocol template for question, study design, participant criteria, consent/privacy, risk, endpoints, monitoring and stop criteria. No protocol submission, ethics determination, recruitment or human-subject activity has occurred or is authorized.

## P6 — risk/governance
Adds structured risk/control and jurisdiction-review schemas. Contracts hard-prohibit patient-data and Clinical Mode authorization. Actual risk ratings, control verification, security/privacy assessment, QMS determination, independent validation and owner acceptance remain outstanding.

## P7 — regulatory preparation
Defines jurisdiction-specific classification, advice, evidence and prospective-evaluation requirements. No regulator advice, submission, clearance, prospective study or regulated deployment is claimed.

## Stop conditions
Stop affected workflow for patient/identifiable data ingress, unclear source rights, reference mismatch, leak/compromise, unsupported/ambiguous calls, misleading clinical wording, missing/withdrawn approval or unexplained discrepancy. Quarantine, preserve minimum non-sensitive audit evidence, notify owner/competent leads and reopen only after review.

## Completion semantics
Schemas, parsers, synthetic tests and green CI close software verification only. They do not close licensing, scientific, legal, ethics, privacy, clinical, regulatory, human-study or physical-device gates. P0–P7 cannot be marked fully complete until their respective evidence exists.


## Exact-head audit refresh (2026-11-11)
- Commit aee8f1e3a73dfa5136ca2472877bd541727453db; [workflow #43002587271](https://github.com/AssayFlux/Kinetics/actions/runs/43002587271) passed 9/9 jobs.
- Python 522 passed, 9 skipped; Ruff and strict mypy passed.
- Android arm64 debug APK 70,389,802 bytes (SHA-256 `4cd8ce2e1f5e6874e39d589e853fdb801c9322c56461a19703653d031f5f9fb5`); AAB 40,260,451 bytes (SHA-256 `90ce8bbfac2e6a17faf385bcffcee1ddcc179bde1ecc625ef93a5b25ff66bdc1`). 16 KB package alignment and JVM tests passed; no emulator/physical-device runtime.
- Host reference comparisons, OpenMM, Vina, RDKit descriptor/ADMET utility smoke checks, SPDX inventory and Node worker security tests passed. Smoke checks are not biological/clinical validation.
- This verifies the committed software/tests only. P0 is NOT APPROVED; independent P1 reference/source/security/device evidence and P2–P7 operational/external review gates remain open.
