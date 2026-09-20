import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "questions.jsonl"

# Day 1 先用固定的假模型輸出，確保評測管線本身可重現。
MOCK_OUTPUTS = {
    "Q001": "5",
    "Q002": "UNKNOWN",
    "Q003": '{"status":"ok"}',
}

def normalize(text: str) -> str:
    return " ".join(text.strip().split())

def exact_match(actual: str, expected: str) -> bool:
    return normalize(actual) == normalize(expected)

def main():
    rows = []
    for line in DATA.read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        actual = MOCK_OUTPUTS[item["id"]]
        passed = exact_match(actual, item["expected"])
        rows.append({
            "id": item["id"],
            "category": item["category"],
            "expected": item["expected"],
            "actual": actual,
            "passed": passed,
        })

    passed = sum(r["passed"] for r in rows)
    total = len(rows)

    print("AI Reliability Lab — Day 1")
    print("=" * 32)
    for row in rows:
        mark = "PASS" if row["passed"] else "FAIL"
        print(f'{row["id"]} [{row["category"]}] {mark}')
    print("-" * 32)
    print(f"Exact-match score: {passed}/{total} = {passed/total:.0%}")

if __name__ == "__main__":
    main()
