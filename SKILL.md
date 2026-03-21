# AutoResearch Skill

> 讓你的 Agent 具備「自動化研究與實驗優化」的能力。

## 概述
AutoResearch 技能允許 OpenClaw Agent 自主管理模型訓練實驗。它會根據之前的成敗（results.tsv）來決定下一個改進方向。

## 當你被要求以下任務時使用：
- "優化這個模型的 BPB 分數"
- "幫我跑幾輪自動化實驗測試參數"
- "分析目前的實驗紀錄並提出下一個改進假設"

## 工具指令
- `python3 cli/main.py run`: 啟動一輪自動化實驗循環。
- `python3 cli/main.py status`: 摘要目前最佳紀錄與歷史。

## 整合建議
Agent 在呼叫此 Skill 前，應先讀取 `results.tsv` 以了解目前的實驗現況，這能幫助 LLM 產生更精確的 Hypothesis。
