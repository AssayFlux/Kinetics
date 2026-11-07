"""Real-browser responsive and interaction acceptance for the Kinetics workbench.

Run with: pip install -e ".[dev,workbench,browser]" && playwright install chromium
"""
from __future__ import annotations

import socket
import threading
import time
from collections.abc import Iterator

import pytest

playwright = pytest.importorskip("playwright.sync_api")
uvicorn = pytest.importorskip("uvicorn")

from kinetics_core.workbench.app import create_app


@pytest.fixture(scope="module")
def workbench_url(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    root = tmp_path_factory.mktemp("browser-workbench")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    app = create_app(
        workspace_root=root / "workspace",
        database_path=root / "metadata.sqlite3",
        max_workers=1,
    )
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    )
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{port}"
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        try:
            import urllib.request

            with urllib.request.urlopen(url + "/api/v1/health", timeout=1) as response:
                if response.status == 200:
                    break
        except Exception:
            time.sleep(0.1)
    else:
        server.should_exit = True
        thread.join(timeout=5)
        raise RuntimeError("Kinetics workbench did not start for browser acceptance")
    yield url
    server.should_exit = True
    thread.join(timeout=10)


@pytest.fixture
def browser_page():
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 960})
        yield page
        browser.close()


@pytest.mark.parametrize("width,height", [(1440, 960), (1024, 768), (768, 1024), (390, 844), (320, 720)])
def test_workbench_renders_without_horizontal_page_overflow(
    workbench_url: str, browser_page, width: int, height: int
):
    browser_page.set_viewport_size({"width": width, "height": height})
    browser_page.goto(workbench_url, wait_until="networkidle")
    assert browser_page.title() == "Kinetics Research Workbench"
    assert browser_page.locator("h1").is_visible()
    assert browser_page.locator("#project").is_visible()
    assert browser_page.locator("#submit-job").is_visible()
    dimensions = browser_page.evaluate(
        "() => ({viewport: document.documentElement.clientWidth, page: document.documentElement.scrollWidth})"
    )
    assert dimensions["page"] <= dimensions["viewport"] + 1, dimensions


def test_researcher_can_create_project_in_real_browser(workbench_url: str, browser_page):
    browser_page.goto(workbench_url, wait_until="networkidle")
    browser_page.locator("#project-name").fill("Browser acceptance project")
    browser_page.locator("#project-description").fill("Created through the real UI")
    browser_page.get_by_role("button", name="Create project").click()
    browser_page.locator("#project option", has_text="Browser acceptance project").wait_for(state="attached")
    assert browser_page.locator("#project").input_value()


def test_structure_viewer_is_responsive_and_exposes_accessible_controls(
    workbench_url: str, browser_page
):
    for width in (1440, 768, 390, 320):
        browser_page.set_viewport_size({"width": width, "height": 844})
        browser_page.goto(workbench_url + "/structure-viewer", wait_until="domcontentloaded")
        assert browser_page.locator("h1").is_visible()
        assert browser_page.locator("#viewer").is_visible()
        assert browser_page.get_by_role("button", name="Export PNG").is_visible()
        dimensions = browser_page.evaluate(
            "() => ({viewport: document.documentElement.clientWidth, page: document.documentElement.scrollWidth})"
        )
        assert dimensions["page"] <= dimensions["viewport"] + 1, dimensions
