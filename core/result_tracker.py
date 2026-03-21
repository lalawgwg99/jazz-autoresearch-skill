import os
import csv
import time
import json

class ResultTracker:
    def __init__(self, filepath=None):
        if filepath is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.filepath = os.path.join(base_dir, "results.tsv")
        else:
            self.filepath = filepath
        self._init_file()

    def _init_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter="	")
                writer.writerow(["timestamp", "hypothesis", "val_bpb", "improved", "config"])

    def log_result(self, hypothesis, bpb, improved, config_dict):
        try:
            with open(self.filepath, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter="	")
                writer.writerow([
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    hypothesis,
                    f"{bpb:.6f}" if bpb is not None else "FAILED",
                    "YES" if improved else "NO",
                    json.dumps(config_dict)
                ])
        except Exception as e:
            print(f"Error logging result: {e}")

    def get_best_score(self):
        if not os.path.exists(self.filepath):
            return 1.5
        
        best = 1.5
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="	")
                for row in reader:
                    try:
                        val = row.get("val_bpb", "1.5")
                        if val in ["FAILED", "N/A", "None", ""]:
                            continue
                        score = float(val)
                        if score < best:
                            best = score
                    except (ValueError, TypeError):
                        continue
        except Exception as e:
            print(f"Error reading best score: {e}")
        return best

    def get_history_summary(self, limit=10):
        if not os.path.exists(self.filepath):
            return "No history yet."
        history = []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="	")
                for row in reader:
                    # 避免換行符號損壞字串
                    summary = f"- {row['timestamp']} | Hypo: {row['hypothesis']} | BPB: {row['val_bpb']} | Improved: {row['improved']}"
                    history.append(summary)
        except Exception as e:
            return f"Error reading history: {e}"
        return "
".join(history[-limit:])
