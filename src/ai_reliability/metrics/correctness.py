"""Day 1 correctness baseline and the shared exact-match accuracy helper."""

from ai_reliability.evaluation.normalize import exact_match, normalize_day1
from ai_reliability.schemas import EvaluationRecord, MetricResult


def evaluate_exact_match(records: list[EvaluationRecord], name: str = "exact_match") -> MetricResult:
    per_case = []
    correct = 0
    for record in records:
        matched = exact_match(record.response, record.expected_answer or "", normalize_day1)
        correct += int(matched)
        per_case.append({"case_id": record.case_id, "is_correct": matched})
    warnings = ["no records"] if not records else []
    return MetricResult(name, correct / len(records) if records else 0.0, len(records), per_case, warnings)


def evaluate_accuracy(records: list[EvaluationRecord], name: str = "accuracy") -> MetricResult:
    per_case = []
    correct = 0
    for record in records:
        matched = exact_match(record.response, record.expected_answer or "", normalize_day1)
        correct += int(matched)
        per_case.append({"case_id": record.case_id, "is_correct": matched})
    warnings = ["no records"] if not records else []
    return MetricResult(name, correct / len(records) if records else 0.0, len(records), per_case, warnings)
