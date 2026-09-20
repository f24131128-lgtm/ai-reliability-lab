"""Orchestrate the small Day 1–Day 6 demo pipeline."""

from pathlib import Path
from typing import Any

from ai_reliability.evaluation.records import day01_record, day02_record, day03_record, day04_record, day05_record, day06_record
from ai_reliability.io import artifact_dir, git_commit, new_run_id, read_csv, read_json, read_jsonl, resolve_dataset, utc_timestamp, write_json, write_jsonl
from ai_reliability.metrics.abstention import evaluate_abstention
from ai_reliability.metrics.aggregation import evaluate_reliability_matrix
from ai_reliability.metrics.consistency import evaluate_consistency
from ai_reliability.metrics.correctness import evaluate_exact_match
from ai_reliability.metrics.format_compliance import evaluate_format
from ai_reliability.metrics.risk_coverage import evaluate_risk_coverage
from ai_reliability.quality_gate.engine import evaluate_gate
from ai_reliability.quality_gate.rules import rules_from_config
from ai_reliability.reporting.summary import render_summary


def _load_day_records(repo_root: Path, mode: str, config: dict[str, Any], run_id: str) -> tuple[dict[str, list], dict[str, str]]:
    records: dict[str, list] = {}
    resolved: dict[str, str] = {}
    for day, configured in config["dataset"].items():
        path = resolve_dataset(repo_root, mode, str(configured))
        resolved[day] = str(path.relative_to(repo_root))
        if day == "day01":
            rows = read_jsonl(path)
            outputs = config.get("day01_mock_outputs", {})
            records[day] = []
            for row in rows:
                question_id = row["id"]
                if question_id not in outputs:
                    raise ValueError(f"Missing Day 1 mock output for question id: {question_id}")
                records[day].append(day01_record(row, str(outputs[question_id]), run_id))
        elif day == "day02":
            records[day] = [day02_record(row, run_id) for row in read_csv(path)]
        elif day == "day03":
            records[day] = [day03_record(row) for row in read_csv(path)]
        elif day == "day04":
            records[day] = [day04_record(row) for row in read_csv(path)]
        elif day == "day05":
            records[day] = [day05_record(row) for row in read_csv(path)]
        elif day == "day06":
            records[day] = [day06_record(row) for row in read_csv(path)]
        else:
            raise ValueError(f"Unsupported dataset key: {day}")
    return records, resolved


def _calculate_metrics(records: dict[str, list], config: dict[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    results["day01_exact_match"] = evaluate_exact_match(records["day01"], "day01_exact_match")
    for name, result in evaluate_consistency(records["day02"]).items():
        results[f"day02_{name}"] = result
    results["day03_reliability_matrix"] = evaluate_reliability_matrix(records["day03"], float(config.get("reliability_threshold", 0.8)))
    results["day04_format_pass_rate"] = evaluate_format(records["day04"], "day04_format_pass_rate")
    for name, result in evaluate_abstention(records["day05"]).items():
        results[f"day05_{name}"] = result
    results["day06_risk_coverage"] = evaluate_risk_coverage(records["day06"])
    return results


def run_pipeline(repo_root: Path, mode: str = "demo", config_path: str = "configs/demo.json", artifacts_root: str = "artifacts") -> tuple[Path, str]:
    config = read_json(repo_root / config_path)
    if config.get("mode") != mode:
        raise ValueError(f"Config mode {config.get('mode')!r} does not match requested mode {mode!r}")
    run_id = new_run_id()
    day_records, resolved_datasets = _load_day_records(repo_root, mode, config, run_id)
    results = _calculate_metrics(day_records, config)
    metrics_json = {name: result.to_dict() for name, result in results.items()}
    gate = evaluate_gate(metrics_json, rules_from_config(config))
    output = artifact_dir(repo_root, artifacts_root, mode, run_id)
    all_records = [record.to_dict() for day in day_records.values() for record in day]
    metadata = {
        "run_id": run_id,
        "mode": mode,
        "timestamp": utc_timestamp(),
        "dataset": resolved_datasets,
        "git_commit": git_commit(repo_root),
        "config": config,
        "synthetic": mode == "demo",
        "data_classification": "synthetic_demo" if mode == "demo" else "real_public",
        "confidence_note": "synthetic demo confidence; not calibrated confidence" if mode == "demo" else "confidence source is dataset-defined; calibration is not implemented",
    }
    write_json(output / "metadata.json", metadata)
    write_jsonl(output / "records.jsonl", all_records)
    write_json(output / "metrics.json", metrics_json)
    write_json(output / "gate.json", {"run_id": run_id, **gate})
    return output, render_summary(metadata, metrics_json, gate)


def load_artifacts(repo_root: Path, mode: str, run_id: str, artifacts_root: str = "artifacts") -> tuple[Path, dict[str, Any], dict[str, Any], dict[str, Any]]:
    output = (repo_root / artifacts_root / mode / run_id).resolve()
    root = (repo_root / artifacts_root).resolve()
    if root not in output.parents or not output.is_dir():
        raise FileNotFoundError(f"Artifact run not found: {output}")
    return output, read_json(output / "metadata.json"), read_json(output / "metrics.json"), read_json(output / "gate.json")


def report_run(repo_root: Path, mode: str, run_id: str, artifacts_root: str = "artifacts") -> str:
    _, metadata, metrics, gate = load_artifacts(repo_root, mode, run_id, artifacts_root)
    return render_summary(metadata, metrics, gate)


def gate_run(repo_root: Path, mode: str, run_id: str, config_path: str, artifacts_root: str = "artifacts") -> str:
    output, metadata, metrics, _ = load_artifacts(repo_root, mode, run_id, artifacts_root)
    config = read_json(repo_root / config_path)
    gate = evaluate_gate(metrics, rules_from_config(config))
    write_json(output / "gate.json", {"run_id": run_id, **gate})
    return render_summary(metadata, metrics, gate)
