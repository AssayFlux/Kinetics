<!-- KINETICS · ASSAYFLUX SCIENTIFIC SYSTEMS -->

<p align="center">
  <table>
    <tr>
      <td align="center" width="33%">
        <img src="Assets/Organization%20Logo%201%E2%98%851.gif" alt="AssayFlux animated organization logo" height="104">
      </td>
      <td align="center" width="34%">
        <img src="Assets/Kinetics%20Guilloche%20Logo.svg" alt="Kinetics guilloche scientific logo" height="104">
      </td>
      <td align="center" width="33%">
        <img src="Assets/DNA%20Rainbow%20Helix.gif" alt="Animated rainbow DNA double helix" height="104">
      </td>
    </tr>
  </table>
</p>

<h1 align="center">KINETICS</h1>
<p align="center">
  <strong>OFFLINE-FIRST SCIENTIFIC RESEARCH WORKBENCH</strong><br>
  <sub>ASSAYFLUX SCIENTIFIC SYSTEMS</sub>
</p>

<p align="center">
  <a href="https://github.com/AssayFlux/Kinetics/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/AssayFlux/Kinetics/ci.yml?branch=main&style=flat-square&label=CI&labelColor=30202A&color=8A6A45" alt="CI status"></a>
  <a href="https://github.com/AssayFlux/Kinetics/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache--2.0-8A6A45?style=flat-square&labelColor=30202A" alt="Apache 2.0 license"></a>
  <a href="https://github.com/AssayFlux/Kinetics/commits/main"><img src="https://img.shields.io/github/last-commit/AssayFlux/Kinetics?style=flat-square&label=Updated&labelColor=30202A&color=8A6A45" alt="Latest commit"></a>
  <a href="https://github.com/AssayFlux/Kinetics/stargazers"><img src="https://img.shields.io/github/stars/AssayFlux/Kinetics?style=flat-square&label=Stars&labelColor=30202A&color=8A6A45" alt="GitHub stars"></a>
</p>

<p align="center">
  <em>Every helix carries a question. Every answer carries its evidence.</em>
</p>

---

## ◈ THE PROJECT

**Kinetics** is an open-source scientific research workbench developed by **AssayFlux Scientific Systems**. It brings an Android-native application together with a Python research core and selected native components, using versioned contracts and a capability registry to organise scientific workflows.

Its engineering priorities are **reproducibility, provenance, bounded inputs, offline-first operation and honest evidence**.

<sub>PROJECT MATURITY · Research-platform engineering prototype. Not a clinically validated platform.</sub>

## ◈ RESEARCH DOMAINS

<table>
  <tr>
    <td width="50%" valign="top">
      <h3><img src="https://api.iconify.design/lucide/dna.svg?color=%23800020" width="20" alt=""> Sequence &amp; Genomics</h3>
      FASTA/FASTQ parsing, quality control, sequence utilities and research-only variant/PGx foundations.
    </td>
    <td width="50%" valign="top">
      <h3><img src="https://api.iconify.design/lucide/network.svg?color=%23800020" width="20" alt=""> Structural Biology</h3>
      PDB/mmCIF parsing, contacts, RMSD and bounded structure-analysis foundations.
    </td>
  </tr>
  <tr>
    <td valign="top">
      <h3><img src="https://api.iconify.design/lucide/flask-conical.svg?color=%23800020" width="20" alt=""> Chemistry &amp; Docking</h3>
      Molecular graph and format utilities, with optional RDKit and AutoDock Vina integrations.
    </td>
    <td valign="top">
      <h3><img src="https://api.iconify.design/lucide/activity.svg?color=%23800020" width="20" alt=""> Kinetics &amp; Dynamics</h3>
      Enzyme-kinetics foundations and optional molecular-dynamics integration through OpenMM.
    </td>
  </tr>
  <tr>
    <td valign="top">
      <h3><img src="https://api.iconify.design/lucide/chart-no-axes-combined.svg?color=%23800020" width="20" alt=""> Omics &amp; Statistics</h3>
      Exploratory data-analysis, statistical and synthetic-cohort utilities.
    </td>
    <td valign="top">
      <h3><img src="https://api.iconify.design/lucide/shield-check.svg?color=%23800020" width="20" alt=""> Evidence &amp; Governance</h3>
      Capability registry, schemas, provenance, source inventory and validation controls.
    </td>
  </tr>
</table>

<p align="center">
  <img src="Assets/Laboratory.gif" alt="Animated scientific laboratory illustration" width="88%">
</p>

## ◈ ENGINEERING

| LAYER | TECHNOLOGY |
|:--|:--|
| Android | Kotlin · Jetpack Compose · AndroidX · Gradle |
| Scientific core | Python 3.10+ · pytest · Ruff · mypy |
| Native | C++17 · JNI/NDK · Rust |
| Optional engines | RDKit · AutoDock Vina · OpenMM |
| Viewer & worker | HTML5 · CSS · JavaScript · WebView · Node.js |
| Data & contracts | SQLite · JSON Schema · YAML · SPDX |

<p align="center">
  <img src="https://skillicons.dev/icons?i=androidstudio,kotlin,gradle,python,cpp,rust,nodejs,html,css,js,sqlite,git,github,linux&perline=7" alt="Kinetics engineering technologies">
</p>

## ◈ SYSTEM ARCHITECTURE

```mermaid
flowchart TD
    USER["RESEARCH USER"] --> APP["ANDROID · KOTLIN / COMPOSE"]
    APP --> CORE["APP ORCHESTRATION"]
    CORE --> PY["PYTHON SCIENTIFIC CORE"]
    CORE --> NAT["C++ / JNI · RUST"]
    CORE --> WEB["OFFLINE VIEWERS"]
    PY --> DOM["SEQUENCE · STRUCTURE · CHEMISTRY"]
    PY --> KIN["KINETICS · OMICS · STATISTICS"]
    PY --> OPT["OPTIONAL HOST ENGINES"]
    CORE --> CONTRACT["VERSIONED CONTRACTS · REGISTRY · PROVENANCE"]
    CI["GITHUB ACTIONS"] --> QA["TESTS · BUILD · QUALITY GATES"]
    CONTRACT --> QA
    classDef royal fill:#800020,color:#FFF8E7,stroke:#D4AF37,stroke-width:2px;
    classDef gold fill:#D4AF37,color:#211820,stroke:#800020,stroke-width:1px;
    class APP,CORE royal;
    class CONTRACT,CI,QA gold;
```

## ◈ TRACK SEQUENCE & STATUS

**Current order — D-023 (12 November 2026):**  
**R → S → I → P → G → U**

Each track follows the same two-step gate: **build the documented base → audit, test and close software gaps**. External evidence remains separately gated.

| TRACK | SOFTWARE POSITION | REMAINING GATE |
|:---:|:--|:--|
| **R** | Software scope closed | Scientific, device, licensing and release evidence carry forward. |
| **S** | Software scope closed | Independent scientific, licensed-resource and device evidence carry forward. |
| **I** | Software scope closed | Scientific benchmarks, licensing, secure-node and device evidence carry forward. |
| **P** | In progress | Exact-head verification; P0 remains **BLOCKED / NOT APPROVED**. |
| **G** | Baseline drafted; sequential implementation gated | P verification, then G build/audit and independent operating evidence. |
| **U** | Partial U0–U3 baseline retained | Further work follows G's two-step gate assessment. |

<sub>Track status is a concise roadmap summary, not a percentage-compliance claim. A green software workflow does not establish scientific validity, clinical suitability or physical-device verification.</sub>

## ◈ CURRENT LIMITATIONS

- Research-only scope. No patient-data workflow or Clinical Decision Support Mode is authorised.
- P0 is **NOT APPROVED**. Its external legal, ethics, clinical, privacy, security and regulatory determinations remain outstanding.
- Host tests and synthetic fixtures do not establish biological, clinical or device validity.
- Optional engines, datasets, models and fonts require separate upstream licence and redistribution review.
- No production deployment or signed public release is claimed.

## ◈ DESIGN REFERENCES

<table>
  <tr>
    <td align="center" width="50%">
      <img src="Assets/App%20UI%20-%20Dashboard%20Design.jpg" alt="Kinetics dashboard design reference" width="92%">
      <sub><strong>DASHBOARD</strong> · DESIGN REFERENCE</sub>
    </td>
    <td align="center" width="50%">
      <img src="Assets/App%20UI%20-%20Login%20Page%20Design.jpg" alt="Kinetics login design reference" width="92%">
      <sub><strong>LOGIN</strong> · DESIGN REFERENCE</sub>
    </td>
  </tr>
</table>

## ◈ PROJECT DOCUMENTS

<p align="center">
  <a href="NORTH_STAR.md"><img src="https://img.shields.io/badge/◈_VISION-North_Star-800020?style=flat-square" alt="North Star"></a>
  <a href="ROADMAP.md"><img src="https://img.shields.io/badge/◈_PLAN-Roadmap-800020?style=flat-square" alt="Roadmap"></a>
  <a href="DECISIONS.md"><img src="https://img.shields.io/badge/◈_RECORD-Decisions-800020?style=flat-square" alt="Decisions"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/◈_CONTRIBUTE-Guide-800020?style=flat-square" alt="Contributing guide"></a>
  <a href="docs/README.md"><img src="https://img.shields.io/badge/◈_DOCS-Index-800020?style=flat-square" alt="Documentation index"></a>
  <a href="SECURITY.md"><img src="https://img.shields.io/badge/◈_SECURITY-Policy-800020?style=flat-square" alt="Security policy"></a>
</p>

## ◈ CONTRIBUTING

1. Read the [North Star](NORTH_STAR.md), [Roadmap](ROADMAP.md) and [Decision Log](DECISIONS.md).
2. Follow [CONTRIBUTING.md](CONTRIBUTING.md) and the active track's acceptance criteria.
3. Include tests, schemas, provenance and licensing evidence with substantive changes.
4. State exactly what was tested, what was not tested and what remains open.

## ◈ LICENSE

**Apache License 2.0.** See [LICENSE](LICENSE). Third-party dependencies, engines, datasets, models, fonts and artwork may carry separate terms.

---

<p align="center">
  <img src="Assets/Goal.png" alt="Illustration representing curiosity, exploration and scientific ambition" width="62%">
</p>

<p align="center">
  <strong>ASSAYFLUX SCIENTIFIC SYSTEMS</strong><br>
  <sub>BUILT FOR RESEARCH · GUIDED BY EVIDENCE</sub>
</p>
<p align="right">
  <img src="Assets/Author%27s%20Signature.svg" alt="Author signature" width="26%">
</p>
<p align="center">
  <sub>© ASSAYFLUX · KINETICS</sub>
</p>
