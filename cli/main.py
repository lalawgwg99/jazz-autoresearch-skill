import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.result_tracker import ResultTracker
from core.experiment import ExperimentEngine
from hypothesis.generator import LLMHypothesisGenerator

def main():
    parser = argparse.ArgumentParser(description="AutoResearch CLI")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="啟動自動化實驗循環")
    status_parser = subparsers.add_parser("status", help="查看紀錄")

    args = parser.parse_args()
    
    if args.command == "run":
        generator = LLMHypothesisGenerator()
        engine = ExperimentEngine()
        
        print("🧠 正在生成自動化假說 (讀取歷史數據並思考)...")
        # 真正執行大腦思考
        hypothesis = generator.generate_next_hypothesis()
        description = hypothesis.get("hypothesis_description", "Unknown")
        
        print(f"🚀 啟動實驗: {description}")
        # 真正執行實驗與分支處理
        engine.run_experiment(hypothesis)
        
    elif args.command == "status":
        tracker = ResultTracker()
        print(f"🏆 目前最佳驗證 BPB: {tracker.get_best_score():.6f}")
        print("📂 歷史紀錄摘要:")
        print(tracker.get_history_summary())

if __name__ == "__main__":
    main()
