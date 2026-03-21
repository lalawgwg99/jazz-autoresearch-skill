import os
import subprocess
import json
import csv
import sys
import random

# 確保能找到 ResultTracker
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.result_tracker import ResultTracker

class LLMHypothesisGenerator:
    def __init__(self, template_path="hypothesis/prompt_template.md"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.template_path = os.path.join(base_dir, "hypothesis", "prompt_template.md")
        self.tracker = ResultTracker()

    def generate_next_hypothesis(self):
        best_score = self.tracker.get_best_score()
        history = self.tracker.get_history_summary()
        
        # 1. 優先嘗試 OpenClaw oracle (Claude-3.5)
        try:
            return self._call_oracle(best_score, history)
        except Exception as e:
            print(f"⚠️ Oracle/Claude unavailable: {e}")
            
            # 2. 次要嘗試 Gemini (OpenClaw 內建指令)
            try:
                return self._call_gemini(best_score, history)
            except Exception as e:
                print(f"⚠️ Gemini unavailable: {e}")
                
                # 3. 終極保底：規則引擎 (Rule-based Fallback)
                return self._rule_based_fallback(best_score, history)

    def _call_oracle(self, best_score, history):
        with open(self.template_path, "r", encoding="utf-8") as f:
            prompt = f.read().replace("{{best_score}}", str(best_score)).replace("{{history_table}}", history)
        
        # 增加思考模式以提高質量
        cmd = ["oracle", "--thinking", "low", "--prompt", prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=True)
        return self._parse_json(result.stdout)

    def _call_gemini(self, best_score, history):
        # 假設系統有 gemini 指令 (OpenClaw 常用工具)
        prompt = f"Optimize Transformer. Best BPB: {best_score}. History: {history}. Output JSON: {{'hypothesis_description': '...', 'proposed_config_changes': {{'n_layer': ...}}}}"
        cmd = ["gemini", "--prompt", prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=True)
        return self._parse_json(result.stdout)

    def _rule_based_fallback(self, best_score, history):
        print("🛠️ 啟動規則保底模式 (Rule-based Logic)...")
        # 簡單邏輯：隨機微調一個參數
        params = ["n_layer", "n_head", "n_embd", "learning_rate"]
        target = random.choice(params)
        return {
            "hypothesis_description": f"Rule-based optimization for {target}",
            "proposed_config_changes": {target: random.choice([8, 10, 12, 16]) if "n_" in target else 0.001}
        }

    def _parse_json(self, output):
        json_str = output
        if "```json" in output:
            json_str = output.split("```json")[1].split("```")[0]
        elif "```" in output:
            json_str = output.split("```")[1].split("```")[0]
        return json.loads(json_str.strip())
