# Foundation v1 architecture

Foundation v1 uses a standard `src/ai_reliability/` layout and one `pyproject.toml`. Runtime code uses the Python standard library so the first pipeline stays transparent and easy to run.

The legacy bundle under `legacy_day01_06/` is the historical source of truth. New adapters preserve its metric semantics: Day 1 uses strip plus whitespace collapse; Day 2 lowercases, removes whitespace and the legacy punctuation set (including backtick), and excludes only raw-whitespace-empty outputs; Day 3 lowercases, strips, and collapses whitespace, uses the first row's expected value for every row in a question group, uses Mode Agreement as consistency, a threshold of `0.8`, `>=` as high, and macro averages; Day 4 rejects code fences or text outside JSON and passes only at 100%; revised Day 5 uses lower/strip/collapse normalization for exact `UNKNOWN`, parses `answerable` with strip/lower, and keeps decision accuracy separate from selective accuracy; Day 6 uses observed confidence values and defines risk as the error ratio among selected cases.

Day-specific loaders convert different CSV/JSONL inputs into a shared `EvaluationRecord`. They do not force one raw input schema onto every day. Metrics return `MetricResult`, and artifacts are plain JSON/JSONL for inspection.

Normalization policies are intentionally day-specific:

- Day 1: strip and collapse whitespace; case and punctuation remain significant.
- Day 2: lowercase, remove whitespace, and remove the legacy punctuation set, including backtick. Raw outputs whose `strip()` is empty are excluded; punctuation-only raw outputs remain in the denominator. Unique Ratio and Mode Agreement use normalized outputs, while Pairwise Jaccard tokenizes raw non-empty outputs after lowercasing.
- Day 3: lowercase, strip, and collapse whitespace. For each `question_id`, the expected answer is taken from the first row and used for every actual in that group. Consistency remains Mode Agreement, with the demo engineering threshold `0.8`, inclusive high boundary, and macro averages.
- Day 5: lowercase, strip, and collapse whitespace. `UNKNOWN` is normalized exact abstention, and `answerable` uses `strip().lower() == "no"`.

Day 7 calibration is a controlled synthetic experiment. Confidence represents an estimated probability that an answer is correct, not real-model calibrated confidence. The metric reports accuracy, mean confidence, signed confidence gap (`mean_confidence - accuracy`), Brier Score, ECE, and reliability-bin data. ECE uses configurable equal-width bins and the deterministic boundary `min(int(confidence * n_bins), n_bins - 1)`; empty bins are emitted with null summary values. Brier Score is a probabilistic scoring rule, not a calibration-only metric. ECE is sensitive to binning and sample size. No Day 7 Quality Gate threshold is currently defined.

Intentional hardening in the refactor:

- Empty inputs return a safe zero plus a warning instead of raising `ZeroDivisionError`.
- Format checks require a JSON object, which makes downstream required-key checks unambiguous.
- Day 6 `correct` must be an explicit `0` or `1`; ambiguous values are rejected.
- Gate rules BLOCK on missing/non-numeric metrics and malformed artifacts.
- Dataset paths are constrained to the selected `data/<mode>/` tree.

For Day 5, `decision_accuracy = (correct_abstention + answered_normally) / total`, where `answered_normally` means the system chose to answer (`should_abstain == False` and `did_abstain == False`) regardless of answer correctness. `selective_accuracy` separately measures correctness among answered cases.

These changes do not alter the legacy demo results. `legacy_day01_06/` is not edited or deleted. Demo and real data have separate roots, raw real data is ignored, and no credentials or API integration are part of this foundation. Day 6 code is migrated for behavior parity; article quality and canonical article migration remain separate work.
