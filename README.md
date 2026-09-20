# AI Reliability Lab

AI Reliability Lab 是一個以 Python 建立的 30 天 AI Engineering 實驗專案：把「AI 好像很準」轉成可重現、可檢查、可量化的工程指標。

核心問題是：**AI 都會回答了，我憑什麼相信它？**

目前 Foundation v1 只實作 Day 1–Day 6，並以 legacy source 的實際行為作為 characterization baseline：

- Day 1：normalization 與 exact-match correctness baseline
- Day 2：unique ratio、mode agreement、average pairwise Jaccard consistency
- Day 3：Accuracy × Consistency reliability matrix、macro average、0.8 demo threshold
- Day 4：strict JSON format compliance 與 format quality gate
- Day 5 revised：correct abstention、unsafe answer、over-refusal、coverage、selective accuracy
- Day 6：以資料中實際 confidence thresholds 計算 risk–coverage points
- Day 7：controlled synthetic calibration、Brier Score、ECE、reliability-bin data

## Project structure

```text
src/ai_reliability/       shared schemas, I/O, runner, CLI
  evaluation/             legacy-compatible normalization and record adapters
  metrics/                Day 1–6 metric implementations
  quality_gate/           metric-consuming gate rules and engine
  reporting/              artifact summary rendering
tests/                    unit, characterization, and integration tests
data/demo/                synthetic datasets only
data/real/public/         future anonymized public real datasets
data/real/raw/            future sensitive raw data; ignored by Git
artifacts/                local run artifacts; run directories ignored
configs/                  JSON configurations for demo and future real runs
legacy_day01_06/          immutable historical source and articles
docs/architecture.md      Foundation v1 design decisions
```

## Installation and demo

The runtime has no mandatory third-party dependency. For a development checkout:

```powershell
python -m pip install -e ".[dev]"
```

Without installing the package, the same commands can be run with `PYTHONPATH=src`:

```powershell
$env:PYTHONPATH = "src"
python -m ai_reliability.cli run --mode demo --config configs/demo.json
python -m ai_reliability.cli report --mode demo --run-id <run_id>
python -m ai_reliability.cli gate --mode demo --run-id <run_id>
```

`airlab run`, `airlab report`, and `airlab gate` are the only first-version CLI commands. A demo run writes a unique directory under `artifacts/demo/<run_id>/` containing `metadata.json`, `records.jsonl`, `metrics.json`, and `gate.json`.

## Demo data versus real experiments

`data/demo/` is synthetic and exists to reproduce the Day 1–Day 7 examples. Its outputs are not measurements of a real model. Day 7 uses two controlled scenarios with identical correctness labels and overall accuracy: one with confidence aligned to observed group accuracy, and one deliberately overconfident. This is an experiment about calibration behavior, not a claim about a real LLM. Demo metadata, calibration metrics, and risk-coverage output explicitly carry this limitation; demo confidence is synthetic demonstration confidence, not calibrated LLM confidence.

Calibration asks whether a stated probability corresponds to the observed correctness frequency. Day 7 reports accuracy, mean confidence, signed mean confidence gap, Brier Score, Expected Calibration Error (ECE), and structured reliability-bin data. ECE depends on the chosen binning policy and sample size. Brier Score is useful as a probabilistic scoring rule, but is not a pure calibration-only metric. No calibration Quality Gate threshold is selected yet.

`data/real/public/` is reserved for anonymized real evidence that may be committed. `data/real/raw/` is reserved for sensitive raw outputs and is ignored by Git. No API integration or API key is needed by Foundation v1.

## Quality Gate

The gate consumes already-produced metrics; it never silently recomputes them. Missing required metrics, malformed metric values, or a failed rule result in `BLOCK`. The demo gate requires a 100% Day 4 format pass rate and zero unsafe answers, so the historical demo intentionally produces `BLOCK`.

## Roadmap

Future directions are groundedness, hallucination analysis, prompt robustness, regression tests, cost/latency, judge reliability, benchmark reliability, dashboards, and case viewing. They are intentionally not scaffolded as empty modules in this release.

The original Day 1–Day 6 articles remain unchanged under `legacy_day01_06/`. Canonical article migration is a separate follow-up.
