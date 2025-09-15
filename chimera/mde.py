# chimera/mde.py
# New Module for V3.0: Mission Decomposition Engine

import json
from typing import Dict, Any, Optional, List

from .config import AI_PROVIDER, GEMINI_API_KEY, LOCAL_AI_URL, LOCAL_AI_MODEL
from .utils import call_generative_model


class MissionDecompositionEngine:
    """
    Takes a high-level mission and uses an AI to break it down into a
    concrete, actionable list of programming tasks.
    """

    def __init__(self):
        print("Initializing Mission Decomposition Engine (MDE)...")
        if AI_PROVIDER == "LOCAL":
            print(f"MDE is configured to use local model: {LOCAL_AI_MODEL}")
        else:
            print("MDE is configured to use Google Gemini.")

    def decompose_mission(self, mission_prompt: str) -> Optional[List[Dict[str, Any]]]:
        """
        Sends the mission to the AI and expects a JSON array of tasks in return.
        """
        print(f"[MDE] Decomposing mission: '{mission_prompt}'")

        decomposition_prompt = (
            "You are an expert software architect. Your task is to take a high-level mission statement and decompose it into a series of concrete, sequential programming tasks. "
            "You must return your response as a valid JSON array of objects. Each object in the array represents one task and must have the following keys:\n"
            "- 'id': A short, unique, snake_case identifier for the task (e.g., 'refactor_scheduler_class').\n"
            "- 'problem_statement': A concise description of the problem this task solves.\n"
            "- 'proposed_solution': A clear, one-sentence description of the work to be done.\n"
            "- 'affected_module': The primary Python module that will be modified to complete this task, in dot notation (e.g., 'core.scheduler').\n\n"
            "Here is an example response format:\n"
            "```json\n"
            "[\n"
            "  {\n"
            "    \"id\": \"create_logger_file\",\n"
            "    \"problem_statement\": \"The application needs a dedicated logging module, but the file doesn't exist.\",\n"
            "    \"proposed_solution\": \"Create a new file at 'src/core/logger.py' with a basic Logger class.\",\n"
            "    \"affected_module\": \"core.logger\"\n"
            "  },\n"
            "  {\n"
            "    \"id\": \"integrate_logger\",\n"
            "    \"problem_statement\": \"The scheduler module does not produce any logs, making it difficult to debug.\",\n"
            "    \"proposed_solution\": \"Import the new Logger class into 'src/core/scheduler.py' and add log statements at key execution points.\",\n"
            "    \"affected_module\": \"core.scheduler\"\n"
            "  }\n"
            "]\n"
            "```\n\n"
            f"Now, please decompose the following mission into a JSON array of tasks:\n"
            f"MISSION: \"{mission_prompt}\""
        )

        response_text = call_generative_model(decomposition_prompt, "[MDE] Generating development plan...")

        if not response_text:
            print("[MDE] ERROR: Failed to get a response from the AI.")
            return None

        try:
            # Clean up the response to extract only the JSON
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            if json_start == -1 or json_end == 0:
                raise json.JSONDecodeError("No JSON array found in response", response_text, 0)

            plan = json.loads(response_text[json_start:json_end])
            print(f"[MDE] Successfully decomposed mission into {len(plan)} tasks.")
            return plan
        except json.JSONDecodeError as e:
            print(f"[MDE] ERROR: Failed to parse JSON response from AI. Error: {e}")
            print(f"Raw AI Response:\n---\n{response_text}\n---")
            return None
