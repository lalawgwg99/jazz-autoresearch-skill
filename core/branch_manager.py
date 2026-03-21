import subprocess
import os
from typing import Optional

class BranchManager:
    """
    處理實驗分支的 Git 操作邏輯
    """
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def _run_git(self, args: list[str]) -> subprocess.CompletedProcess:
        try:
            return subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Git error: {e.stderr}")
            raise e

    def create_branch(self, branch_name: str) -> bool:
        """建立並切換到新分支"""
        try:
            self._run_git(["checkout", "-b", branch_name])
            return True
        except Exception:
            return False

    def commit_success(self, message: str) -> bool:
        """提交實驗成功的改動"""
        try:
            self._run_git(["add", "."])
            self._run_git(["commit", "-m", message])
            return True
        except Exception:
            return False

    def rollback(self, main_branch: str = "main") -> bool:
        """實驗失敗時切換回主分支並捨棄改動"""
        try:
            self._run_git(["reset", "--hard"])
            self._run_git(["checkout", main_branch])
            return True
        except Exception:
            return False
