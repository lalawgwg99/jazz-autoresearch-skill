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
                writer = csv.writer(f, delimiter="\t")
                writer.writerow(["timestamp", "hypothesis", "val_bpb", "improved", "config"])

    def log_result(self, hypothesis, bpb, improved, config_dict):
        with open(self.filepath, "a", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                hypothesis,
                f"{bpb:.6f}" if bpb is not None else "N/A",
                "YES" if improved else "NO",
                str(config_dict)
            ])

    def log_failed(self, hypothesis, error_msg=""):
        """記錄執行失敗（例外錯誤）的實驗，確保失敗歷史不遺失"""
        with open(self.filepath, "a", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                hypothesis,
                "N/A",
                "FAILED",
                error_msg[:200] if error_msg else "experiment error"
            ])

    def get_best_score(self):
        if not os.path.exists(self.filepath):
            return 1.5  # 預設初始分數

        best = 1.5
        with open(self.filepath, "r") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                if row["val_bpb"] == "N/A":
                    continue
                try:
                    score = float(row["val_bpb"])
                    if score < best:
                        best = score
                except (ValueError, KeyError):
                    continue
        return best

    def get_history_summary(self, limit=10):
        """回傳最近 N 筆實驗的摘要，包含成功與失敗紀錄，供 LLM 分析"""
        if not os.path.exists(self.filepath):
            return []
        rows = []
        with open(self.filepath, "r") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                rows.append(row)
        return rows[-limit:]
