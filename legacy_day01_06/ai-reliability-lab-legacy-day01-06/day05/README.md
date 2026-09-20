# AI Reliability Lab — Day 5 (Revised)

這是加強版 Day 5，重點是把 Abstention 從概念擴充成可量化的工程評測。

新增指標：
- Correct Abstentions
- Unsafe Answers
- Over-refusals
- Abstention Recall
- Unsafe Answer Rate
- Over-refusal Rate
- Coverage
- Selective Accuracy

執行：

```bash
python src/abstention_gate.py data/demo_abstention_cases.csv
```

注意：`demo_abstention_cases.csv` 為示範資料，不代表任何真實模型實測。
