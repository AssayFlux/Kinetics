from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIEWER = ROOT / 'web' / 'viewers' / 'src'

def test_offline_structure_viewer_has_local_assets_and_network_denial() -> None:
    html = (VIEWER / 'structure-viewer.html').read_text(encoding='utf-8')
    script = (VIEWER / 'structure-viewer.js').read_text(encoding='utf-8')
    css = (VIEWER / 'structure-viewer.css').read_text(encoding='utf-8')
    assert 'src="structure-viewer.js"' in html
    assert 'href="structure-viewer.css"' in html
    assert "connect-src 'none'" in html
    assert "default-src 'none'" in html
    assert 'https://' not in html + script + css
    assert 'window.KineticsStructureViewer' in script
    assert 'MAX_BYTES = 32 * 1024 * 1024' in script
    assert 'MAX_ATOMS = 200000' in script

def test_viewer_uses_typed_payload_surface_without_generic_bridge_or_eval() -> None:
    script = (VIEWER / 'structure-viewer.js').read_text(encoding='utf-8')
    assert 'function validate(payload)' in script
    assert 'function load(payload)' in script
    assert 'window.KineticsStructureViewer = Object.freeze({' in script
    assert 'load,exportSvg,getState,setState' in script
    assert 'addJavascriptInterface' not in script
    assert 'eval(' not in script
    assert 'fetch(' not in script
    assert 'XMLHttpRequest' not in script

def test_viewer_uses_bounded_accessible_selection_list() -> None:
    html = (VIEWER / 'structure-viewer.html').read_text(encoding='utf-8')
    script = (VIEWER / 'structure-viewer.js').read_text(encoding='utf-8')
    assert 'aria-label="Structure atoms"' in html
    assert 'aria-live="polite"' in html
    assert 'atoms.slice(0, 500)' in script



def test_android_viewer_assets_are_byte_identical_to_reviewed_web_assets() -> None:
    android = ROOT / 'android' / 'app' / 'src' / 'main' / 'assets' / 'structure-viewer'
    for name in (
        'structure-viewer.html',
        'structure-viewer.js',
        'structure-viewer.css',
    ):
        assert (android / name).read_bytes() == (VIEWER / name).read_bytes()


def test_android_webview_and_document_io_keep_offline_security_boundary() -> None:
    source = (
        ROOT / 'android' / 'app' / 'src' / 'main' / 'java'
        / 'org' / 'assayflux' / 'kinetics' / 'StructureViewer.kt'
    ).read_text(encoding='utf-8')
    assert 'WebViewAssetLoader' in source
    assert 'settings.allowFileAccess = false' in source
    assert 'settings.allowContentAccess = false' in source
    assert 'settings.blockNetworkLoads = true' in source
    assert 'MIXED_CONTENT_NEVER_ALLOW' in source
    assert 'shouldOverrideUrlLoading' in source
    assert 'addJavascriptInterface' not in source
    assert 'ActivityResultContracts.OpenDocument()' in source
    assert 'ActivityResultContracts.CreateDocument("application/json")' in source
    assert 'MAX_STRUCTURE_SOURCE_BYTES = 16 * 1024 * 1024' in source
    assert 'CodingErrorAction.REPORT' in source
    assert 'prepare_structure_viewer_import' in source


def test_android_viewer_supports_bounded_png_snapshot_export() -> None:
    source = (
        ROOT / 'android' / 'app' / 'src' / 'main' / 'java'
        / 'org' / 'assayflux' / 'kinetics' / 'StructureViewer.kt'
    ).read_text(encoding='utf-8')
    assert 'CreateDocument("image/png")' in source
    assert 'Bitmap.CompressFormat.PNG' in source
    assert '16_777_216L' in source
    assert 'viewerWebView = webView' in source
    assert 'pendingPngBitmap?.recycle()' in source



def test_viewer_exports_bounded_svg_and_serializable_interactive_state() -> None:
    script = (VIEWER / "structure-viewer.js").read_text(encoding="utf-8")
    assert "function exportSvg()" in script
    assert "function getState()" in script
    assert "function setState(state)" in script
    assert "kinetics.structure-view-state.v1" in script
    assert "SVG exceeds 32 MiB" in script


def test_android_saf_exports_svg_and_session_view_state() -> None:
    source = (
        ROOT / "android" / "app" / "src" / "main" / "java"
        / "org" / "assayflux" / "kinetics" / "StructureViewer.kt"
    ).read_text(encoding="utf-8")
    assert 'CreateDocument("image/svg+xml")' in source
    assert "Export viewer SVG" in source
    assert 'getState()' in source
    assert 'put("viewer_state", state)' in source
    assert "Restore saved view state" in source
    assert "32 * 1024 * 1024" in source
