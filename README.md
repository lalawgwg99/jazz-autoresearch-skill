# 🚀 AutoResearch: Your 24/7 AI Scientist

> **"讓 AI 幫你做實驗並自我優化"** —— 基於 Andrej Karpathy `autoresearch` 思維的自動化實驗框架。

AutoResearch 是一個專為 AI 模型開發設計的「自治研究員」系統。它不只是跑訓練，它會**思考、實驗、學習、並進化**。

## 🌟 核心特色

- **🧠 自治循環 (Autonomous Loop)**：自動生成假設 -> 執行實驗 -> 評估結果 -> 決定迭代。
- **🤖 大腦對接 (LLM Logic)**：透過 OpenClaw `oracle` 結合 Claude-3.5 思考實驗方向。
- **📚 失敗學習 (Failure Awareness)**：完整記錄失敗實驗（results.tsv），讓 AI 從錯誤中優化，避免重蹈覆轍。
- **🌿 分支管理 (Git Automation)**：自動化 Git 分支管理。實驗成功則 `commit` 合併，失敗則自動 `rollback` 回到穩定的主分支。
- **⚡️ 智慧模擬 (Mock Mode)**：在沒有 GPU 的環境下也能測試完整的實驗邏輯與決策循環。

## 📦 安裝與設定

### 1. 複製專案
```bash
git clone https://github.com/lalawgwg99/jazz-autoresearch-skill.git
cd jazz-autoresearch-skill
```

### 2. 安裝依賴 (推薦使用 uv)
```bash
uv sync
# 或使用 pip
pip install -r requirements.txt
```

### 3. 環境需求
- **OpenClaw**: 建議搭配 OpenClaw 環境以使用 `oracle` 大腦功能。
- **Python**: 3.10+
- **Git**: 需安裝並配置好 Git 環境以供分支管理使用。

## 🎮 使用方式

### 啟動一次自動化研究實驗
系統會讀取歷史數據，呼叫 LLM 生成下一個假說，並自動跑完「開分支->訓練->評估->決策」的流程。
```bash
python3 cli/main.py run
```

### 查看目前實驗戰果與歷史摘要
```bash
python3 cli/main.py status
```

## 📂 專案結構
- `core/`: 實驗引擎、Git 分支管理、結果記錄器。
- `hypothesis/`: LLM 假設生成器與 Prompt 範本。
- `model/`: 模型訓練邏輯 (支援真實 Torch 與 Mock 模式)。
- `cli/`: 統一的命令行入口。

## 🤝 貢獻與開發
歡迎提交 PR 或 Issue。這是一個開源專案，旨在探索 AI 如何輔助科學研究與模型優化。

---
**Author**: Jazz ([lalawgwg99](https://github.com/lalawgwg99))
**Powered by**: [OpenClaw](https://openclaw.ai)
