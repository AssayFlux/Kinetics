#!/usr/bin/env python3
"""Build the public, evidence-based corpus growth dashboard (SVG + history JSON)."""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data/corpus-manifests/metadata_index.json"
DEFAULT_HISTORY = ROOT / "data/corpus-manifests/corpus_history.json"
DEFAULT_DATABASE = ROOT / "data/kinetics.sqlite3"
DEFAULT_SVG = ROOT / "Assets/corpus-growth.svg"


def database_metrics(path: Path) -> dict[str, int]:
    metrics = {"indexed_documents": 0, "indexed_chunks": 0, "indexed_tokens": 0}
    if not path.is_file():
        return metrics
    try:
        with sqlite3.connect(path) as db:
            tables = {row[0] for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
            if "knowledge_documents" in tables:
                row = db.execute(
                    "SELECT COUNT(*), COALESCE(SUM(token_count),0) "
                    "FROM knowledge_documents WHERE status='indexed'"
                ).fetchone()
                metrics["indexed_documents"], metrics["indexed_tokens"] = map(int, row)
            if "knowledge_chunks" in tables:
                metrics["indexed_chunks"] = int(
                    db.execute("SELECT COUNT(*) FROM knowledge_chunks").fetchone()[0])
    except sqlite3.Error:
        # A missing/partial database must never be represented as indexed content.
        return {"indexed_documents": 0, "indexed_chunks": 0, "indexed_tokens": 0}
    return metrics


def corpus_metrics(manifest: dict[str, Any], database: Path) -> dict[str, int]:
    published = [
        record for record in manifest.get("items", {}).values()
        if record.get("status") == "downloaded" and record.get("release_uploaded") is True
    ]
    return {
        "published_objects": len(published),
        "published_bytes": sum(max(0, int(record.get("bytes", 0) or 0)) for record in published),
        "published_domains": len({str(r.get("domain")) for r in published if r.get("domain")}),
        "published_sources": len({str(r.get("source")) for r in published if r.get("source")}),
        **database_metrics(database),
    }


def load_history(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "snapshots": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("snapshots"), list):
        raise ValueError(f"Unsupported corpus history format: {path}")
    return data


def render_svg(history: dict[str, Any], metrics: dict[str, int], generated_at: str) -> str:
    width, height = 960, 430
    left, right, top, bottom = 92, 38, 92, 105
    plot_w, plot_h = width - left - right, height - top - bottom
    snapshots = history.get("snapshots", [])[-12:]
    max_mib = max((int(p.get("published_bytes", 0)) for p in snapshots), default=0) / (1024 * 1024)
    max_mib = max(1.0, max_mib * 1.12)
    max_mib = max(1, int(max_mib + 0.999))
    coords = []
    for i, point in enumerate(snapshots):
        x = left + (plot_w / max(1, len(snapshots) - 1)) * i
        mib = int(point.get("published_bytes", 0)) / (1024 * 1024)
        y = top + plot_h - (mib / max_mib) * plot_h
        coords.append((x, y, mib, str(point.get("captured_at", ""))[:10]))
    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y, _, _ in coords)
    grid = []
    for tick in range(5):
        value = max_mib * tick / 4
        y = top + plot_h - (tick / 4) * plot_h
        grid.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="grid"/>'
            f'<text x="{left-14}" y="{y+5:.1f}" text-anchor="end" class="axis">{value:.0f}</text>'
        )
    circles = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" class="dot"><title>{escape(date)} · {mib:.2f} MiB</title></circle>'
        for x, y, mib, date in coords
    )
    labels = ""
    if len(coords) == 1:
        labels = f'<text x="{coords[0][0]:.1f}" y="{top+plot_h+30}" text-anchor="middle" class="axis">{escape(coords[0][3])}</text>'
    elif len(coords) > 1:
        labels = (
            f'<text x="{left}" y="{top+plot_h+30}" text-anchor="start" class="axis">{escape(coords[0][3])}</text>'
            f'<text x="{width-right}" y="{top+plot_h+30}" text-anchor="end" class="axis">{escape(coords[-1][3])}</text>'
        )
    if not coords or metrics["published_objects"] == 0:
        empty = '<text x="480" y="245" text-anchor="middle" class="empty">Waiting for the first verified public corpus release</text>'
    else:
        empty = ""
    mib_now = metrics["published_bytes"] / (1024 * 1024)
    gb_now = metrics["published_bytes"] / (1024 ** 3)
    storage = f"{gb_now:.2f} GiB" if gb_now >= 1 else f"{mib_now:.1f} MiB"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Kinetics public corpus growth</title>
<desc id="desc">Cumulative size of verified, downloadable corpus objects published as GitHub Release assets over time. Current total {storage} across {metrics['published_objects']} objects. Latest workflow index: {metrics['indexed_documents']} documents and {metrics['indexed_chunks']} searchable chunks.</desc>
<style>
  .bg {{ fill:#0b1220; }} .title {{ fill:#f8fafc; font:700 25px sans-serif; }}
  .subtitle {{ fill:#a8b4c7; font:14px sans-serif; }} .grid {{ stroke:#29364a; stroke-width:1; }}
  .axis {{ fill:#9aa9bd; font:12px sans-serif; }} .line {{ fill:none; stroke:#4ade80; stroke-width:4; stroke-linecap:round; stroke-linejoin:round; }}
  .dot {{ fill:#4ade80; stroke:#0b1220; stroke-width:3; }} .empty {{ fill:#cbd5e1; font:16px sans-serif; }}
  .metric {{ fill:#f8fafc; font:700 21px sans-serif; }} .metric-label {{ fill:#94a3b8; font:12px sans-serif; }}
</style>
<rect class="bg" width="100%" height="100%" rx="18"/>
<text x="42" y="45" class="title">Kinetics · Open Research Corpus</text>
<text x="42" y="69" class="subtitle">Verified public corpus assets · cumulative growth · updated {escape(generated_at[:10])}</text>
{''.join(grid)}
<polyline points="{polyline}" class="line"/>
{circles}{labels}{empty}
<text x="480" y="337" text-anchor="middle" class="axis">Published corpus size (MiB)</text>
<line x1="42" y1="365" x2="918" y2="365" class="grid"/>
<text x="55" y="397" class="metric">{storage}</text>
<text x="55" y="416" class="metric-label">{metrics['published_objects']} public objects · {metrics['published_domains']} domains · {metrics['published_sources']} sources</text>
<text x="510" y="397" class="metric">{metrics['indexed_documents']:,}</text>
<text x="510" y="416" class="metric-label">documents indexed in latest workflow · {metrics['indexed_chunks']:,} searchable chunks · {metrics['indexed_tokens']:,} tokens</text>
</svg>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--history", type=Path, default=DEFAULT_HISTORY)
    parser.add_argument("--output", type=Path, default=DEFAULT_SVG)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    metrics = corpus_metrics(manifest, args.database)
    now = datetime.now(timezone.utc).isoformat()
    history = load_history(args.history)
    run_id = os.getenv("GITHUB_RUN_ID") or now[:10]
    snapshot = {"run_id": str(run_id), "captured_at": now, **metrics}
    snapshots = [p for p in history["snapshots"] if str(p.get("run_id")) != str(run_id)]
    snapshots.append(snapshot)
    snapshots.sort(key=lambda p: str(p.get("captured_at", "")))
    history["snapshots"] = snapshots[-200:]

    args.history.parent.mkdir(parents=True, exist_ok=True)
    args.history.write_text(json.dumps(history, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_svg(history, metrics, now), encoding="utf-8")
    print(json.dumps({"dashboard": str(args.output), **metrics}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
