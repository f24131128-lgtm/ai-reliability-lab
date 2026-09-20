"""Day 2 consistency metrics with the legacy definitions."""

import re
from itertools import combinations
from collections import Counter

from ai_reliability.evaluation.normalize import normalize_day2
from ai_reliability.schemas import EvaluationRecord, MetricResult


def _values(records: list[EvaluationRecord]) -> tuple[list[str], list[str]]:
    raw = [record.response for record in records]
    normalized = [normalize_day2(value) for value in raw]
    pairs = [(raw_value, value) for raw_value, value in zip(raw, normalized) if value]
    return [pair[0] for pair in pairs], [pair[1] for pair in pairs]


def unique_ratio(records: list[EvaluationRecord]) -> MetricResult:
    _, values = _values(records)
    result = len(set(values)) / len(values) if values else 0.0
    return MetricResult("unique_ratio", result, len(values), [{"normalized": value} for value in values], ["no non-empty outputs"] if not values else [])


def mode_agreement(records: list[EvaluationRecord]) -> MetricResult:
    _, values = _values(records)
    count = Counter(values).most_common(1)[0][1] if values else 0
    result = count / len(values) if values else 0.0
    return MetricResult("mode_agreement", result, len(values), [{"normalized": value} for value in values], ["no non-empty outputs"] if not values else [])


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[\u4e00-\u9fff]|[A-Za-z0-9_]+", text))


def jaccard(left: str, right: str) -> float:
    first, second = _tokens(left), _tokens(right)
    if not first and not second:
        return 1.0
    if not first or not second:
        return 0.0
    return len(first & second) / len(first | second)


def pairwise_jaccard(records: list[EvaluationRecord]) -> MetricResult:
    _, values = _values(records)
    points = [jaccard(left, right) for left, right in combinations(values, 2)]
    result = sum(points) / len(points) if points else 0.0
    return MetricResult("pairwise_jaccard", result, len(points), [{"value": point} for point in points], ["fewer than two non-empty outputs"] if not points else [])


def evaluate_consistency(records: list[EvaluationRecord]) -> dict[str, MetricResult]:
    return {"unique_ratio": unique_ratio(records), "mode_agreement": mode_agreement(records), "pairwise_jaccard": pairwise_jaccard(records)}
