"""Gate engine that consumes metrics and does not recalculate them."""

from typing import Any

from ai_reliability.quality_gate.rules import GateRule


def evaluate_gate(metrics: dict[str, Any], rules: list[GateRule]) -> dict[str, Any]:
    results = []
    for rule in rules:
        passed, message = rule.evaluate(metrics)
        results.append({"metric": rule.metric, "operator": rule.operator, "threshold": rule.threshold, "passed": passed, "message": message})
    blocked_reasons = [result["message"] for result in results if not result["passed"]]
    return {"decision": "PASS" if not blocked_reasons and results else "BLOCK", "passed": not blocked_reasons and bool(results), "reasons": blocked_reasons, "rules": results}
