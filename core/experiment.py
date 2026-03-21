import time
import os
import subprocess
from core.branch_manager import BranchManager
from core.result_tracker import ResultTracker
from model.trainer import Trainer

class ExperimentEngine:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.branch_manager = BranchManager(repo_path=base_dir)
        self.tracker = ResultTracker()
        self.history_best_score = self.tracker.get_best_score()
        if self.history_best_score == 0.0:
            self.history_best_score = float("inf")

    def _check_temperature(self):
        try:
            cmd = ["osx-cpu-temp"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                temp = float(result.stdout.replace("°C", "").strip())
                if temp > 85.0:
                    print("CPU temperature high: " + str(temp) + "C")
                    time.sleep(60)
                    return False
            return True
        except:
            return True

    def _send_telegram_report(self, message):
        try:
            cmd = ["openclaw", "message", "send", "--message", message]
            subprocess.run(cmd, capture_output=True, text=True)
        except:
            pass

    def run_experiment(self, hypothesis):
        if not self._check_temperature():
            return

        hypo_desc = hypothesis.get("hypothesis_description", "Unknown")
        config_changes = hypothesis.get("proposed_config_changes", {})
        branch_name = "exp-" + str(int(time.time()))

        print("🚀 Starting: " + hypo_desc)
        
        try:
            self.branch_manager.create_branch(branch_name)
            trainer = Trainer(config_changes)
            result = trainer.train(time_budget=5)
            current_score = result.get("val_bpb", float("inf"))
            
            improved = current_score < self.history_best_score
            self.tracker.log_result(hypo_desc, current_score, improved, config_changes)
            
            status = "✅" if improved else "❌"
            report = "AutoResearch Report: " + status + " BPB: " + str(current_score)
            
            if improved:
                self.branch_manager.commit_success("Improvement: " + hypo_desc)
                self.history_best_score = current_score
            else:
                self.branch_manager.rollback(branch_name)

            self._send_telegram_report(report)

        except Exception as e:
            error_msg = "⚠️ Experiment failed: " + str(e)
            self.tracker.log_result(hypo_desc, None, False, {"error": str(e)})
            self.branch_manager.rollback(branch_name)
            self._send_telegram_report(error_msg)
