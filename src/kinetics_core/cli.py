"""Command-line entry points for target-specific research workflows."""

from __future__ import annotations

import argparse
import json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kinetics-research")
    subparsers = parser.add_subparsers(dest="command", required=True)

    legacy = subparsers.add_parser(
        "import-legacy",
        help="Convert a legacy paired-target CSV to canonical observations",
    )
    legacy.add_argument("--input", required=True, help="Unmodified legacy paired-row CSV")
    legacy.add_argument("--output", required=True, help="New canonical observations CSV")
    legacy.add_argument("--source", required=True, help="Dataset/source identifier")
    legacy.add_argument(
        "--source-record-id-column", required=True,
        help="Column containing stable source record IDs; IDs are never generated",
    )
    legacy.add_argument(
        "--km-unit", choices=("M", "mM", "uM", "µM", "nM"), default="mM"
    )
    legacy.add_argument(
        "--kcat-unit", choices=("s^-1", "s-1", "min^-1", "h^-1"), default="s^-1"
    )
    legacy.add_argument("--source-version")
    legacy.add_argument("--license-id")
    legacy.add_argument("--sequence-column", default="sequence")
    legacy.add_argument("--smiles-column", default="smiles")
    legacy.add_argument(
        "--overwrite", action="store_true",
        help="Replace existing output and manifest files (never the input file)",
    )

    persist = subparsers.add_parser(
        "persist", help="Audit and persist canonical observations into SQLite"
    )
    persist.add_argument("--input", required=True, help="Canonical observations CSV")
    persist.add_argument("--database", required=True, help="SQLite metadata database")
    persist.add_argument("--dataset-id", required=True, help="Immutable dataset snapshot ID")
    persist.add_argument("--name", required=True, help="Human-readable dataset name")
    persist.add_argument("--source", required=True, help="Upstream source identifier")
    persist.add_argument("--version", help="Source dataset release/version")
    persist.add_argument("--license-id", help="Verified source license identifier")
    persist.add_argument("--citation", help="Dataset citation or DOI")

    release = subparsers.add_parser(
        "release", help="Create an immutable, license-gated dataset release"
    )
    release.add_argument("--observations", required=True)
    release.add_argument(
        "--rejected", action="append", required=True,
        help="Rejection audit CSV; repeat to combine audits",
    )
    release.add_argument("--output-dir", required=True)
    release.add_argument("--dataset-id", required=True)
    release.add_argument("--dataset-name", required=True)
    release.add_argument("--source", required=True)
    release.add_argument("--source-version", required=True)
    release.add_argument("--license-id", required=True)
    release.add_argument("--citation", required=True)
    release.add_argument("--source-url")
    release.add_argument(
        "--source-manifest", action="append", default=[],
        help="Source acquisition/curation manifest; repeat as needed",
    )

    verify = subparsers.add_parser(
        "verify-release", help="Verify all dataset release artifact hashes"
    )
    verify.add_argument("--release-dir", required=True)

    identities = subparsers.add_parser(
        "normalize-identities", help="Validate sequences and canonicalize substrate SMILES"
    )
    identities.add_argument("--input", required=True)
    identities.add_argument("--output-dir", required=True)
    identities.add_argument("--sequence-column", default="sequence")
    identities.add_argument("--smiles-column", default="smiles")

    scaffolds = subparsers.add_parser(
        "annotate-scaffolds",
        help="Assign stereo-agnostic Bemis-Murcko scaffold IDs with row-level rejection audit",
    )
    scaffolds.add_argument("--input", required=True)
    scaffolds.add_argument("--output-dir", required=True)
    scaffolds.add_argument("--smiles-column", default="smiles_canonical")

    clusters = subparsers.add_parser(
        "cluster-sequences", help="Cluster validated protein sequences with MMseqs2"
    )
    clusters.add_argument("--input", required=True)
    clusters.add_argument("--output-dir", required=True)
    clusters.add_argument("--sequence-column", default="sequence")
    clusters.add_argument("--record-id-column", default="source_record_id")
    clusters.add_argument("--source-column", default="source")
    clusters.add_argument("--min-sequence-identity", type=float, default=0.4)
    clusters.add_argument("--coverage", type=float, default=0.8)
    clusters.add_argument("--threads", type=int, default=1)

    features = subparsers.add_parser(
        "build-features", help="Build versioned ESM-2, Morgan and molecular-graph features"
    )
    features.add_argument("--input", required=True)
    features.add_argument("--output", required=True)
    features.add_argument("--target", choices=("km", "kcat"), required=True)
    features.add_argument("--cache-dir", default="data/cache")
    features.add_argument("--model-name", default="facebook/esm2_t6_8M_UR50D")
    features.add_argument(
        "--model-revision",
        default="8c576d2aba1b27317e9321c8491d72f00d1b110a",
    )
    features.add_argument("--tokenizer-revision")
    features.add_argument("--device")
    features.add_argument("--max-residues", type=int, default=1022)
    features.add_argument("--radius", type=int, default=2)
    features.add_argument("--n-bits", type=int, default=2048)
    features.add_argument("--no-chirality", action="store_true")
    features.add_argument("--batch-size", type=int, default=16)
    features.add_argument("--group-column", action="append", default=[])
    features.add_argument("--overwrite", action="store_true")

    audit = subparsers.add_parser("audit")
    audit.add_argument("--input", required=True, help="Normalized observations CSV")
    audit.add_argument("--output-dir", required=True)
    audit.add_argument("--log10-tolerance", type=float, default=1e-8)

    partition = subparsers.add_parser("partition")
    partition.add_argument("--observations", required=True)
    partition.add_argument("--output-dir", required=True)
    partition.add_argument("--target", choices=("km", "kcat"), required=True)
    partition.add_argument("--protein-group-column", default="protein_cluster_id")
    partition.add_argument("--substrate-group-column", default="scaffold_id")
    partition.add_argument("--test-fraction", type=float, default=0.2)
    partition.add_argument("--calibration-fraction", type=float, default=0.2)
    partition.add_argument("--random-state", type=int, default=42)

    for command in ("compare", "fit"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--train", required=True, help="Training NPZ feature archive")
        sub.add_argument("--test", required=True, help="Untouched held-out NPZ feature archive")
        sub.add_argument("--target", choices=("km", "kcat"), required=True)
        sub.add_argument("--output-dir", required=True)
        sub.add_argument("--group-array", help="Training CV group array, e.g. protein_cluster_id")
        sub.add_argument(
            "--holdout-group-array", action="append", default=[],
            help="Repeat for every required train/test leakage-check axis",
        )
        sub.add_argument("--random-state", type=int, default=42)
        sub.add_argument("--n-splits", type=int, default=5)
        if command == "fit":
            sub.add_argument("--calibration-archive")
            sub.add_argument("--conformal-alpha", type=float, default=0.1)
            sub.add_argument("--n-estimators", type=int, default=500)
            sub.add_argument("--max-depth", type=int, default=6)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "import-legacy":
        from pathlib import Path

        import pandas as pd

        from . import __version__
        from .legacy import paired_frame_to_records
        from .provenance import environment_record, file_record, write_json_atomic

        input_path = Path(args.input)
        output_path = Path(args.output)
        manifest_path = output_path.with_suffix(output_path.suffix + ".manifest.json")
        temporary_path = output_path.with_name(f".{output_path.name}.tmp")
        generated_paths = (output_path, manifest_path, temporary_path)
        if input_path.resolve() in {path.resolve() for path in generated_paths}:
            raise ValueError("Input path must differ from every generated output path.")
        if not args.overwrite and any(path.exists() for path in generated_paths):
            raise FileExistsError(
                "Output, manifest, or temporary file already exists; "
                "pass --overwrite to replace it."
            )

        # Preserve opaque identifiers (including leading zeroes) as text.
        source_frame = pd.read_csv(
            input_path, dtype={args.source_record_id_column: "string"}
        )
        records = paired_frame_to_records(
            source_frame,
            source=args.source,
            source_record_id_column=args.source_record_id_column,
            km_unit=args.km_unit,
            kcat_unit=args.kcat_unit,
            source_version=args.source_version,
            license_id=args.license_id,
            sequence_column=args.sequence_column,
            smiles_column=args.smiles_column,
        )
        output_frame = pd.DataFrame.from_records(records)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            output_frame.to_csv(temporary_path, index=False)
            temporary_path.replace(output_path)
        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise

        result = {
            "workflow": "legacy_paired_csv_to_canonical_observations",
            "source": args.source,
            "source_version": args.source_version,
            "license_id": args.license_id,
            "source_record_id_column": args.source_record_id_column,
            "input": file_record(input_path),
            "output": file_record(output_path),
            "n_input_rows": int(len(source_frame)),
            "n_observations": int(len(output_frame)),
            "target_counts": {
                str(key): int(value)
                for key, value in output_frame["target"].value_counts().items()
            },
            "units": {"km": args.km_unit, "kcat": args.kcat_unit},
            "kinetics_version": __version__,
            "environment": environment_record(),
        }
        write_json_atomic(result, manifest_path)
    elif args.command == "persist":
        from .persistence import persist_observation_csv

        result = persist_observation_csv(
            args.input, args.database,
            dataset_id=args.dataset_id, name=args.name, source=args.source,
            version=args.version, license_id=args.license_id, citation=args.citation,
        )
    elif args.command == "release":
        from .release import create_dataset_release

        result = create_dataset_release(
            args.observations, args.rejected, args.output_dir,
            dataset_id=args.dataset_id, dataset_name=args.dataset_name,
            source=args.source, source_version=args.source_version,
            license_id=args.license_id, citation=args.citation,
            source_url=args.source_url, source_manifests=args.source_manifest,
        )
    elif args.command == "verify-release":
        from .release import verify_dataset_release

        result = verify_dataset_release(args.release_dir)
    elif args.command == "normalize-identities":
        import shutil
        import tempfile
        from pathlib import Path

        import pandas as pd

        from .identity import normalize_biomolecular_identities
        from .provenance import environment_record, file_record, write_json_atomic

        input_path = Path(args.input).resolve()
        output = Path(args.output_dir).resolve()
        if not input_path.is_file():
            raise FileNotFoundError(input_path)
        if output.exists():
            raise FileExistsError("Identity output directory exists; choose a new directory")
        if output == input_path.parent or output in input_path.parents:
            raise ValueError("Identity output directory must not contain the source file")
        frame = pd.read_csv(input_path, dtype={"source_record_id": "string"})
        accepted, rejected = normalize_biomolecular_identities(
            frame, sequence_column=args.sequence_column, smiles_column=args.smiles_column
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=output.parent))
        try:
            accepted_path = staging / "observations_with_identities.csv"
            rejected_path = staging / "identity_rejected_rows.csv"
            accepted.to_csv(accepted_path, index=False)
            rejected.to_csv(rejected_path, index=False)
            manifest = {
                "workflow": "biomolecular_identity_normalization",
                "input": file_record(input_path),
                "outputs": {
                    path.name: {
                        "sha256": file_record(path)["sha256"],
                        "size_bytes": path.stat().st_size,
                    }
                    for path in (accepted_path, rejected_path)
                },
                "input_rows": int(len(frame)),
                "accepted_rows": int(len(accepted)),
                "rejected_rows": int(len(rejected)),
                "identity_policy": (
                    "Sequence and stereochemistry-preserving canonical SMILES content hashes "
                    "are internal identities, not external database accessions."
                ),
                "environment": environment_record(),
            }
            write_json_atomic(manifest, staging / "identity_manifest.json")
            staging.rename(output)
        except Exception:
            shutil.rmtree(staging, ignore_errors=True)
            raise
        result = {
            "output_dir": str(output),
            "accepted_rows": int(len(accepted)),
            "rejected_rows": int(len(rejected)),
        }
    elif args.command == "annotate-scaffolds":
        import shutil
        import tempfile
        from pathlib import Path

        import pandas as pd
        from rdkit import rdBase

        from .chemistry import annotate_scaffolds_audited
        from .provenance import environment_record, file_record, write_json_atomic

        input_path = Path(args.input).resolve()
        output = Path(args.output_dir).resolve()
        if not input_path.is_file():
            raise FileNotFoundError(input_path)
        if output.exists():
            raise FileExistsError("Scaffold output directory already exists")
        if output == input_path.parent or output in input_path.parents:
            raise ValueError("Scaffold output directory must not contain the input file")
        frame = pd.read_csv(input_path, dtype={"source_record_id": "string"})
        accepted, rejected = annotate_scaffolds_audited(
            frame, smiles_column=args.smiles_column
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(
            prefix=f".{output.name}.staging-", dir=output.parent
        ))
        try:
            accepted_path = staging / "observations_with_scaffolds.csv"
            rejected_path = staging / "scaffold_rejected_rows.csv"
            accepted.to_csv(accepted_path, index=False)
            rejected.to_csv(rejected_path, index=False)
            manifest = {
                "workflow": "murcko_scaffold_annotation",
                "input": file_record(input_path),
                "outputs": {
                    item.name: {
                        "size_bytes": item.stat().st_size,
                        "sha256": file_record(item)["sha256"],
                    }
                    for item in (accepted_path, rejected_path)
                },
                "input_rows": len(frame),
                "accepted_rows": len(accepted),
                "rejected_rows": len(rejected),
                "rdkit_version": rdBase.rdkitVersion,
                "stereochemistry_policy": (
                    "Scaffold grouping ignores stereochemistry; molecular features "
                    "retain stereochemistry. No salt or tautomer normalization."
                ),
                "environment": environment_record(),
            }
            write_json_atomic(manifest, staging / "scaffold_manifest.json")
            staging.rename(output)
        except Exception:
            shutil.rmtree(staging, ignore_errors=True)
            raise
        result = {
            "output_dir": str(output),
            "accepted_rows": len(accepted),
            "rejected_rows": len(rejected),
        }
    elif args.command == "cluster-sequences":
        from pathlib import Path

        import pandas as pd

        from .provenance import file_record, write_json_atomic
        from .sequence_clustering import cluster_sequences

        input_path = Path(args.input).resolve()
        output = Path(args.output_dir).resolve()
        if not input_path.is_file():
            raise FileNotFoundError(input_path)
        if output.exists():
            raise FileExistsError("Sequence-cluster output directory already exists")
        if output == input_path.parent or output in input_path.parents:
            raise ValueError("Sequence-cluster output directory must not contain the input file")
        csv_dtypes = {args.record_id_column: "string"}
        if args.source_column:
            csv_dtypes[args.source_column] = "string"
        frame = pd.read_csv(input_path, dtype=csv_dtypes)
        if "protein_cluster_id" in frame.columns:
            raise ValueError("Input already contains protein_cluster_id")
        mapping_path, manifest_path = cluster_sequences(
            frame,
            sequence_column=args.sequence_column,
            record_id_column=args.record_id_column,
            source_column=args.source_column or None,
            output_dir=output,
            min_sequence_identity=args.min_sequence_identity,
            coverage=args.coverage,
            threads=args.threads,
        )
        mapping_dtypes = {
            "source_record_id": "string",
            "cluster_representative_record_id": "string",
            "source": "string",
            "cluster_representative_source": "string",
        }
        mapping = pd.read_csv(mapping_path, dtype=mapping_dtypes)
        left_join_columns = [args.record_id_column]
        right_join_columns = ["source_record_id"]
        if (
            args.source_column
            and args.source_column in frame.columns
            and "source" in mapping.columns
        ):
            left_join_columns.insert(0, args.source_column)
            right_join_columns.insert(0, "source")
        clustered = frame.merge(
            mapping,
            left_on=left_join_columns,
            right_on=right_join_columns,
            how="left",
            validate="many_to_one",
        )
        if clustered["cluster_representative_record_id"].isna().any():
            raise RuntimeError("Cluster mapping failed to assign every source record")
        if "cluster_representative_source" in clustered.columns:
            clustered["protein_cluster_id"] = [
                json.dumps([source, record_id], separators=(",", ":"))
                for source, record_id in zip(
                    clustered["cluster_representative_source"],
                    clustered["cluster_representative_record_id"],
                    strict=True,
                )
            ]
        else:
            clustered["protein_cluster_id"] = (
                clustered["cluster_representative_record_id"].astype(str)
            )
        clustered_path = output / "observations_with_protein_clusters.csv"
        clustered.to_csv(clustered_path, index=False)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["source_observations"] = file_record(input_path)
        manifest["clustered_observations"] = file_record(clustered_path)
        manifest["clustered_observations_all_assigned"] = (
            len(clustered) == len(frame)
        )
        write_json_atomic(manifest, manifest_path)
        result = {
            "input": file_record(input_path),
            "mapping": file_record(mapping_path),
            "clustered_observations": file_record(clustered_path),
            "manifest": str(manifest_path),
        }
    elif args.command == "build-features":
        from pathlib import Path

        import pandas as pd

        from .features import ObservationFeatureBuilder
        from .provenance import file_record, write_json_atomic

        input_path = Path(args.input).resolve()
        output_path = Path(args.output).resolve()
        manifest_path = output_path.with_suffix(
            output_path.suffix + ".manifest.json"
        )
        if not input_path.is_file():
            raise FileNotFoundError(input_path)
        if input_path in {output_path, manifest_path}:
            raise ValueError("Feature outputs must differ from the input file")
        if not args.overwrite and (
            output_path.exists() or manifest_path.exists()
        ):
            raise FileExistsError(
                "Feature archive or manifest exists; pass --overwrite to replace"
            )
        frame = pd.read_csv(input_path, dtype={"source_record_id": "string"})
        builder = ObservationFeatureBuilder(
            model_name=args.model_name,
            model_revision=args.model_revision,
            tokenizer_revision=args.tokenizer_revision,
            device=args.device,
            max_residues=args.max_residues,
            cache_dir=args.cache_dir,
            radius=args.radius,
            n_bits=args.n_bits,
            include_chirality=not args.no_chirality,
        )
        archive = builder.transform_frame(
            frame,
            target=args.target,
            output_path=output_path,
            group_columns=tuple(args.group_column),
            batch_size=args.batch_size,
        )
        feature_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        feature_manifest["source_input"] = file_record(input_path)
        write_json_atomic(feature_manifest, manifest_path)
        result = {
            "input": file_record(input_path),
            "archive": file_record(archive),
            "manifest": str(manifest_path),
            "target": args.target,
        }
    elif args.command == "partition":
        from .partition import prepare_target_partitions

        result = prepare_target_partitions(
            args.observations, args.output_dir, target=args.target,
            protein_group_column=args.protein_group_column,
            substrate_group_column=args.substrate_group_column,
            test_fraction=args.test_fraction,
            calibration_fraction=args.calibration_fraction,
            random_state=args.random_state,
        )
    elif args.command == "audit":
        from pathlib import Path

        import pandas as pd

        from .provenance import write_json_atomic
        from .quality import audit_observations

        frame = pd.read_csv(args.input, dtype={"source_record_id": "string"})
        annotated, duplicates, report = audit_observations(
            frame, log10_tolerance=args.log10_tolerance
        )
        output = Path(args.output_dir)
        output.mkdir(parents=True, exist_ok=True)
        annotated.to_csv(output / "observations_audited.csv", index=False)
        duplicates.to_csv(output / "duplicate_audit.csv", index=False)
        write_json_atomic(report, output / "quality_report.json")
        result = report
    elif args.command == "compare":
        from .benchmark import compare_regressors

        result = compare_regressors(
            args.train, args.test, target=args.target, output_dir=args.output_dir,
            group_array=args.group_array,
            holdout_group_arrays=tuple(args.holdout_group_array),
            random_state=args.random_state, n_splits=args.n_splits,
        )
    else:
        from .modeling import fit_target_model

        result = fit_target_model(
            args.train, args.test, target=args.target, output_dir=args.output_dir,
            group_array=args.group_array,
            holdout_group_arrays=tuple(args.holdout_group_array),
            random_state=args.random_state, n_splits=args.n_splits,
            calibration_archive=args.calibration_archive,
            conformal_alpha=args.conformal_alpha,
            n_estimators=args.n_estimators, max_depth=args.max_depth,
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
