# Canonical kinetic observation data model

> **Project-wide direction:** Follow the authoritative [Kinetics mission](../KINETICS_MISSION.md). This module is one component of a cross-disciplinary biomedical and precision-health research platform; preserve domain semantics, provenance, uncertainty, privacy and clinical safety. The integrated scientific foundation precedes polished end-user applications; constrained Android performance is a first-class requirement.

## One row represents one measured target

A canonical observation represents exactly one value: either Km or kcat. This design is necessary because public enzyme-kinetics resources often publish target-specific tables, and two records with similar protein/substrate identifiers are not automatically matched experiments.

## Required fields

- target: km or kcat.
- value and unit: original numeric value and explicit source unit.
- source: upstream database or publication source.
- source_record_id: stable identifier in the upstream source.

## Optional contextual fields

- protein sequence and accession;
- substrate SMILES or stable chemical identifier;
- organism, strain, construct, and mutation information;
- pH, temperature, assay ID, and experimental notes;
- publication DOI, source version, and license identifier.

Absence of a field is represented as missing. The pipeline must not infer an organism, sequence, substrate structure, assay condition, or DOI from weak matches.

## Canonical units

- Km: molar (M).
- kcat: reciprocal seconds (s^-1).

The original value and unit must be preserved alongside the canonical value. Unit conversion is permitted only when the original unit is explicit and supported by the conversion table.

## Rejected records

Every curation operation should emit a row-level rejection table with source row identifier and reason. Rejected rows are not silently deleted. Curation manifests must record source file hash, mapping configuration, source version, license note, and accepted/rejected counts.


---

## Kinetics mission alignment

This document contributes to Kinetics' wider mission: connect scientific knowledge across disciplines, advance evidence-centred biomedical research, and preserve essential knowledge through resilient offline infrastructure. Its technical scope must remain aligned with the authoritative [Kinetics mission](../KINETICS_MISSION.md), expanded [vision](../VISION.md), and [emergency and humanitarian resilience requirements](EMERGENCY_HUMANITARIAN_RESILIENCE.md). Planned capabilities must not be represented as implemented or clinically validated; scientific integrity, privacy, provenance, human oversight and measurable validation remain mandatory.
