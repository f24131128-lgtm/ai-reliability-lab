"""Day 4 strict JSON format compliance."""

import json

from ai_reliability.schemas import EvaluationRecord, MetricResult


def check_json_format(response: str, required_keys: list[str]) -> tuple[bool, str]:
    try:
        parsed = json.loads(response.strip())
    except json.JSONDecodeError:
        return False, "invalid_json_or_extra_text"
    if not isinstance(parsed, dict):
        return False, "json_object_required"
    missing = [key for key in required_keys if key not in parsed]
    if missing:
        return False, "missing_keys:" + ",".join(missing)
    return True, "valid"


def evaluate_format(records: list[EvaluationRecord], name: str = "format_pass_rate") -> MetricResult:
    per_case = []
    passed = 0
    for record in records:
        valid, reason = check_json_format(record.response, list(record.metadata.get("required_keys", [])))
        passed += int(valid)
        per_case.append({"case_id": record.case_id, "passed": valid, "reason": reason})
    return MetricResult(name, passed / len(records) if records else 0.0, len(records), per_case, ["no records"] if not records else [])
