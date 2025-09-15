# chimera/utils.py
# Shared utilities for the Chimera agent, including Spinner and GitManager.

import sys
import time
import itertools
import threading
import subprocess
from pathlib import Path
from typing import List

# --- UTILITY: SPINNER FOR VISUAL FEEDBACK ---
class Spinner:
    def __init__(self, message="Processing..."):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.message = message
        self.running = False
        self.thread = None

    def _spin(self):
        while self.running:
            sys.stdout.write(f"\r{self.message} {next(self.spinner)}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write(f"\r{' ' * (len(self.message) + 2)}\r")
        sys.stdout.flush()

    def __enter__(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.running = False
        if self.thread:
            self.thread.join()

# --- UTILITY: GIT MANAGER ---
class GitManager:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.main_branch = self._get_main_branch_name()

    def _run_command(self, command: list) -> subprocess.CompletedProcess:
        return subprocess.run(command, cwd=self.repo_path, capture_output=True, text=True)

    def _get_main_branch_name(self) -> str:
        for name in ["main", "master"]:
            result = self._run_command(["git", "show-branch", f"refs/heads/{name}"])
            if result.returncode == 0:
                return name
        print("[GIT] WARNING: Could not determine main branch name. Defaulting to 'main'.")
        return "main"

    def create_branch(self, branch_name: str) -> bool:
        print(f"[GIT] Creating and switching to new branch: {branch_name}")
        result = self._run_command(["git", "checkout", "-b", branch_name])
        if result.returncode != 0:
            print(f"[GIT] ERROR: Failed to create branch '{branch_name}'.\n{result.stderr}")
            return False
        return True

    def add_and_commit(self, file_paths: List[Path], message: str) -> bool:
        print(f"[GIT] Committing changes with message: '{message}'")
        add_result = self._run_command(["git", "add", *[str(p) for p in file_paths]])
        if add_result.returncode != 0:
            print(f"[GIT] ERROR: 'git add' failed.\n{add_result.stderr}")
            return False
        
        commit_result = self._run_command(["git", "commit", "-m", message])
        if commit_result.returncode != 0:
            print(f"[GIT] ERROR: 'git commit' failed.\n{commit_result.stderr}")
            return False
        return True

    def switch_to_main(self) -> bool:
        print(f"[GIT] Switching back to '{self.main_branch}' branch.")
        result = self._run_command(["git", "checkout", self.main_branch])
        if result.returncode != 0:
            print(f"[GIT] ERROR: Failed to switch to '{self.main_branch}'.\n{result.stderr}")
            return False
        return True

    def merge_branch(self, branch_name: str) -> bool:
        print(f"[GIT] Merging branch '{branch_name}' into '{self.main_branch}'.")
        self.switch_to_main()
        result = self._run_command(["git", "merge", "--no-ff", "-m", f"Merge branch '{branch_name}'", branch_name])
        if result.returncode != 0:
            print(f"[GIT] ERROR: Failed to merge '{branch_name}'.\n{result.stderr}")
            self._run_command(["git", "merge", "--abort"])
            return False
        return True

    def delete_branch(self, branch_name: str):
        print(f"[GIT] Deleting branch: {branch_name}")
        self._run_command(["git", "branch", "-D", branch_name])
