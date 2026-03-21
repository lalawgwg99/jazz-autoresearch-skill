import os
import subprocess
import json
from core.result_tracker import ResultTracker

class LLMHypothesisGenerator:
    def __init__(self, template_path="hypothesis/prompt_template.md"):
        # 修正：確保能找到正確的路徑
        self.template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), template_path)
        self.tracker = ResultTracker()

    def generate_next_hypothesis(self):
        best_score = self.tracker.get_best_score()
        # 這裡未來會從 results.tsv 抓歷史數據
        history = "No history available."
        
        with open(self.template_path, "r") as f:
            template = f.read()
        
        # 填充模板
        prompt = template.replace("{{best_score}}", str(best_score))
        prompt = prompt.replace("{{history_table}}", history)
        
        # 這裡會透過 oracle CLI 呼叫 LLM
        return {
            "hypothesis_description": "Auto-generated hypothesis via LLM Logic",
            "proposed_config_changes": {"n_layer": 10}
        }
