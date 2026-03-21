import os, csv, time, json

class ResultTracker:
    def __init__(self, filepath=None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.filepath = filepath or os.path.join(base_dir, 'results.tsv')
        self._init_file()

    def _init_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='	')
                writer.writerow(['timestamp', 'hypothesis', 'val_bpb', 'improved', 'config'])

    def log_result(self, hypothesis, bpb, improved, config_dict):
        try:
            with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='	')
                writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), hypothesis, f'{bpb:.6f}' if bpb is not None else 'FAILED', 'YES' if improved else 'NO', json.dumps(config_dict)])
        except Exception as e:
            print(f'Error: {e}')

    def get_best_score(self):
        if not os.path.exists(self.filepath): return 1.5
        best = 1.5
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                for row in csv.DictReader(f, delimiter='	'):
                    try:
                        v = row.get('val_bpb', '1.5')
                        if v not in ['FAILED', 'N/A', '']: best = min(best, float(v))
                    except: continue
        except: pass
        return best

    def get_history_summary(self, limit=10):
        if not os.path.exists(self.filepath): return 'No history.'
        history = []
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                for row in csv.DictReader(f, delimiter='	'):
                    history.append(f'- {row.get(timestamp)} | Hypo: {row.get(hypothesis)}')
        except: return 'Error.'
        return '
'.join(history[-limit:])