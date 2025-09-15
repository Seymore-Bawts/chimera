# chimera/tasking_engine.py
# V3.0: Refactored from CAE to TaskingEngine for the new mission-oriented architecture.

import json
import uuid
from typing import Dict, Any, List, Optional

from .config import MISSION_STATE_FILE


class TaskingEngine:
    """
    Manages the mission's state, tracking completed tasks and providing
    the next available task from the AI-generated plan.
    """

    def __init__(self):
        print("Initializing Tasking Engine...")
        self.mission_state = self._load_mission_state()
        if self.mission_state.get('tasks'):
            completed = len(self.mission_state.get('completed_tasks', []))
            total = len(self.mission_state.get('tasks', []))
            print(f"Tasking Engine Initialized. Mission progress: {completed}/{total} tasks complete.")
        else:
            print("Tasking Engine Initialized. No active mission found.")

    @staticmethod
    def _load_mission_state() -> Dict[str, Any]:
        """Loads the current mission plan and its completion status."""
        if not MISSION_STATE_FILE.exists():
            return {}
        try:
            with open(MISSION_STATE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves the next unsolved task from the mission plan.
        Returns None if all tasks are complete or no mission is active.
        """
        print("[TASKING] Checking for the next available task...")

        if not self.mission_state.get('tasks'):
            print("[TASKING] No active mission plan.")
            return None

        completed_tasks = self.mission_state.get('completed_tasks', [])

        for task in self.mission_state['tasks']:
            if task['id'] not in completed_tasks:
                print(f"[TASKING] Next task identified: '{task['id']}'.")
                # Add a unique ID for this specific attempt
                task['hypothesis_id'] = str(uuid.uuid4())
                return task

        print("[TASKING] All tasks for the current mission are complete.")
        return None
