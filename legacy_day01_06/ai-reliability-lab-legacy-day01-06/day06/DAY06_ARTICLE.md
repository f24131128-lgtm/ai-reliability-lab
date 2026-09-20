# Day 6｜AI 回答得越多，真的越好嗎？第一次做 Risk-Coverage Curve

昨天做 Abstention Test 時，我遇到一個矛盾：AI 什麼都回答，Coverage 很高但可能亂猜；動不動就說 UNKNOWN，風險可能降低，卻沒有人想用。

所以今天把兩件事放在一起：**Coverage 與 Risk**。

## Coverage 與 Risk

Coverage 是系統願意回答的比例。10 題回答 8 題，Coverage 就是 80%。

今天先把 Risk 定義成「已回答案例中的錯誤比例」。如果回答 8 題、錯 2 題，Risk 就是 25%。

問題因此變成：**如果只讓 AI 回答比較有把握的題目，Risk 會不會下降？**

## 用 threshold 控制回答範圍

今天的 Demo Dataset 新增 `confidence`。threshold 越高，只有高 confidence 案例會被回答；逐步降低 threshold，Coverage 會上升，但錯誤也可能跟著進來。

`risk_coverage.py` 會把 confidence 由高到低排序，逐步列出每個工作點的 Threshold、Coverage 與 Risk。

這次依然全部是 **Demo Data**。尤其 CSV 裡的 confidence 是我為驗證演算法刻意建立的合成數字，**不是任何 LLM 真實回傳的信心值**。

## 為什麼不能只追最低 Risk？

如果系統幾乎什麼都不回答，Risk 當然可能很好看，但那不是可靠，而是沒在工作。

真正的部署問題比較像：

> **在可接受 Risk 下，盡可能提高 Coverage。**

客服 FAQ 與高風險決策能接受的工作點，本來就不應該相同。

這也表示 Quality Gate 不應只有一條永遠不變的線，而應該跟任務風險一起設定。

## 為什麼繼續走 AI Engineering？

今年同組已經有人跑 50-case benchmark、保存原始輸出與評分腳本；有人把品質門檻接進 CI/CD；也有人提出 Eval-first：先知道系統失敗在哪，再決定是否增加 Agent、Memory 或 Judge。

因此 AI Reliability Lab 的差異化不應是「再做一個 AI 功能」，而是把「能不能相信它」做成**可重跑、可比較、可阻擋部署的工程流程**。

## Day 6 結論

昨天我以為「會拒答」就是比較安全。今天才發現真正的問題是：

> **你願意犧牲多少 Coverage，換多少 Risk？**

目前 Reliability Lab 已經有 Accuracy、Consistency、Format Compliance、Abstention、Coverage、Risk 與 Quality Gate。

但今天埋了一個更大的坑：我直接用了 `confidence`。

**AI 說自己有 90% 把握，我真的能信這個 90% 嗎？**

Day 7 會開始做 **Calibration**：下一步不只測 AI 的答案，而是測它對「自己有多可靠」這件事，到底準不準。
