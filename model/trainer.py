import time
import math
from dataclasses import dataclass

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

@dataclass
class GPTConfig:
    sequence_len: int = 2048
    vocab_size: int = 32768
    n_layer: int = 8
    n_head: int = 8
    n_kv_head: int = 8
    n_embd: int = 512

class Trainer:
    def __init__(self, config=None):
        self.config = config or GPTConfig()
        if HAS_TORCH:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(f"Trainer initialized on {self.device} (Torch Mode)")
        else:
            print("Trainer initialized in Mock Mode (No Torch)")

    def train(self, time_budget=300):
        print(f"Starting training with budget: {time_budget}s")
        start_time = time.time()
        step = 0
        while (time.time() - start_time) < time_budget:
            # 模擬訓練步驟
            time.sleep(0.5) 
            step += 1
            if step % 2 == 0:
                elapsed = time.time() - start_time
                print(f"Step {step:03d} | Progress: {int(elapsed/time_budget*100)}%")
        
        # 模擬一個會隨時間下降的分數 (BPB)
        final_score = 1.5 - (step * 0.002)
        return {"val_bpb": final_score}

    def evaluate(self):
        return 1.45
