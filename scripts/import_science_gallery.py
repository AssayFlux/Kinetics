#!/usr/bin/env python3
"""Import 30 openly licensed biological/medical science photographs from Wikimedia Commons.

Usage:
  python scripts/import_science_gallery.py

Only CC0, public-domain, CC BY and CC BY-SA assets are accepted. Every image is
converted to an optimized PNG and its source/license/attribution is recorded in
Assets/Future/ATTRIBUTION.json. Review the manifest before redistribution.
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Install Pillow first: python -m pip install Pillow")

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Assets" / "Future" / "PNG"
MANIFEST = ROOT / "Assets" / "Future" / "ATTRIBUTION.json"
API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "KineticsScienceGallery/1.0 (open-source research project)"}
CATEGORIES = [
    ("01-genomics", "DNA genome sequencing chromosome fluorescence in situ hybridization"),
    ("02-genetics", "genetics inheritance karyotype chromosomes"),
    ("03-transcriptomics", "RNA sequencing transcriptomics gene expression"),
    ("04-proteomics", "proteomics protein gel electrophoresis mass spectrometry"),
    ("05-structural-biology", "protein molecular structure cryo electron microscopy"),
    ("06-cell-biology", "cell culture fluorescence microscopy"),
    ("07-molecular-biology", "molecular biology PCR laboratory"),
    ("08-microbiology", "bacteria microbiology microscopy"),
    ("09-virology", "virus virion electron microscopy"),
    ("10-immunology", "immune cells immunology antibody microscopy"),
    ("11-neuroscience", "neuron brain neuroscience microscopy"),
    ("12-cardiology", "heart cardiovascular anatomy medical imaging"),
    ("13-oncology", "cancer histopathology tumor microscopy"),
    ("14-pathology", "histopathology tissue pathology microscope"),
    ("15-pharmacology", "pharmacology pharmaceutical laboratory research"),
    ("16-medicinal-chemistry", "medicinal chemistry molecular drug discovery"),
    ("17-biochemistry", "biochemistry enzyme laboratory"),
    ("18-enzymology", "enzyme assay enzymology laboratory"),
    ("19-metabolomics", "metabolomics chromatography mass spectrometry"),
    ("20-microbiome", "human gut microbiome bacteria microscopy"),
    ("21-anatomy", "human anatomy anatomical specimen"),
    ("22-physiology", "human physiology organ medical research"),
    ("23-radiology", "MRI medical radiology scan"),
    ("24-medical-ultrasound", "medical ultrasound sonography"),
    ("25-surgery", "surgical operating room medical team"),
    ("26-public-health", "public health epidemiology laboratory"),
    ("27-clinical-research", "clinical research hospital laboratory"),
    ("28-regenerative-medicine", "stem cells regenerative medicine microscopy"),
    ("29-bioinformatics", "bioinformatics genomic data visualization"),
    ("30-biomedical-engineering", "biomedical engineering medical device research"),
]
LICENSE_OK = re.compile(r"(CC0|Public domain|CC BY(?:-SA)?(?:\s|$))", re.I)


def api(params):
    url = API + "?" + urllib.parse.urlencode({"format": "json", **params})
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)


def find_file(term, used):
    data = api({
        "action": "query", "generator": "search", "gsrsearch": term,
        "gsrnamespace": 6, "gsrlimit": 30,
        "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 1800,
    })
    pages = (data.get("query") or {}).get("pages") or {}
    candidates = sorted(pages.values(), key=lambda p: p.get("title", ""))
    for page in candidates:
        title = page.get("title", "")
        if title in used:
            continue
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata") or {}
        def val(key):
            return re.sub(r"<[^>]+>", "", (meta.get(key) or {}).get("value", "")).strip()
        license_name = val("LicenseShortName") or val("UsageTerms")
        if not LICENSE_OK.search(license_name):
            continue
        mime = info.get("mime", "")
        if not mime.startswith("image/") or mime == "image/svg+xml":
            continue
        url = info.get("thumburl") or info.get("url")
        if url:
            return {
                "title": title, "url": url, "source_page": info.get("descriptionurl", ""),
                "license": license_name, "license_url": val("LicenseUrl"),
                "artist": val("Artist"), "credit": val("Credit"),
                "description": val("ImageDescription"),
            }
    return None


def download_png(item, target):
    req = urllib.request.Request(item["url"], headers=HEADERS)
    with urllib.request.urlopen(req, timeout=90) as response:
        raw = response.read()
    from io import BytesIO
    with Image.open(BytesIO(raw)) as im:
        im = im.convert("RGB")
        im.thumbnail((1800, 1200), Image.Resampling.LANCZOS)
        target.parent.mkdir(parents=True, exist_ok=True)
        im.save(target, format="PNG", optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    used, records = set(), []
    for filename, search in CATEGORIES:
        target = OUT / f"{filename}.png"
        if target.exists():
            print(f"SKIP existing {target.name}")
            continue
        print(f"Searching: {filename} ...", flush=True)
        item = find_file(search, used)
        if not item:
            print(f"  NOT FOUND: no matching freely licensed image for {search}")
            continue
        try:
            download_png(item, target)
            used.add(item["title"])
            records.append({
                "file": f"Assets/Future/PNG/{target.name}",
                "category": filename.replace("-", " ").title(),
                **item,
            })
            print(f"  SAVED {target.name} ({item['license']})", flush=True)
        except Exception as exc:
            print(f"  ERROR {target.name}: {exc}", file=sys.stderr)
            if target.exists():
                target.unlink()
        time.sleep(0.15)

    previous = []
    if MANIFEST.exists():
        try:
            previous = json.loads(MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            pass
    merged = {x["file"]: x for x in previous}
    merged.update({x["file"]: x for x in records})
    MANIFEST.write_text(json.dumps(list(merged.values()), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    count = len(list(OUT.glob("*.png")))
    print(f"\nPNG files present: {count}/30")
    print(f"Attribution manifest: {MANIFEST.relative_to(ROOT)}")
    if count < 30:
        print("Run again to retry categories for which Commons had no acceptable match.")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
