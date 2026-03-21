import os
import json
import csv

class HypothesisGenerator:
    def __init__(self, history_file="results.tsv"):
        self.history_file = history_file

    def read_history(self, limit=10):
        if not os.path.exists(self.history_file):
            return []
        history = []
        with open(self.history_file, "r") as f:
            reader = csv.DictReader(f, delimiter="	")
            for row in reader:
                history.append(row)
        return history[-limit:]

    def generate_next_hypothesis(self):
        history = self.read_history()
        # 這裡未來會接 LLM 呼叫，現在先用一個模擬邏輯
        if not history:
            return {
                "hypothesis_description": "Initial experiment: default config",
                "proposed_config_changes": {"n_layer": 8}
            }
        
        # 模擬邏輯：如果上次改進成功，就再加一層
        last_run = history[-1]
        if last_run["improved"] == "YES":
            current_layer = eval(last_run["config"]).get("n_layer", 8)
            return {
                "hypothesis_description": f"Previous improvement seen, adding more depth: {current_layer + 1}",
                "proposed_config_changes": {"n_layer": current_layer + 1}
            }
        else:
            return {
                "hypothesis_description": "Previous failed, trying more heads instead",
                "proposed_config_changes": {"n_head": 12}
            }
