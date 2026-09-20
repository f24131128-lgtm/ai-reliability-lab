# AI Reliability Lab

30 天用 Python 把「我覺得 AI 好像很準」變成「我可以量出它到底多可靠」。

## Day 1 goal
建立最小可重現的評測骨架，不綁任何特定模型 API。

## Core dimensions
- Accuracy：答案是否正確
- Consistency：重複詢問是否穩定
- Groundedness：是否有證據支持
- Abstention：不知道時能不能拒答
- Format compliance：是否遵守輸出格式
- Cost / latency：品質之外的工程代價

## Run
```bash
python src/baseline.py
```
