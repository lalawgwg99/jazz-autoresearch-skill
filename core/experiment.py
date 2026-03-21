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
        """偵測 Mac CPU 溫度 (人性化保護)"""
        try:
            # macOS 專用指令取得 CPU 溫度 (需安裝 osx-cpu-temp 或類似工具，若無則跳過)
            cmd = ["osx-cpu-temp"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                temp = float(result.stdout.replace("°C", "").strip())
                if temp > 85.0:
                    print(f"🌡️ 警報：CPU 溫度過高 ({temp}°C)，暫停實驗 60 秒...")
                    time.sleep(60)
                    return False
            return True
        except:
            return True

    def _send_telegram_report(self, message, image_path=None):
        """透過 OpenClaw 主動發送 Telegram 戰報"""
        try:
            # 使用 OpenClaw 內建的 message send 指令
            cmd = ["openclaw", "message", "send", "--message", message]
            subprocess.run(cmd, capture_output=True, text=True)
            # 如果有圖表，發送圖表 (示意，實際需視 channel 支援)
            if image_path and os.path.exists(image_path):
                print(f"📸 戰報圖表已生成：{image_path}")
        except:
            pass

    def run_experiment(self, hypothesis):
        if not self._check_temperature():
            return

        hypo_desc = hypothesis.get("hypothesis_description", "Unknown")
        config_changes = hypothesis.get("proposed_config_changes", {})
        branch_name = "exp-" + str(int(time.time()))

        print(f"🚀 啟動實驗：{hypo_desc}")
        
        try:
            self.branch_manager.create_branch(branch_name)
            trainer = Trainer(config_changes)
            result = trainer.train(time_budget=5)
            current_score = result.get("val_bpb", float("inf"))
            
            improved = current_score < self.history_best_score
            self.tracker.log_result(hypo_desc, current_score, improved, config_changes)
            
            status_emoji = "✅" if improved else "❌"
            diff = self.history_best_score - current_score if improved else 0
            
            # 建立人性化戰報內容
            report = (
                f"📊 *AutoResearch 實驗戰報*
"
                f"━━━━━━━━━━━━━━━
"
                f"💡 *假設*：{hypo_desc}
"
                f"📈 *結果*：{current_score:.6f} ({status_emoji})
"
                f"🏆 *進步*：{diff:.6f}
"
                f"━━━━━━━━━━━━━━━
"
                f"✨ 系統已自動更新主分支並記錄。" if improved else "⚠️ 此改動已自動回滾。"
            )
            
            if improved:
                self.branch_manager.commit_success(f"Improvement: {hypo_desc}")
                self.history_best_score = current_score
            else:
                self.branch_manager.rollback(branch_name)

            # 主動回報
            self._send_telegram_report(report)

        except Exception as e:
            error_msg = f"⚠️ 實驗發生崩潰：{str(e)}"
            self.tracker.log_result(hypo_desc, None, False, {"error": str(e)})
            self.branch_manager.rollback(branch_name)
            self._send_telegram_report(error_msg)
