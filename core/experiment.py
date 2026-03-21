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

    def _diagnose_failure(self, error_msg, config_changes):
        try:
            prompt = f"Experiment Failed. Error: {error_msg} Config: {config_changes} Analyze why it failed."
            cmd = ["oracle", "--prompt", prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout.strip() if result.returncode == 0 else "Oracle diagnosis failed."
        except:
            return "Diagnosis unavailable."

    def run_experiment(self, hypothesis):
        hypo_desc = hypothesis.get("hypothesis_description", "Unknown")
        config_changes = hypothesis.get("proposed_config_changes", {})
        branch_name = "exp-" + str(int(time.time()))
        print(f"🚀 Starting: {hypo_desc}")
        
        try:
            self.branch_manager.create_branch(branch_name)
            trainer = Trainer(config_changes)
            result = trainer.train(time_budget=5)
            current_score = result.get("val_bpb", float("inf"))
            improved = current_score < self.history_best_score
            self.tracker.log_result(hypo_desc, current_score, improved, config_changes)
            if improved:
                self.branch_manager.commit_success(f"Improvement: {hypo_desc}")
                self.history_best_score = current_score
            else:
                self.branch_manager.rollback(branch_name)
        except Exception as e:
            error_str = str(e)
            print(f"⚠️ Experiment failed: {error_str}")
            rca = self._diagnose_failure(error_str, config_changes)
            self.tracker.log_result(hypo_desc, float("inf"), False, config_changes, failure_category="runtime_error", exit_code=1, rca=rca)
            self.branch_manager.rollback(branch_name)
