# Day 3｜又準又穩才算可靠？我把 AI 放進四象限

昨天我做了 Consistency Test，開始測同一個 Prompt 重跑五次會不會得到一樣的答案。

結果也讓我遇到第一個評測陷阱：

> 一致，不代表正確。

如果 AI 五次都回答同一個錯誤答案，它可以非常「穩」，但我顯然不能叫它可靠。

所以今天我把 Day 1 的 Accuracy 和 Day 2 的 Consistency 放到一起。

## 只看 Accuracy 會發生什麼？

假設一題問五次，AI 答對三次。

Accuracy 是 60%。

但這個 60% 可能來自完全不同的行為。

模型 A：
`對、對、對、錯、錯`

模型 B：
`對、錯A、對、錯B、對`

兩者答對率相同，但第二個模型的錯誤更加飄忽。

因此我今天不再只問「答對幾次」，還會問：

> 五次回答有沒有集中在同一個答案？

## Reliability Matrix

我先用兩個最簡單的軸：

- X 軸：Accuracy
- Y 軸：Consistency

暫時用 80% 當作 Day 3 的工程門檻，就會得到四種狀態。

### 1. 又準又穩
Accuracy 高、Consistency 高。

這是最理想的情況：多次執行不只答案集中，而且大多是正確答案。

### 2. 準但不穩
Accuracy 高、Consistency 低。

平均看起來不錯，但每次輸出變化很大。這種模型在 Demo 可能很好看，放進自動化流程卻可能讓人很不安。

### 3. 穩但不準
Accuracy 低、Consistency 高。

這是我今天覺得最危險的一格。

因為它每次都很有自信地給你同一個錯誤答案，看起來甚至比「亂答」更值得信任。

### 4. 又不準又不穩
Accuracy 低、Consistency 低。

至少這種問題比較容易被發現：答案本身就很飄，而且常常錯。

## Python：把每一題自動分類

今天新增 `reliability_matrix.py`。

輸入資料長這樣：

```csv
question_id,run_id,expected,actual
Q1,1,5,5
Q1,2,5,5
...
```

程式會對每一題算：

- Accuracy
- Mode Agreement（今天先拿它當 Consistency baseline）
- Reliability Quadrant

示範資料刻意放入四種不同情況，因此會看到像：

```text
Question    Accuracy   Consistency  Quadrant
Q1              100%          100%  又準又穩
Q2               80%           80%  又準又穩
Q3                0%          100%  穩但不準
Q4               60%           60%  又不準又不穩
```

這裡最值得看的不是 Q1，而是 Q3。

它的 Consistency 是 100%。

如果我昨天只做「穩定性排行榜」，它甚至可能拿第一名。

但 Accuracy 是 0%。

## 評測開始變成工程問題

我今天重新看今年 AI Engineering 組的作品，發現競爭者並不只是在介紹模型。

已經有人做到 benchmark、LLM Judge、回歸防線；也有人從 MLOps 角度把品質門檻直接放進 CI/CD，目的就是避免「程式成功執行，但品質已經壞掉」的模型被部署。

這給我一個很重要的方向：

AI Reliability Lab 最後不能只是 Dashboard。

它應該變成一個 **Quality Gate**。

也就是：

```text
新 Prompt / 新模型
        ↓
Reliability Test Suite
        ↓
Accuracy / Consistency / ...
        ↓
PASS → 可以進下一階段
FAIL → 擋下來並列出失敗 Case
```

如果 Day 30 可以做到這裡，整個作品就會從「模型評測小工具」升級成 AI Engineering workflow。

## 今天的另一個問題：80% 是誰決定的？

今天程式暫時把 80% 當門檻。

但我不打算假裝 80% 是什麼科學真理。

客服、醫療、娛樂聊天、程式碼生成，能接受的錯誤率根本不一樣。

所以後面我們會把門檻從硬編碼，逐漸變成：

- 可設定
- 依任務分類
- 可做 regression comparison
- 最後進 CI quality gate

## Day 3 結論

前三天我已經把「AI 很好用」拆成兩件不同的事：

**它答得對嗎？**
以及
**它每次都能答得差不多嗎？**

而今天最值得留下的一句話是：

> 最危險的不一定是亂答的 AI，而可能是穩定地答錯的 AI。

明天我會處理另一個很常被忽略的問題：

> AI 明明知道答案，卻沒有照我要的格式輸出，這算成功嗎？

Day 4 會開始做 **Format Compliance**，並把它變成第一個真正可以「擋部署」的 Quality Gate。
