import argparse
import sys
import os

# 確保能找到同目錄下的模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.result_tracker import ResultTracker
from model.trainer import Trainer, GPTConfig

def main():
    parser = argparse.ArgumentParser(description="AutoResearch CLI")
    subparsers = parser.add_subparsers(dest="command")

    # run 指令
    run_parser = subparsers.add_parser("run", help="執行一次實驗")
    run_parser.add_argument("--hypo", type=str, default="Default Experiment", help="實驗假設描述")

    # status 指令
    status_parser = subparsers.add_parser("status", help="查看目前最佳實驗結果")

    args = parser.parse_args()

    tracker = ResultTracker()

    if args.command == "run":
        print(f"🚀 啟動實驗: {args.hypo}")
        best_so_far = tracker.get_best_score()
        print(f"📊 目前最佳分數: {best_so_far:.6f}")
        
        trainer = Trainer()
        result = trainer.train(time_budget=5)
        bpb = result["val_bpb"]
        
        improved = bpb < best_so_far
        tracker.log_result(args.hypo, bpb, improved, {})
        
        if improved:
            print(f"✅ 成功! 新紀錄: {bpb:.6f}")
        else:
            print(f"❌ 失敗: {bpb:.6f} (未超過最佳紀錄)")

    elif args.command == "status":
        best = tracker.get_best_score()
        print(f"🏆 目前 AutoResearch 最佳驗證 BPB: {best:.6f}")
        if os.path.exists("results.tsv"):
            print(f"📂 詳情請見: {os.path.abspath("results.tsv")}")
        else:
            print("📭 尚無實驗紀錄。")

if __name__ == "__main__":
    main()
