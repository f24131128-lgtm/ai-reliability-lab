# Day 4｜答案是對的，但 JSON 壞掉，這算成功嗎？

前三天我把 AI Reliability 拆成 Accuracy 與 Consistency。今天加入第三個維度：**Format Compliance**。

如果只是跟 AI 聊天，多一句「以下是答案」通常沒差。但如果下一步不是人，而是另一支程式，事情就完全不同。

假設後端要求模型只能回：

```json
{"status":"ok","answer":42}
```

模型卻回：

```text
當然可以！以下是 JSON：
{"status":"ok","answer":42}
```

人看得懂，答案也是 42，但程式直接解析整段文字就可能失敗。

## 今天的規則

我先定三個最低要求：輸出必須是合法 JSON、包含必要欄位，而且 JSON 外不能混入其他文字。符合才 PASS。

今天新增 `format_gate.py`。它會逐筆檢查測試 Case，最後輸出 `QUALITY GATE: PASS` 或 `QUALITY GATE: BLOCK`。

示範資料刻意包含：完全正確、Markdown code fence、缺欄位、JSON 前多一句說明。**這些全部是 demo data，不是任何真實模型的實測結果。**

所以今天不是在宣稱某模型 Format Pass Rate 有多少，而是在確認我們的 Gate 能不能抓到不同格式錯誤。

## 從排行榜走向 Quality Gate

目前架構開始變成：

```text
新模型 / 新 Prompt
        ↓
Reliability Test Suite
        ↓
Accuracy
Consistency
Format Compliance
        ↓
Quality Gate
   ↙           ↘
 PASS          BLOCK
```

排行榜只是在描述模型；Quality Gate 則是在做工程決策。

真正的系統需要知道的往往不是「平均 87 分」，而是：**這個版本到底能不能進下一個環境？**

## 今天又冒出一個問題

如果模型只是多包了一層 ```json code fence，其實程式很容易自動修掉。

那應該直接 BLOCK，還是 repair 後繼續？

這又牽涉到一個更有意思的問題：我們究竟是在測「裸模型」，還是在測「模型 + 修復程式」的 production pipeline？

這題先留著，後面會做 Raw Model vs Production Pipeline。

## Day 4 結論

今天最重要的一句話：

> **答案正確，不代表系統可以使用。**

AI Reliability Lab 現在已經有 Accuracy、Consistency、Format Compliance，以及第一個 PASS/BLOCK Quality Gate。

Day 5 會測另一種可靠性：當資訊根本不足時，AI 能不能說「我不知道」？也就是 **Abstention Test**。
