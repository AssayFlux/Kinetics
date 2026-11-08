#!/usr/bin/env python3
"""Generate a transparent SPDX 2.3 inventory of declared direct source dependencies.

This is not a resolved/transitive SBOM. Unresolved versions and licenses are explicitly
NOASSERTION; release packaging must additionally resolve and audit every artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPDX_LICENSE = "CC0-1.0"


def generate(root: Path = ROOT) -> dict[str, object]:
    packages: dict[tuple[str, str], dict[str, object]] = {}

    def add(name: str, version: str, ecosystem: str, purl: str | None = None) -> None:
        key = (name.casefold(), version)
        if key in packages:
            return
        item: dict[str, object] = {
            "name": name, "SPDXID": f"SPDXRef-Package-{len(packages) + 1}",
            "versionInfo": version, "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False, "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION", "copyrightText": "NOASSERTION",
            "primaryPackagePurpose": "APPLICATION",
        }
        if purl:
            item["externalRefs"] = [{
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl", "referenceLocator": purl,
            }]
        packages[key] = item

    gradle_app = (root / "android/app/build.gradle.kts").read_text(encoding="utf-8")
    gradle_root = (root / "android/build.gradle.kts").read_text(encoding="utf-8")
    for source in (gradle_root, gradle_app):
        for group, artifact, version in re.findall(
            r'(?:"|id\()"([A-Za-z0-9_.-]+):([A-Za-z0-9_.-]+):([A-Za-z0-9_.+-]+)(?:"|\))',
            source,
        ):
            add(f"{group}:{artifact}", version, "maven",
                f"pkg:maven/{group}/{artifact}@{version}")
        for plugin, version in re.findall(
            r'id\("([A-Za-z0-9_.-]+)"\) version "([^"]+)"', source,
        ):
            add(plugin, version, "gradle-plugin", f"pkg:generic/{plugin}@{version}")

    bom = re.search(r'compose-bom:([0-9.]+)', gradle_app)
    bom_version = bom.group(1) if bom else "NOASSERTION"
    for group, artifact in re.findall(
        r'implementation\("([A-Za-z0-9_.-]+):([A-Za-z0-9_.-]+)"\)', gradle_app,
    ):
        add(f"{group}:{artifact}", f"managed-by-compose-bom-{bom_version}", "maven",
            f"pkg:maven/{group}/{artifact}")

    for versioned_name in re.findall(r'install\("([^"]+)"\)', gradle_app):
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)==([^=]+)", versioned_name)
        if match:
            name, version = match.groups()
            add(name, version, "pypi", f"pkg:pypi/{name}@{version}")

    for line in (root / "requirements-dev.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith(("-", "http")):
            continue
        match = re.match(r"([A-Za-z0-9_.-]+)(?:\[[^]]+\])?\s*(.*)", line)
        if match:
            name, constraint = match.groups()
            add(name, constraint.strip() or "UNPINNED", "pypi",
                f"pkg:pypi/{name}")

    cargo = root / "android/native-rust/Cargo.toml"
    if cargo.is_file():
        section = ""
        for line in cargo.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                section = stripped
            elif section == "[dependencies]" and "=" in stripped:
                name, value = (part.strip() for part in stripped.split("=", 1))
                version = value.strip('"')
                add(name, version, "cargo", f"pkg:cargo/{name}@{version}")

    ordered = sorted(packages.values(), key=lambda item: str(item["name"]).casefold())
    for index, package in enumerate(ordered, 1):
        package["SPDXID"] = f"SPDXRef-Package-{index}"
    identity = "\n".join(
        f"{item['name']}@{item['versionInfo']}" for item in ordered
    )
    namespace_hash = hashlib.sha256(identity.encode()).hexdigest()
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "spdxVersion": "SPDX-2.3", "dataLicense": SPDX_LICENSE,
        "SPDXID": "SPDXRef-DOCUMENT", "name": "Kinetics declared direct dependencies",
        "documentNamespace": f"https://assayflux.github.io/Kinetics/sbom/{namespace_hash}",
        "creationInfo": {
            "creators": ["Tool: kinetics-source-sbom-generator"],
            "created": now,
            "comment": "Static declared-dependency inventory; not a resolved transitive release SBOM.",
        },
        "packages": ordered,
        "relationships": [{
            "spdxElementId": "SPDXRef-DOCUMENT", "relationshipType": "DESCRIBES",
            "relatedSpdxElement": item["SPDXID"],
        } for item in ordered],
        "annotations": [{
            "annotationDate": now, "annotationType": "OTHER",
            "annotator": "Tool: kinetics-source-sbom-generator",
            "comment": (
                "Direct declarations only. Gradle BOM-managed modules are not resolved here. "
                "Transitive artifacts, exact resolved versions, checksums, file-level licenses "
                "and native binary contents are not included. Do not use as the final release SBOM."
            ),
        }],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "sbom/source-dependencies.spdx.json")
    args = parser.parse_args()
    document = generate(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote declared-dependency SPDX inventory: {args.output}")
    print("WARNING: this is not a resolved transitive release SBOM.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
