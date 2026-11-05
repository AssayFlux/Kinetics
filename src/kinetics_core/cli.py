"""Command-line entry points for target-specific research workflows."""

from __future__ import annotations

import argparse
import json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kinetics-research")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit")
    audit.add_argument("--input", required=True, help="Normalized observations CSV")
    audit.add_argument("--output-dir", required=True)
    audit.add_argument("--log10-tolerance", type=float, default=1e-8)

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
    if args.command == "audit":
        from pathlib import Path
        import pandas as pd
        from .quality import audit_observations
        from .provenance import write_json_atomic

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
