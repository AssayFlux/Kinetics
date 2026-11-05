# Astronaut assistant integration

## Decision and current boundary

Kinetics will expose a small, dependency-free assistant interface. The intended
assistant runtime is the separate **AssayFlux/Astronaut** project, which is still
under development. Kinetics does not clone, modify, vendor, or depend on
Astronaut yet. Integration begins only after the project owner confirms that
Astronaut is ready.

The initial contract lives in `src/kinetics_core/assistant.py`:

- `AssistantBackend`: protocol implemented by a local runtime adapter.
- `AssistantRequest`: bounded conversation plus explicit project context.
- `AssistantResponse`: generated content and backend/model/offline provenance.
- `KineticsAssistant`: research-aware facade that forwards requests to the
  injected backend.

No model weights, hosted API, network client, or additional runtime dependency
is introduced. Importing Kinetics must not trigger model downloads.

## Integration contract for Astronaut

When Astronaut is ready, implement an adapter whose `generate(request)`
method returns `AssistantResponse`. The adapter should:

1. Load only locally available model/runtime assets.
2. report `offline=True` only when generation does not require network access;
3. preserve backend and model identifiers in every response;
4. enforce context-window limits and reject malformed requests;
5. avoid exposing filesystem, shell, GitHub, or network tools to the model by
   default;
6. require explicit application-level authorization for any future tool use;
7. keep user data and research datasets local unless the user explicitly
   authorizes another destination.

The Kinetics facade does not execute generated code, mutate research data, or
perform repository operations. Any future action-taking layer must be separate,
auditable, permission-scoped, and covered by tests before activation.

## Research-assistant behavior

The system prompt establishes baseline scientific safeguards:

- distinguish experimental measurements from computational predictions;
- do not fabricate citations, provenance, metrics, or completed experiments;
- keep Km and kcat observations separate unless source evidence links them;
- surface uncertainty, missing assay context, and applicability limitations;
- never equate passing software tests with scientific validation.

These are behavioral instructions, not a substitute for output review or
scientific verification.

## Planned integration sequence

1. **Now:** maintain the adapter contract and document the security boundary.
2. **Owner readiness signal:** inspect the Astronaut repository and its actual
   local inference API; do not assume its runtime, model format, or capabilities.
3. Implement a thin adapter in a separate integration module.
4. Add offline smoke tests, malformed-input tests, and provenance checks during
   the final verification stage.
5. Evaluate assistant answers against a curated set of Kinetics research tasks.
6. Only then expose the assistant in a user-facing CLI or application.

## Explicit non-goals before Astronaut is ready

- No hosted LLM dependency or cloud fallback.
- No silent telemetry or network access.
- No autonomous shell, filesystem, dataset, or GitHub modifications.
- No changes to the Astronaut repository.
- No claim that an AI assistant is already operational.

The integration is currently an interface and plan, not a connected assistant.
