#!/usr/bin/env python3
"""Download a 100-domain biomedical image gallery from Wikimedia Commons.

Only public-domain, CC0, CC BY and CC BY-SA assets are accepted. Every PNG
receives a source/license/creator entry in Assets/Future/ATTRIBUTION.json.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path
try:
    from PIL import Image
except ImportError:
    raise SystemExit("Install gallery support: python -m pip install -e '.[gallery]'")

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"Assets"/"Future"/"PNG"
MANIFEST=ROOT/"Assets"/"Future"/"ATTRIBUTION.json"
API="https://commons.wikimedia.org/w/api.php"
HEADERS={"User-Agent":"KineticsScienceGallery/2.0 (open-source research project)"}
LICENSE_OK=re.compile(r"^(?:CC0|Public domain|CC BY(?:-SA)?(?: |$))",re.I)
CATEGORIES=[
  [
    "genomics",
    "DNA genome sequencing chromosome FISH"
  ],
  [
    "genetics",
    "genetics inheritance karyotype chromosomes"
  ],
  [
    "transcriptomics",
    "RNA sequencing transcriptomics gene expression"
  ],
  [
    "proteomics",
    "proteomics protein gel electrophoresis mass spectrometry"
  ],
  [
    "structural-biology",
    "protein molecular structure cryo electron microscopy"
  ],
  [
    "cell-biology",
    "cell culture fluorescence microscopy"
  ],
  [
    "molecular-biology",
    "molecular biology PCR laboratory"
  ],
  [
    "biochemistry",
    "biochemistry enzyme laboratory"
  ],
  [
    "epigenetics",
    "epigenetics chromatin histone DNA methylation"
  ],
  [
    "systems-biology",
    "systems biology pathway network biology"
  ],
  [
    "metabolomics",
    "metabolomics chromatography mass spectrometry"
  ],
  [
    "lipidomics",
    "lipidomics mass spectrometry lipid analysis"
  ],
  [
    "glycomics",
    "glycomics glycan mass spectrometry"
  ],
  [
    "metagenomics",
    "metagenomics microbial sequencing"
  ],
  [
    "single-cell-biology",
    "single cell RNA sequencing cell atlas"
  ],
  [
    "spatial-omics",
    "spatial transcriptomics tissue microscopy"
  ],
  [
    "developmental-biology",
    "developmental biology embryo microscopy"
  ],
  [
    "stem-cell-biology",
    "stem cell culture pluripotent cells"
  ],
  [
    "microbiome-science",
    "human gut microbiome bacteria microscopy"
  ],
  [
    "regenerative-medicine",
    "regenerative medicine stem cell tissue engineering"
  ],
  [
    "microbiology",
    "bacteria microbiology microscopy"
  ],
  [
    "virology",
    "virus virion electron microscopy"
  ],
  [
    "immunology",
    "immune cells immunology antibody microscopy"
  ],
  [
    "bacteriology",
    "bacteriology bacterial culture microscopy"
  ],
  [
    "mycology",
    "mycology fungi microscopy"
  ],
  [
    "parasitology",
    "parasitology parasite microscopy"
  ],
  [
    "vaccinology",
    "vaccine research immunology laboratory"
  ],
  [
    "antimicrobial-resistance",
    "antimicrobial resistance bacteria laboratory"
  ],
  [
    "infectious-diseases",
    "infectious disease clinical microbiology"
  ],
  [
    "oncology",
    "cancer histopathology tumor microscopy"
  ],
  [
    "pharmacology",
    "pharmacology pharmaceutical laboratory research"
  ],
  [
    "medicinal-chemistry",
    "medicinal chemistry molecular drug discovery"
  ],
  [
    "enzymology",
    "enzyme assay enzymology laboratory"
  ],
  [
    "protein-engineering",
    "protein engineering laboratory protein design"
  ],
  [
    "biophysics",
    "biophysics protein binding spectroscopy"
  ],
  [
    "molecular-simulation",
    "molecular dynamics protein simulation"
  ],
  [
    "chemical-biology",
    "chemical biology fluorescent probe laboratory"
  ],
  [
    "pharmacogenomics",
    "pharmacogenomics DNA sequencing"
  ],
  [
    "clinical-pharmacology",
    "clinical pharmacology drug research"
  ],
  [
    "toxicology",
    "toxicology laboratory pathology"
  ],
  [
    "anatomy",
    "human anatomy anatomical specimen"
  ],
  [
    "physiology",
    "human physiology organ medical research"
  ],
  [
    "pathology",
    "histopathology tissue pathology microscope"
  ],
  [
    "cardiology",
    "heart cardiovascular anatomy medical imaging"
  ],
  [
    "neuroscience",
    "neuron brain neuroscience microscopy"
  ],
  [
    "endocrinology",
    "endocrinology thyroid pancreas histology"
  ],
  [
    "pulmonology",
    "lung respiratory medicine imaging"
  ],
  [
    "nephrology",
    "kidney nephrology histology"
  ],
  [
    "gastroenterology",
    "gastroenterology digestive system endoscopy"
  ],
  [
    "hepatology",
    "liver histology hepatology"
  ],
  [
    "hematology",
    "hematology blood smear microscopy"
  ],
  [
    "dermatology",
    "dermatology skin histology"
  ],
  [
    "rheumatology",
    "rheumatology joint anatomy"
  ],
  [
    "orthopedics",
    "orthopedic surgery bone anatomy"
  ],
  [
    "obstetrics",
    "obstetrics prenatal ultrasound"
  ],
  [
    "gynecology",
    "gynecology reproductive anatomy"
  ],
  [
    "pediatrics",
    "pediatrics child healthcare"
  ],
  [
    "geriatrics",
    "geriatrics elderly care research"
  ],
  [
    "ophthalmology",
    "ophthalmology retina fundus imaging"
  ],
  [
    "psychiatry",
    "psychiatry neuroscience brain imaging"
  ],
  [
    "radiology",
    "MRI medical radiology scan"
  ],
  [
    "medical-ultrasound",
    "medical ultrasound sonography"
  ],
  [
    "nuclear-medicine",
    "nuclear medicine PET scan"
  ],
  [
    "computed-tomography",
    "computed tomography CT scan"
  ],
  [
    "histology",
    "histology tissue microscope slide"
  ],
  [
    "cytology",
    "cytology cells microscope"
  ],
  [
    "laboratory-medicine",
    "clinical laboratory medicine blood testing"
  ],
  [
    "clinical-chemistry",
    "clinical chemistry laboratory analyzer"
  ],
  [
    "clinical-genetics",
    "clinical genetics karyotype genetic testing"
  ],
  [
    "medical-imaging-engineering",
    "medical imaging engineering MRI scanner"
  ],
  [
    "surgery",
    "surgical operating room medical team"
  ],
  [
    "anesthesiology",
    "anesthesiology operating room"
  ],
  [
    "emergency-medicine",
    "emergency medicine hospital trauma"
  ],
  [
    "critical-care",
    "intensive care unit hospital"
  ],
  [
    "radiation-oncology",
    "radiation oncology linear accelerator"
  ],
  [
    "pharmaceutics",
    "pharmaceutics pharmaceutical formulation"
  ],
  [
    "drug-delivery",
    "drug delivery nanoparticles research"
  ],
  [
    "rehabilitation-medicine",
    "physical rehabilitation therapy clinic"
  ],
  [
    "palliative-care",
    "palliative care healthcare team"
  ],
  [
    "preventive-medicine",
    "preventive medicine public health screening"
  ],
  [
    "public-health",
    "public health epidemiology laboratory"
  ],
  [
    "epidemiology",
    "epidemiology public health data"
  ],
  [
    "global-health",
    "global health healthcare outreach"
  ],
  [
    "clinical-research",
    "clinical research hospital laboratory"
  ],
  [
    "clinical-trials",
    "clinical trial research hospital"
  ],
  [
    "evidence-synthesis",
    "systematic review research papers"
  ],
  [
    "health-economics",
    "health economics health technology assessment"
  ],
  [
    "bioethics",
    "bioethics medical research discussion"
  ],
  [
    "biomedical-engineering",
    "biomedical engineering medical device research"
  ],
  [
    "bioinformatics",
    "bioinformatics genomic data visualization"
  ],
  [
    "medical-robotics",
    "medical robotics surgical robot"
  ],
  [
    "prosthetics",
    "prosthetic limb bionic hand"
  ],
  [
    "biomaterials",
    "biomaterials medical implant"
  ],
  [
    "bioinstrumentation",
    "bioinstrumentation biosensor laboratory"
  ],
  [
    "medical-devices",
    "medical devices hospital monitor"
  ],
  [
    "nanomedicine",
    "nanomedicine nanoparticles microscopy"
  ],
  [
    "health-informatics",
    "health informatics hospital data"
  ],
  [
    "digital-health",
    "digital health remote patient monitoring"
  ],
  [
    "artificial-intelligence-in-medicine",
    "artificial intelligence medical imaging"
  ],
  [
    "humanitarian-and-disaster-health",
    "humanitarian disaster medicine field hospital"
  ]
]

def api(params):
    url=API+"?"+urllib.parse.urlencode({"format":"json",**params})
    request=urllib.request.Request(url,headers=HEADERS)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request,timeout=45) as response: return json.load(response)
        except Exception:
            if attempt==3: raise
            time.sleep(2**attempt)
    raise RuntimeError("Wikimedia API retries exhausted")

def clean(value):
    return re.sub(r"<[^>]+>","",value or "").strip()

def find_file(term,used):
    data=api({"action":"query","generator":"search","gsrsearch":term,"gsrnamespace":6,"gsrlimit":50,
              "prop":"imageinfo","iiprop":"url|size|mime|extmetadata","iiurlwidth":1600})
    pages=(data.get("query") or {}).get("pages") or {}
    candidates=sorted(pages.values(),key=lambda p:p.get("index",10**9))
    for page in candidates:
        title=page.get("title","")
        if title in used: continue
        info=(page.get("imageinfo") or [{}])[0]
        meta=info.get("extmetadata") or {}
        def val(key): return clean((meta.get(key) or {}).get("value",""))
        license_name=val("LicenseShortName") or val("UsageTerms")
        if not LICENSE_OK.search(license_name): continue
        mime=info.get("mime","")
        if not mime.startswith("image/") or mime=="image/svg+xml": continue
        if int(info.get("width",0))<600 or int(info.get("height",0))<400: continue
        url=info.get("thumburl") or info.get("url")
        if url:
            return {"title":title,"url":url,"source_page":info.get("descriptionurl",""),
                    "license":license_name,"license_url":val("LicenseUrl"),"artist":val("Artist"),
                    "credit":val("Credit"),"description":val("ImageDescription"),
                    "original_width":info.get("width"),"original_height":info.get("height")}
    return None

def download_png(item,target):
    request=urllib.request.Request(item["url"],headers=HEADERS)
    with urllib.request.urlopen(request,timeout=90) as response: raw=response.read()
    with Image.open(BytesIO(raw)) as image: image.verify()
    with Image.open(BytesIO(raw)) as source:
        image=source.convert("RGB")
        image.thumbnail((1200,800),Image.Resampling.LANCZOS)
        if image.width<500 or image.height<300: raise ValueError("Image below minimum dimensions")
        target.parent.mkdir(parents=True,exist_ok=True)
        image.save(target,format="PNG",optimize=True)


def update_readme_gallery():
    readme_path = ROOT / "README.md"
    text = readme_path.read_text(encoding="utf-8")
    start_marker = "<!-- KINETICS_GALLERY_START -->"
    end_marker = "<!-- KINETICS_GALLERY_END -->"
    if start_marker not in text or end_marker not in text:
        raise RuntimeError("README gallery insertion markers are missing")
    cells = []
    for number, (slug, _) in enumerate(CATEGORIES, 1):
        filename = f"{number:03d}-{slug}.png"
        label = slug.replace("-", " ").title()
        cells.append(
            f'<td align="center"><img src="Assets/Future/PNG/{filename}" '
            f'width="170" alt="{label}"><br><b>{label}</b></td>'
        )
    rows = ["<table>"]
    for offset in range(0, len(cells), 4):
        rows.append("<tr>" + "".join(cells[offset:offset + 4]) + "</tr>")
    rows.append("</table>")
    gallery = chr(10).join(rows)
    left = text.index(start_marker) + len(start_marker)
    right = text.index(end_marker, left)
    updated = text[:left] + chr(10) + gallery + chr(10) + text[right:]
    readme_path.write_text(updated, encoding="utf-8")
    print("README gallery updated with all 100 local PNG images.", flush=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start",type=int,default=1)
    parser.add_argument("--end",type=int,default=100)
    parser.add_argument("--overwrite",action="store_true")
    args=parser.parse_args()
    if not 1<=args.start<=args.end<=100: parser.error("range must be within 1–100")
    OUT.mkdir(parents=True,exist_ok=True)
    previous=[]
    if MANIFEST.exists():
        try: previous=json.loads(MANIFEST.read_text(encoding="utf-8"))
        except (OSError,json.JSONDecodeError): print("Warning: old manifest unreadable",file=sys.stderr)
    records={x.get("file"):x for x in previous if x.get("file")}
    used={x.get("title") for x in previous if x.get("title")}
    for number,(slug,term) in enumerate(CATEGORIES,1):
        if not args.start<=number<=args.end: continue
        target=OUT/f"{number:03d}-{slug}.png"
        key=f"Assets/Future/PNG/{target.name}"
        if target.exists() and key in records and not args.overwrite:
            print(f"SKIP {number:03d}/100 {target.name}",flush=True); continue
        print(f"SEARCH {number:03d}/100 {slug}",flush=True)
        try:
            item=find_file(term,used)
            if not item: print("  NOT FOUND: no qualifying image"); continue
            download_png(item,target); used.add(item["title"])
            records[key]={"file":key,"number":number,"category":slug.replace("-"," ").title(),**item}
            print(f"  SAVED {target.name} ({item['license']})",flush=True)
        except Exception as exc:
            print(f"  ERROR {type(exc).__name__}: {exc}",file=sys.stderr,flush=True)
            if target.exists(): target.unlink()
        time.sleep(0.25)
    MANIFEST.parent.mkdir(parents=True,exist_ok=True)
    MANIFEST.write_text(json.dumps(sorted(records.values(),key=lambda x:x.get("number",999)),indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    present=sum((OUT/f"{i:03d}-{slug}.png").exists() for i,(slug,_) in enumerate(CATEGORIES,1))
    attributed=sum(f"Assets/Future/PNG/{i:03d}-{slug}.png" in records for i,(slug,_) in enumerate(CATEGORIES,1))
    print(f"\nPNG files present: {present}/100; attributed: {attributed}/100")
    if present<100 or attributed<100:
        print("Retry missing categories with the same command or process a range.")
        raise SystemExit(2)
    update_readme_gallery()
if __name__=="__main__": main()
