# chimera/cae.py
# Cognitive Analysis Engine for the Chimera agent.
# V2.5.2: Corrected KeyError by reverting 'hypothesis_instance_id' to 'hypothesis_id'.

import json
import random
import uuid
from typing import Dict, Any, List, Optional

from .config import HYPOTHESIS_BACKLOG, EVOLUTION_LOG_FILE


class CognitiveAnalysisEngine:
    """
    Analyzes the swarm's performance and codebase to identify opportunities
    for evolution and generates actionable hypotheses from a backlog.
    """

    def __init__(self):
        print("Initializing Cognitive Analysis Engine (CAE)...")
        self.evolution_log = self._load_evolution_log()
        print(f"CAE Initialized. Loaded {len(self.evolution_log)} completed evolutions from log.")

    @staticmethod
    def _load_evolution_log() -> List[str]:
        """Loads the list of completed hypothesis IDs from the log file."""
        if not EVOLUTION_LOG_FILE.exists():
            return []
        try:
            with open(EVOLUTION_LOG_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def generate_hypothesis(self) -> Optional[Dict[str, Any]]:
        """
        Selects a random, unsolved hypothesis from the global backlog.
        Returns None if all hypotheses have been solved.
        """
        print("[CAE] Analyzing swarm performance data and evolutionary log...")

        unsolved_hypotheses = [
            h for h in HYPOTHESIS_BACKLOG if h['id'] not in self.evolution_log
        ]

        if not unsolved_hypotheses:
            print("[CAE] Analysis complete: All known evolutionary paths have been completed.")
            return None

        selected_hypothesis = random.choice(unsolved_hypotheses)
        print(f"[CAE] Analysis complete: Identified unsolved problem '{selected_hypothesis['id']}'.")

        # Add a unique ID for this specific attempt
        # This key must match what the GSM expects.
        selected_hypothesis['hypothesis_id'] = str(uuid.uuid4())
        return selected_hypothesis

