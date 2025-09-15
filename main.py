# main.py
# Main orchestrator for the Chimera agent.
# V2.7.4: Removed incorrect dependency on GEMINI_API_KEY when using LOCAL provider.

import sys
import time
import shutil
import subprocess
from pathlib import Path

# Fix for ModuleNotFoundError: Add project root to the Python path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from chimera.config import AI_PROVIDER, GEMINI_API_KEY, EVOLUTION_LOG_FILE
from chimera.utils import GitManager
from chimera.cae import CognitiveAnalysisEngine
from chimera.gsm import GenerativeSynthesisModule
from chimera.gve import GitValidationEnvironment
from chimera.dcp import DistributedConsensusProtocol
from chimera.gpm import GitPersistenceModule


def run_evolutionary_cycle(git_manager: GitManager):
    """Runs a single evolutionary cycle."""
    print("=" * 45 + "\n=== INITIATING CHIMERA EVOLUTIONARY CYCLE ===\n" + "=" * 45 + "\n")

    cae = CognitiveAnalysisEngine()
    hypothesis = cae.generate_hypothesis()
    if not hypothesis:
        return False

    # The GSM will internally decide which AI provider to use based on config
    gsm = GenerativeSynthesisModule()
    candidate_package = gsm.generate_mutation_candidate(hypothesis)
    if not candidate_package:
        return True

    gve = GitValidationEnvironment(git_manager)
    validation_report = gve.validate_mutation(candidate_package)

    if validation_report.get("validation_status") != "PASSED":
        print("\n[ORCHESTRATOR] FAILURE: Mutation failed validation.")
        print("--- Validation Details ---\n" + validation_report.get("test_output", "No output captured."))
        print("--------------------------")
        return True  # Continue to next cycle

    dcp = DistributedConsensusProtocol(network_size=150)
    consensus_result = dcp.propose_and_vote(validation_report)

    if consensus_result.get("proposal_status") == "ACCEPTED":
        gpm = GitPersistenceModule(git_manager)
        gpm.apply_and_log_mutation(validation_report, candidate_package)
    else:
        print("\n[ORCHESTRATOR] Mutation was rejected by consensus. Discarding branch.")
        git_manager.delete_branch(validation_report['branch_name'])

    print("\n--- CYCLE COMPLETE ---\n" + (
        "MUTATION ACCEPTED and APPLIED" if consensus_result.get(
            "proposal_status") == "ACCEPTED" else "MUTATION REJECTED") +
          "\n" + "=" * 45 + "\n======= CHIMERA CYCLE EXECUTION ENDED =======\n" + "=" * 45 + "\n")
    return True


def setup_initial_files():
    """Sets up the initial environment for the agent to run."""
    print("[SETUP] Checking for initial files and dependencies...")
    remote_url = "https://github.com/Seymore-Bawts/chimera.git"

    if not shutil.which("git"):
        print("[SETUP] FATAL: 'git' command not found. Please install Git and ensure it's in your PATH.")
        sys.exit(1)

    if not (PROJECT_ROOT / ".git").is_dir():
        print("[SETUP] This is not a git repository. Initializing one now.")
        subprocess.run(["git", "init"], cwd=PROJECT_ROOT)
        subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT)
        subprocess.run(["git", "commit", "-m", "Initial commit: Setup Chimera agent"], cwd=PROJECT_ROOT)

    remotes = subprocess.run(["git", "remote"], cwd=PROJECT_ROOT, capture_output=True, text=True).stdout
    if "origin" not in remotes.split():
        print(f"[SETUP] Adding remote 'origin': {remote_url}")
        subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=PROJECT_ROOT)
    else:
        print("[SETUP] Remote 'origin' already configured.")

    try:
        import requests
    except ImportError:
        print("[SETUP] WARNING: 'requests' library not found. Please run: pip install requests")
        sys.exit(1)

    # --- Corrected API Key Check ---
    if AI_PROVIDER == "GEMINI":
        api_key_value = GEMINI_API_KEY.strip()
        if not api_key_value or api_key_value == "YOUR_API_KEY_HERE":
            print("\n[SETUP] FATAL: AI_PROVIDER is set to 'GEMINI' but your API Key is missing or invalid.")
            print(
                "Please edit the 'chimera/config.py' file and replace 'YOUR_API_KEY_HERE' with your actual key from Google AI Studio.")
            sys.exit(1)
        print("[SETUP] Gemini API Key found.")
    elif AI_PROVIDER == "LOCAL":
        print("[SETUP] AI_PROVIDER is 'LOCAL'. Skipping Gemini API Key check.")

    src_dir = PROJECT_ROOT / 'src' / 'core'
    src_dir.mkdir(parents=True, exist_ok=True)
    scheduler_path = src_dir / 'scheduler.py'
    if not scheduler_path.exists():
        print(f"[SETUP] Creating baseline file: {scheduler_path}")
        scheduler_path.write_text(
            "# Original scheduler file V1.0\n\ndef schedule_task(tasks: list):\n    # Simple FIFO logic\n    return sorted(tasks, key=lambda t: t.get('priority', 99))\n")
    if not EVOLUTION_LOG_FILE.exists():
        print(f"[SETUP] Creating new evolutionary log at: {EVOLUTION_LOG_FILE}")
        EVOLUTION_LOG_FILE.write_text("[]")


def handle_reset_argument():
    """Clears the evolutionary log if the --reset flag is used."""
    if "--reset" in sys.argv:
        print("[SETUP] --reset flag detected. Clearing evolutionary log.")
        if EVOLUTION_LOG_FILE.exists():
            try:
                EVOLUTION_LOG_FILE.write_text("[]")
                print("[SETUP] Evolutionary log has been reset.")
            except IOError as e:
                print(f"[SETUP] ERROR: Could not reset log file: {e}")


if __name__ == "__main__":
    handle_reset_argument()
    setup_initial_files()
    main_git_manager = GitManager(PROJECT_ROOT)
    cycle_count = 0
    while True:
        cycle_count += 1
        print(f"--- Starting Evolutionary Cycle #{cycle_count} ---")
        keep_running = run_evolutionary_cycle(main_git_manager)
        if not keep_running:
            print("\nAll evolutionary tasks complete. Chimera is entering a dormant state.")
            break
        print(f"--- Cycle #{cycle_count} Finished. Waiting 5 seconds before next cycle. ---")
        time.sleep(5)

