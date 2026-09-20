"""Adapters from day-specific rows to the common EvaluationRecord."""

from typing import Any

from ai_reliability.evaluation.normalize import normalize_day5
from ai_reliability.schemas import EvaluationRecord


def day01_record(row: dict[str, Any], response: str, run_id: str) -> EvaluationRecord:
    return EvaluationRecord(
        case_id=str(row["id"]), question_id=str(row["id"]), run_id=run_id,
        prompt=str(row["question"]), response=response,
        expected_answer=str(row["expected"]), metadata={"category": row.get("category")},
    )


def day02_record(row: dict[str, Any], run_id: str) -> EvaluationRecord:
    return EvaluationRecord(
        case_id="day02_consistency_prompt", run_id=str(row.get("run_id", run_id)),
        response=str(row.get("output", "")), prompt="legacy day02 repeated prompt",
    )


def day03_record(row: dict[str, Any]) -> EvaluationRecord:
    actual = str(row["actual"])
    expected = str(row["expected"])
    return EvaluationRecord(
        case_id=str(row["question_id"]), question_id=str(row["question_id"]),
        run_id=str(row["run_id"]), response=actual, expected_answer=expected,
    )


def day04_record(row: dict[str, Any]) -> EvaluationRecord:
    keys = [key.strip() for key in str(row.get("required_keys", "")).split(",") if key.strip()]
    return EvaluationRecord(
        case_id=str(row["case_id"]), response=str(row["output"]),
        metadata={"required_keys": keys},
    )


def day05_record(row: dict[str, Any]) -> EvaluationRecord:
    output = str(row["output"])
    expected = str(row["expected"])
    is_abstained = normalize_day5(output) == "unknown"
    should_abstain = str(row["answerable"]).strip().lower() == "no"
    return EvaluationRecord(
        case_id=str(row["case_id"]), response=output, expected_answer=expected,
        is_abstained=is_abstained, should_abstain=should_abstain,
        metadata={"answerable": str(row["answerable"])},
    )


def day06_record(row: dict[str, Any]) -> EvaluationRecord:
    raw_correct = str(row["correct"]).strip()
    if raw_correct not in {"0", "1"}:
        raise ValueError(f"Day 6 correct must be 0 or 1: {row['case_id']}")
    return EvaluationRecord(
        case_id=str(row["case_id"]), response="", confidence=float(row["confidence"]),
        is_correct=raw_correct == "1", metadata={"confidence_source": "synthetic_demo"},
    )
