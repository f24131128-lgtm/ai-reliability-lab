"""Day 3 Accuracy × Consistency matrix."""

from collections import defaultdict

from ai_reliability.evaluation.normalize import exact_match, normalize_day3
from ai_reliability.schemas import EvaluationRecord, MetricResult


def quadrant(accuracy: float, consistency: float, threshold: float = 0.8) -> str:
    accurate = accuracy >= threshold
    stable = consistency >= threshold
    if accurate and stable:
        return "又準又穩"
    if accurate and not stable:
        return "準但不穩"
    if not accurate and stable:
        return "穩但不準"
    return "又不準又不穩"


def evaluate_reliability_matrix(records: list[EvaluationRecord], threshold: float = 0.8) -> MetricResult:
    groups: dict[str, list[EvaluationRecord]] = defaultdict(list)
    for record in records:
        groups[record.question_id or record.case_id].append(record)
    per_case: list[dict[str, object]] = []
    for question_id, group in groups.items():
        expected = group[0].expected_answer or "" if group else ""
        accuracy = sum(exact_match(r.response, expected, normalize_day3) for r in group) / len(group) if group else 0.0
        normalized = [normalize_day3(r.response) for r in group]
        counts = {value: normalized.count(value) for value in set(normalized)}
        consistency = max(counts.values()) / len(normalized) if normalized else 0.0
        per_case.append({"question_id": question_id, "accuracy": accuracy, "consistency": consistency, "quadrant": quadrant(accuracy, consistency, threshold)})
    mean_accuracy = sum(float(row["accuracy"]) for row in per_case) / len(per_case) if per_case else 0.0
    mean_consistency = sum(float(row["consistency"]) for row in per_case) / len(per_case) if per_case else 0.0
    return MetricResult(
        "reliability_matrix", {"mean_accuracy": mean_accuracy, "mean_consistency": mean_consistency},
        len(per_case), per_case, ["no questions"] if not per_case else [],
        {"threshold": threshold, "threshold_note": "demo engineering threshold; not a universal standard"},
    )
