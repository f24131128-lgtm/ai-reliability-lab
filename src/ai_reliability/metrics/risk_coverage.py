"""Day 6 observed-threshold risk–coverage calculation."""

from ai_reliability.schemas import EvaluationRecord, MetricResult


def evaluate_risk_coverage(records: list[EvaluationRecord]) -> MetricResult:
    usable = [record for record in records if record.confidence is not None and record.is_correct is not None]
    thresholds = sorted({float(record.confidence) for record in usable}, reverse=True)
    points = []
    total = len(usable)
    for threshold in thresholds:
        selected = [record for record in usable if float(record.confidence) >= threshold]
        errors = sum(not bool(record.is_correct) for record in selected)
        points.append({"threshold": threshold, "coverage": len(selected) / total if total else 0.0, "risk": errors / len(selected) if selected else 0.0, "selected": len(selected), "errors": errors})
    return MetricResult(
        "risk_coverage", points, len(points), points, ["no usable confidence records"] if not usable else [],
        {"threshold_source": "observed confidence values", "confidence_note": "synthetic demo confidence; not calibrated confidence"},
    )
