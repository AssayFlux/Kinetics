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
    assert 'window.KineticsStructureViewer = Object.freeze({load,clear()' in script
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
