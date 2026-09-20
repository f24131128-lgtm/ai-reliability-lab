# Foundation v1 architecture

Foundation v1 uses a standard `src/ai_reliability/` layout and one `pyproject.toml`. Runtime code uses the Python standard library so the first pipeline stays transparent and easy to run.

The legacy bundle under `legacy_day01_06/` is the historical source of truth. New adapters preserve its metric semantics: Day 1 and Day 2 intentionally have different normalization policies; Day 2 ignores empty outputs; Day 3 uses Mode Agreement as consistency, a threshold of `0.8`, `>=` as high, and macro averages; Day 4 rejects code fences or text outside JSON and passes only at 100%; revised Day 5 uses normalized exact `UNKNOWN` and the original confusion-matrix denominators; Day 6 uses observed confidence values and defines risk as the error ratio among selected cases.

Day-specific loaders convert different CSV/JSONL inputs into a shared `EvaluationRecord`. They do not force one raw input schema onto every day. Metrics return `MetricResult`, and artifacts are plain JSON/JSONL for inspection.

Intentional hardening in the refactor:

- Empty inputs return a safe zero plus a warning instead of raising `ZeroDivisionError`.
- Format checks require a JSON object, which makes downstream required-key checks unambiguous.
- Day 6 `correct` must be an explicit `0` or `1`; ambiguous values are rejected.
- Gate rules BLOCK on missing/non-numeric metrics and malformed artifacts.
- Dataset paths are constrained to the selected `data/<mode>/` tree.

These changes do not alter the legacy demo results. `legacy_day01_06/` is not edited or deleted. Demo and real data have separate roots, raw real data is ignored, and no credentials or API integration are part of this foundation. Day 6 code is migrated for behavior parity; article quality and canonical article migration remain separate work.
