"""Day 7 synthetic calibration metrics and reliability-bin data."""

import math
from collections.abc import Iterable

from ai_reliability.schemas import EvaluationRecord, MetricResult


def _validate_record(record: EvaluationRecord) -> None:
    if record.confidence is None or not math.isfinite(float(record.confidence)):
        raise ValueError(f"Calibration confidence must be finite: {record.case_id}")
    if not 0.0 <= float(record.confidence) <= 1.0:
        raise ValueError(f"Calibration confidence must be within [0, 1]: {record.case_id}")
    if record.is_correct not in {True, False}:
        raise ValueError(f"Calibration correctness must be boolean: {record.case_id}")


def _empty_bin(index: int, n_bins: int) -> dict[str, float | int | None]:
    return {
        "lower_bound": index / n_bins,
        "upper_bound": (index + 1) / n_bins,
        "count": 0,
        "mean_confidence": None,
        "empirical_accuracy": None,
        "absolute_gap": None,
    }


def reliability_bins(records: Iterable[EvaluationRecord], n_bins: int = 5) -> list[dict[str, float | int | None]]:
    if n_bins <= 0:
        raise ValueError("n_bins must be positive")
    bins = [_empty_bin(index, n_bins) for index in range(n_bins)]
    grouped: list[list[EvaluationRecord]] = [[] for _ in range(n_bins)]
    for record in records:
        _validate_record(record)
        index = min(int(float(record.confidence) * n_bins), n_bins - 1)
        grouped[index].append(record)
    for index, group in enumerate(grouped):
        if not group:
            continue
        mean_confidence = sum(float(record.confidence) for record in group) / len(group)
        empirical_accuracy = sum(int(bool(record.is_correct)) for record in group) / len(group)
        bins[index].update({
            "count": len(group),
            "mean_confidence": mean_confidence,
            "empirical_accuracy": empirical_accuracy,
            "absolute_gap": abs(empirical_accuracy - mean_confidence),
        })
    return bins


def evaluate_calibration(
    records: list[EvaluationRecord],
    n_bins: int = 5,
    name: str = "calibration",
) -> MetricResult:
    if n_bins <= 0:
        raise ValueError("n_bins must be positive")
    for record in records:
        _validate_record(record)
    total = len(records)
    accuracy = sum(int(bool(record.is_correct)) for record in records) / total if total else 0.0
    mean_confidence = sum(float(record.confidence) for record in records) / total if total else 0.0
    confidence_gap = mean_confidence - accuracy
    brier_score = sum((float(record.confidence) - int(bool(record.is_correct))) ** 2 for record in records) / total if total else 0.0
    bins = reliability_bins(records, n_bins)
    ece = sum((int(item["count"]) / total) * float(item["absolute_gap"]) for item in bins if item["count"] and total) if total else 0.0
    value = {
        "accuracy": accuracy,
        "mean_confidence": mean_confidence,
        "confidence_gap": confidence_gap,
        "brier_score": brier_score,
        "ece": ece,
        "n_bins": n_bins,
        "reliability_bins": bins,
    }
    return MetricResult(
        name, value, total, bins, ["no records"] if not records else [],
        {
            "binning": "equal-width bins over [0, 1]",
            "boundary_policy": "min(int(confidence * n_bins), n_bins - 1)",
            "confidence_note": "synthetic demo confidence; not calibrated real LLM confidence",
            "brier_note": "Brier Score is a probabilistic scoring rule, not a calibration-only metric",
        },
    )
