# Seed data

> **Mission authority:** This document is governed by [KINETICS_MISSION.md](../KINETICS_MISSION.md). Kinetics is a cross-disciplinary biomedical and precision-health research platform—not only an enzyme-kinetics project. All domains, datasets, models and applications must align with the mission, preserve provenance and clinical safety, and follow the foundation-first build order. Small Android devices are a first-class performance target.

This directory contains only small, openly redistributable reference packs and their manifest.
Run `python scripts/data/fetch_seed_data.py` from the repository root to fetch the enabled
starter ontologies. Files are streamed with resumable partial downloads and SHA-256 checksums.
Large biological databases are not starter packs: use provider-specific, scoped query or bulk
download workflows after verifying the exact release license and storage requirements.

Downloaded seed files are intended to be committed only when their license and repository size
are acceptable. The generated MANIFEST.json records retrieval provenance and checksums.
