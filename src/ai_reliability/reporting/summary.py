"""Human-readable summaries built from existing artifact files."""

from typing import Any


def render_summary(metadata: dict[str, Any], metrics: dict[str, Any], gate: dict[str, Any]) -> str:
    lines = [
        f"run_id: {metadata.get('run_id')}",
        f"mode: {metadata.get('mode')} ({metadata.get('data_classification')})",
        f"dataset: {metadata.get('dataset')}",
        f"quality_gate: {gate.get('decision')}",
    ]
    for name, result in metrics.items():
        lines.append(f"{name}: {result.get('value')}")
    if gate.get("reasons"):
        lines.append("gate_reasons: " + "; ".join(gate["reasons"]))
    return "\n".join(lines)
