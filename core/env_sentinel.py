import os, sys, subprocess

class EnvSentinel:
    def __init__(self):
        self.results = {}

    def scan(self):
        # 1. 檢查 Python 版本
        self.results['python_version'] = sys.version.split()[0]
        
        # 2. 檢查 Torch 與 GPU 支援 (MPS for Mac, CUDA for Linux/PC)
        try:
            import torch
            self.results['torch_installed'] = True
            if torch.backends.mps.is_available():
                self.results['gpu_type'] = 'MPS (Apple Silicon)'
            elif torch.cuda.is_available():
                self.results['gpu_type'] = f'CUDA ({torch.cuda.get_device_name(0)})'
            else:
                self.results['gpu_type'] = 'None (CPU Only)'
        except ImportError:
            self.results['torch_installed'] = False
            self.results['gpu_type'] = 'None'

        # 3. 檢查關鍵依賴
        deps = ['pandas', 'matplotlib', 'uv']
        self.results['dependencies'] = {}
        for dep in deps:
            try:
                subprocess.run([dep, '--version'], capture_output=True, check=True) if dep == 'uv' else __import__(dep)
                self.results['dependencies'][dep] = True
            except:
                self.results['dependencies'][dep] = False
        
        return self.results

    def get_report(self):
        r = self.scan()
        report = f'🔍 [EnvSentinel] 環境掃描報告:
'
        report += f'- Python: {r[python_version]}
'
        report += f'- GPU: {r[gpu_type]}
'
        report += f'- Torch: {✅ if r[torch_installed] else ❌}
'
        for dep, ok in r[dependencies].items():
            report += f'- {dep}: {✅ if ok else ❌}
'
        return report