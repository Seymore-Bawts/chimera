# chimera/config.py
# Configuration file for the Chimera agent.
# V2.7: Added support for switching between AI providers.

from pathlib import Path

# --- CORE PATHS ---
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
EVOLUTION_LOG_FILE = PROJECT_ROOT / "evolution_log.json"

# --- AI PROVIDER CONFIGURATION ---
# Set this to "GEMINI" to use the Google Gemini API,
# or "LOCAL" to use a local model via an Ollama-compatible API.
AI_PROVIDER = "LOCAL"

# --- GEMINI CONFIGURATION (only used if AI_PROVIDER is "GEMINI") ---
# IMPORTANT: Replace with your actual Google AI Studio API Key
GEMINI_API_KEY = "YOUR_API_KEY_HERE"

# --- LOCAL AI CONFIGURATION (only used if AI_PROVIDER is "LOCAL") ---
# The URL of your local Ollama API endpoint
LOCAL_AI_URL = "http://localhost:11434/api/generate"
# The name of the local model you are using (e.g., 'deepseek-coder' or 'codellama')
LOCAL_AI_MODEL = "chimera-coder"
LOCAL_AI_PROVIDER = "LOCAL"


# --- HYPOTHESIS BACKLOG ---
# A list of potential problems for the CAE to "discover".
HYPOTHESIS_BACKLOG = [
    {
        "id": "CPU_INEFFICIENCY",
        "problem_statement": "The current scheduler is not CPU-aware, leading to inefficient task ordering on high-load nodes.",
        "proposed_solution": "Modify the scheduling algorithm to consider CPU cost as a secondary sorting criterion after priority.",
        "affected_module": "core.scheduler"
    },
    {
        "id": "MEMORY_INEFFICIENCY",
        "problem_statement": "The scheduler does not account for task memory usage, potentially causing out-of-memory errors on constrained nodes.",
        "proposed_solution": "Incorporate memory cost (RAM usage) into the scheduling logic, sorting by lowest memory after priority.",
        "affected_module": "core.scheduler"
    },
    {
        "id": "DEPENDENCY_HANDLING",
        "problem_statement": "The scheduler cannot handle tasks with dependencies, where one task must complete before another begins.",
        "proposed_solution": "Refactor the scheduling logic to understand a 'depends_on' key in task dictionaries. It should perform a topological sort to ensure correct execution order while still respecting priority for independent tasks.",
        "affected_module": "core.scheduler"
    },
    {
        "id": "REMOTE_PUSH_FAILURE",
        "problem_statement": "The agent's persistence module does not push its successful evolutions to a remote git repository, limiting collaboration and backup.",
        "proposed_solution": "Enhance the GitPersistenceModule to automatically perform a 'git push' to the 'origin' remote after a successful merge to the main branch.",
        "affected_module": "utils" # The GitManager in utils.py is the target
    }
]

