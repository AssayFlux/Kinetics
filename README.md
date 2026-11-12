<p align="center" style="white-space: nowrap;">
  <img src="assets/brand/organization-logo.gif" alt="AssayFlux animated organization logo" width="100" height="100" style="object-fit: contain; vertical-align: middle;">
  &nbsp;&nbsp;
  <img src="assets/brand/brand-logo.svg" alt="AssayFlux original SVG brand logo" width="100" height="100" style="object-fit: contain; vertical-align: middle;">
  &nbsp;&nbsp;
  <img src="assets/brand/kinetics-logo.gif" alt="Kinetics animated logo" width="100" height="100" style="object-fit: contain; vertical-align: middle;">
</p>

<h1 align="center">Kinetics</h1>
<p align="center">
  <strong>Offline-first scientific research workbench</strong><br>
  Android-native · Reproducible · Provenance-aware · Research-only
</p>

<p align="center">
  <a href="https://github.com/AssayFlux/Kinetics/actions/workflows/ci.yml"><img src="https://github.com/AssayFlux/Kinetics/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
  <img src="https://img.shields.io/badge/platform-Android%20%7C%20Linux-3B6B68" alt="Platform">
  <img src="https://img.shields.io/badge/mode-Research%20only-7B1E34" alt="Research only">
  <img src="https://img.shields.io/badge/license-Apache--2.0-D9A441" alt="Apache 2.0">
  <img src="https://img.shields.io/badge/release-pre--release-lightgrey" alt="Pre-release">
</p>

Kinetics is a modular workbench for computational biology and in-silico research. It combines an Android-native experience with Python, C++ and Rust scientific components, reproducible workflows and provenance-aware outputs.

<blockquote>
  <strong>Development status:</strong> This is an active pre-release project, not a validated scientific product or production release. Research Mode only. Patient/clinical data, individual clinical interpretation, treatment recommendations and Clinical Mode remain disabled.
</blockquote>

## Project snapshot

<table>
  <tr>
    <td width="33%" align="center"><strong>6 tracks</strong><br>Owner-approved sequence</td>
    <td width="33%" align="center"><strong>Android-first</strong><br>Offline-first architecture</td>
    <td width="33%" align="center"><strong>Research only</strong><br>No clinical deployment</td>
  </tr>
  <tr>
    <td align="center"><strong>R → S → I</strong><br>Software exit gates closed</td>
    <td align="center"><strong>P → G → U</strong><br>Current and upcoming work</td>
    <td align="center"><strong>Evidence-led</strong><br>Build ≠ validation</td>
  </tr>
</table>

## Track order & progress

**Canonical order: R → S → I → P → G → U** · Decision D-023 · 12 November 2026.

The percentages below measure **documented engineering-gate closure only**, not scientific, clinical, legal, regulatory or release compliance. A completed software gate does not close its external acceptance obligations.

| Track | Focus | Engineering gate | Remaining position |
|---|---|---:|---|
| **R** · Research platform | Android foundation, storage, scientific engines, genomics and hardening | **100%** · software audit closed | Physical-device, scientific, licensing and release evidence open |
| **S** · Structure & discovery | Structure viewer, sequence triage, genome annotation and protein intelligence | **100%** · software scope closed | Independent references, licensed resources/models and device evidence open |
| **I** · In-silico lab | Chemistry, docking, molecular dynamics, ADMET and simulations | **100%** · software audit closed | Real scientific benchmarks, data/model licences, secure node and device tests open |
| **P** · Precision medicine | PGx-first research foundation and governance | **In progress** | Latest recorded software CI passed 9/9 jobs; P0 remains **NOT APPROVED** and external evidence gates remain open |
| **G** · Governance | Security, supply chain, quality, privacy, scientific integrity and publication | **0% accepted** | Planning/register baseline drafted; G0 owner acceptance and G1–G7 implementation/reviews remain open |
| **U** · User experience | Brand system, app shell, authentication and research workflows | **0% accepted** | Partial U0–U3 work is retained as baseline; further sequential work follows G |

<details>
  <summary><strong>How to read the percentages</strong></summary>

  - 100% means the documented software implementation/audit gate for that track was recorded as closed.
  - 0% accepted means no formal track exit gate has been accepted yet; it does not mean no source code or planning exists.
  - P is shown as in progress rather than assigned an invented percentage: software checks have passed, but the formal track/P0 gate is not accepted.
  - No overall scientific or regulatory compliance percentage is claimed. Independent validation, legal/ethics/privacy determinations, licensing decisions and physical-device acceptance are separate evidence gates.
</details>

## Product experience

<p align="center">
  <img src="assets/design-previews/dashboard-reference.jpg" alt="Owner-supplied Kinetics dashboard design reference" width="48%">
  <img src="assets/design-previews/login-reference.jpg" alt="Owner-supplied Kinetics login design reference" width="48%">
</p>

The active product direction is D-015 Light Classic, with Dark Classic and System appearance. These are owner-supplied design references, not screenshots of a completed application. Real app screens, accessibility, device behaviour and brand integration are verified separately.

## Engineering principles

- **Offline-first:** local research workflows and explicit boundaries for optional remote compute.
- **Reproducible:** pinned inputs, parameters, versions, seeds and output provenance.
- **Evidence-aware:** distinguish implementation, automated tests, independent scientific validation and real-device acceptance.
- **Safe by default:** bounded parsing/resources, explicit abstention and no invented scientific conclusions.
- **Research-only:** no patient/clinical workflow or treatment/dosing recommendation.

## Current safeguards

- P0 remains **BLOCKED / NOT APPROVED**.
- No patient data, human-subject activity, individual PGx interpretation or Clinical Mode.
- Public availability does not imply data/model redistribution rights.
- CI green does not establish biological accuracy, independent security review or physical-device operation.
- Debug APK/AAB artifacts are not signed production releases.

## Explore the repository

<p>
  <a href="ROADMAP.md"><img src="https://img.shields.io/badge/ROADMAP-track%20plan-7B1E34" alt="Roadmap"></a>
  <a href="DECISIONS.md"><img src="https://img.shields.io/badge/DECISIONS-owner%20decisions-D9A441" alt="Decisions"></a>
  <a href="docs/README.md"><img src="https://img.shields.io/badge/DOCS-documentation%20index-3B6B68" alt="Documentation"></a>
  <a href="docs/track-g/implementation-plan.md"><img src="https://img.shields.io/badge/GOVERNANCE-Track%20G-6C5B7B" alt="Track G"></a>
  <a href="assets/brand/README.md"><img src="https://img.shields.io/badge/BRAND-assets-8A5967" alt="Brand assets"></a>
  <a href="paper/manuscript-skeleton.md"><img src="https://img.shields.io/badge/PAPER-methods%20draft-596B7A" alt="Manuscript"></a>
</p>

<details>
  <summary><strong>Track R — Research platform</strong></summary>

  Android/runtime foundation, secure local storage, sequence and structural analysis, chemistry, phylogenetics, omics, gene catalogue and quality/release hardening. Software audit is closed; device, scientific, licensing and release acceptance remain open.
</details>

<details>
  <summary><strong>Track S — Structure, sequence & discovery</strong></summary>

  Structure viewer and geometry, variant/interface evidence, prediction boundary, session export, unknown-sequence triage, genome annotation, genetic-code investigation, protein intelligence and constrained design. Software scope is closed; independent validation and approved resources remain open.
</details>

<details>
  <summary><strong>Track I — In-silico laboratory</strong></summary>

  Ligand preparation, docking, molecular dynamics, ADMET/PK-PD utilities and synthetic variant/cohort research. Software implementation/integration audit is closed; real scientific benchmarks, licensing, secure compute and device tests remain open.
</details>

<details>
  <summary><strong>Track P — Precision medicine</strong></summary>

  PGx-first research preparation (P0–P7). Internal schemas and software checks do not constitute clinical approval. P0 remains NOT APPROVED; external legal, ethics, privacy, security, regulatory and scientific evidence is outstanding.
</details>

<details>
  <summary><strong>Track G — Governance</strong></summary>

  G0–G7: governance map, security assurance, licensing/supply chain, software quality, privacy/data governance, scientific integrity/bias, publication integrity and operations. The initial plan and evidence register are drafts, not accepted controls or certifications.
</details>

<details>
  <summary><strong>Track U — User experience</strong></summary>

  U0–U6: design system, adaptive shell, privacy/lock, research workflow screens, scientific visualisations, genomics/PGx research screens and accessibility/localisation. Partial U0–U3 source is pre-existing baseline; the next sequential U implementation follows G under D-023.
</details>

## Build & verification

GitHub Actions is the source of current automated build/test status. Historical passing runs are not evidence for a different commit. Physical Android-device testing and independent scientific validation remain separate.

## License

Project code: Apache-2.0. Third-party engines, dependencies, models, datasets, fonts and assets retain their own terms and require separate review.
