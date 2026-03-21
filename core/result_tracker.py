import os
import csv
import time
import json

class ResultTracker:
    def __init__(self, filepath="results.tsv"):
        self.filepath = filepath
        self._init_file()

    def _init_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="") as f:
                writer = csv.writer(f, delimiter="	")
                writer.writerow(["timestamp", "hypothesis", "val_bpb", "improved", "config"])

    def log_result(self, hypothesis, bpb, improved, config_dict):
        # 確保即使失敗也會記錄，以便 LLM 學習
        with open(self.filepath, "a", newline="") as f:
            writer = csv.writer(f, delimiter="	")
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                hypothesis,
                f"{bpb:.6f}" if bpb is not None else "FAILED",
                "YES" if improved else "NO",
                json.dumps(config_dict)
            ])

    def get_best_score(self):
        if not os.path.exists(self.filepath):
            return 1.5
        
        best = 1.5
        with open(self.filepath, "r") as f:
            reader = csv.DictReader(f, delimiter="	")
            for row in reader:
                try:
                    score = float(row["val_bpb"])
                    if score < best:
                        best = score
                except (ValueError, KeyError):
                    continue
        return best

    def get_history_summary(self, limit=10):
        if not os.path.exists(self.filepath):
            return "No history yet."
        history = []
        with open(self.filepath, "r") as f:
            reader = csv.DictReader(f, delimiter="	")
            for row in reader:
                history.append(f"- {row[timestamp]} | Hypo: {row[hypothesis]} | BPB: {row[val_bpb]} | Improved: {row[improved]}")
        return "
".join(history[-limit:])
