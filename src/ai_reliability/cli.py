"""Minimal CLI: run, report, gate."""

import argparse
from pathlib import Path

from ai_reliability.runner import gate_run, report_run, run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="airlab", description="AI Reliability Lab Foundation v1")
    parser.add_argument("--repo-root", default=".")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="run the configured evaluation pipeline")
    run.add_argument("--mode", choices=["demo", "real"], default="demo")
    run.add_argument("--config", default="configs/demo.json")
    run.add_argument("--artifacts-root", default="artifacts")

    for command in ("report", "gate"):
        child = subparsers.add_parser(command, help=f"{command} an existing artifact run")
        child.add_argument("--mode", choices=["demo", "real"], default="demo")
        child.add_argument("--run-id", required=True)
        child.add_argument("--artifacts-root", default="artifacts")
        if command == "gate":
            child.add_argument("--config", default="configs/demo.json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    if args.command == "run":
        output, summary = run_pipeline(repo_root, args.mode, args.config, args.artifacts_root)
        print(summary)
        print(f"artifacts: {output}")
    elif args.command == "report":
        print(report_run(repo_root, args.mode, args.run_id, args.artifacts_root))
    elif args.command == "gate":
        print(gate_run(repo_root, args.mode, args.run_id, args.config, args.artifacts_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
