"""Command-line interface for Cron Builder."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from .core import CronError, CronExpression, build

VERSION = "1.0.0"

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cron-builder", description="Build, validate, explain and preview standard five-field cron expressions.")
    p.add_argument("--version", action="version", version=f"cron-builder {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    sub = p.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate", help="Validate an expression")
    v.add_argument("expression")
    e = sub.add_parser("explain", help="Explain an expression")
    e.add_argument("expression")
    n = sub.add_parser("next", help="Preview upcoming run times")
    n.add_argument("expression"); n.add_argument("--count", type=int, default=5); n.add_argument("--from", dest="start"); n.add_argument("--json", action="store_true")
    b = sub.add_parser("build", help="Build an expression from fields")
    for flag in ("minute","hour","day","month","weekday"):
        b.add_argument(f"--{flag}", default="*")
    return p

def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "validate":
            expr = CronExpression.parse(args.expression); print(f"valid: {expr}")
        elif args.command == "explain":
            expr = CronExpression.parse(args.expression); print(expr.explain())
        elif args.command == "build":
            print(build(args.minute, args.hour, args.day, args.month, args.weekday))
        else:
            expr = CronExpression.parse(args.expression)
            start = datetime.fromisoformat(args.start) if args.start else datetime.now().astimezone().replace(tzinfo=None)
            runs = expr.next_runs(start, args.count)
            if args.json:
                print(json.dumps({"expression": str(expr), "from": start.isoformat(), "runs": [x.isoformat() for x in runs]}, indent=2))
            else:
                for item in runs: print(item.isoformat(sep=" ", timespec="minutes"))
        return 0
    except (CronError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr); return 2

if __name__ == "__main__":
    raise SystemExit(main())
