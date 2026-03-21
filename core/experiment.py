import time
from core.branch_manager import BranchManager
from core.result_tracker import ResultTracker
from model.trainer import Trainer

class ExperimentEngine:
    def __init__(self):
        self.branch_manager = BranchManager()
        self.tracker = ResultTracker()
        # 修正：BPB 越低越好，初始化為無限大
        self.history_best_score = self.tracker.get_best_score()
        if self.history_best_score == 0.0: # 防禦舊邏輯殘留
            self.history_best_score = float("inf")

    def run_experiment(self, hypothesis):
        hypo_desc = hypothesis.get("hypothesis_description", "Unknown")
        config_changes = hypothesis.get("proposed_config_changes", {})
        branch_name = f"exp-{int(time.time())}"

        try:
            # 1. 建立分支
            self.branch_manager.create_branch(branch_name)
            
            # 2. 執行訓練
            trainer = Trainer(config_changes)
            result = trainer.train(time_budget=5)
            current_score = result.get("val_bpb", float("inf"))
            
            # 3. 評估 (修正比較方向: 低於最佳分數才是改進)
            improved = current_score < self.history_best_score
            
            # 4. 記錄與分支處理
            self.tracker.log_result(hypo_desc, current_score, improved, config_changes)
            
            if improved:
                print(f"✅ 改進成功! 分數: {current_score}")
                self.branch_manager.commit_success(f"Improvement: {hypo_desc}")
                self.history_best_score = current_score
            else:
                print(f"❌ 無明顯改進: {current_score}")
                self.branch_manager.rollback(branch_name)

        except Exception as e:
            print(f"⚠️ 實驗過程發生錯誤: {str(e)}")
            # 修正：補上失敗記錄，讓 LLM 學習
            self.tracker.log_result(hypo_desc, None, False, {"error": str(e)})
            self.branch_manager.rollback(branch_name)
