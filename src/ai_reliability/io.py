"""Plain JSON, JSONL, CSV, and artifact I/O."""

import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]


def git_commit(repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-c", f"safe.directory={repo_root}", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def resolve_dataset(repo_root: Path, mode: str, configured_path: str) -> Path:
    expected_root = (repo_root / "data" / mode).resolve()
    candidate = (repo_root / configured_path).resolve()
    if candidate != expected_root and expected_root not in candidate.parents:
        raise ValueError(f"Dataset must stay under data/{mode}/: {configured_path}")
    if not candidate.is_file():
        raise FileNotFoundError(f"Dataset not found: {candidate}")
    return candidate


def artifact_dir(repo_root: Path, artifacts_root: str, mode: str, run_id: str) -> Path:
    root = (repo_root / artifacts_root).resolve()
    output = (root / mode / run_id).resolve()
    if root not in output.parents:
        raise ValueError("Artifact path escaped artifacts root")
    output.mkdir(parents=True, exist_ok=False)
    return output
