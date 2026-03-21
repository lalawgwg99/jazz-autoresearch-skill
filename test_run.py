import sys
import os
import time

# 將目前目錄加入路徑，以便導入模組
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.trainer import Trainer, GPTConfig

def mock_experiment_loop():
    print("🚀 [AutoResearch] 啟動測試循環...")
    
    # 1. 模擬假設生成
    hypothesis = "增加模型層數 (n_layer: 8 -> 10)"
    print(f"💡 [Hypothesis] 生成新假設: {hypothesis}")
    
    # 2. 模擬分支管理
    print("🌿 [Branch] 建立實驗分支: experiment/add-layers")
    time.sleep(1)
    
    # 3. 呼叫 Trainer 執行訓練 (模擬 5 秒預算)
    config = GPTConfig(n_layer=10)
    trainer = Trainer(config)
    print("⏳ [Training] 啟動模型訓練 (預算: 5s)...")
    result = trainer.train(time_budget=5)
    
    # 4. 評估結果
    val_bpb = result["val_bpb"]
    print(f"📊 [Evaluation] 訓練完成! 驗證集 BPB: {val_bpb:.6f}")
    
    # 5. 決策
    history_best = 1.500000
    if val_bpb < history_best:
        print(f"✅ [Decision] 改進成功! (BPB 降低)")
    else:
        print(f"❌ [Decision] 無明顯改進 -> 回滾分支")
    
    print("FINISHED")

if __name__ == "__main__":
    mock_experiment_loop()
