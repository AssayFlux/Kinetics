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

        frame = pd.read_csv(args.input)
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
