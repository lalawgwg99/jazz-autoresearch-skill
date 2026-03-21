import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_progress():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "results.tsv")
    
    if not os.path.exists(file_path):
        print("No results to plot.")
        return

    df = pd.read_csv(file_path, sep="	")
    # 清洗 FAILED 數據
    df = df[df["val_bpb"] != "FAILED"]
    df["val_bpb"] = df["val_bpb"].astype(float)
    
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["val_bpb"], marker="o", linestyle="-", color="b")
    plt.title("AutoResearch Training Progress (BPB)")
    plt.xlabel("Experiment Round")
    plt.ylabel("Validation BPB (Lower is Better)")
    plt.grid(True)
    
    output_path = os.path.join(base_dir, "progress.png")
    plt.savefig(output_path)
    print(f"📊 Progress chart saved to: {output_path}")

if __name__ == "__main__":
    plot_progress()
