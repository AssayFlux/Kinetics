# Kinetics Research Workbench

> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

The optional workbench provides a local-first researcher interface over the existing Python scientific workflows. It is a browser-based desktop experience bound to loopback; scientific functions remain independently usable from the CLI.

## Install and start

From a clean environment with the repository checked out:

```bash
python -m pip install -e ".[dev,workbench]"
kinetics-workbench
```

Open [http://127.0.0.1:8765](http://127.0.0.1:8765). The service binds only to `127.0.0.1`; it is not a public or multi-user deployment. Stop it with Ctrl+C.

Optional paths:

```bash
kinetics-workbench --port 8765 --workspace "$HOME/kinetics-workspace" \
  --database "$HOME/.kinetics/kinetics.sqlite3"
```

Equivalent environment variables are `KINETICS_WORKSPACE` and `KINETICS_DATABASE`. The workbench uses the same versioned SQLite metadata store as the Python research tools. Schema migration from version 1 to 2 is additive and preserves existing tables and records.

## Researcher workflow

1. Create a project. The workbench creates project-scoped `datasets/`, `runs/`, `artifacts/`, `reports/`, and `logs/` directories.
2. Upload a source table to the project. Uploads are limited to 500 MiB, cannot overwrite an existing filename, are atomically written, and receive a SHA-256 checksum. The source license and access conditions remain the researcher's responsibility.
3. Select a task from the allow-listed workflow actions and supply a JSON parameter object. All file paths must be relative to the active project; absolute paths and parent-directory traversal are rejected. Output paths must be new.
4. Queue the task. The bounded worker runs the existing `kinetics-research` command using an argument vector (never a shell command). The job state and log are persisted; active work can be cancelled.
5. Inspect the result, job log and registered output artifacts. Downloads re-check the artifact SHA-256 before serving bytes.
6. Generate a Markdown experiment report. The report captures the input/output file hashes, command configuration, software environment, package versions and available result metrics. Missing metrics remain explicitly "not reported"; report generation is not independent scientific validation.

## Supported workbench actions

- `import-legacy`: convert legacy paired-target CSV rows into canonical observations with explicit source record IDs and units.
- `audit`: non-destructive source-record duplicate and quality audit.
- `persist`: validate and persist canonical observations into the shared SQLite dataset registry.
- `release` / `verify-release`: create and verify immutable, checksum-backed dataset releases.
- `normalize-identities`: validate protein sequence and canonicalize substrate identity.
- `annotate-scaffolds`: add chemical scaffold group IDs and rejected-row audit.
- `cluster-sequences`: run MMseqs2 and map cluster assignments back to observations.
- `build-features`: generate pinned ESM-2, Morgan and molecular graph features.
- `partition`: create protein/scaffold-aware target partitions.
- `compare`: compare classical baseline regressors.
- `fit`: fit the target-specific model and optional conformal calibration.
- `fit-multi`: fit the multimodal feature-fusion model.
- `predict-multi`: infer using a trusted model bundle.

For example, after uploading `observations.csv`, select **Quality audit** and use:

```json
{
  "input": "datasets/observations.csv",
  "output_dir": "runs/audit-001"
}
```

A feature-building task expects a canonical observations file with valid sequence and chemical identities and the required optional scientific dependencies installed. ESM-2 weights are pinned in the scientific pipeline; the workbench does not silently substitute a different model or invent missing assay metadata.

## Data and security boundaries

- Workbench binds to loopback and does not configure remote authentication. Do not expose it through a reverse proxy, tunnel, LAN interface or public address.
- No arbitrary shell, executable, Python expression or user-supplied environment variable is accepted.
- Jobs run as the local OS user. Do not open untrusted project files or run this local service with elevated privileges.
- Uploaded files are stored inside the active project. Filenames are reduced to a basename, hidden names and path separators are rejected, and upload size is bounded.
- Job inputs and outputs are project-relative and resolved after symlink normalization. Symlink escapes are rejected.
- Artifact downloads are project-scoped and hash-verified.
- A single local worker is the default to avoid competing heavy model loads. This is not a distributed queue or multi-tenant service.
- The metadata database contains dataset records, paths, job parameters, checksums, experiment metrics and scientific provenance. Protect the workspace and database with OS-level access controls and encrypted backups as appropriate.
- Dataset upload does not grant data rights. Review license, gate, privacy and retention conditions before use.

## Accessibility and usability notes

The initial interface uses semantic headings, labels, tables, native form controls, keyboard-visible focus, a live status region, responsive layouts and system light/dark color preferences. It avoids canvas-only interaction and uses text-based logs and tables for assistive technology compatibility. These are implementation checks, not a substitute for testing with keyboard-only navigation, screen readers, zoom and actual researchers.

## Current limitations and acceptance gates

This increment delivers the software workbench foundation and an integration test that uploads a canonical fixture, queues a real audit command, verifies output hashes, downloads an artifact and creates a report. It does not claim completed researcher user-acceptance testing.

Before Step 8 can be declared fully complete:

- Run usability sessions with researchers and record task completion, accessibility findings and revisions.
- Exercise the full curation → partition → features → model comparison/training → inference → report flow on a reviewed, licensed real dataset. This remains blocked by the CatPred gated download and source-level scientific audit documented in the Step 2 status.
- Run representative ESM-2 and MMseqs2 workloads on supported hardware; record runtime, memory, cancellation and recovery.
- Validate installation from a built wheel on supported desktop environments and document upgrade/rollback.
- Add remote multi-user authentication and per-tenant authorization only as a separately reviewed deployment profile; the current local workbench intentionally does not expose network access.
- Verify result/uncertainty fields against the scientific model output schema and ensure reports preserve calibration and applicability limitations.

Do not interpret a successful job or report as evidence of model validity, clinical readiness or suitability for treatment decisions.
