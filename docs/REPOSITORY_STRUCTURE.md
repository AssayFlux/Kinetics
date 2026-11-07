# Repository structure

> This is the repository-wide directory map. It describes the current tracked layout, not the full long-term architecture. For the subsystem-specific ingestion map, see [KNOWLEDGE_INGESTION_STRUCTURE.md](KNOWLEDGE_INGESTION_STRUCTURE.md).

```text
Kinetics/
├── .github/workflows/       # CI, data acquisition, SQLite and native structure checks
├── Assets/                  # Original brand assets and responsive HTML/CSS UI layouts
├── database/
│   ├── domains/             # Canonical extension scopes
│   ├── seed/                # Seed-data instructions
│   ├── sources/             # Public source and licensing registries
│   └── sqlite/              # Initial schema and numbered migrations
├── data/                    # Local-only research data; never commit private/raw corpora
├── deploy/aws/              # Candidate AWS infrastructure (Terraform)
├── docs/
│   ├── api/                 # OpenAPI contracts
│   ├── ...                  # Mission, architecture, research, acceptance and user docs
│   ├── DOCUMENTATION_INDEX.md
│   ├── DOCUMENTATION_GOVERNANCE.md
│   ├── REPOSITORY_STRUCTURE.md
│   └── IMPLEMENTATION_STATUS.md
├── models/                  # Local model/artifact workspace placeholder
├── native/                  # C++17 molecular scene/parser core and CTest fixtures
├── rust/kinetics-infra/     # Rust service, worker, storage and API foundations
├── scripts/
│   ├── data/                # Dataset acquisition and SQLite validation utilities
│   └── ...                  # Knowledge ingestion, restore and verification scripts
├── src/
│   ├── kinetics_core/       # Installable Python research package
│   │   ├── knowledge/       # Source-grounded local retrieval API/CLI
│   │   ├── storage/         # SQLite persistence
│   │   └── workbench/       # Local-first FastAPI application and static UI
│   └── ...                  # Compatibility and research entry-point modules
├── tests/                   # Python unit, integration, UI and browser tests
├── ARCHITECTURE.md          # Platform architecture
├── KINETICS_MISSION.md      # Authoritative project mission
├── ROADMAP.md               # Long-term programme roadmap
├── VISION.md                # Long-term vision
├── README.md                # Public project overview and getting started
└── pyproject.toml           # Python package, extras, CLI entry points and tooling
```

## Directory ownership

| Path | Owns | Does not imply |
|---|---|---|
| `.github/workflows/` | Automated checks and scheduled/manual workflow definitions | That a workflow has run or succeeded |
| `Assets/` | Brand identity and static UI layout prototypes | Native Windows/macOS/Linux applications or an Android APK |
| `database/` | Versioned schemas, domain scopes and source metadata | That all registered sources have been downloaded |
| `data/` | Local datasets, indexes, manifests and runtime databases | Permission to commit private or restricted material |
| `deploy/aws/` | Infrastructure-as-code candidate | A deployed or security-reviewed production environment |
| `docs/` | Mission, design, research, operations, acceptance and status documents | Implementation merely because a capability is specified |
| `native/` | C++ molecular parsing and scene-data implementation | Full GPU visualization or executed molecular dynamics |
| `rust/kinetics-infra/` | Rust infrastructure services and runtime | Registered scientific task execution or production deployment |
| `scripts/` | Explicit data acquisition, transformation, restore and audit commands | Implicit network access during package import |
| `src/kinetics_core/` | Reusable Python scientific and platform modules | A completed implementation of every catalogued domain |
| `tests/` | Automated fixture and integration coverage | Independent biological, clinical or production validation |

## Layout maintenance rules

1. Keep the mission and roadmap at the repository root; keep subsystem-specific structure maps under `docs/`.
2. Place new scientific modules under `src/kinetics_core/` with domain-owned contracts and tests.
3. Keep external source adapters separate from normalized scientific models.
4. Store schema changes as ordered migrations and test fresh and upgrade paths.
5. Keep large datasets, model weights, generated indexes and sensitive data outside Git unless an explicit license/security review approves a small artifact.
6. Add every maintained document to [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md).
7. Update this map when a top-level directory or major ownership boundary changes.
