# Validation result manifest (JSON Schema-like contract)

Each completed benchmark writes one immutable JSON record. This YAML is a human-readable contract; the JSON output is stored alongside benchmark artifacts.

Required top-level fields:
- schema_version: string, currently "1.0"
- benchmark_id: stable identifier
- phase_id: roadmap phase such as R3 or I1
- implementation: repository, commit_sha, module, version
- environment: OS, architecture, CPU, RAM, runtime/toolchain versions, device_model when applicable
- input: dataset_id, accession_or_uri, release, license, sha256, record_count, inclusion_exclusions
- method: algorithm, parameters, random_seed, baseline, dependency_versions
- metrics: named numeric measurements with units and definitions
- uncertainty: interval/method/sample_size where applicable
- outcomes: passed, failed, unsupported, indeterminate counts and failure categories
- resources: wall_time_seconds, peak_memory_bytes, output_bytes, energy_measurement if available
- provenance: command, reproduction_script, output_sha256, ci_run_url
- review: independent_reviewer, review_date, review_notes
- limitations: list of explicit caveats
- status: software_test | reference_validated | independently_replicated | device_verified

Rules:
- Missing values are null or omitted with a reason; never use zero to mean unknown.
- A software_test record must not be described as reference_validated.
- Dataset and model license/source metadata are mandatory before redistribution.
- Keep development and held-out evaluation datasets disjoint and record the split manifest hash.
- Record all failed runs; do not retain only successful benchmark runs.
