"""Declarative, small quality-gate rules."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GateRule:
    metric: str
    operator: str
    threshold: float
    label: str = ""

    def evaluate(self, metrics: dict[str, Any]) -> tuple[bool, str]:
        if self.metric not in metrics:
            return False, f"missing metric: {self.metric}"
        value = metrics[self.metric].get("value") if isinstance(metrics[self.metric], dict) else metrics[self.metric]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return False, f"metric is not numeric: {self.metric}"
        comparisons = {">=": value >= self.threshold, ">": value > self.threshold, "<=": value <= self.threshold, "<": value < self.threshold, "==": value == self.threshold}
        if self.operator not in comparisons:
            return False, f"unsupported operator: {self.operator}"
        passed = comparisons[self.operator]
        return passed, self.label or f"{self.metric} {self.operator} {self.threshold}"


def rules_from_config(config: dict[str, Any]) -> list[GateRule]:
    return [GateRule(str(item["metric"]), str(item["operator"]), float(item["threshold"]), str(item.get("label", ""))) for item in config.get("quality_gate", {}).get("rules", [])]
