import os
import csv
import time

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
        with open(self.filepath, "a", newline="") as f:
            writer = csv.writer(f, delimiter="	")
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                hypothesis,
                f"{bpb:.6f}",
                "YES" if improved else "NO",
                str(config_dict)
            ])

    def get_best_score(self):
        if not os.path.exists(self.filepath):
            return 1.5  # 預設初始分數
        
        best = 1.5
        with open(self.filepath, "r") as f:
            reader = csv.DictReader(f, delimiter="	")
            for row in reader:
                score = float(row["val_bpb"])
                if score < best:
                    best = score
        return best
