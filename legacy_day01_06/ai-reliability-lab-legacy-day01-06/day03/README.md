# AI Reliability Lab — Day 3

今天把 Accuracy × Consistency 合併成四象限，避免「只看答對一次」或「只看穩定」的誤判。

## 直接執行
```bash
python src/reliability_matrix.py data/demo_results.csv
```

## 真人實測
把每題 5 次獨立回答整理進 CSV：
`question_id,run_id,expected,actual`

再執行：
```bash
python src/reliability_matrix.py data/manual_results.csv
```

輸出會包含每題：
- accuracy
- mode agreement
- quadrant
以及整體平均。
