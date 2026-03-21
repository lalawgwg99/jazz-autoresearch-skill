import os
import subprocess
import json
import sys

# 確保能找到 ResultTracker
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.result_tracker import ResultTracker

class LLMHypothesisGenerator:
    def __init__(self, template_path="hypothesis/prompt_template.md"):
        # 使用絕對路徑定位 Prompt 模板
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.template_path = os.path.join(base_dir, "hypothesis", "prompt_template.md")
        self.tracker = ResultTracker()

    def generate_next_hypothesis(self):
        best_score = self.tracker.get_best_score()
        history = self.tracker.get_history_summary()
        
        if not os.path.exists(self.template_path):
            return {"hypothesis_description": "Initial experiment", "proposed_config_changes": {"n_layer": 8}}

        with open(self.template_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        # 填充模板：加入防重複實驗機制
        prompt = template.replace("{{best_score}}", str(best_score))
        prompt = prompt.replace("{{history_table}}", history)
        prompt += "

CRITICAL: DO NOT repeat the exact same experiments that failed in the history. Focus on different parameters if current direction stalls."
        
        try:
            # 使用 oracle 並開啟 thinking mode 以獲得更高質量的假說
            cmd = ["oracle", "--thinking", "low", "--prompt", prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            output = result.stdout.strip()
            
            # JSON 解析加強：處理 Markdown Code Block
            json_str = output
            if "```json" in output:
                json_str = output.split("```json")[1].split("```")[0]
            elif "```" in output:
                json_str = output.split("```")[1].split("```")[0]
            
            return json.loads(json_str.strip())
        except Exception as e:
            print(f"LLM Generation failed: {e}")
            return {
                "hypothesis_description": f"Fallback due to system error: {e}",
                "proposed_config_changes": {"n_layer": 8}
            }
