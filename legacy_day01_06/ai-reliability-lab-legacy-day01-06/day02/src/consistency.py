import csv
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

def normalize(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[，。！？、；：,.!?;:\-\u2022*#`]", "", text)
    return text

def tokens(text: str):
    # 簡單 baseline：中文以單字元、英文/數字以連續片段切分。
    return set(re.findall(r"[\u4e00-\u9fff]|[a-zA-Z0-9_]+", text.lower()))

def jaccard(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)

def load_outputs(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    outputs = [r["output"].strip() for r in rows if r.get("output", "").strip()]
    return outputs

def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/demo_runs.csv")
    outputs = load_outputs(path)

    if len(outputs) < 2:
        raise SystemExit("至少需要 2 筆非空白 output；建議使用 5 筆。")

    normalized = [normalize(x) for x in outputs]
    counts = Counter(normalized)

    unique_ratio = len(counts) / len(normalized)
    mode_agreement = counts.most_common(1)[0][1] / len(normalized)

    sims = [jaccard(a, b) for a, b in combinations(outputs, 2)]
    pairwise = sum(sims) / len(sims) if sims else 1.0

    print("AI Reliability Lab — Day 2")
    print("=" * 36)
    print(f"Runs:              {len(outputs)}")
    print(f"Unique answers:    {len(counts)}")
    print(f"Unique ratio:      {unique_ratio:.0%}  (lower = more stable)")
    print(f"Mode agreement:    {mode_agreement:.0%}  (higher = more stable)")
    print(f"Pairwise Jaccard:  {pairwise:.0%}  (higher = more similar)")
    print("-" * 36)
    print("Note: 這是 Day 2 baseline，不代表語意完全等價。")

if __name__ == "__main__":
    main()
