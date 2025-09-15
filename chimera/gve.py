# chimera/gve.py
# Git-based Validation Environment for the Chimera agent.
# V2.8: Corrected ModuleNotFoundError by setting PYTHONPATH for pytest.

import sys
import time
import shutil
import tempfile
import subprocess
import os
from pathlib import Path
from typing import Dict

from .utils import GitManager


class GitValidationEnvironment:
    def __init__(self, git_manager: GitManager):
        print("Initializing Git-based Validation Environment...")
        self.git = git_manager
        print("Validation Environment Initialized.")

    def validate_mutation(self, candidate_package: Dict) -> Dict:
        start_time = time.time()
        mutation_id = candidate_package.get('mutation_id', 'N/A')
        branch_name = f"chimera-mutation-{mutation_id[:8]}"

        print(f"\n--- Starting Validation for Mutation {mutation_id} ---")

        status = "FAILED"
        output = "Validation did not complete."

        if not self.git.create_branch(branch_name):
            output = "Failed to create git branch."
        else:
            try:
                # Apply changes to files
                code_file = candidate_package['code_patch']['file_path']
                test_file = candidate_package['new_unit_tests']['file_path']
                code_file.write_text(candidate_package['code_patch']['patch_content'])
                test_file.parent.mkdir(parents=True, exist_ok=True)
                test_file.write_text(candidate_package['new_unit_tests']['test_content'])
                print("[VALIDATION] Applied code and test patches to branch.")

                # Commit changes
                commit_msg = candidate_package.get('commit_message', f"Mutation {mutation_id}")
                if not self.git.add_and_commit([code_file, test_file], commit_msg):
                    output = "Failed to commit changes."
                else:
                    # Run tests with the corrected environment
                    print("[VALIDATION] Executing pytest on the feature branch...")

                    # --- FIX for ModuleNotFoundError ---
                    # Create a copy of the current environment and add the project root to PYTHONPATH
                    env = os.environ.copy()
                    env["PYTHONPATH"] = str(self.git.repo_path) + os.pathsep + env.get("PYTHONPATH", "")

                    result = subprocess.run(
                        [sys.executable, "-m", "pytest"],
                        cwd=self.git.repo_path,
                        capture_output=True,
                        text=True,
                        env=env  # Pass the modified environment to the subprocess
                    )
                    status = "PASSED" if result.returncode == 0 else "FAILED"
                    output = result.stdout + result.stderr
                    print(f"[VALIDATION] Test execution finished. Status: {status}")

            except Exception as e:
                status, output = "FAILED", f"An unexpected error occurred during validation: {e}"
                print(f"[VALIDATION] ERROR: {output}")
            finally:
                self.git.switch_to_main()
                if status == "FAILED":
                    self.git.delete_branch(branch_name)

        end_time = time.time()
        return {
            "mutation_id": mutation_id, "branch_name": branch_name,
            "validation_status": status, "test_output": output,
            "metrics": {"duration_seconds": round(end_time - start_time, 4)}
        }

