# 🚀 AutoResearch: Roadmap & TODO

## 🎯 P0: 核心邏輯與失敗學習 (Failure Analysis)
- [ ] **失敗原因分析 (RCA)**: 在 `results.tsv` 中新增 `failure_category` 與 `exit_code`。
- [ ] **LLM 診斷引擎**: 實驗失敗時自動抓取最後 500 行日誌交給 Oracle 進行原因判斷。
- [ ] **失敗知識庫 (Failure KB)**: 建立 `failure_kb.jsonl`，避免 AI 重複執行已知會失敗的參數組合。
- [ ] **與 Oracle 深度整合**: 不僅用於假設生成，還用於實驗決策與結果評估。

## ⚙️ P1: 架構擴展與 Skill 規範化
- [ ] **Plugin 系統**: 解耦 LLM Provider 與 Model Backend。
- [ ] **OpenClaw Skill 規範化**: 完善 `SKILL.md`，定義 `capabilities` 與 `config_schema`。
- [ ] **統一配置管理**: 建立 `config.yaml` 取代硬編碼參數。

## 📊 P2: 實驗監控與視覺化
- [ ] **SQLite 時序監控**: 將實驗數據寫入本地 SQLite。
- [ ] **即時儀表板**: 使用 Streamlit 或 Gradio 建立 Web UI。
- [ ] **Rich CLI**: 在終端機中使用 `rich` 顯示訓練曲線與進度條。

## 🔔 P3: 事件通知與自動化
- [ ] **OpenClaw Event Bus**: 實驗完成後發送事件，觸發 Telegram 通知。
- [ ] **自動 PR/Issue**: 實驗成功後自動建立 Git 分支並開啟 Pull Request。

---
*Last Updated: 2026-03-22 00:43:14 by UUZero*
