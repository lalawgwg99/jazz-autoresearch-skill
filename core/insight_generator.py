import os
import subprocess
from core.result_tracker import ResultTracker

class InsightGenerator:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.insight_file = os.path.join(base_dir, "INSIGHTS.md")
        self.tracker = ResultTracker()

    def update_insights(self):
        history = self.tracker.get_history_summary(limit=50)
        prompt = (
            f"你是首席 AI 研究員。根據以下實驗歷史，總結出 3 條具體的科研洞察(Insights)。
"
            f"哪些參數最有效？哪些方向是死胡同？

"
            f"實驗歷史：
{history}

"
            f"請輸出為 Markdown 格式的 INSIGHTS.md 內容。"
        )
        
        try:
            # 透過 LLM 進行深度總結
            cmd = ["oracle", "--prompt", prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                with open(self.insight_file, "w", encoding="utf-8") as f:
                    f.write("# 📓 AutoResearch 科研筆記

")
                    f.write(result.stdout)
                print(f"📓 科研筆記已更新：{self.insight_file}")
        except:
            pass
