import os
import logging
from typing import Dict, Any, Optional

# 設定簡單的 Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExperimentEngine:
    """
    自動化實驗執行主引擎
    """
    def __init__(self, workspace_path: str, trainer: Any, branch_manager: Any):
        self.workspace_path = workspace_path
        self.trainer = trainer
        self.branch_mgr = branch_manager
        self.history_best_score = 0.0

    def run_experiment(self, hypothesis: Dict[str, Any]) -> Dict[str, Any]:
        """
        執行實驗的主流程：
        1. 建立實驗分支 (create branch)
        2. 執行訓練任務 (run training)
        3. 取得並評估指標 (evaluate metrics)
        4. 決定是否提交成功分支 (commit or rollback)
        """
        experiment_id = hypothesis.get("id", "exp_temp")
        branch_name = f"experiment/{experiment_id}"

        logger.info(f"🚀 Starting experiment: {experiment_id} (Branch: {branch_name})")

        # Step 1: 建立分支
        if not self.branch_mgr.create_branch(branch_name):
             raise Exception(f"❌ Failed to create branch: {branch_name}")

        try:
            # Step 2: 執行訓練流程 (這裡假設 trainer 已準備好)
            # 實際場景中 hypothesis 應轉換為程式碼改動，目前先執行現有腳本
            metrics = self.trainer.train()

            # Step 3: 評估結果
            is_improved = self._evaluate_result(metrics)

            if is_improved:
                logger.info(f"✅ Improvement detected! Score: {metrics.get('score', 0)}")
                # Step 4a: 成功，提交並回傳結果
                self.branch_mgr.commit_success(f"Success: {hypothesis.get('summary', 'Improvement')}")
                return {"status": "success", "metrics": metrics, "improved": True}
            else:
                logger.warning(f"⚠️ No improvement. Score: {metrics.get('score', 0)}")
                # Step 4b: 失敗，回溯分支
                self.branch_mgr.rollback()
                return {"status": "discarded", "metrics": metrics, "improved": False}

        except Exception as e:
            logger.error(f"❌ Experiment failed with error: {str(e)}")
            self.branch_mgr.rollback()
            return {"status": "failed", "error": str(e)}

    def _evaluate_result(self, metrics: Dict[str, Any]) -> bool:
        """
        判斷實驗是否比歷史最佳分數更好
        假設主要評估指標為 'score'
        """
        current_score = metrics.get("score", 0.0)
        if current_score > self.history_best_score:
            self.history_best_score = current_score
            return True
        return False
