"""Command-line search interface for the Kinetics knowledge corpus."""
from __future__ import annotations

import argparse
import json

from kinetics_core.knowledge import KnowledgeStore


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="FTS5 query, e.g. 'cardiac AND imaging'")
    parser.add_argument("--database", default="data/kinetics.sqlite3")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--domain")
    args = parser.parse_args()
    store = KnowledgeStore(args.database)
    print(json.dumps(store.search(args.query, limit=args.limit, domain=args.domain),
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
