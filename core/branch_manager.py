import subprocess
import os

class BranchManager:
    def __init__(self, repo_path="."):
        self.repo_path = repo_path
        self.timeout = 30 

    def _run_git(self, args):
        try:
            result = subprocess.run(
                ["git"] + args, 
                cwd=self.repo_path, 
                capture_output=True, 
                text=True, 
                timeout=self.timeout
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Git Error: {str(e)}")
            return False

    def create_branch(self, name):
        return self._run_git(["checkout", "-b", name])

    def rollback(self, branch_name):
        self._run_git(["checkout", "main"])
        return self._run_git(["branch", "-D", branch_name])

    def commit_success(self, message):
        self._run_git(["add", "."])
        return self._run_git(["commit", "-m", message])
