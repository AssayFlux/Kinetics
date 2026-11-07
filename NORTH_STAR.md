# KINETICS — NORTH STAR
**Status:** Proposed baseline — awaiting owner approval  
**Direction changes:** Only with explicit owner approval and a corresponding DECISIONS.md entry.

## Mission
Build an offline-first, Android-first, publication-grade scientific workbench that makes rigorous biomedical research tools, engines and data packs accessible on mobile and connected compute. Preserve reproducibility, provenance, privacy and scientific honesty. Extend responsibly into pharmacogenomics and precision-medicine research, structure analysis and in-silico experimentation. Clinical decision support is a later, gated possibility—not the default product.

## Users
- Biomedical and life-science researchers.
- Computational biologists, bioinformaticians and structural biologists.
- Enzymologists and biochemists.
- Students and educators using research/learning workflows.
- Later, licensed clinicians and clinical pharmacists reviewing evidence-linked reports, only after clinical/regulatory gates.
- Research operators administering an optional remote compute node.

## Five tracks
- **R — Research platform:** Android-first platform, scientific capabilities, registry, reproducible workflows, sequence/protein/kinetics flagship, omics and release hardening.
- **S — Structure excellence:** Mol*/3Dmol.js offline viewing, preparation provenance, quality assessment, structural analyses, variant mapping and validated exports.
- **I — In-silico lab:** ligand preparation, docking, MD, ADMET/PK-PD and computational hypothesis generation with benchmarked uncertainty.
- **P — Precision medicine (PGx first):** public-data Research Mode pipeline, QC, PGx calling, guideline mapping and clinician-reviewed reports; clinical mode remains gated.
- **G — Governance:** privacy/security, licenses, QMS, fairness, validation evidence, registry enforcement and paper integrity.

## Measurable goals and success criteria
1. **Governance baseline:** all roadmap items have owner, status, date field, dependencies and gate; all direction/scope/license/data/regulatory decisions are logged.
2. **Reproducibility:** every validated capability has machine-readable provenance, pinned versions, reference data, tolerances and automated validation; reproduce-all regenerates paper tables/figures from raw evidence.
3. **Mobile feasibility:** Phase 1 records measured results for embedded Python/Biopython, Rust FFI, C++ JNI, one engine, chemistry feasibility, 16 KB alignment, APK/AAB size, cold start and memory on emulator and real arm64 device.
4. **v0.1.0:** Phases 0–3 pass their documented gates; sequence, protein-property and enzyme-kinetics capabilities have independent validation records; installs and works offline on declared real devices.
5. **Structure quality:** every supported structure displays provenance and quality indicators; S2 metrics meet predeclared tolerances on a fixed benchmark before being called validated.
6. **In-silico quality:** docking reports redocking RMSD success and decoy enrichment; MD reports stability/energy checks and reference reproduction; ADMET/PK reports held-out metrics and applicability domain. No performance number is pre-assumed.
7. **PGx research quality:** each supported gene has separate caller validation, reference-material concordance, genome-build tracking and explicit indeterminate handling; guideline mapping preserves versions and evidence strength.
8. **Fairness:** ancestry coverage is disclosed for every relevant source/model; portability limitations appear in outputs and validation reports.
9. **Clinical safety:** public builds never expose Clinical Decision Support Mode before all applicable Part G requirements and owner approval are documented.
10. **Privacy:** no real patient data before P0; no genomic upload by default; all transfers are explicit, consented and encrypted.

## Non-goals
- Autonomous diagnosis, prescribing, dosing, emergency triage or patient-directed start/stop medication instructions.
- Clinical claims or clinical-grade release without analytical validity, clinical validity, clinical utility, regulatory/legal review and required authorization.
- Universal disease-treatment recommendation across all diseases.
- Treating in-silico predictions as proof of efficacy/safety.
- Bulk library of books, papers, tutorials or scraped documents.
- Silent network upload, telemetry by default, executable-code downloads or unlicensed redistribution.
- Dangerous pathogen/toxin design or enhancement.
- Adding languages, engines, tiers or restricted data sources without approval.

## Guardrails
1. The app does not autonomously prescribe, dose, diagnose or make emergency decisions.
2. No clinical claims in app, store listing, README or paper without matching validation and regulatory standing.
3. Public builds ship Research Mode only.
4. No real patient data is handled before P0 passes.
5. In-silico results are predictions, always labelled as such with measured accuracy.
6. Every database, model and engine has a verified license and recorded version; restrictive items need owner decision.
7. No invented numbers, results, references or validations. Citations are verified against sources.
8. No features aimed at designing or enhancing dangerous pathogens or toxins.
9. Direction changes only through DECISIONS.md with owner's approval.

## Definitions of done

### v0.1.0
- Track R Phase 0–3 exit gates passed with repository evidence and explicit gate approvals.
- Android app installs on documented real arm64 devices and operates offline for supported workflows.
- Sequence tools, protein properties and enzyme-kinetics tools are implemented and independently validated against cited references with tolerances.
- Provenance is captured and reproducibility checks pass.
- Registry and public claims match actual capability status.
- Research-use-only language is visible; no clinical mode or patient treatment recommendation.

### v1.0
- Stable, documented app/project formats, import/export, resumable jobs, registry and data-pack verification.
- Declared Track R capabilities are implemented and validated with reproducible reports; no capability is overstated.
- Privacy/security controls, offline behaviour, crash/performance/accessibility budgets and release checklist pass.
- Structure and in-silico features are included only to their independently demonstrated validation level.
- Third-party licenses and data rights are reviewed and recorded; paper claims trace to benchmark/registry evidence.
- Research Mode only unless clinical release criteria independently met.

### Clinical-grade release
- P0 and all applicable Part G requirements completed and documented for each jurisdiction and intended use.
- Intended-use statement/classification and qualified legal/regulatory advice recorded.
- QMS and lifecycle/risk/usability controls established; analytical validity, clinical validity and clinical utility separately evidenced.
- Only accredited/validated genotype sources accepted for clinical use.
- Clinical advisory board reviews claims and workflows; prospective evaluation has ethics approval.
- Clinical mode is feature-flagged, access-controlled, audited and requires clinician sign-off.
- Post-release surveillance, incident reporting, guideline updates and versioned re-analysis operational.
- Explicit owner approval before any clinical release. The app never autonomously prescribes.

## Governance of this document
This is the permanent direction baseline. Proposed changes must be written as a decision with options, rationale, consequences and explicit owner approval before changing this file.
