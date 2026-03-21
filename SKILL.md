# AutoResearch Skill

> 自動化研究假說驗證框架

## 概述

Autoresearch 是一個用於自動化研究假說生成與驗證的 Skill。它能夠：

- 根據領域問題生成研究假說
- 設計與執行實驗
- 分析實驗結果並提供洞察

## 模組結構

```
autoresearch-skill/
├── core/              # 核心實驗引擎
├── hypothesis/       # 假說管理與生成
├── model/            # 模型介面與整合
└── cli/              # 命令列工具
```

## 使用方式

```bash
# 初始化研究專案
autoresearch init <project_name>

# 生成假說
autoresearch hypothesize --domain <領域> --problem <問題描述>

# 執行實驗
autoresearch run --hypothesis <假說ID>

# 分析結果
autoresearch analyze --experiment <實驗ID>
```

## 核心功能

1. **假說生成** - 基於領域知識生成可驗證的假說
2. **實驗設計** - 自動規劃實驗參數與控制組
3. **結果分析** - 統計分析與視覺化
4. **迭代優化** - 根據結果改進假說

## 依賴

- Python 3.10+
- pydantic
- requests
- pandas
- matplotlib
