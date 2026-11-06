"""Local-first Kinetics research workbench API and bounded job runner."""

from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import subprocess
import sys
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlsplit

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from ..storage import KineticsSQLite

_ALLOWED_COMMANDS = {
    "audit",
    "import-legacy",
    "persist",
    "release",
    "verify-release",
    "normalize-identities",
    "annotate-scaffolds",
    "cluster-sequences",
    "build-features",
    "partition",
    "compare",
    "fit",
    "fit-multi",
    "predict-multi",
}
_JOB_TIMEOUT_SECONDS = 24 * 60 * 60
_MAX_ARTIFACTS_PER_JOB = 2000


class ProjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=80)
    description: str = Field(default="", max_length=1000)


class JobCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    command: Literal[
        "audit",
        "import-legacy",
        "persist",
        "release",
        "verify-release",
        "normalize-identities",
        "annotate-scaffolds",
        "cluster-sequences",
        "build-features",
        "partition",
        "compare",
        "fit",
        "fit-multi",
        "predict-multi",
    ]
    parameters: dict[str, Any] = Field(default_factory=dict)


def _project_path(root: Path, value: Any, *, must_exist: bool, kind: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{kind} must be a non-empty project-relative path")
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"{kind} must stay inside the project workspace")
    resolved = (root / candidate).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"{kind} resolves outside the project workspace")
    if must_exist:
        exists = resolved.is_dir() if kind in {"output_dir", "release_dir"} else resolved.is_file()
        if not exists:
            raise FileNotFoundError(f"{kind} does not exist: {value}")
    if not must_exist and resolved.exists() and kind in {"output", "output_dir"}:
        raise FileExistsError(f"{kind} already exists: {value}")
    return resolved


def build_cli_arguments(command: str, parameters: dict[str, Any], root: Path) -> list[str]:
    """Validate a fixed research command and translate it to CLI arguments.

    This is intentionally an allow-list. The workbench never accepts a shell
    command, Python expression, executable path, or arbitrary environment map.
    """
    if command not in _ALLOWED_COMMANDS:
        raise ValueError("Unsupported workbench command")

    schemas: dict[str, tuple[set[str], set[str], set[str]]] = {
        "audit": ({"input", "output_dir"}, {"log10_tolerance"}, {"input", "output_dir"}),
        "import-legacy": (
            {"input", "output", "source", "source_record_id_column"},
            {"km_unit", "kcat_unit", "source_version", "license_id",
             "sequence_column", "smiles_column", "overwrite"},
            {"input", "output"},
        ),
        "persist": (
            {"input", "dataset_id", "name", "source"},
            {"version", "license_id", "citation"},
            {"input"},
        ),
        "release": (
            {"observations", "rejected", "output_dir", "dataset_id", "dataset_name",
             "source", "source_version", "license_id", "citation"},
            {"source_url", "source_manifest"},
            {"observations", "output_dir"},
        ),
        "verify-release": (
            {"release_dir"},
            set(),
            {"release_dir"},
        ),
        "normalize-identities": (
            {"input", "output_dir"},
            {"sequence_column", "smiles_column"},
            {"input", "output_dir"},
        ),
        "annotate-scaffolds": (
            {"input", "output_dir"},
            {"smiles_column"},
            {"input", "output_dir"},
        ),
        "cluster-sequences": (
            {"input", "output_dir"},
            {"sequence_column", "record_id_column", "source_column",
             "min_sequence_identity", "coverage", "threads"},
            {"input", "output_dir"},
        ),
        "build-features": (
            {"input", "output", "target"},
            {"cache_dir", "model_name", "model_revision", "tokenizer_revision",
             "device", "max_residues", "radius", "n_bits", "no_chirality",
             "batch_size", "group_column", "overwrite"},
            {"input", "output", "cache_dir"},
        ),
        "partition": (
            {"observations", "output_dir", "target"},
            {"protein_group_column", "substrate_group_column", "test_fraction",
             "calibration_fraction", "random_state"},
            {"observations", "output_dir"},
        ),
        "compare": (
            {"train", "test", "target", "output_dir"},
            {"group_array", "holdout_group_array", "random_state", "n_splits"},
            {"train", "test", "output_dir"},
        ),
        "fit": (
            {"train", "test", "target", "output_dir"},
            {"group_array", "holdout_group_array", "random_state", "n_splits",
             "calibration_archive", "conformal_alpha", "n_estimators", "max_depth"},
            {"train", "test", "output_dir", "calibration_archive"},
        ),
        "fit-multi": (
            {"train", "test", "target", "output_dir"},
            {"calibration_archive", "group_array", "holdout_group_array",
             "random_state", "n_splits", "hidden_layers", "alpha", "max_iter",
             "conformal_alpha", "git_revision"},
            {"train", "test", "output_dir", "calibration_archive"},
        ),
        "predict-multi": (
            {"model", "features", "output"},
            set(),
            {"model", "features", "output"},
        ),
    }
    required, optional, path_fields = schemas[command]
    supplied = set(parameters)
    missing = required - supplied
    unknown = supplied - required - optional
    if missing:
        raise ValueError(f"Missing required parameters: {', '.join(sorted(missing))}")
    if unknown:
        raise ValueError(f"Unknown parameters: {', '.join(sorted(unknown))}")

    values = dict(parameters)
    path_values: dict[str, str] = {}
    path_list_values: dict[str, list[str]] = {}
    for field in path_fields:
        if field not in values or values[field] is None:
            continue
        must_exist = field not in {"output", "output_dir", "cache_dir"}
        resolved = _project_path(
            root, values[field], must_exist=must_exist, kind=field
        )
        path_values[field] = resolved.relative_to(root.resolve()).as_posix()
    for field in ("rejected", "source_manifest"):
        if field in values:
            items = values[field]
            if not isinstance(items, list) or not items:
                raise ValueError(f"{field} must be a non-empty list of project-relative paths")
            resolved_items = []
            for item in items:
                resolved = _project_path(root, item, must_exist=True, kind=field)
                resolved_items.append(resolved.relative_to(root.resolve()).as_posix())
            path_list_values[field] = resolved_items

    result = [command]
    ordered_fields = [
        "input", "observations", "train", "test", "model", "features", "release_dir",
        "output", "output_dir", "target", "sequence_column", "smiles_column",
        "record_id_column", "source_column", "min_sequence_identity", "coverage",
        "threads", "cache_dir", "model_name", "model_revision", "tokenizer_revision",
        "device", "max_residues", "radius", "n_bits", "batch_size", "group_array",
        "protein_group_column", "substrate_group_column", "test_fraction",
        "calibration_fraction", "random_state", "n_splits", "calibration_archive",
        "conformal_alpha", "n_estimators", "max_depth", "hidden_layers", "alpha",
        "max_iter", "git_revision", "log10_tolerance", "source", "source_record_id_column",
        "km_unit", "kcat_unit", "version", "license_id", "citation", "dataset_id",
        "name", "dataset_name", "source_version", "source_url", "rejected", "source_manifest",
    ]
    list_fields = {
        "group_column": "--group-column",
        "holdout_group_array": "--holdout-group-array",
        "rejected": "--rejected",
        "source_manifest": "--source-manifest",
    }
    bool_flags = {"no_chirality": "--no-chirality", "overwrite": "--overwrite"}
    for field in ordered_fields:
        if field not in values or values[field] is None:
            continue
        option = "--" + field.replace("_", "-")
        value = values[field]
        if field in path_values:
            result.extend([option, path_values[field]])
        elif field in path_list_values:
            for item in path_list_values[field]:
                result.extend([list_fields[field], item])
        elif field in list_fields:
            if not isinstance(value, list) or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                raise ValueError(f"{field} must be a list of non-empty strings")
            for item in value:
                result.extend([list_fields[field], item])
        elif field in bool_flags:
            if not isinstance(value, bool):
                raise ValueError(f"{field} must be a boolean")
            if value:
                result.append(bool_flags[field])
        elif isinstance(value, bool):
            raise ValueError(f"{field} must not be a boolean")
        elif isinstance(value, (str, int, float)):
            result.extend([option, str(value)])
        else:
            raise ValueError(f"{field} has an unsupported value type")

    return result


def _row_dict(row: Any) -> dict[str, Any]:
    return dict(row) if row is not None else {}


def create_app(
    *,
    workspace_root: str | Path | None = None,
    database_path: str | Path | None = None,
    max_workers: int = 1,
) -> FastAPI:
    workspace = Path(
        workspace_root or os.environ.get(
            "KINETICS_WORKSPACE", Path.home() / ".kinetics" / "workspace"
        )
    ).expanduser().resolve()
    database = Path(
        database_path or os.environ.get(
            "KINETICS_DATABASE", Path.home() / ".kinetics" / "kinetics.sqlite3"
        )
    ).expanduser().resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    store = KineticsSQLite(database)
    store.initialize()
    executor = ThreadPoolExecutor(max_workers=max(1, max_workers))
    process_lock = threading.RLock()
    processes: dict[str, subprocess.Popen[str]] = {}

    with store.transaction() as connection:
        connection.execute(
            """UPDATE workbench_jobs
               SET state='interrupted',
                   error='Workbench restarted before this job reached a terminal state',
                   finished_at=CURRENT_TIMESTAMP
               WHERE state IN ('queued','running')"""
        )

    app = FastAPI(
        title="Kinetics Research Workbench",
        version="0.1.0",
        description=(
            "Local-first researcher interface. Scientific tasks execute through "
            "the versioned kinetics-research command interface."
        ),
    )
    app.state.store = store
    app.state.workspace_root = workspace
    app.state.executor = executor

    @app.middleware("http")
    async def local_origin_guard(request: Any, call_next: Any) -> Any:
        host = (request.url.hostname or "").lower()
        if host not in {"127.0.0.1", "localhost", "testserver"}:
            return JSONResponse(status_code=400, content={"detail": "Local workbench only"})
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            if request.headers.get("sec-fetch-site") == "cross-site":
                return JSONResponse(status_code=403, content={"detail": "Cross-site request blocked"})
            origin = request.headers.get("origin")
            if origin:
                parsed = urlsplit(origin)
                origin_host = (parsed.hostname or "").lower()
                if (
                    parsed.scheme != request.url.scheme
                    or origin_host != host
                    or parsed.port != request.url.port
                ):
                    return JSONResponse(status_code=403, content={"detail": "Cross-origin request blocked"})
        return await call_next(request)

    def project_record(project_id: str) -> dict[str, Any]:
        rows = store.fetch_all(
            "SELECT * FROM workbench_projects WHERE project_id=?", (project_id,)
        )
        if not rows:
            raise HTTPException(status_code=404, detail="Project not found")
        record = rows[0]
        root = Path(record["root_path"]).resolve()
        if not root.is_relative_to(workspace):
            raise HTTPException(status_code=409, detail="Project path is outside the workspace")
        record["root_path"] = root.relative_to(workspace).as_posix()
        return record

    def register_output_artifacts(
        project_id: str,
        job_id: str,
        command: str,
        parameters: dict[str, Any],
        root: Path,
    ) -> list[dict[str, Any]]:
        candidate = (parameters.get("output_dir") or parameters.get("output")
                     or parameters.get("release_dir"))
        if not candidate:
            return []
        try:
            output_kind = ("release_dir" if parameters.get("release_dir") else
                           "output_dir" if parameters.get("output_dir") else "output")
            output_path = _project_path(
                root, candidate, must_exist=True, kind=output_kind
            )
        except (ValueError, FileNotFoundError):
            return []
        paths = [output_path] if output_path.is_file() else sorted(
            item for item in output_path.rglob("*")
            if item.is_file() and not item.is_symlink()
        )
        artifacts: list[dict[str, Any]] = []
        for path in paths[:_MAX_ARTIFACTS_PER_JOB]:
            resolved = path.resolve()
            if not resolved.is_relative_to(root.resolve()):
                continue
            digest = KineticsSQLite.sha256_file(resolved)
            relative = resolved.relative_to(root.resolve()).as_posix()
            media_type = mimetypes.guess_type(resolved.name)[0]
            artifact_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{project_id}:{relative}:{digest}"))
            size = resolved.stat().st_size
            with store.transaction() as connection:
                connection.execute(
                    """INSERT OR IGNORE INTO workbench_artifacts
                       (artifact_id, project_id, job_id, relative_path,
                        artifact_type, checksum_sha256, byte_size, media_type)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (artifact_id, project_id, job_id, relative, command,
                     digest, size, media_type),
                )
            artifacts.append({
                "artifact_id": artifact_id,
                "relative_path": relative,
                "checksum_sha256": digest,
                "byte_size": size,
                "media_type": media_type,
            })
        return artifacts

    def run_job(job_id: str, project_id: str, command: str,
                parameters: dict[str, Any]) -> None:
        project = store.fetch_all(
            "SELECT root_path FROM workbench_projects WHERE project_id=?",
            (project_id,),
        )
        if not project:
            return
        root = Path(project[0]["root_path"]).resolve()
        log_path = root / "logs" / f"{job_id}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with store.transaction() as connection:
            row = connection.execute(
                "SELECT cancellation_requested FROM workbench_jobs WHERE job_id=?",
                (job_id,),
            ).fetchone()
            if row is None:
                return
            if row["cancellation_requested"]:
                connection.execute(
                    """UPDATE workbench_jobs SET state='cancelled',
                       finished_at=CURRENT_TIMESTAMP WHERE job_id=?""",
                    (job_id,),
                )
                return
            connection.execute(
                """UPDATE workbench_jobs SET state='running',
                   started_at=CURRENT_TIMESTAMP, log_path=? WHERE job_id=?""",
                (log_path.relative_to(root).as_posix(), job_id),
            )

        try:
            arguments = build_cli_arguments(command, parameters, root)
            if command == "persist":
                arguments.extend(["--database", str(database)])
            process = subprocess.Popen(
                [sys.executable, "-m", "kinetics_core.cli", *arguments],
                cwd=root,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            with process_lock:
                processes[job_id] = process
            try:
                output, _ = process.communicate(timeout=_JOB_TIMEOUT_SECONDS)
            except subprocess.TimeoutExpired:
                process.kill()
                output, _ = process.communicate()
                raise TimeoutError(
                    f"Research job exceeded {_JOB_TIMEOUT_SECONDS} seconds"
                )
            finally:
                with process_lock:
                    processes.pop(job_id, None)
            log_path.write_text(output or "", encoding="utf-8")
            current = store.fetch_all(
                "SELECT cancellation_requested FROM workbench_jobs WHERE job_id=?",
                (job_id,),
            )
            cancelled = bool(current and current[0]["cancellation_requested"])
            if cancelled:
                state = "cancelled"
                error = None
                result: dict[str, Any] = {}
            elif process.returncode == 0:
                state = "succeeded"
                error = None
                try:
                    parsed = json.loads(output)
                    result = parsed if isinstance(parsed, dict) else {"value": parsed}
                except json.JSONDecodeError:
                    result = {"stdout": (output or "")[-12000:]}
                artifacts = register_output_artifacts(
                    project_id, job_id, command, parameters, root
                )
                result["artifacts"] = artifacts
            else:
                state = "failed"
                error = (output or f"Process exited {process.returncode}")[-12000:]
                result = {}
        except Exception as exc:
            state = "failed"
            error = f"{type(exc).__name__}: {exc}"
            result = {}
            log_path.write_text(error, encoding="utf-8")

        with store.transaction() as connection:
            connection.execute(
                """UPDATE workbench_jobs
                   SET state=?, result_json=?, error=?, finished_at=CURRENT_TIMESTAMP
                   WHERE job_id=?""",
                (state, KineticsSQLite.json_dumps(result), error, job_id),
            )
            if command in {"compare", "fit", "fit-multi"}:
                target = parameters.get("target", "unspecified")
                code_revision = result.get("git_revision") or parameters.get("git_revision")
                connection.execute(
                    """INSERT INTO training_runs
                       (run_id, model_name, status, config_json, metrics_json,
                        random_seed, code_revision, started_at, finished_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                       ON CONFLICT(run_id) DO UPDATE SET
                         status=excluded.status,
                         metrics_json=excluded.metrics_json,
                         finished_at=excluded.finished_at""",
                    (
                        job_id,
                        f"{command}:{target}",
                        state,
                        KineticsSQLite.json_dumps(parameters),
                        KineticsSQLite.json_dumps(result),
                        parameters.get("random_state"),
                        code_revision,
                    ),
                )

    @app.get("/", include_in_schema=False)
    def home() -> FileResponse:
        return FileResponse(Path(__file__).parent / "static" / "index.html")

    @app.get("/api/v1/health")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "api_version": "v1",
            "database_schema_version": 2,
            "workspace": workspace.name,
        }

    @app.get("/api/v1/projects")
    def list_projects() -> list[dict[str, Any]]:
        rows = store.fetch_all(
            "SELECT project_id, name, description, root_path, created_at, updated_at "
            "FROM workbench_projects ORDER BY updated_at DESC"
        )
        for row in rows:
            root = Path(row["root_path"]).resolve()
            row["root_path"] = (
                root.relative_to(workspace).as_posix()
                if root.is_relative_to(workspace) else None
            )
        return rows

    @app.post("/api/v1/projects", status_code=201)
    def create_project(payload: ProjectCreate) -> dict[str, Any]:
        name = payload.name.strip()
        if not name:
            raise HTTPException(status_code=422, detail="Project name cannot be blank")
        project_id = str(uuid.uuid4())
        root = (workspace / "projects" / project_id).resolve()
        if not root.is_relative_to(workspace):
            raise HTTPException(status_code=400, detail="Invalid project workspace path")
        for folder in ("datasets", "runs", "artifacts", "reports", "logs"):
            (root / folder).mkdir(parents=True, exist_ok=True)
        with store.transaction() as connection:
            connection.execute(
                """INSERT INTO workbench_projects
                   (project_id, name, description, root_path)
                   VALUES (?, ?, ?, ?)""",
                (project_id, name, payload.description.strip(), str(root)),
            )
        return project_record(project_id)

    @app.post("/api/v1/projects/{project_id}/uploads", status_code=201)
    async def upload_project_file(
        project_id: str, file: UploadFile = File(...)
    ) -> dict[str, Any]:
        project = project_record(project_id)
        root = (workspace / project["root_path"]).resolve()
        raw_name = file.filename or ""
        filename = Path(raw_name).name
        if (
            not filename or filename in {".", ".."} or filename.startswith(".")
            or "\x00" in filename or "/" in filename or "\\" in filename
        ):
            raise HTTPException(status_code=422, detail="Invalid upload filename")
        destination = root / "datasets" / filename
        if destination.exists():
            raise HTTPException(status_code=409, detail="A file with that name already exists")
        staging = destination.with_name(f".{uuid.uuid4().hex}.upload")
        digest = hashlib.sha256()
        size = 0
        maximum_bytes = 500 * 1024 * 1024
        try:
            with staging.open("xb") as stream:
                while chunk := await file.read(1024 * 1024):
                    size += len(chunk)
                    if size > maximum_bytes:
                        raise HTTPException(
                            status_code=413, detail="Upload exceeds the 500 MiB limit"
                        )
                    digest.update(chunk)
                    stream.write(chunk)
            if size == 0:
                raise HTTPException(status_code=422, detail="Empty files are not accepted")
            try:
                os.link(staging, destination)
            except FileExistsError as exc:
                raise HTTPException(
                    status_code=409, detail="A file with that name already exists"
                ) from exc
            staging.unlink()
        except Exception:
            staging.unlink(missing_ok=True)
            raise
        finally:
            await file.close()
        checksum = digest.hexdigest()
        relative = destination.relative_to(root).as_posix()
        artifact_id = str(uuid.uuid5(
            uuid.NAMESPACE_URL, f"{project_id}:{relative}:{checksum}"
        ))
        media_type = mimetypes.guess_type(destination.name)[0]
        with store.transaction() as connection:
            connection.execute(
                """INSERT OR IGNORE INTO workbench_artifacts
                   (artifact_id, project_id, relative_path, artifact_type,
                    checksum_sha256, byte_size, media_type)
                   VALUES (?, ?, ?, 'uploaded-input', ?, ?, ?)""",
                (artifact_id, project_id, relative, checksum, size, media_type),
            )
        return {
            "artifact_id": artifact_id,
            "relative_path": relative,
            "checksum_sha256": checksum,
            "byte_size": size,
        }

    @app.get("/api/v1/datasets")
    def list_datasets() -> list[dict[str, Any]]:
        return store.fetch_all(
            """SELECT dataset_id, name, source, version, license, citation,
                      checksum_sha256, local_path, created_at
               FROM datasets ORDER BY created_at DESC"""
        )

    @app.get("/api/v1/experiments")
    def list_experiments() -> list[dict[str, Any]]:
        rows = store.fetch_all(
            """SELECT run_id, model_name, model_version, status, dataset_id,
                      config_json, metrics_json, random_seed, code_revision,
                      started_at, finished_at, created_at
               FROM training_runs ORDER BY created_at DESC"""
        )
        for row in rows:
            row["configuration"] = json.loads(row.pop("config_json"))
            row["metrics"] = json.loads(row.pop("metrics_json"))
        return rows

    @app.get("/api/v1/projects/{project_id}/jobs")
    def list_jobs(project_id: str) -> list[dict[str, Any]]:
        project_record(project_id)
        rows = store.fetch_all(
            """SELECT job_id, project_id, command, state, parameters_json,
                      result_json, error, log_path, created_at, started_at, finished_at
               FROM workbench_jobs WHERE project_id=?
               ORDER BY created_at DESC LIMIT 200""",
            (project_id,),
        )
        for row in rows:
            row["parameters"] = json.loads(row.pop("parameters_json"))
            row["result"] = json.loads(row.pop("result_json"))
        return rows

    @app.post("/api/v1/projects/{project_id}/jobs", status_code=202)
    def create_job(project_id: str, payload: JobCreate) -> dict[str, Any]:
        project = project_record(project_id)
        root = (workspace / project["root_path"]).resolve()
        try:
            build_cli_arguments(payload.command, payload.parameters, root)
        except (ValueError, FileNotFoundError, FileExistsError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        job_id = str(uuid.uuid4())
        with store.transaction() as connection:
            pending = connection.execute(
                """SELECT COUNT(*) FROM workbench_jobs
                   WHERE state IN ('queued','running')"""
            ).fetchone()[0]
            if pending >= 100:
                raise HTTPException(status_code=429, detail="Workbench queue is full")
            connection.execute(
                """INSERT INTO workbench_jobs
                   (job_id, project_id, command, state, parameters_json)
                   VALUES (?, ?, ?, 'queued', ?)""",
                (job_id, project_id, payload.command,
                 KineticsSQLite.json_dumps(payload.parameters)),
            )
        executor.submit(
            run_job, job_id, project_id, payload.command, payload.parameters
        )
        return {"job_id": job_id, "state": "queued", "command": payload.command}

    @app.post("/api/v1/jobs/{job_id}/cancel")
    def cancel_job(job_id: str) -> dict[str, str]:
        rows = store.fetch_all(
            "SELECT state FROM workbench_jobs WHERE job_id=?", (job_id,)
        )
        if not rows:
            raise HTTPException(status_code=404, detail="Job not found")
        if rows[0]["state"] not in {"queued", "running"}:
            raise HTTPException(status_code=409, detail="Job is already terminal")
        with store.transaction() as connection:
            connection.execute(
                """UPDATE workbench_jobs SET cancellation_requested=1
                   WHERE job_id=?""",
                (job_id,),
            )
        with process_lock:
            process = processes.get(job_id)
            if process is not None and process.poll() is None:
                process.terminate()
        return {"job_id": job_id, "state": "cancellation_requested"}

    @app.get("/api/v1/projects/{project_id}/artifacts")
    def list_artifacts(project_id: str) -> list[dict[str, Any]]:
        project_record(project_id)
        return store.fetch_all(
            """SELECT artifact_id, job_id, relative_path, artifact_type,
                      checksum_sha256, byte_size, media_type, created_at
               FROM workbench_artifacts WHERE project_id=?
               ORDER BY created_at DESC LIMIT 1000""",
            (project_id,),
        )

    @app.get("/api/v1/projects/{project_id}/artifacts/{artifact_id}")
    def download_artifact(project_id: str, artifact_id: str) -> FileResponse:
        project = project_record(project_id)
        rows = store.fetch_all(
            """SELECT relative_path, checksum_sha256 FROM workbench_artifacts
               WHERE project_id=? AND artifact_id=?""",
            (project_id, artifact_id),
        )
        if not rows:
            raise HTTPException(status_code=404, detail="Artifact not found")
        root = (workspace / project["root_path"]).resolve()
        path = (root / rows[0]["relative_path"]).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise HTTPException(status_code=404, detail="Artifact file is unavailable")
        if KineticsSQLite.sha256_file(path) != rows[0]["checksum_sha256"]:
            raise HTTPException(status_code=409, detail="Artifact checksum verification failed")
        return FileResponse(path, filename=path.name)

    @app.get("/api/v1/projects/{project_id}/jobs/{job_id}/log")
    def read_job_log(project_id: str, job_id: str) -> dict[str, str]:
        project = project_record(project_id)
        rows = store.fetch_all(
            "SELECT log_path FROM workbench_jobs WHERE project_id=? AND job_id=?",
            (project_id, job_id),
        )
        if not rows:
            raise HTTPException(status_code=404, detail="Job not found")
        if not rows[0]["log_path"]:
            return {"log": ""}
        root = (workspace / project["root_path"]).resolve()
        path = (root / rows[0]["log_path"]).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            return {"log": ""}
        return {"log": path.read_text(encoding="utf-8", errors="replace")[-20000:]}

    @app.post("/api/v1/projects/{project_id}/jobs/{job_id}/report", status_code=201)
    def create_job_report(project_id: str, job_id: str) -> dict[str, Any]:
        project = project_record(project_id)
        rows = store.fetch_all(
            """SELECT command, state, parameters_json, result_json, created_at
               FROM workbench_jobs WHERE project_id=? AND job_id=?""",
            (project_id, job_id),
        )
        if not rows:
            raise HTTPException(status_code=404, detail="Job not found")
        job = rows[0]
        if job["state"] != "succeeded":
            raise HTTPException(status_code=409, detail="Reports require a successful job")
        root = (workspace / project["root_path"]).resolve()
        parameters = json.loads(job["parameters_json"])
        result = json.loads(job["result_json"])
        report_path = root / "reports" / f"{job_id}.md"
        inputs = []
        for field in ("input", "observations", "train", "test", "model", "features", "release_dir"):
            value = parameters.get(field)
            if isinstance(value, str):
                candidate = (root / value).resolve()
                if candidate.is_file() and candidate.is_relative_to(root):
                    inputs.append(candidate)
        outputs = []
        for artifact in result.get("artifacts", []):
            candidate = (root / artifact["relative_path"]).resolve()
            if candidate.is_file() and candidate.is_relative_to(root):
                outputs.append(candidate)
        from ..experiments import build_experiment_manifest
        from ..reporting import write_experiment_report

        manifest = build_experiment_manifest(
            experiment_id=job_id,
            research_question=f"Workbench {job['command']} workflow",
            inputs=inputs,
            outputs=outputs,
            configuration={"command": job["command"], "parameters": parameters},
            notes=[
                "Generated from the local Kinetics workbench.",
                "Review source licenses, split design, uncertainty and limitations "
                "before scientific interpretation.",
            ],
        )
        report_path.parent.mkdir(parents=True, exist_ok=True)
        write_experiment_report(
            experiment_manifest=manifest,
            metrics=result,
            limitations=[
                "This report records the software job output; it is not independent "
                "scientific validation.",
                "Any metrics absent from the job result are intentionally reported "
                "as not reported.",
            ],
            destination=report_path,
        )
        digest = KineticsSQLite.sha256_file(report_path)
        relative = report_path.relative_to(root).as_posix()
        artifact_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{project_id}:{relative}:{digest}"))
        with store.transaction() as connection:
            connection.execute(
                """INSERT OR IGNORE INTO workbench_artifacts
                   (artifact_id, project_id, job_id, relative_path, artifact_type,
                    checksum_sha256, byte_size, media_type)
                   VALUES (?, ?, ?, ?, 'experiment-report', ?, ?, 'text/markdown')""",
                (artifact_id, project_id, job_id, relative, digest, report_path.stat().st_size),
            )
        return {
            "artifact_id": artifact_id,
            "relative_path": relative,
            "checksum_sha256": digest,
        }

    @app.on_event("shutdown")
    def shutdown() -> None:
        with process_lock:
            active = list(processes.values())
        for process in active:
            if process.poll() is None:
                process.terminate()
        executor.shutdown(wait=False, cancel_futures=True)

    return app


app = create_app()
