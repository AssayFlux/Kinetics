<!--
KINETICS README
LANGUAGE PERCENTAGES ARE INTENTIONALLY NOT FABRICATED; SEE THE SOURCE-STATISTICS TODO BELOW.
-->

<p align="center">
  <img src="assets/brand/readme-header.svg" alt="KINETICS — ASSAYFLUX animated colour header" width="100%">
</p>

<p align="center">
  <img src="assets/brand/organization-logo.gif" alt="ASSAYFLUX ORGANIZATION LOGO" width="200">
</p>

<p align="center">
  <img src="assets/brand/rainbow-helix.gif" alt="RAINBOW DNA DOUBLE HELIX" width="480">
</p>

<h1 align="center"><strong>KINETICS</strong></h1>
<p align="center">
  <strong>EXPLORE BIOLOGY. REPRODUCE THE WORK. KEEP THE EVIDENCE.</strong>
</p>
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=IBM+Plex+Mono&weight=500&size=16&pause=1200&color=38BDF8&center=true&vCenter=true&width=720&lines=Android-native+%C2%B7+Offline-first;Python+%C2%B7+Kotlin+%C2%B7+Rust+%C2%B7+C%2B%2B;Reproducible+workflows+%C2%B7+Explicit+provenance;Research-only+%C2%B7+Evidence-led" alt="Kinetics project tagline">
</p>

<p align="center">
  <a href="https://github.com/AssayFlux/Kinetics/blob/main/LICENSE"><img src="https://img.shields.io/github/license/AssayFlux/Kinetics?style=for-the-badge&label=license" alt="Apache 2.0 license"></a>
  <img src="https://img.shields.io/badge/version-0.0.0-lightgrey?style=for-the-badge" alt="Pre-release version 0.0.0">
  <a href="https://github.com/AssayFlux/Kinetics/stargazers"><img src="https://img.shields.io/github/stars/AssayFlux/Kinetics?style=for-the-badge" alt="GitHub stars"></a>
  <a href="https://github.com/AssayFlux/Kinetics/forks"><img src="https://img.shields.io/github/forks/AssayFlux/Kinetics?style=for-the-badge" alt="GitHub forks"></a>
  <a href="https://github.com/AssayFlux/Kinetics/issues"><img src="https://img.shields.io/github/issues/AssayFlux/Kinetics?style=for-the-badge" alt="Open issues"></a>
  <a href="https://github.com/AssayFlux/Kinetics/commits/main"><img src="https://img.shields.io/github/last-commit/AssayFlux/Kinetics?style=for-the-badge" alt="Last commit"></a>
  <a href="https://github.com/AssayFlux/Kinetics/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/AssayFlux/Kinetics/ci.yml?branch=main&style=for-the-badge&label=CI" alt="GitHub Actions CI"></a>
</p>

<p align="center">
  <strong>PRE-RELEASE · RESEARCH USE ONLY · NOT CLINICALLY VALIDATED</strong>
</p>

---

## **VISUAL PREVIEW**

<p align="center">
  <strong>APP DASHBOARD AND LOGIN — UI DESIGN REFERENCES</strong>
</p>

<table>
  <tr>
    <td align="center" width="50%">
      <img src="assets/design-previews/dashboard-reference.jpg" alt="Kinetics dashboard design reference" width="100%">
      <sub><strong>DASHBOARD CONCEPT</strong></sub>
    </td>
    <td align="center" width="50%">
      <img src="assets/design-previews/login-reference.jpg" alt="Kinetics login page design reference" width="100%">
      <sub><strong>LOGIN CONCEPT</strong></sub>
    </td>
  </tr>
</table>

<p align="center"><em><strong>THESE ARE EXISTING DESIGN-PREVIEW ASSETS, NOT VERIFIED CAPTURES OF A RUNNING OR PRODUCTION-READY APP. A REAL IN-APP WALKTHROUGH CAN BE ADDED AFTER DEVICE CAPTURE.</strong></em></p>

## **ABOUT KINETICS**

**KINETICS IS AN OPEN-SOURCE, MODULAR SCIENTIFIC RESEARCH WORKBENCH DESIGNED AROUND AN ANDROID-NATIVE, OFFLINE-FIRST EXPERIENCE. ITS REPOSITORY COMBINES SCIENTIFIC PYTHON MODULES, A KOTLIN/JETPACK COMPOSE ANDROID APPLICATION, SELECTED RUST AND C++ NATIVE COMPONENTS, VERSIONED DATA CONTRACTS, AND REPRODUCIBILITY AND GOVERNANCE TOOLING.**

**THE CODEBASE EXPLORES WORKFLOWS ACROSS GENOMICS, SEQUENCE ANALYSIS, STRUCTURAL BIOLOGY, COMPUTATIONAL CHEMISTRY, ENZYME KINETICS, OMICS AND RESEARCH-ORIENTED PHARMACOLOGY UTILITIES. A CAPABILITY REGISTRY CONNECTS TOOLS WITH ENGINES, DATA PACKS AND SCIENTIFIC DOMAINS. RESULTS ARE DESIGNED TO RETAIN INPUT HASHES, PARAMETERS, VERSIONS, UNITS AND OTHER PROVENANCE NEEDED TO INSPECT OR REPRODUCE AN ANALYSIS.**

**KINETICS IS AN EVOLVING ENGINEERING PROTOTYPE. SOURCE CODE, AUTOMATED TESTS, INDEPENDENT SCIENTIFIC VALIDATION, PHYSICAL-DEVICE VERIFICATION AND FORMAL ACCEPTANCE ARE TRACKED AS DISTINCT EVIDENCE STATES.**

### **WHY THIS PROJECT?**

- **RESEARCH WORKFLOWS THAT CAN TRAVEL: AN ANDROID-FIRST ARCHITECTURE WITH LOCAL/OFFLINE CONSTRAINTS AND A SEPARATELY GATED OPTIONAL COMPUTE WORKER.**
- **EVIDENCE, NOT JUST OUTPUT: VERSIONED SCHEMAS, EXPLICIT UNITS, PROVENANCE METADATA, REFERENCE COMPARISONS AND CONSERVATIVE FAILURE BOUNDARIES.**
- **A VISIBLE PATH TO TRUST: CAPABILITY AND GOVERNANCE REGISTERS DISTINGUISH IMPLEMENTATION FROM VALIDATION, LICENSING, DEVICE SUPPORT AND EXTERNAL APPROVAL.**

> **[!IMPORTANT]**
> **RESEARCH-ONLY BOUNDARY: KINETICS IS NOT A VALIDATED MEDICAL DEVICE OR CLINICAL DECISION-SUPPORT SYSTEM. P0 REMAINS BLOCKED / NOT APPROVED. PATIENT/CLINICAL DATA, IDENTIFIABLE HUMAN-SUBJECT ACTIVITY, INDIVIDUAL CLINICAL INTERPRETATION, DIAGNOSIS, TREATMENT OR DOSING RECOMMENDATIONS, AND CLINICAL MODE ARE NOT AUTHORIZED. DO NOT USE OUTPUTS FOR PATIENT CARE.**

## **WHAT EXISTS IN THE CODEBASE**

| **🧬 BIOLOGY & SEQUENCE** | **🧪 CHEMISTRY & QUANTITATIVE RESEARCH** |
|---|---|
| **FASTA/FASTQ PARSING, SEQUENCE STATISTICS, ALIGNMENT AND K-MER UTILITIES** | **MOLECULAR GRAPH AND SMILES/MOLBLOCK ANALYSIS THROUGH AN OPTIONAL RDKIT ADAPTER** |
| **SAM/BAM/VCF PARSING AND SMALL-VARIANT NORMALIZATION UTILITIES** | **AUTODOCK VINA DOCKING RUNNER FOR CALLER-PREPARED PDBQT INPUTS** |
| **ORF, GFF3, GENOME QC AND ANNOTATION HELPERS** | **OPENMM MOLECULAR-DYNAMICS RUNNER WITH EXPLICIT SETUP LIMITATIONS** |
| **HMMER/BLASTP/AUGUSTUS/PRODIGAL ADAPTERS AND EVIDENCE-ORIENTED WORKFLOWS** | **MICHAELIS–MENTEN MODELS, FITTING AND EXPLORATORY TRANSFORMS** |
| **PHYLOGENETIC DISTANCE, NEIGHBOUR JOINING, UPGMA AND NEWICK UTILITIES** | **PK/PD REFERENCE MODELS, OMICS STATISTICS AND SYNTHETIC COHORT UTILITIES** |
| **PGX/PHARMVAR PARSING AND SYNTHETIC/REFERENCE-BOUND GENOTYPE QC FOUNDATIONS** | **ADMET EVALUATION METRICS AND APPLICABILITY-DOMAIN UTILITIES; NO BUNDLED PREDICTIVE MODEL** |

| **🧩 PLATFORM & INTEGRATION** | **🔎 QUALITY & GOVERNANCE** |
|---|---|
| **KOTLIN + JETPACK COMPOSE ANDROID APP FOUNDATION** | **PYTEST SUITE AND GITHUB ACTIONS VALIDATION WORKFLOW** |
| **PYTHON PACKAGE UNDER `PYTHON/KINETICS/`** | **RUFF, MYPY AND PRE-COMMIT CONFIGURATION** |
| **RUST ANDROID ARM64 LIBRARY AND C++/JNI BUILD INTEGRATION** | **JSON SCHEMA CONTRACTS AND CAPABILITY REGISTRY CHECKS** |
| **OFFLINE STRUCTURE VIEWER IN HTML/CSS/JAVASCRIPT** | **SCIENTIFIC REFERENCE-COMPARISON AND ENGINE SMOKE WORKFLOWS** |
| **OPTIONAL NODE 22 RESEARCH DOCKING WORKER, DISABLED BY DEFAULT** | **SOURCE DEPENDENCY INVENTORY, THREAT MODEL, PRIVACY AND GOVERNANCE REGISTERS** |

**FEATURE NAMES DESCRIBE CODE PRESENT IN THE REPOSITORY, NOT A PROMISE THAT EVERY WORKFLOW IS COMPLETE, INDEPENDENTLY VALIDATED OR SUPPORTED ON EVERY DEVICE. SEE THE CAPABILITY REGISTRY, RESEARCH-READINESS AUDIT AND DOCUMENTATION INDEX.**

## **ENGINEERING PROGRESS**

**THE PERCENTAGES BELOW ARE THE REPOSITORY'S DOCUMENTED TRACK ENGINEERING-GATE STATUS, NOT A PERCENTAGE OF SCIENTIFIC VALIDITY, CLINICAL READINESS, RELEASE READINESS OR REGULATORY COMPLIANCE.**

<table>
  <thead>
    <tr><th align="left"><strong>TRACK</strong></th><th align="left"><strong>SCOPE</strong></th><th align="left"><strong>ENGINEERING GATE</strong></th><th align="left"><strong>EVIDENCE STILL OPEN</strong></th></tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>R</strong></td><td><strong>RESEARCH PLATFORM, ANDROID FOUNDATION, SCIENTIFIC PRIMITIVES</strong></td>
      <td><img src="https://img.shields.io/badge/100%25-software%20audit%20closed-238636?style=flat" alt="R software audit closed"></td>
      <td><strong>PHYSICAL-DEVICE, INDEPENDENT SCIENTIFIC, LICENSING AND RELEASE EVIDENCE</strong></td>
    </tr>
    <tr>
      <td><strong>S</strong></td><td><strong>STRUCTURE, SEQUENCE DISCOVERY, ANNOTATION AND PROTEIN INTELLIGENCE</strong></td>
      <td><img src="https://img.shields.io/badge/100%25-software%20scope%20closed-238636?style=flat" alt="S software scope closed"></td>
      <td><strong>INDEPENDENT REFERENCES, APPROVED RESOURCES/MODELS AND DEVICE EVIDENCE</strong></td>
    </tr>
    <tr>
      <td><strong>I</strong></td><td><strong>IN-SILICO CHEMISTRY, DOCKING, MD, ADMET AND PK/PD UTILITIES</strong></td>
      <td><img src="https://img.shields.io/badge/100%25-software%20audit%20closed-238636?style=flat" alt="I software audit closed"></td>
      <td><strong>REAL SCIENTIFIC BENCHMARKS, DATA/MODEL LICENCES, SECURE NODE AND DEVICE TESTS</strong></td>
    </tr>
    <tr>
      <td><strong>P</strong></td><td><strong>PGX-FIRST PRECISION-MEDICINE RESEARCH PREPARATION</strong></td>
      <td><img src="https://img.shields.io/badge/in%20progress-not%20accepted-yellow?style=flat" alt="P in progress"></td>
      <td><strong>P0 EXTERNAL DETERMINATIONS, INDEPENDENT EVIDENCE AND FORMAL OWNER GATE; P0 IS NOT APPROVED</strong></td>
    </tr>
    <tr>
      <td><strong>G</strong></td><td><strong>SECURITY, SUPPLY CHAIN, QUALITY, PRIVACY AND SCIENTIFIC/PUBLICATION INTEGRITY</strong></td>
      <td><img src="https://img.shields.io/badge/0%25%20accepted-gate%20open-red?style=flat" alt="G gate open"></td>
      <td><strong>EXACT-HEAD AUDIT, INDEPENDENT REVIEWS, ROLE APPOINTMENTS AND OPERATING EXERCISES</strong></td>
    </tr>
    <tr>
      <td><strong>U</strong></td><td><strong>DESIGN SYSTEM, ANDROID UX AND RESEARCH WORKFLOWS</strong></td>
      <td><img src="https://img.shields.io/badge/0%25%20accepted-gate%20not%20started-red?style=flat" alt="U gate not started"></td>
      <td><strong>FURTHER SEQUENTIAL IMPLEMENTATION FOLLOWS G; PRIOR U0–U3 WORK REMAINS PARTIAL BASELINE</strong></td>
    </tr>
  </tbody>
</table>

<sub><strong>ESTIMATE METHOD: VALUES REPRODUCE THE TRACK-LEVEL ENGINEERING-GATE STATEMENTS IN THE CURRENT PROJECT STATUS DOCUMENTATION AND D-023. “100%” MEANS THAT TRACK'S DOCUMENTED SOFTWARE IMPLEMENTATION/AUDIT GATE WAS CLOSED; “0% ACCEPTED” MEANS THE FORMAL TRACK EXIT GATE HAS NOT BEEN ACCEPTED, NOT THAT NO SOURCE EXISTS. P IS DELIBERATELY NOT ASSIGNED A MADE-UP PERCENTAGE.</strong></sub>

## **CURRENT PROJECT STATUS**

<p align="center">
  <a href="https://github.com/AssayFlux/Kinetics/actions/workflows/ci.yml"><img src="https://img.shields.io/badge/Build-GitHub%20Actions%20configured-238636?style=for-the-badge" alt="Build configured"></a>
  <a href="https://github.com/AssayFlux/Kinetics/tree/main/tests"><img src="https://img.shields.io/badge/Tests-62%20test%20modules-2563EB?style=for-the-badge" alt="62 test modules"></a>
  <img src="https://img.shields.io/badge/Release-pre--release-lightgrey?style=for-the-badge" alt="Pre-release">
  <img src="https://img.shields.io/badge/Clinical%20use-not%20approved-red?style=for-the-badge" alt="Clinical use not approved">
</p>

- **BUILD / CI: GITHUB ACTIONS VALIDATION IS CONFIGURED; USE THE LIVE WORKFLOW BADGE ABOVE FOR CURRENT STATUS.**
- **TESTS: 62 PYTHON TEST MODULES ARE PRESENT. THE CI WORKFLOW ALSO DEFINES ANDROID JVM TESTS, SCIENTIFIC REFERENCE COMPARISONS, NATIVE-ENGINE SMOKE CHECKS AND NODE WORKER SECURITY TESTS.**
- **COVERAGE: NO VERIFIED COVERAGE PERCENTAGE IS PUBLISHED; NONE IS CLAIMED HERE.**
- **DEPLOYMENT: NO PRODUCTION DEPLOYMENT IS CLAIMED. ANDROID CI ARTIFACTS ARE DEBUG APK/AAB OUTPUTS.**
- **MAINTENANCE: THE REPOSITORY IS ACTIVELY CHANGING; SEE RECENT COMMITS.**
- **CONTRIBUTIONS: READ CONTRIBUTING.MD AND THE ACTIVE ROADMAP BEFORE PROPOSING WORK. THE REPOSITORY DOES NOT DECLARE AN UNCONDITIONAL PR ACCEPTANCE POLICY.**

## **TECHNOLOGY**

<p align="center">
  <a href="https://skillicons.dev/icons?i=python,kotlin,cpp,rust,js,html,css,bash,cmake,gradle,githubactions"><img src="https://skillicons.dev/icons?i=python,kotlin,cpp,rust,js,html,css,bash,cmake,gradle,githubactions" alt="Python, Kotlin, C++, Rust, JavaScript, HTML, CSS, Bash, CMake, Gradle and GitHub Actions"></a>
</p>

| **LAYER** | **TECHNOLOGIES IN REPOSITORY** |
|---|---|
| **ANDROID** | **KOTLIN, JETPACK COMPOSE, ANDROIDX, GRADLE, CHAQUOPY** |
| **SCIENTIFIC CORE** | **PYTHON 3.10+, NUMPY; OPTIONAL BIOPYTHON, RDKIT, AUTODOCK VINA AND OPENMM** |
| **NATIVE** | **C++17, JNI/NDK, RUST 1.88 TOOLCHAIN** |
| **VISUALISATION** | **HTML5, CSS, JAVASCRIPT, ANDROID WEBVIEW** |
| **CONTRACTS & METADATA** | **JSON SCHEMA, YAML, SPDX SOURCE INVENTORY** |
| **QUALITY** | **PYTEST, RUFF, MYPY, PRE-COMMIT, GITHUB ACTIONS** |
| **OPTIONAL WORKER** | **NODE.JS 22, DEPENDENCY-FREE HTTP/TLS SERVICE** |

**THE ROOT PACKAGE METADATA IS IN PYPROJECT.TOML. OPTIONAL EXTRAS ARE DECLARED THERE; VALIDATION-ONLY PINNED DEPENDENCY SETS LIVE UNDER `validation/`. THIRD-PARTY ENGINES, MODELS, DATASETS, FONTS AND ARTWORK MAY CARRY SEPARATE TERMS.**

<details>
  <summary><strong>SOURCE-LANGUAGE MIX AND REPOSITORY STATISTICS</strong></summary>

  - **A DATED REPOSITORY AUDIT RECORDS 356 TRACKED FILES ACROSS 55 NON-ROOT DIRECTORIES AT ITS AUDITED REVISION.**
  - **THE CURRENT `tests/` DIRECTORY CONTAINS 62 TEST MODULES.**
  - **PYTHON IS THE PRIMARY SCIENTIFIC IMPLEMENTATION LANGUAGE. KOTLIN, C++17 AND RUST ARE USED IN THE ANDROID/NATIVE STACK; JAVASCRIPT, HTML AND CSS SUPPORT THE OFFLINE VIEWER; BASH/YAML SUPPORT BUILD AND CI AUTOMATION.**
  - **TODO — EXACT LANGUAGE LINE-COUNT PERCENTAGES: PUBLISH A REPRODUCIBLE SOURCE-ONLY LOC REPORT (FOR EXAMPLE, GITHUB LINGUIST OR CLOC OUTPUT), EXCLUDING GENERATED ASSETS, LOCKFILES, VENDORED MATERIAL AND DOCUMENTATION. PERCENTAGES ARE INTENTIONALLY OMITTED RATHER THAN GUESSED.**
  - **NO ROOT `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `.env.example`, DOCKERFILE OR COMPOSE FILE IS PRESENT. NODE PACKAGE METADATA IS ISOLATED IN `remote-node/package.json`; RUST METADATA IS UNDER `android/native-rust/Cargo.toml`.**
  - **THE OPTIONAL NODE WORKER DOCUMENTS TWO HTTP ROUTES: `GET /health` AND `POST /v1/docking`.**
</details>

## **QUICK START**

### **1. PYTHON DEVELOPMENT ENVIRONMENT**

<details>
  <summary><strong>INSTALL THE DEVELOPMENT DEPENDENCIES</strong></summary>

**  PYTHON 3.10 OR NEWER IS DECLARED BY THE PACKAGE METADATA. THE CI WORKFLOW CURRENTLY USES PYTHON 3.11.**

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip
  python -m pip install -r requirements-dev.txt
  python -m pip install -e .
  ```

**  WINDOWS POWERSHELL ACTIVATION:**

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

**  THE BASE PROJECT DECLARES NO MANDATORY PYTHON RUNTIME DEPENDENCIES. OPTIONAL ENGINE EXTRAS ARE SEPARATE:**

  ```bash
  python -m pip install -e ".[docking]"
  python -m pip install -e ".[md]"
  ```

**  THESE EXTRAS INSTALL PINNED AUTODOCK VINA OR OPENMM DEPENDENCIES; THEY DO NOT SUPPLY RECEPTOR/LIGAND PREPARATION, FORCE FIELDS, DATASETS OR INDEPENDENT SCIENTIFIC VALIDATION.**
</details>

### **2. RUN TESTS AND REPOSITORY CHECKS**

<details>
  <summary><strong>RUN THE PYTHON TEST SUITE</strong></summary>

  ```bash
  pytest
  ```

**  RUN THE REPOSITORY'S REPRODUCTION ENTRY POINT:**

  ```bash
  scripts/reproduce-all
  ```

**  RUN THE CONFIGURED STATIC CHECKS:**

  ```bash
  ruff check scripts tests
  mypy scripts python/kinetics
  python scripts/check_registry.py
  python scripts/check_governance.py
  ```

**  CI RUNS ADDITIONAL CATALOGUE, GENERATED-FILE, SCIENTIFIC-REFERENCE, ENGINE-SMOKE AND ANDROID CHECKS. SEE THE WORKFLOW DEFINITION.**
</details>

### **3. BUILD THE ANDROID DEBUG ARTIFACTS**

<details>
  <summary><strong>LINUX X86_64 / X86_64 WSL2 BUILD PREREQUISITES</strong></summary>

**  THE CHECKED-IN BUILD SCRIPT REQUIRES JDK 17, PYTHON 3.11.18, RUST/CARGO AND RUSTUP, ANDROID SDK PLATFORM 36, ANDROID NDK 28.2.13676358, BUILD TOOLS 36.0.0, CMAKE 3.22.1, `patchelf`, `patch`, GIT, CURL AND STANDARD SHELL UTILITIES. THE SCRIPT DOWNLOADS A CHECKSUM-PINNED GRADLE 8.13 DISTRIBUTION.**

**  SET `ANDROID_HOME` OR `ANDROID_SDK_ROOT` TO THE INSTALLED SDK LOCATION, THEN RUN FROM THE REPOSITORY ROOT:**

  ```bash
  chmod +x scripts/build_android_local.sh
  scripts/build_android_local.sh
  ```

**  OUTPUTS ARE A DEBUG APK AND DEBUG AAB UNDER `android/app/build/outputs/`. THE SCRIPT EXPLICITLY DOES NOT RUN AN EMULATOR OR PHYSICAL-DEVICE TEST. TERMUX/ANDROID ITSELF IS NOT A SUPPORTED BUILD HOST FOR THIS PINNED TOOLCHAIN.**

**  SEE LOCAL ANDROID BUILD NOTES.**
</details>

### **4. OPTIONAL PRIVATE RESEARCH NODE**

<details>
  <summary><strong>RUN THE DEPENDENCY-FREE NODE 22 WORKER TESTS</strong></summary>

**  THE WORKER IS DISABLED FOR DOCKING BY DEFAULT AND IS NOT A PRODUCTION DEPLOYMENT.**

  ```bash
  cd remote-node
  npm test
  ```

**  FOR ITS INSTALL/RUN PROCEDURE, REQUIRED ENVIRONMENT VARIABLES, TLS BOUNDARY AND SECURITY LIMITATIONS, FOLLOW REMOTE-NODE/README.MD. DO NOT COMMIT TOKENS, CERTIFICATES OR PRIVATE KEYS.**
</details>

### **ENVIRONMENT CONFIGURATION**

**THERE IS NO ROOT `.env.example` AND THE PYTHON DEVELOPMENT WORKFLOW DOES NOT REQUIRE A PROJECT-WIDE ENVIRONMENT FILE. THE OPTIONAL RESEARCH NODE USES THE ENVIRONMENT VARIABLES DOCUMENTED IN ITS OWN README. CONFIGURE SECRETS THROUGH THE HOST ENVIRONMENT OR SECRET MANAGER; NEVER ADD THEM TO GIT.**

## **REPOSITORY STRUCTURE**

```text
Kinetics/
├── android/             # Kotlin app, Compose design system, JNI, Rust and embedded Python
├── api/                 # Versioned API and cross-component JSON Schemas
├── assets/              # Brand assets and design references
├── benchmarks/          # Benchmark protocols and fixtures
├── capabilities/        # Capability registry and status metadata
├── cpp/                 # Native C++ implementation and build integration
├── data/                # Source catalogues and metadata
├── datapacks/           # Data-pack manifests / planned pack content
├── design/              # Design tokens and generated design inputs
├── docs/                # Architecture, track plans, audits and UI specifications
├── domains/             # Scientific domain metadata
├── engines/             # Engine metadata and integration points
├── governance/           # Governance and assurance registers
├── paper/               # Manuscript planning and claim-evidence ledger
├── python/kinetics/     # Scientific Python package
├── remote-node/         # Optional, disabled-by-default Node docking worker
├── rust/                # Rust source and integration area
├── schemas/             # Reusable domain/data schemas
├── scripts/             # Build, generation, validation and inventory scripts
├── sbom/                # Software bill-of-materials materials
├── tests/               # Python regression and contract tests
├── validation/          # Pinned independent-reference and engine smoke checks
├── web/viewers/         # Offline HTML/CSS/JavaScript structure viewer
├── .github/workflows/   # GitHub Actions CI
├── pyproject.toml       # Python package metadata and tool configuration
├── requirements-dev.txt # Python development dependencies
├── ROADMAP.md           # Canonical track plan
├── DECISIONS.md         # Owner decisions and supersession history
├── NORTH_STAR.md        # Mission, product boundaries and direction
└── LICENSE              # Apache License 2.0
```

**SOME DIRECTORIES INTENTIONALLY CONTAIN METADATA, PLACEHOLDERS OR PLANNED EXTENSION POINTS. THEIR PRESENCE DOES NOT MEAN A COMPLETE ENGINE OR PRODUCT FEATURE IS DELIVERED. FOR THE CANONICAL NAVIGATION MAP, SEE DOCS/README.MD.**

## **ROADMAP**

**THE OWNER-APPROVED EXECUTION ORDER IS R → S → I → P → G → U (DECISION D-023). TRACK SEQUENCING AND GATE REQUIREMENTS ARE DEFINED IN ROADMAP.MD.**

- [x] **R — RESEARCH PLATFORM SOFTWARE AUDIT RECORDED CLOSED.**
- [x] **S — STRUCTURE, SEQUENCE AND DISCOVERY SOFTWARE SCOPE RECORDED CLOSED.**
- [x] **I — IN-SILICO LABORATORY SOFTWARE AUDIT RECORDED CLOSED.**
- [ ] **P — COMPLETE THE PERMITTED RESEARCH-ONLY ENGINEERING BASE; P0 EXTERNAL EVIDENCE AND FORMAL APPROVAL REMAIN BLOCKED.**
- [ ] **G — COMPLETE G0–G7 ENGINEERING AUDIT, EXACT-HEAD VERIFICATION, INDEPENDENT REVIEWS AND OPERATING EXERCISES.**
- [ ] **U — RESUME SEQUENTIAL UI IMPLEMENTATION AFTER G'S GATE IS ASSESSED; AUDIT AND VERIFY ON TARGET DEVICES.**
- [ ] **PUBLISH REPRODUCIBLE, CAPABILITY-LEVEL SCIENTIFIC REFERENCE AND BENCHMARK EVIDENCE.**
- [ ] **COMPLETE DATA/MODEL/DEPENDENCY LICENSING DECISIONS AND RELEASE-GRADE SBOM COVERAGE.**
- [ ] **COMPLETE PHYSICAL ANDROID DEVICE, OFFLINE-MODE, ACCESSIBILITY AND RECOVERY VERIFICATION.**
- [ ] **ADD A REAL APPLICATION DEMO CAPTURE AND VERIFY THE HTML DNA LOADER INTEGRATION ON TARGET DEVICES.**

**SEE THE FULL ROADMAP, CURRENT G AUDIT AND P IMPLEMENTATION PLAN FOR DETAILS.**

## **CONTRIBUTING**

**CONTRIBUTIONS SHOULD FOLLOW THE CURRENT ROADMAP, OWNER DECISIONS, INTEGRATION STANDARD AND EVIDENCE GATES.**

1. **READ NORTH_STAR.MD, ROADMAP.MD AND DECISIONS.MD.**
2. **READ CONTRIBUTING.MD AND DOCS/ENGINEERING_INTEGRATION_STANDARD.MD.**
3. **WORK ONLY ON AN ACTIVE, PERMITTED ITEM; PRESERVE TRACK ORDER R → S → I → P → G → U.**
4. **ADD OR UPDATE TESTS, SCHEMAS, PROVENANCE AND LICENSING EVIDENCE ALONGSIDE IMPLEMENTATION.**
5. **REPORT CHECKS RUN, CHECKS NOT RUN, LIMITATIONS AND THE NEXT STEP. NEVER CLAIM SCIENTIFIC VALIDATION OR DEVICE SUPPORT WITHOUT ITS EVIDENCE.**

## **LICENSE**

**KINETICS PROJECT CODE IS DISTRIBUTED UNDER THE APACHE LICENSE 2.0. THIRD-PARTY DEPENDENCIES, ENGINES, DATASETS, MODELS, FONTS AND VISUAL ASSETS MAY HAVE SEPARATE LICENCES AND REDISTRIBUTION CONDITIONS. REVIEW THE RELEVANT UPSTREAM TERMS BEFORE BUNDLING OR REDISTRIBUTING THEM.**

## **CONTACT**

- **REPOSITORY: GITHUB.COM/ASSAYFLUX/KINETICS**
- **MAINTAINER / PROJECT OWNER: ASSAYFLUX**
- **ISSUES AND QUESTIONS: GITHUB ISSUES**
- **PROJECT DOCUMENTATION: DOCS/README.MD**

---

<p align="center">
  <img src="assets/brand/owner-signature.svg" alt="MD SAFARUJJAMAN — PROJECT OWNER SIGNATURE OVER KINETICS BACKGROUND" width="100%">
  <br>
  <sub><strong>BUILD CAREFULLY. MEASURE HONESTLY. SHARE REPRODUCIBLY.</strong></sub>
</p>
