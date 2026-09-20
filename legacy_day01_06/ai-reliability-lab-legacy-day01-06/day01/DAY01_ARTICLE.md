# Day 1｜AI 很會回答，但「很會」到底是多少分？

今年我想做的，不是再做一個會聊天的 AI。

我想做一件比較不討喜、但更接近工程的事：

**量它。**

我們平常使用大型語言模型時，很容易用一種模糊的方式評價它：

- 這個模型好像比較聰明
- 那個模型比較穩
- 這次回答感覺不錯
- 換個 Prompt 好像有變好

問題是，「好像」不能當成工程指標。

如果我要把 AI 放進真正的系統，我需要知道的不是「它看起來很厲害」，而是：

- 正確率是多少？
- 同一題問五次，答案會不會變？
- 沒有資料時，它會承認不知道，還是開始編？
- 要求輸出 JSON，它有多少次真的照格式？
- 多花十倍成本，品質到底提升多少？

所以這 30 天，我決定用 Python 做一個 **AI Reliability Lab**。

## 為什麼選 AI Engineering？

2026 iThome 鐵人賽把 AI Engineering 獨立成一個競賽組別。現在同組已經有 RAG、Agent、AI Infrastructure、Code Review Benchmark、Agent 治理等偏工程實作的系列。

這代表只寫「Prompt 怎麼下」或「我用了哪個模型」很難形成差異。

我的切角因此會放在一件更底層的事：

> **當 AI 的輸出具有不確定性，我們要怎麼建立可重現的測試方法？**

這也是這個系列和另一條 C++／Codex 專案最明顯的差別。

那一條是在問：
「AI 都會寫 Code 了，我還需要學 Coding 嗎？」

這一條要問的是：
「AI 都能回答了，我憑什麼相信它？」

## 最後想做出什麼？

我希望 Day 30 的成品可以把一個模型丟進去，得到類似這樣的報告：

```text
MODEL REPORT

Accuracy          84%
Consistency       91%
Abstention        72%
Format Pass       96%
Groundedness      81%

Cost / 100 tests  ...
Latency P50       ...

Most Dangerous Cases
#014  confident but unsupported
#027  correct once, wrong twice
#041  ignored required format
```

而且不是只秀一個分數。

我希望每一個分數都可以回頭追到：
測試資料、模型輸出、評分規則與原始紀錄。

## Day 1：先不要碰模型 API

第一天我故意不直接接 ChatGPT、Claude 或 Gemini。

原因很簡單。

如果評測程式本身都還沒固定，就立刻把模型接進來，我很難分辨：

「今天結果變了，是模型變了，還是我的程式變了？」

所以 Day 1 先做最小骨架。

我建立三種最簡單的測試：

1. **Exact**：有明確標準答案，例如 2 + 3。
2. **Abstention**：資料不足時，能不能回答 UNKNOWN。
3. **Format**：要求只輸出指定 JSON 時，有沒有遵守。

今天甚至先用固定的假輸出（mock output），目的只有一個：

**先確認評測管線是可重現的。**

執行：

```bash
python src/baseline.py
```

目前會得到：

```text
AI Reliability Lab — Day 1
================================
Q001 [exact] PASS
Q002 [abstention] PASS
Q003 [format] PASS
--------------------------------
Exact-match score: 3/3 = 100%
```

這個 100% 沒有任何值得高興的。

因為今天測的不是 AI。

今天測的是：

> **我的測試工具能不能先正確地測試。**

## 我暫時把「可靠」拆成六個方向

接下來 30 天會逐步把它們做成真正的指標：

- Accuracy
- Consistency
- Groundedness
- Abstention
- Format Compliance
- Cost / Latency

後面還會碰到一個更麻煩的問題：

**如果答案不是 5 這種唯一答案，要由誰來評分？**

人工？
規則？
另一個 LLM？
還是多個 Judge？

這就是後面我最想玩的地方。

## Day 1 結論

今天沒有做出很炫的 AI Demo。

只有三筆資料、一個 Python script，以及一個很小的分數。

但這反而是我希望這個系列維持的方向：

**先有測量，再談優化。**

明天，我會把第一個真正的模型接進來。

然後看看第一個問題：

> 同一個問題問 AI 五次，它真的會給我同一個答案嗎？
