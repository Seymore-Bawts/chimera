# chimera/gsm.py
# Generative Synthesis Module for the Chimera agent.
# V2.7.4: Refactored __init__ to be self-sufficient and respect config.

import requests
import json
import uuid
import time
from pathlib import Path
from typing import Dict, Any, Optional

from .config import PROJECT_ROOT, AI_PROVIDER, GEMINI_API_KEY, LOCAL_AI_URL, LOCAL_AI_MODEL
from .utils import Spinner


class GenerativeSynthesisModule:
    """
    Translates an abstract hypothesis into a concrete code mutation and
    accompanying unit tests using a live generative AI model.
    """

    def __init__(self):
        print("Initializing Generative Synthesis Module (GSM)...")
        self.repo_path = PROJECT_ROOT
        self.ai_provider = AI_PROVIDER

        if self.ai_provider == "GEMINI":
            self.api_key = GEMINI_API_KEY
            self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={self.api_key}"
        elif self.ai_provider == "LOCAL":
            self.api_key = None  # Not needed for local
            self.api_url = LOCAL_AI_URL
        else:
            raise ValueError(f"Unknown AI_PROVIDER: {self.ai_provider}")

        print(f"GSM Initialized. Using AI Provider: {self.ai_provider}")

    def _call_generative_model(self, prompt: str, task_message: str) -> Optional[str]:
        """Makes an API call to the configured AI model with retries."""
        max_retries = 3
        delay = 1.0  # seconds

        for attempt in range(max_retries):
            with Spinner(f"{task_message} (Attempt {attempt + 1}/{max_retries})"):
                try:
                    if self.ai_provider == "GEMINI":
                        payload = {"contents": [{"parts": [{"text": prompt}]}]}
                        headers = {'Content-Type': 'application/json'}
                        response = requests.post(self.api_url, json=payload, headers=headers, timeout=120)
                    elif self.ai_provider == "LOCAL":
                        payload = {"model": LOCAL_AI_MODEL, "prompt": prompt, "stream": False}
                        headers = {'Content-Type': 'application/json'}
                        response = requests.post(self.api_url, json=payload, headers=headers, timeout=120)

                    response.raise_for_status()
                    data = response.json()

                    if self.ai_provider == "GEMINI":
                        if 'candidates' not in data or not data['candidates']:
                            error_info = data.get('promptFeedback', 'No feedback available.')
                            print(f"\n[GSM-AI] ERROR: AI returned no candidates. Feedback: {error_info}")
                            return None
                        text = data['candidates'][0]['content']['parts'][0]['text']
                    elif self.ai_provider == "LOCAL":
                        text = data.get('response', '')

                    if text.strip().startswith("```python"):
                        text = '\n'.join(text.strip().split('\n')[1:-1])
                    return text

                except requests.exceptions.RequestException as e:
                    print(f"\n[GSM-AI] ERROR: API request failed: {e}")
                    if attempt < max_retries - 1:
                        print(f"Waiting {delay:.0f}s before next retry.")
                        time.sleep(delay)
                        delay *= 2  # Exponential backoff
                    else:
                        print(f"\n[GSM-AI] FATAL: API call failed after {max_retries} attempts.")
                        return None
                except (KeyError, IndexError) as e:
                    print(f"\n[GSM-AI] ERROR: Could not parse AI response: {e}\nRaw response: {data}")
                    return None
        return None

    def _live_source_code_retriever(self, module_path: str) -> str:
        """
        Retrieves source code. If the file is missing, it recreates a
        baseline version to allow the agent to self-heal.
        """
        absolute_path = (self.repo_path / 'src' / module_path.replace('.', '/')).with_suffix('.py')
        if not absolute_path.exists():
            print(f"[CSCR] WARNING: File not found at '{absolute_path}'. Recreating baseline version.")
            absolute_path.parent.mkdir(parents=True, exist_ok=True)
            baseline_content = (
                "# Original scheduler file V1.0\n\n"
                "def schedule_task(tasks: list):\n"
                "    # Simple FIFO logic\n"
                "    return sorted(tasks, key=lambda t: t.get('priority', 99))\n"
            )
            absolute_path.write_text(baseline_content)
            return baseline_content
        return absolute_path.read_text()

    def _generate_code_from_llm(self, context_code: str, hypothesis: Dict[str, Any]) -> Optional[str]:
        prompt = (
            "You are an expert Python programmer. Your task is to modify Python code based on a specific requirement.\n"
            f"Here is the original code from `src/{hypothesis['affected_module'].replace('.', '/')}.py`:\n"
            "```python\n"
            f"{context_code}\n"
            "```\n\n"
            f"Problem Statement: {hypothesis['problem_statement']}\n"
            f"Proposed Solution: {hypothesis['proposed_solution']}\n\n"
            "Provide the complete, new version of the Python code. "
            "IMPORTANT: ONLY output the raw Python code. Do not include any explanations or markdown formatting."
        )
        return self._call_generative_model(prompt, "[GSM-AI] Generating new code")

    def _generate_tests_from_llm(self, new_code: str, hypothesis: Dict[str, Any]) -> Optional[str]:
        prompt = (
            "You are an expert Python programmer specializing in testing with pytest.\n"
            f"Here is a new Python module intended for `src/{hypothesis['affected_module'].replace('.', '/')}.py`:\n"
            "```python\n"
            f"{new_code}\n"
            "```\n\n"
            f"This code was designed to solve: '{hypothesis['problem_statement']}'\n\n"
            "Write a complete, runnable pytest unit test file to verify the code's new logic. "
            f"The module to import is `src.{hypothesis['affected_module']}`. For example, use `from src.core.scheduler import schedule_task`.\n"
            "Cover edge cases. If the solution involves dependencies, test the topological sort logic is correct. "
            "IMPORTANT: ONLY output the raw Python code for the test file. Do not include explanations or markdown formatting."
        )
        return self._call_generative_model(prompt, "[GSM-AI] Generating new unit tests")

    def generate_mutation_candidate(self, hypothesis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        print(f"\n--- Generating Mutation for Hypothesis: {hypothesis['id']} ({hypothesis['hypothesis_id']}) ---")
        original_code = self._live_source_code_retriever(hypothesis['affected_module'])
        if not original_code:
            return None
        new_code = self._generate_code_from_llm(original_code, hypothesis)
        if not new_code:
            return None
        new_tests = self._generate_tests_from_llm(new_code, hypothesis)
        if not new_tests:
            return None
        return self._package_mutation(hypothesis, new_code, new_tests)

    def _package_mutation(self, hypothesis: Dict, code: str, tests: str) -> Dict[str, Any]:
        code_file_path = self.repo_path / 'src' / hypothesis['affected_module'].replace('.', '/')
        code_file_path = code_file_path.with_suffix('.py')

        test_file_path = self.repo_path / 'tests' / f"test_{hypothesis['affected_module'].replace('.', '_')}.py"

        package = {
            "mutation_id": str(uuid.uuid4()),
            "hypothesis_id": hypothesis['hypothesis_id'],
            "hypothesis_type_id": hypothesis['id'],
            "code_patch": {"file_path": code_file_path, "patch_content": code},
            "new_unit_tests": {"file_path": test_file_path, "test_content": tests},
            "commit_message": f"feat(core): Evolve scheduler for {hypothesis['id']}"
        }
        print("--- Mutation Candidate Package Created ---")
        return package

