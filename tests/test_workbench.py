from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from kinetics_core.storage import KineticsSQLite
from kinetics_core.workbench.app import build_cli_arguments, create_app


def test_workbench_schema_migrates_to_version_two(tmp_path):
    database = tmp_path / "metadata.sqlite3"
    store = KineticsSQLite(database)
    store.initialize()
    with store.session() as connection:
        assert connection.execute("PRAGMA user_version").fetchone()[0] == 2
        names = {
            row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
    assert {
        "workbench_projects", "workbench_jobs", "workbench_artifacts"
    } <= names


def test_command_builder_is_allowlisted_and_confines_paths(tmp_path):
    (tmp_path / "input.csv").write_text("target\n", encoding="utf-8")
    args = build_cli_arguments(
        "audit",
        {"input": "input.csv", "output_dir": "runs/audit-1"},
        tmp_path,
    )
    assert args == ["audit", "--input", "input.csv", "--output-dir", "runs/audit-1"]

    with pytest.raises(ValueError, match="inside the project workspace"):
        build_cli_arguments(
            "audit",
            {"input": "../outside.csv", "output_dir": "runs/audit-2"},
            tmp_path,
        )
    with pytest.raises(ValueError, match="Unknown parameters"):
        build_cli_arguments(
            "audit",
            {"input": "input.csv", "output_dir": "runs/audit-3", "shell": "echo"},
            tmp_path,
        )
    with pytest.raises(ValueError, match="Unsupported workbench command"):
        build_cli_arguments("arbitrary-shell", {}, tmp_path)


def test_workbench_uploads_runs_audits_registers_artifacts_and_builds_report(tmp_path):
    workspace = tmp_path / "workspace"
    app = create_app(
        workspace_root=workspace,
        database_path=tmp_path / "metadata.sqlite3",
        max_workers=1,
    )
    with TestClient(app) as client:
        assert client.get("/api/v1/health").json()["status"] == "ok"
        created = client.post(
            "/api/v1/projects",
            json={"name": "Kinetics validation", "description": "Workbench integration"},
        )
        assert created.status_code == 201
        project_id = created.json()["project_id"]

        csv = (
            "target,source,source_record_id,canonical_value,canonical_unit\n"
            "km,fixture,00017,0.001,M\n"
        )
        uploaded = client.post(
            f"/api/v1/projects/{project_id}/uploads",
            files={"file": ("observations.csv", csv.encode(), "text/csv")},
        )
        assert uploaded.status_code == 201
        assert uploaded.json()["relative_path"] == "datasets/observations.csv"
        assert len(uploaded.json()["checksum_sha256"]) == 64

        queued = client.post(
            f"/api/v1/projects/{project_id}/jobs",
            json={
                "command": "audit",
                "parameters": {
                    "input": "datasets/observations.csv",
                    "output_dir": "runs/audit-001",
                },
            },
        )
        assert queued.status_code == 202
        job_id = queued.json()["job_id"]

        deadline = time.monotonic() + 30
        job = None
        while time.monotonic() < deadline:
            response = client.get(f"/api/v1/projects/{project_id}/jobs")
            assert response.status_code == 200
            jobs = response.json()
            job = next((item for item in jobs if item["job_id"] == job_id), None)
            if job and job["state"] in {"succeeded", "failed", "cancelled"}:
                break
            time.sleep(0.1)

        assert job is not None
        assert job["state"] == "succeeded", job
        artifacts = client.get(
            f"/api/v1/projects/{project_id}/artifacts"
        ).json()
        paths = {item["relative_path"] for item in artifacts}
        assert "runs/audit-001/quality_report.json" in paths
        artifact = next(
            item for item in artifacts
            if item["relative_path"] == "runs/audit-001/quality_report.json"
        )
        downloaded = client.get(
            f"/api/v1/projects/{project_id}/artifacts/{artifact['artifact_id']}"
        )
        assert downloaded.status_code == 200
        assert json.loads(downloaded.content)["n_rows"] == 1

        report = client.post(
            f"/api/v1/projects/{project_id}/jobs/{job_id}/report"
        )
        assert report.status_code == 201
        assert report.json()["relative_path"] == f"reports/{job_id}.md"
        report_artifact = client.get(
            f"/api/v1/projects/{project_id}/artifacts/{report.json()['artifact_id']}"
        )
        assert report_artifact.status_code == 200
        assert b"not independent scientific validation" in report_artifact.content or (
            b"not reported" in report_artifact.content
        )


def test_workbench_rejects_path_escape_and_upload_overwrite(tmp_path):
    app = create_app(
        workspace_root=tmp_path / "workspace",
        database_path=tmp_path / "metadata.sqlite3",
    )
    with TestClient(app) as client:
        project = client.post(
            "/api/v1/projects", json={"name": "Secure workspace"}
        ).json()
        project_id = project["project_id"]
        cross_site = client.post(
            f"/api/v1/projects/{project_id}/uploads",
            headers={"Origin": "https://attacker.example", "Sec-Fetch-Site": "cross-site"},
            files={"file": ("blocked.csv", b"not accepted", "text/csv")},
        )
        assert cross_site.status_code == 403
        first = client.post(
            f"/api/v1/projects/{project_id}/uploads",
            files={"file": ("input.csv", b"content", "text/csv")},
        )
        assert first.status_code == 201
        duplicate = client.post(
            f"/api/v1/projects/{project_id}/uploads",
            files={"file": ("input.csv", b"other", "text/csv")},
        )
        assert duplicate.status_code == 409
        escape = client.post(
            f"/api/v1/projects/{project_id}/jobs",
            json={
                "command": "audit",
                "parameters": {"input": "../secret.csv", "output_dir": "runs/x"},
            },
        )
        assert escape.status_code == 422
