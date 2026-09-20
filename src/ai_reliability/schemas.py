"""Small, serializable schemas shared by loaders, metrics, and artifacts."""

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class EvaluationRecord:
    case_id: str
    response: str
    question_id: str | None = None
    run_id: str | None = None
    prompt: str | None = None
    expected_answer: str | None = None
    is_correct: bool | None = None
    is_abstained: bool | None = None
    should_abstain: bool | None = None
    confidence: float | None = None
    latency_ms: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class MetricResult:
    name: str
    value: Any
    denominator: int | float | None = None
    per_case: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
