# chimera/gpm.py
# Git-based Persistence Module for the Chimera agent.
# V2.5.1: Corrected unresolved reference for 'hypothesis_id'.

import json
from typing import Dict

from .utils import GitManager
from .config import EVOLUTION_LOG_FILE

class GitPersistenceModule:
    def __init__(self, git_manager: GitManager):
        print("Initializing Git Persistence Module...")
        self.git = git_manager
        print("Persistence Module Initialized.")

    def apply_and_log_mutation(self, validation_report: Dict, candidate_package: Dict):
        branch_name = validation_report['branch_name']
        hypothesis_id = candidate_package.get('hypothesis_type_id') # Use .get for safety

        if self.git.merge_branch(branch_name):
            self.git.delete_branch(branch_name)
            if hypothesis_id:
                self._update_evolution_log(hypothesis_id)
            # Push to remote after successful merge
            self.git.push_to_remote()
        else:
            print("[PERSISTENCE] ERROR: Merge failed. Discarding branch.")
            self.git.delete_branch(branch_name)

    @staticmethod
    def _update_evolution_log(hypothesis_id: str):
        print(f"[PERSISTENCE] Logging completed evolution: {hypothesis_id}")
        try:
            log_data = []
            if EVOLUTION_LOG_FILE.exists():
                with open(EVOLUTION_LOG_FILE, 'r') as f:
                    log_data = json.load(f)
            if hypothesis_id not in log_data:
                log_data.append(hypothesis_id)
                with open(EVOLUTION_LOG_FILE, 'w') as f:
                    json.dump(log_data, f, indent=4)
                print("[PERSISTENCE] SUCCESS: Evolutionary log updated.")
        except Exception as e:
            print(f"[PERSISTENCE] FAILURE: Could not update log. Error: {e}")