import os, sys, subprocess

class EnvSentinel:
    def __init__(self):
        self.results = {}

    def scan(self):
        self.results['python_version'] = sys.version.split()[0]
        try:
            import torch
            self.results['torch_installed'] = True
            if torch.backends.mps.is_available():
                self.results['gpu_type'] = 'MPS (Apple Silicon)'
            elif torch.cuda.is_available():
                self.results['gpu_type'] = 'CUDA'
            else:
                self.results['gpu_type'] = 'None'
        except ImportError:
            self.results['torch_installed'] = False
            self.results['gpu_type'] = 'None'

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
        report = "🔍 [EnvSentinel] Environment Scan:" + chr(10)
        report += "- Python: " + str(r["python_version"]) + chr(10)
        report += "- GPU: " + str(r["gpu_type"]) + chr(10)
        report += "- Torch: " + ("✅" if r["torch_installed"] else "❌") + chr(10)
        return report
