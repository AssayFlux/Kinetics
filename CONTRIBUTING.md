# Contributing

Kinetics is governed by NORTH_STAR.md, ROADMAP.md and DECISIONS.md. Read those files and the current phase plan before proposing work.

## Rules
- Follow [the Engineering & Integration Standard](docs/ENGINEERING_INTEGRATION_STANDARD.md) before every substantial change: identify components, call direction, transport, versioned contract, boundary risks and matching implementation/tests.
- Use `api/engine-envelope-v1.schema.json` as the semantic contract for cross-component engine messages; do not silently fork field definitions.
- Every engineering update must include a **Check** section and a **Next step**.
- Work only on an active roadmap item; respect every owner approval gate.
- Preserve the five-track scope and approved language plan. Do not add languages, engines, datasets, models, dependencies or engine tiers without review and approval.
- Never claim a capability is implemented, validated or device-verified without committed evidence.
- Do not add real patient data, secrets, binaries or bulk document collections.
- Do not select or change the project license.
- Keep changes small, typed, tested and reproducible. Record provenance and upstream licenses.
- Scientific outputs must state uncertainty, limitations and research-use status.
- Stop at phase exit gates and report evidence and blockers.

The repository owner controls integration to main. No branch or release policy is implied by this document.
