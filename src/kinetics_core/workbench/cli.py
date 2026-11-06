"""Start the Kinetics local research workbench."""

from __future__ import annotations

import argparse
import os

import uvicorn


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="kinetics-workbench")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--workspace",
        help="Workspace directory (defaults to KINETICS_WORKSPACE or ~/.kinetics/workspace)",
    )
    parser.add_argument(
        "--database",
        help="Metadata database (defaults to KINETICS_DATABASE or ~/.kinetics/kinetics.sqlite3)",
    )
    args = parser.parse_args(argv)
    if not 1024 <= args.port <= 65535:
        parser.error("--port must be between 1024 and 65535")
    if args.workspace:
        os.environ["KINETICS_WORKSPACE"] = args.workspace
    if args.database:
        os.environ["KINETICS_DATABASE"] = args.database
    from .app import create_app

    uvicorn.run(
        create_app(), host="127.0.0.1", port=args.port, reload=False, access_log=True
    )
    return 0
